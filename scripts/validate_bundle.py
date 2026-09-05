#!/usr/bin/env python3
"""Validate SOP package and JSON handoffs; standard library only, no API calls."""
import argparse, json, re, hashlib
from pathlib import Path
STATES={'planned','generated','passed','failed','blocked','stale'}
def check(ok,msg):
    if not ok: raise ValueError(msg)
def read(p): return json.loads(p.read_text(encoding='utf-8'))
def local(root,value):
    check(isinstance(value,str) and bool(value),'Missing file path')
    p=Path(value)
    check(not p.is_absolute() and not re.match(r'^[A-Za-z]:',value),'Use relative paths')
    dest=(root/p).resolve()
    check(root.resolve() in dest.parents,'Path escapes production root')
    return dest
def file_ok(root,value):
    p=local(root,value);check(p.is_file() and p.stat().st_size>0,f'Missing/empty file: {value}');return p

def ids(rows,label):
    keys=[r['id'] for r in rows]
    check(len(keys)==len(set(keys)),f'Duplicate {label} IDs')
    return set(keys)
def media_ok(root,row):
    check(row['status'] in STATES,'Invalid media status')
    if row['status']=='passed':
        p=file_ok(root,row.get('path'))
        check(row.get('qa') and all(v=='passed' for v in row['qa'].values()),'Passed media needs passed QA entries')
        check(bool(row.get('provider')) and bool(row.get('model')),'Passed media needs provider/model provenance')
        digest=hashlib.sha256(p.read_bytes()).hexdigest()
        check(row.get('sha256')==digest,'Passed media hash mismatch')
    elif row.get('path'): local(root,row['path'])

def production(root):
    h=read(root/'handoff.json')
    check(h['schema_version']=='1.0' and h['status'] in STATES,'Invalid handoff version/status')
    for key in ('world','story','atlas'): file_ok(root,h['documents'][key])
    entity_ids=ids(h['entities'],'entity'); shot_ids=set(); kf_ids=set()
    segment_ids=ids(h['segments'],'segment')
    check(bool(segment_ids),'No segments')
    for entity in h['entities']:
        check(entity['scope'] in ('global','civilization'),'Invalid entity scope')
        check(entity['kind'] in ('character','prop','location'),'Invalid entity kind')
        check(bool(entity['locked_features']),'Entity missing locked features')
        check(entity['status'] in STATES,'Invalid entity status')
        if entity['status']=='passed':
            check(bool(entity['design_files']),'Passed entity missing actual design images')
            for f in entity['design_files']: file_ok(root,f)
        if h['status']=='passed': check(entity['status']=='passed','Handoff passed with unfinished entity')
    for seg in h['segments']:
        check(15<=seg['duration_s']<=20,'Segment duration outside 15-20 seconds')
        cursor=0
        for shot in seg['shots']:
            check(shot['id'] not in shot_ids,'Duplicate shot ID');shot_ids.add(shot['id'])
            check(abs(shot['start_s']-cursor)<1e-6 and shot['end_s']>cursor,'Shot gap/overlap/nonpositive length')
            cursor=shot['end_s']
            check(set(shot['entity_ids'])<=entity_ids,'Unknown entity reference')
            check(bool(shot['keyframe_ids']),'Shot missing keyframe references')
            kf_ids.update(shot['keyframe_ids'])
            for key in ('pov','era','action','start_state','end_state'):check(bool(shot[key]),'Missing shot '+key)
        check(abs(cursor-seg['duration_s'])<1e-6,'Shots do not cover full segment')
    image_path=root/'image_manifest.json'
    if not image_path.exists(): return 'SOP 1 structure checked; SOP 2/3 not supplied'
    im=read(image_path)
    for field in ('schema_version','project_id','revision'):check(im[field]==h[field],'Image handoff version mismatch')
    check(im['status'] in STATES,'Invalid image manifest status')
    image_ids=ids(im['images'],'image')
    check(kf_ids<=image_ids,'Missing planned keyframe records')
    passed_images=set()
    for image in im['images']:
        check(set(image['shot_ids'])<=shot_ids,'Unknown image shot')
        check(set(image['entity_ids'])<=entity_ids,'Unknown image entity')
        media_ok(root,image)
        if image['status']=='passed':
            for ref in image['reference_files']:file_ok(root,ref)
            passed_images.add(image['id'])
    if im['status']=='passed':
        check(h['status']=='passed' and kf_ids<=passed_images,'Images passed before upstream/coverage passed')
    vp=root/'video_manifest.json'
    if not vp.exists():return 'SOP 1/2 structure checked; SOP 3 not supplied'
    vm=read(vp)
    for field in ('schema_version','project_id','revision'):check(vm[field]==h[field],'Video handoff version mismatch')
    check(vm['status'] in STATES,'Invalid video manifest status')
    ids(vm['videos'],'video');done=set()
    for video in vm['videos']:
        check(video['segment_id'] in segment_ids,'Unknown video segment')
        check(set(video['keyframe_ids'])<=image_ids,'Unknown video keyframes')
        media_ok(root,video)
        if video['status']=='passed':
            check(im['status']=='passed','Video passed before images passed')
            check(15<=video['duration_s']<=20,'Actual video duration outside 15-20 seconds')
            check(set(video['keyframe_ids'])<=passed_images,'Video uses unpassed images')
            done.add(video['segment_id'])
    if vm['status']=='passed': check(segment_ids<=done,'Video manifest has missing final segments')
    return 'Handoff references and timing valid; media/visual verification remains separate'

def bundle(root):
    skills=sorted(root.glob('project_*_skill_*/.agents/skills/*/SKILL.md'))
    check(len(skills)==3,'Expected three skills')
    for p in skills:
        text=p.read_text(encoding='utf-8')
        m=re.match(r'^---\n(.*?)\n---\n',text,re.S);check(m is not None,'Missing frontmatter')
        name=re.search(r'^name: ([a-z0-9-]+)$',m[1],re.M)
        check(name is not None and name[1]==p.parent.name,'Invalid name/directory')
        check(re.search(r'^description: .+',m[1],re.M) is not None,'Missing description')
        for link in re.findall(r'\]\(([^)]+)\)',text):
            if not re.match(r'https?://',link):check((p.parent/link).is_file(),'Missing skill reference '+link)
        check((p.parent/'agents/openai.yaml').is_file(),'Missing UI metadata')
    for p in root.rglob('*.json'):read(p)
    return production(root/'examples/atlantis')
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--production',type=Path);args=parser.parse_args()
    try: print(production(args.production.resolve()) if args.production else bundle(Path(__file__).resolve().parents[1]))
    except (ValueError,KeyError,TypeError,OSError) as error:parser.exit(1,'Validation failed: '+str(error)+'\n')
