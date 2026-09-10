#!/usr/bin/env python3
"""Check art delivery names, references and registration boundaries (stdlib only)."""
import argparse,hashlib,json,re
from pathlib import Path
STATES={'planned','generated','passed','failed','blocked','stale'}
DELIVERY={'draft','ready_for_development','approved_for_runtime'}
ROLES={'main','source','preview','thumbnail','albedo','normal','roughness','metallic','emissive','ao','height','mask','bgm','ambience','sfx','voice'}
CATEGORIES={'source','runtime','preview','reference','history'}
PROVENANCE={'original','third_party','outsourced','commercial_library','free_library','open_source','ai_generated','ai_assisted'}
def check(ok,msg):
    if not ok:raise ValueError(msg)
def read(path):return json.loads(path.read_text(encoding='utf-8'))
def snake(text):return isinstance(text,str) and re.fullmatch(r'[a-z0-9]+(?:_[a-z0-9]+)*',text) is not None
def revision(value):
    check(isinstance(value,str) and re.fullmatch(r'r[0-9]{3}',value) and value!='r000','Revision must be r001-r999')
    return int(value[1:])
def local(root,value):
    check(isinstance(value,str) and value,'Missing file path')
    check('\\' not in value and not Path(value).is_absolute() and not re.match(r'^[A-Za-z]:',value),'Use relative forward-slash paths')
    p=(root/value).resolve();check(root.resolve() in p.parents,'Path escapes production root');return p
def naming(root,value,category=None,rev=None):
    p=local(root,value);parts=Path(value).parts
    check(all(snake(x) for x in parts[:-1]),'Directories must be lowercase snake_case: '+value)
    check(snake(p.stem) and re.fullmatch(r'\.[a-z0-9]+',p.suffix),'Filename must be lowercase snake_case: '+value)
    words=p.stem.split('_')
    check(not any(re.fullmatch(r'(?:final|new|copy)[0-9]*|v[0-9]+|[0-9]{8}',w) for w in words),'Forbidden temporary/date/version token: '+value)
    if category:
        check(parts[0]==category,'File stored in wrong delivery category: '+value)
        suffix=re.search(r'_(r[0-9]+)$',p.stem)
        if suffix:revision(suffix[1])
        if category in {'source','history'}:
            check(suffix is not None and suffix[1]==rev,'Source/history must retain matching rNNN: '+value)
        if category=='runtime':
            check(not any(re.fullmatch(r'r[0-9]+',w) for w in words),'Runtime path must not carry revision')
            check('source' not in words and p.suffix not in {'.psd','.blend','.kra','.xcf','.txt','.md','.json'},'Source/work files cannot enter runtime')
    return p

def file_ok(root,path):
    p=naming(root,path);check(p.is_file() and p.stat().st_size>0,'Missing/empty file: '+path);return p

def known(value):return value is not None and value not in ('','unknown','pending')
def registration(row):
    dev=row['developer_registration'];check(dev['status'] in {'pending','confirmed'},'Invalid developer registration status')
    for k in ('asset_id','asset_key','runtime_path','confirmation'):check(k in dev,'Missing developer field '+k)
    if dev['status']=='confirmed':
        check(row['name_status']=='confirmed','Confirmed registration requires confirmed logical name')
        check(all(isinstance(dev[k],str) and dev[k].strip() for k in ('asset_id','asset_key','runtime_path','confirmation')),'Developer confirmation cannot be fabricated from empty fields')
    if row['files']['runtime']:check(dev['status']=='confirmed','Runtime requires developer confirmation')

