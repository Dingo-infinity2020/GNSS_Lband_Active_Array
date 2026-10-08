from __future__ import print_function
import ast, argparse, json, sys
from pathlib import Path

EXPECTED_MAIN_ARGS=["parent","macro","reference_macro","inventory_contract","out","review_copy","evidence"]
EXPECTED_CLI_ATTRS=["parent_cst","macro","kernel_reference_macro","inventory_contract","out","review_copy","evidence"]

def main(path,out):
    path=Path(path)
    text=path.read_text(encoding="utf-8")
    tree=ast.parse(text,filename=str(path))
    defs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=="main"]
    args=[a.arg for a in defs[0].args.args] if len(defs)==1 else []
    calls=[]
    for n in ast.walk(tree):
        if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=="main":
            attrs=[]
            for x in n.args:
                if isinstance(x,ast.Attribute) and isinstance(x.value,ast.Name) and x.value.id=="a":
                    attrs.append(x.attr)
                else:
                    attrs.append(ast.dump(x))
            calls.append(attrs)
    checks={
      "one_main_definition":len(defs)==1,
      "main_args_exact":args==EXPECTED_MAIN_ARGS,
      "one_cli_main_call":len(calls)==1,
      "cli_main_call_exact":len(calls)==1 and calls[0]==EXPECTED_CLI_ATTRS,
      "review_copy_argparse_present":"--review-copy" in text,
      "no_run_solver_token":"run_solver(" not in text
    }
    status="PASS_E2C_BUILD_ENTRYPOINT_STATIC_CONTRACT" if all(checks.values()) else "HOLD_E2C_BUILD_ENTRYPOINT_STATIC_CONTRACT"
    result={"status":status,"path":str(path),"main_args":args,"main_calls":calls,"checks":checks}
    Path(out).write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,sort_keys=True))
    return 0 if status.startswith("PASS_") else 4

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--runner",required=True)
    ap.add_argument("--out",required=True)
    a=ap.parse_args()
    try:
        sys.exit(main(a.runner,a.out))
    except Exception as ex:
        print("EXCEPTION="+repr(ex))
        sys.exit(9)
