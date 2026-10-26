param(
    [Parameter(Mandatory=$true)][string]$ProjectRoot,
    [Parameter(Mandatory=$true)][string]$ControlPython,
    [Parameter(Mandatory=$true)][string]$CstPython,
    [Parameter(Mandatory=$true)][string]$OpsRoot,
    [Parameter(Mandatory=$true)][string]$EvidenceRoot
)
$ErrorActionPreference = 'Stop'
$env:GIT_OPTIONAL_LOCKS = '0'
$env:PYTHONDONTWRITEBYTECODE = '1'
if (Test-Path -LiteralPath $EvidenceRoot) { throw 'HOLD_QUALIFICATION_EVIDENCE_EXISTS' }
New-Item -ItemType Directory -Path $EvidenceRoot | Out-Null
$testOutput = & $ControlPython -B (Join-Path $ProjectRoot 'scripts\test_m7c_storage_recovery_v01.py') 2>&1
$testExit = $LASTEXITCODE
$testOutput | Out-File -LiteralPath (Join-Path $EvidenceRoot 'regression.txt') -Encoding utf8
if ($testExit -ne 0) { throw 'HOLD_M7C_RECOVERY_REGRESSION' }
& $ControlPython -B (Join-Path $ProjectRoot 'scripts\audit_m7c_storage_recovery_v01.py') --project-root $ProjectRoot --host-readonly --output (Join-Path $EvidenceRoot 'HOST_QUALIFICATION.json')
if ($LASTEXITCODE -ne 0) { throw 'HOLD_M7C_RECOVERY_HOST_AUDIT' }
& $CstPython -B (Join-Path $ProjectRoot 'scripts\run_m7c_storage_recovery_solve_v01.py') --help | Out-File -LiteralPath (Join-Path $EvidenceRoot 'simulator_runtime_help.txt') -Encoding utf8
if ($LASTEXITCODE -ne 0) { throw 'HOLD_M7C_RECOVERY_RUNTIME_HELP' }
$importProbe = @'
import json,sys
sys.path.insert(0,sys.argv[1])
import configure_r1e1a4a_ar0_b1r_r4_a0_e2c_s0_presolve as p
import qualify_r1e1a4a_ar0_b1r_r4_a0_e2c_s0_readonly as q
import evaluate_m7c_modal_restoration_readonly_v01 as e
print(json.dumps({'status':'PASS_RUNTIME_IMPORT_ONLY','python':sys.executable,'version':sys.version,'interface_module':p.ci.__file__,'design_environment_callable':callable(p.ci.DesignEnvironment),'new_build':False,'new_solve':False,'application_instantiated':False}))
'@
$importOutput = & $CstPython -B -c $importProbe (Join-Path $ProjectRoot 'scripts')
$importExit = $LASTEXITCODE
$importOutput | Out-File -LiteralPath (Join-Path $EvidenceRoot 'runtime_import.json') -Encoding utf8
if ($importExit -ne 0) { throw 'HOLD_M7C_RECOVERY_RUNTIME_IMPORT' }
$contractOutput = & (Join-Path $OpsRoot 'runner\nw\simops.cmd') contract-check --contract (Join-Path $ProjectRoot 'execution\stage_contract.json')
$contractExit = $LASTEXITCODE
$contractOutput | Out-File -LiteralPath (Join-Path $EvidenceRoot 'CONTRACT_CHECK.json') -Encoding utf8
if ($contractExit -ne 0) { throw 'HOLD_M7C_RECOVERY_CONTRACT_CHECK' }
$inventoryRelative = 'execution\R1E1A4A_AR0_B1R_R4_A0_E2C_DUALPOL_BUILD_INVENTORY_V01.json'
$inventoryProbe = @'
import hashlib,json,sys
from pathlib import Path
a=Path(sys.argv[1]);b=Path(sys.argv[2]);load=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
same=load(a)==load(b)
print(json.dumps({'historical_checkout_sha256':hashlib.sha256(a.read_bytes()).hexdigest(),'qualification_checkout_sha256':hashlib.sha256(b.read_bytes()).hexdigest(),'parsed_inventory_equal':same}))
sys.exit(0 if same else 4)
'@
$inventoryOutput = & $ControlPython -B -c $inventoryProbe (Join-Path 'D:\GNSS_R4A0E1_20260928' $inventoryRelative) (Join-Path $ProjectRoot $inventoryRelative)
$inventoryExit = $LASTEXITCODE
$inventoryOutput | Out-File -LiteralPath (Join-Path $EvidenceRoot 'INVENTORY_BYTE_BINDING.json') -Encoding utf8
if ($inventoryExit -ne 0) { throw 'HOLD_M7C_RECOVERY_INVENTORY_SEMANTICS' }
$receipt = [ordered]@{
    status='PASS_M7C_RECOVERY_NONPRODUCTION_HOST_QUALIFICATION'
    observed_at_utc=[DateTime]::UtcNow.ToString('yyyy-MM-ddTHH:mm:ssZ')
    host_name=[System.Net.Dns]::GetHostName()
    source_commit=(& git -C $ProjectRoot rev-parse HEAD)
    source_status=@(& git -C $ProjectRoot status --porcelain)
    source_autocrlf=(& git -C $ProjectRoot config core.autocrlf)
    regression_exit=$testExit
    runtime_help_exit=0
    runtime_import_exit=$importExit
    contract_check_exit=$contractExit
    inventory_semantics_exit=$inventoryExit
    build_invocations=0
    solve_invocations=0
    simulator_application_launched=$false
    actual_formal_packet_generated=$false
    BUILD_AUTHORIZED=$false
    SOLVE_AUTHORIZED=$false
    transport='DIRECT_SSH_USER_AUTHORIZED_ROUTE_EXCEPTION'
    output_root_created=(Test-Path -LiteralPath 'C:\GNSS_Lband_Active_Array\runs\formal\solver_runs\M7C_STORAGE_RECOVERY_20261026_V01')
}
if ($receipt.source_status.Count -ne 0 -or $receipt.output_root_created) { throw 'HOLD_M7C_RECOVERY_QUALIFICATION_SIDE_EFFECT' }
$receipt | ConvertTo-Json -Depth 8 | Out-File -LiteralPath (Join-Path $EvidenceRoot 'RECEIPT.json') -Encoding utf8
$receipt | ConvertTo-Json -Depth 8 -Compress