def record(root,row,kind):
    check(snake(row['production_ref']),'Invalid internal production_ref')
    check(snake(row['asset_name']),'Invalid asset_name')
    check(row['name_status'] in {'proposed','confirmed'},'Invalid name_status')
    revision(row['revision']);check(row['change_type'] in {'new','modified'},'Invalid change_type')
    check(row['status'] in STATES,'Invalid asset status')
    check(row['purpose'] and row['runtime_export_format'],'Missing purpose/export format')
    check(set(row['files'])==CATEGORIES,'Expected five file categories')
    approved=row.get('developer_approved_roles',[])
    for item in approved:check(snake(item['role']) and item.get('confirmation'),'New role needs developer confirmation')
    role_set=ROLES|{x['role'] for x in approved}
    variant=row.get('variant');check(variant is None or snake(variant),'Invalid variant')
    base=row['asset_name']+('_'+variant if variant else '')
    all_paths=[]
    for category,paths in row['files'].items():
        check(isinstance(paths,list),'File category must be an array')
        for path in paths:
            p=naming(root,path,category,row['revision']);stem=re.sub(r'_r[0-9]{3}$','',p.stem)
            check(stem==base or stem.startswith(base+'_'),'Filename differs from logical name/variant')
            role='main' if stem==base else stem[len(base)+1:]
            check(role in role_set,'Nonstandard role requires developer confirmation: '+role)
            if category=='runtime':check(p.suffix[1:]==row['runtime_export_format'],'Runtime export format mismatch')
            if row['status']=='passed':file_ok(root,path)
            all_paths.append(path)
    check(len(all_paths)==len(set(all_paths)),'Duplicate path in asset categories')
    for dep in row['dependencies']:
        naming(root,dep)
        if row['status']=='passed':file_ok(root,dep)
    registration(row)
    proposal=row.get('proposed_runtime_filename')
    if proposal:naming(root,'runtime/'+proposal,'runtime',row['revision'])
    check(row['software'] and all(x.get('name') and x.get('version') for x in row['software']),'Software/version fields required')
    pr=row['provenance'];check(pr['category'] in PROVENANCE,'Unknown provenance category')
    check(pr.get('source') and pr.get('license_scope') and isinstance(pr.get('evidence'),list),'Source/license/evidence fields required')
    check(row['source_availability']['status'] in {'available','not_available'},'Invalid source availability')
    if row['source_availability']['status']=='not_available':check(row['source_availability'].get('reason'),'Missing source absence reason')
    spec=row['specifications']
    required={'image':['width','height','color_space','has_alpha','lossless','usage'],'video':['width','height','duration_s','fps','codec','has_audio'],'audio':['duration_s','sample_rate','channels','loop','seamless_loop'],'model':['units','orientation','pivot','skeleton','animations','materials','collision_objects','godot_suffixes']}[kind]
    check(all(k in spec for k in required),'Missing '+kind+' specification fields')
    if row['status']=='passed':
        check(all(known(spec[k]) for k in required),'Passed asset has unknown specifications')
        for k in ('width','height','duration_s','fps','sample_rate','channels'):
            if k in spec:check(isinstance(spec[k],(int,float)) and not isinstance(spec[k],bool) and spec[k]>0,'Invalid numeric specification '+k)
        check(row.get('qa') and all(v=='passed' for v in row['qa'].values()),'Passed asset needs passed QA entries')
        if kind=='image':
            check(type(spec['has_alpha']) is bool and type(spec['lossless']) is bool,'Invalid image boolean fields')
            check(spec['usage'] in {'ui','texture','reference'},'Invalid image usage')
        if kind=='video':check(type(spec['has_audio']) is bool,'has_audio must be boolean')
    return all_paths

def media(root,row,kind):
    paths=record(root,row,kind)
    if row.get('path'):check(row['path'] in paths,'Primary media path absent from categories')
    if row['status']=='passed':
        p=file_ok(root,row.get('path'));check(row.get('sha256')==hashlib.sha256(p.read_bytes()).hexdigest(),'Passed media hash mismatch')
        check(row.get('provider') and row.get('model'),'Missing generator provenance')
        if kind=='video':
            check(15<=row['duration_s']<=20 and row['duration_s']==row['specifications']['duration_s'],'Actual video must be 15-20 seconds')
            check(isinstance(row.get('audio_specifications'),list),'Audio specifications array required')
            if row['specifications']['has_audio']:
                check(bool(row['audio_specifications']),'Audio track specification missing')
                for a in row['audio_specifications']:check(all(known(a.get(k)) for k in ('duration_s','sample_rate','channels','loop','seamless_loop')),'Incomplete audio information')
    elif row.get('path'):naming(root,row['path'])

