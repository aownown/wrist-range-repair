#!/usr/bin/env python3
"""Recount stored tables only. No scientific program is imported or executed."""
from pathlib import Path
import csv,json,hashlib,statistics,math
B=Path(__file__).resolve().parent
checks=[]
def load(name):
 p=B/name
 return json.loads(p.read_text()) if p.suffix=='.json' else list(csv.DictReader(p.open()))
def check(label,ok):
 checks.append({'check':label,'passed':bool(ok)})
 if not ok:raise AssertionError(label)
def n(x):return int(x)
def truth(x):return str(x).lower() in ('1','true')
can=load('results/can_all840_membership.csv');valid=[r for r in can if r['eligibility']=='normal_qualified'];na=[r for r in can if r not in valid]
check('Can 840 unique declared cells; 700 scored and 140 NA',len(can)==840 and len({(r['context_id'],r['method']) for r in can})==840 and len(valid)==700 and len(na)==140)
check('Can ten scored source groups',len({r['source_group'] for r in valid})==10)
check('Can strict equals original G AND C AND R',all(n(r['original_S'])==n(r['original_G'])*n(r['original_C'])*n(r['original_R']) for r in valid))
src={r['context_id']:r for r in valid if r['method']=='source_copy'}
check('Can source original12 and plus40 18',sum(n(r['original_S']) for r in src.values())==12 and sum(n(r['plus40_S']) for r in src.values())==18)
check('Can stored source-clock pairings',all(r['original_source_S']==src[r['context_id']]['original_S'] and r['plus40_source_S']==src[r['context_id']]['plus40_S'] for r in valid))
comp=load('results/can_two_clock_components.csv');cost=load('results/can_condition_cost_ms.csv');methods=load('results/can_original_summary.csv')
check('Can cost covers every scored condition-method exactly',len(cost)==700 and {(r['context_id'],r['method']) for r in valid}=={(r['context_id'],r['method']) for r in cost})
for c in comp:
 m=c['method'];rs=[r for r in valid if r['method']==m];check(m+' scored/NA membership',len(rs)==50 and len([r for r in na if r['method']==m])==10)
 for clock,prefix,source_prefix,P,F in [('original','orig','original',12,38),('plus40','plus40','plus40',18,32)]:
  strict=sum(n(r[clock+'_S']) for r in rs)
  repair=sum(n(r[clock+'_S']) and not n(r[source_prefix+'_source_S']) for r in rs)
  damage=sum(not n(r[clock+'_S']) and n(r[source_prefix+'_source_S']) for r in rs)
  check(m+' '+clock+' totals/repair/regression',strict==n(c[prefix+'_strict']) and repair==n(c[prefix+'_repair']) and damage==n(c[prefix+'_damage']) and strict==P+repair-damage and n(c[prefix+'_source_P'])==P and n(c[prefix+'_source_F'])==F)
 for part in ['G','C','R']:check(m+' original '+part,sum(n(r['original_'+part]) for r in rs)==n(c['orig_'+part]))
 s=next(x for x in methods if x['method']==m);check(m+' plot/table agreement',all(n(s[a])==n(c[b]) for a,b in [('strict','orig_strict'),('repair','orig_repair'),('damage','orig_damage')]))
diffs=load('results/can_source_differences.csv')
for r in diffs:
 rs=[x for x in valid if x['source_group']==r['source']]
 total=lambda mode:sum(n(x['original_S']) for x in rs if x['method'].startswith('nn_expanded_'+mode+'_seed'))
 check(r['source']+' Full-Constant paired difference',math.isclose((total('full')-total('constant'))/3,float(r['delta']),abs_tol=1e-12))
