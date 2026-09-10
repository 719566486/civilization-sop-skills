#!/usr/bin/env python3
"""Offline regression checks; writes fixtures only under the required --workdir."""
import argparse,copy,json,runpy,shutil,hashlib
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--workdir',required=True,type=Path);args=p.parse_args()
root=Path(__file__).resolve().parents[1];work=args.workdir.resolve();work.mkdir(parents=True,exist_ok=True)
m=runpy.run_path(str(root/'scripts/validate_bundle.py'));results=[]
def expect(name,fn,fail=True):
    try:fn()
    except (ValueError,KeyError,TypeError) as e:
        if not fail:raise
        results.append({'case':name,'result':'rejected_as_expected','reason':str(e)})
    else:
        if fail:raise AssertionError('Invalid fixture accepted: '+name)
        results.append({'case':name,'result':'accepted_as_expected'})
def name(path,category=None,rev='r001'):return lambda:m['naming'](work,path,category,rev)
for path in ['runtime/TicketMachine.png','runtime/ticket-machine.png','runtime/售票机.png','runtime/ticket_machine.PNG','runtime/ticket_machine_final2.png','runtime/ticket_machine_new.png','runtime/ticket_machine_copy.png','runtime/ticket_machine_v2.png','runtime/ticket_machine_20260907.png','Runtime/ticket_machine.png']:
    expect(path,name(path))
expect('runtime_revision',name('runtime/ch01_signal03_r001.mp4','runtime'))
expect('runtime_source',name('runtime/ticket_machine_source.blend','runtime'))
expect('source_missing_revision',name('source/ticket_machine_source.blend','source'))
expect('history_revision_mismatch',name('history/ch01_signal03_r002.mp4','history'))
for rev in ['r000','r1','r1000','v001']:expect('revision_'+rev,lambda rev=rev:m['revision'](rev))
expect('runtime_stable',name('runtime/ch01_signal03.mp4','runtime'),False)
expect('source_valid',name('source/ticket_machine_source_r001.blend','source'),False)
expect('history_valid',name('history/ch01_signal03_r001.mp4','history'),False)
row=json.loads((root/'examples/atlantis/image_delivery.json').read_text(encoding='utf-8'))['images'][0]
bad=copy.deepcopy(row);bad['files']['runtime']=['runtime/ch01_signal03_sh01.png']
expect('runtime_missing_developer',lambda:m['record'](work,bad,'image'))
confirmed=copy.deepcopy(bad);confirmed['name_status']='confirmed';confirmed['developer_registration']={'status':'confirmed','asset_id':'Developer-ID-42','asset_key':'story.ch01.signal03.image.main','runtime_path':'res://story/ch01_signal03_sh01.png','confirmation':'developer approved test fixture'}
expect('developer_fields_are_not_filenames',lambda:m['record'](work,confirmed,'image'),False)
missing=copy.deepcopy(row);del missing['specifications']['color_space'];expect('missing_color_space',lambda:m['record'](work,missing,'image'))
role=copy.deepcopy(row);role['files']['reference']=['reference/ch01_signal03_sh01_layout_r001.png'];expect('unapproved_role',lambda:m['record'](work,role,'image'))
role['developer_approved_roles']=[{'role':'layout','confirmation':'developer approved explicit test role'}];expect('approved_custom_role',lambda:m['record'](work,role,'image'),False)
expect('schema_2_example',lambda:m['production'](root/'examples/atlantis'),False)
# Isolated full pipeline malformed inputs.
for case,file,mutator in [
 ('timing_gap','handoff.json',lambda x:x['nodes'][0]['shots'][1].update(start_s=6)),
 ('bad_duration','handoff.json',lambda x:x['nodes'][0].update(duration_s=14)),
 ('unknown_ref','handoff.json',lambda x:x['nodes'][0]['shots'][0]['entity_refs'].append('missing')),
 ('story_mismatch','image_delivery.json',lambda x:x.update(story_snapshot='story_002')),
 ('false_runtime_approval','video_delivery.json',lambda x:x.update(delivery_status='approved_for_runtime'))]:
    dest=work/case;shutil.copytree(root/'examples/atlantis',dest,dirs_exist_ok=True);f=dest/file;x=json.loads(f.read_text(encoding='utf-8'));mutator(x);f.write_text(json.dumps(x),encoding='utf-8');expect(case,lambda dest=dest:m['production'](dest))
# Previous-delivery comparisons do not modify the user's assets.
previous=work/'previous';current=work/'current';previous.mkdir(exist_ok=True);current.mkdir(exist_ok=True)
a=copy.deepcopy(confirmed);a['production_ref']='asset_ref';a['sha256']='old';a['files']['runtime']=[]
b=copy.deepcopy(a);b.update(change_type='modified',revision='r002',sha256='changed')
def put(folder,row): (folder/'image_delivery.json').write_text(json.dumps({'images':[row]}),encoding='utf-8')
put(previous,a);put(current,b);expect('revision_increase_same_identity',lambda:m['compare'](previous,current),False)
for field in ['asset_name','asset_id','asset_key','runtime_path']:
    c=copy.deepcopy(b)
    if field=='asset_name':c[field]='different_name'
    else:c['developer_registration'][field]='different'
    put(current,c);expect('modified_'+field,lambda:m['compare'](previous,current))
c=copy.deepcopy(b);c['revision']='r001';put(current,c);expect('changed_without_revision',lambda:m['compare'](previous,current))
put(current,b);(previous/'history').mkdir(exist_ok=True);(current/'history').mkdir(exist_ok=True)
(previous/'history/asset_r001.png').write_bytes(b'old');(current/'history/asset_r001.png').write_bytes(b'overwritten');expect('old_history_overwritten',lambda:m['compare'](previous,current))
(current/'history/asset_r001.png').write_bytes(b'old');expect('history_preserved',lambda:m['compare'](previous,current),False)
(work/'test_results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
print(str(len(results))+' offline checks passed')
