import json,sys,subprocess
from pathlib import Path
root=Path(sys.argv[1]);sys.path.insert(0,str(root/'scripts'))
import m7c_storage_recovery_preflight_v01 as g
m=json.loads((root/'execution/M7C_STORAGE_RECOVERY_SOLVE_MANIFEST_V01.json').read_text(encoding='utf-8'))
c=json.loads((root/'execution/stage_contract.json').read_text(encoding='utf-8-sig'))
checks=g.artifact_checks(m,root)
storage=g.storage_check(m['storage_policy'],m['execution']['target_root'])
try:
 g.require_live_grant(c,m,root);refused=False
except RuntimeError as e:
 refused='NO_LIVE_SOLVE_GRANT' in str(e)
head=subprocess.check_output(['git','-C',str(root),'rev-parse','HEAD'],universal_newlines=True).strip()
ok=all(checks.values()) and storage['status']=='PASS_M7C_STORAGE_PREFLIGHT' and refused
print(json.dumps({'status':'PASS_CST_PYTHON36_RECOVERY_PREFLIGHT_COMPATIBILITY' if ok else 'HOLD_CST_PYTHON36_RECOVERY_PREFLIGHT_COMPATIBILITY','python':sys.executable,'version':sys.version,'source_commit':head,'artifact_checks':checks,'storage':storage,'ungranted_launch_refused':refused,'new_build':False,'new_solve':False,'application_instantiated':False}))
sys.exit(0 if ok else 4)