check('Can all ten source differences: four positive three negative three zero',len(diffs)==10 and sum(float(r['delta'])>1e-12 for r in diffs)==4 and sum(float(r['delta'])< -1e-12 for r in diffs)==3 and sum(abs(float(r['delta']))<=1e-12 for r in diffs)==3)
check('Can stored effect point estimate only (no resampling)',math.isclose(statistics.mean(float(r['delta']) for r in diffs),load('results/figure3_effect_summary.json')['mean_success_difference_per_source'],abs_tol=1e-12))
lift=load('results/lift_all300_cells.csv');ls=load('results/lift_method_summary.json')['rows'];src={r['context_id']:r for r in lift if r['method']=='source_copy'}
check('Lift 300 unique cells and ten independent sources',len(lift)==300 and len({(r['context_id'],r['method']) for r in lift})==300 and len({r['source'] for r in lift})==10)
check('Lift both clocks retain exact same strict member set',all(truth(r['strict_original_clock'])==truth(r['strict_extended_clock']) for r in lift))
check('Lift original G/C/R conjunction',all(truth(r['strict_original_clock'])==(truth(r['native_goal_original']) and not truth(r['original_carry_failure']) and truth(r['all9_original'])) for r in lift))
for s in ls:
 rs=[r for r in lift if r['method']==s['method']]
 for clock,field in [('original','strict_original_clock'),('extended','strict_extended_clock')]:
  strict=sum(truth(r[field]) for r in rs);repair=sum(truth(r[field]) and not truth(src[r['context_id']][field]) for r in rs);damage=sum(not truth(r[field]) and truth(src[r['context_id']][field]) for r in rs)
  check(s['method']+' Lift '+clock+' accounting',len(rs)==30 and strict==s['strict_'+clock+'_count'] and strict==28+repair-damage and all(truth(r['repair_'+clock])==(truth(r[field]) and not truth(src[r['context_id']][field])) and truth(r['damage_'+clock])==(not truth(r[field]) and truth(src[r['context_id']][field])) for r in rs))
  if clock=='original':check(s['method']+' Lift summary repairs/regressions',repair==s['repair_original_count'] and damage==s['damage_original_count'])
 check(s['method']+' Lift warm timing median',math.isclose(statistics.median(float(r['median_warm_generation_ms']) for r in rs),s['median_of30_context_median_warm_generation_ms'],rel_tol=0,abs_tol=1e-12))
 check(s['method']+' Lift stored same-CPU executed pairing',all(truth(r['matched_CPU_generated_programme_physically_executed']) for r in rs))
# Source disjointness is scoped to the exact role lists actually included.
roles=load('protocols/source_roles.csv')
for task,sets in [('Can',[['original_TRAIN_contributor','new_train_expansion'],['new_development'],['new_final_confirmation']]),('Lift',[['TRAIN'],['DEV'],['TEST']])]:
 groups=[{r['source'] for r in roles if r['task']==task and r['role'] in names} for names in sets]
 check(task+' listed TRAIN/DEV/FINAL source-disjoint',all(not groups[i]&groups[j] for i in range(3) for j in range(i+1,3)))
for fn,count,repairs in [('Can_original36',36,31),('Can_expanded59',59,49),('Lift45',45,5)]:
 rs=load('protocols/'+fn+'_teacher_membership.csv');check(fn+' retained teacher mix',len(rs)==count and sum(truth(r['repaired_original_failure']) for r in rs)==repairs)
sel=load('protocols/can_DEV_family_update_candidates.csv');check('DEV staged selection totals',len(sel)==5 and all(sum(n(r['Full_seed'+str(i)]) for i in range(3))==n(r['Full_total']) for r in sel))
models=load('protocols/selected_models_and_constant.json');constants=[r['capability_constant'] for r in models if r['mode']=='constant'];check('Three Constant feature vectors are identical 14-D',len(constants)==3 and all(len(x)==14 and x==constants[0] for x in constants))
for entry in load('FILE_MANIFEST.json'):
 p=B/entry['file'];check('file bytes '+entry['file'],p.is_file() and hashlib.sha256(p.read_bytes()).hexdigest()==entry['sha256'])
out={'passed':all(x['passed'] for x in checks),'checks':checks,'check_count':len(checks),'scope':'Stored-table aggregation and local included-file checks only; no bootstrap, numerical model forward, FK, simulator or external artifact hash verification.','scientific_results_changed':False}
(B/'VERIFICATION_RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print('PASS',len(checks),'stored-table and included-file checks')