def refs(rows,label):
    values=[x['production_ref'] for x in rows];check(len(values)==len(set(values)),'Duplicate '+label+' refs');return set(values)
def top(data):
    check(data.get('schema_version')=='2.0','Use schema 2.0; migrate old manifests explicitly')
    check(snake(data['project_id']) and snake(data['story_snapshot']),'Invalid project/story snapshot')
    check(data['status'] in STATES and data['delivery_status'] in DELIVERY,'Invalid top-level status')
def delivery(data,rows):
    if data['delivery_status']!='draft':
        check(data['status']=='passed','Non-draft delivery requires passed production')
        for row in rows:
            check(row['status']=='passed','Delivery includes unfinished media')
            pr=row['provenance'];check(known(pr['source']) and known(pr['license_scope']) and bool(pr['evidence']),'Delivery needs source/license evidence')
    if data['delivery_status']=='approved_for_runtime':
        check(any(row['files']['runtime'] for row in rows),'No runtime export in approved delivery')
        for row in rows:
            if row['files']['runtime']:check(row['developer_registration']['status']=='confirmed','Runtime not confirmed')

def production(root):
    root=root.resolve();h=read(root/'handoff.json');top(h)
    for k in ('world','story','atlas'):file_ok(root,h['documents'][k])
    entities=refs(h['entities'],'entity');nodes=refs(h['nodes'],'node');check(nodes,'No story nodes')
    for e in h['entities']:
        record(root,e,'image');check(e['kind'] in {'character','prop','location'} and e['scope'] in {'global','civilization'},'Invalid entity kind/scope')
        check(e['locked_features'],'Missing identity locks')
        if e['status']=='passed':
            check(e['design_files'],'Passed entity missing design images')
            for p in e['design_files']:
                file_ok(root,p);check(p in sum(e['files'].values(),[]),'Design missing from categories')
        if h['status']=='passed':check(e['status']=='passed','Handoff has unfinished entity')
    delivery(h,h['entities']);shots=set();keyframes=set()
    for n in h['nodes']:
        check(15<=n['duration_s']<=20,'Node duration outside 15-20 seconds');cursor=0
        for s in n['shots']:
            check(s['production_ref'] not in shots,'Duplicate shot ref');shots.add(s['production_ref'])
            check(s['start_s']==cursor and s['end_s']>cursor,'Shot gap/overlap');cursor=s['end_s']
            check(set(s['entity_refs'])<=entities,'Unknown entity reference');check(s['keyframe_refs'],'Missing keyframe references');keyframes.update(s['keyframe_refs'])
            check(all(s[k] for k in ('action','start_state','end_state','pov','era')),'Missing shot detail')
        check(cursor==n['duration_s'],'Incomplete node duration')
    ip=root/'image_delivery.json'
    if not ip.exists():return 'SOP 1 valid; SOP 2/3 not supplied'
    im=read(ip);top(im)
    for k in ('project_id','story_snapshot'):check(im[k]==h[k],'Image story baseline mismatch')
    image_refs=refs(im['images'],'image');check(keyframes<=image_refs,'Missing keyframe records');passed=set()
    for row in im['images']:
        media(root,row,'image');check(set(row['shot_refs'])<=shots and set(row['entity_refs'])<=entities,'Unknown image references')
        for p in row['reference_files']:
            naming(root,p)
            if row['status']=='passed':file_ok(root,p)
        if row['status']=='passed':passed.add(row['production_ref'])
    if im['status']=='passed':check(h['status']=='passed' and keyframes<=passed,'Incomplete upstream/keyframe coverage')
    delivery(im,im['images']);vp=root/'video_delivery.json'
    if not vp.exists():return 'SOP 1/2 valid; SOP 3 not supplied'
    vm=read(vp);top(vm)
    for k in ('project_id','story_snapshot'):check(vm[k]==h[k],'Video story baseline mismatch')
    refs(vm['videos'],'video');done=set()
    for row in vm['videos']:
        media(root,row,'video');check(row['node_ref'] in nodes and set(row['keyframe_refs'])<=image_refs,'Unknown video references')
        if row['status']=='passed':
            check(im['status']=='passed' and set(row['keyframe_refs'])<=passed,'Video uses unpassed images');done.add(row['node_ref'])
    if vm['status']=='passed':check(nodes<=done,'Missing completed nodes')
    delivery(vm,vm['videos'])
    return 'Schema 2.0, naming, registration boundaries and handoff references valid; visual/decode checks remain separate'

def all_records(root):
    rows=[]
    for fn,key in [('handoff.json','entities'),('image_delivery.json','images'),('video_delivery.json','videos')]:
        p=root/fn
        if p.exists():rows.extend(read(p)[key])
    return {r['production_ref']:r for r in rows}
def compare(previous,current):
    old=all_records(previous);new=all_records(current)
    for ref,row in new.items():
        if ref not in old or row['change_type']!='modified':continue
        before=old[ref];check(revision(row['revision'])>=revision(before['revision']),'Revision decreased')
        changed=row.get('sha256')!=before.get('sha256')
        if changed:check(revision(row['revision'])>revision(before['revision']),'Changed content needs increased Revision')
        if before['name_status']=='confirmed':check(row['asset_name']==before['asset_name'],'Modified existing logical name changed')
        if before['developer_registration']['status']=='confirmed':
            check(row['developer_registration']['status']=='confirmed','Existing registration lost')
            for k in ('asset_id','asset_key','runtime_path'):check(row['developer_registration'][k]==before['developer_registration'][k],'Modified existing '+k+' changed')
    for p in previous.rglob('*'):
        if p.is_file() and p.relative_to(previous).parts[0] in {'source','history'}:
            dest=current/p.relative_to(previous)
            check(dest.is_file() and p.read_bytes()==dest.read_bytes(),'Previous source/history revision overwritten or missing')

def bundle(root):
    entries=sorted(root.glob('project_*_skill_*/.agents/skills/*/SKILL.md'));check(len(entries)==3,'Expected three skills')
    for p in entries:
        text=p.read_text(encoding='utf-8');m=re.match(r'^---\n(.*?)\n---\n',text,re.S);check(m,'Missing frontmatter')
        name=re.search(r'^name: ([a-z0-9-]+)$',m[1],re.M);check(name and name[1]==p.parent.name,'Skill name mismatch')
        check(re.search(r'^description: .+',m[1],re.M),'Missing description')
    for p in root.rglob('*'):
        if '.git' in p.relative_to(root).parts:continue
        if p.suffix=='.json':read(p)
        if p.suffix=='.md':
            for link in re.findall(r'\]\(([^)]+)\)',p.read_text(encoding='utf-8')):
                if not link.startswith(('https://','http://','#')):check((p.parent/link).is_file(),'Broken local link: '+link)
    return production(root/'examples/atlantis')
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--production',type=Path);parser.add_argument('--previous',type=Path);args=parser.parse_args()
    try:
        print(production(args.production) if args.production else bundle(Path(__file__).resolve().parents[1]))
        if args.previous:
            check(args.production is not None,'--previous requires --production');production(args.previous);compare(args.previous,args.production);print('Previous delivery stability checked')
    except (ValueError,KeyError,TypeError,OSError) as e:parser.exit(1,'Validation failed: '+str(e)+'\n')
