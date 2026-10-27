#!/usr/bin/env python3
"""Static arithmetic audit for R4-A0-E1 one-LNA landing-zone geometry.

No CST dependency. No remote execution.
"""
from __future__ import print_function
import json, math
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
MANIFEST=ROOT/"execution"/"R1E1A4A_AR0_B1R_R4_A0_E1_PREBUILD_MANIFEST_V01.json"
OUT=ROOT/"evidence"/"r4_a0_e1_static_prebuild_20260927"/"R4_A0_E1_STATIC_ARITHMETIC_AUDIT_REPRODUCED.json"

def inside(x,a,b,margin=0.0,eps=1e-12):
    return x+eps>=a+margin and b-margin+eps>=x

def main():
    m=json.loads(MANIFEST.read_text())
    checks={}
    detail={}
    qmin,qmax=m["substrate"]["q_mm"]
    qpkg=m["package"]["center_qv_mm"][0]
    pkg=(qpkg-1.0,qpkg+1.0)
    detail["package_edge_margins_q_mm"]=[pkg[0]-qmin,qmax-pkg[1]]
    checks["package_body_edge_margin_ge_0p25"]=min(detail["package_edge_margins_q_mm"])>=0.25

    paddle=(-0.55,1.05,6.60,7.40)
    r=0.35/2.0
    vm=[]
    for v in m["paddle_vias"]:
        vals=[v["q_mm"]-r-paddle[0],paddle[1]-(v["q_mm"]+r),
              v["v_mm"]-r-paddle[2],paddle[3]-(v["v_mm"]+r)]
        vm.append({"q_mm":v["q_mm"],"margins_mm":vals})
    detail["paddle_via_margins"]=vm
    checks["paddle_vias_inside_paddle"]=all(min(x["margins_mm"])>=-1e-12 for x in vm)

    # Right-side lane lands occupy q=1.15..1.75 in the frozen 4-mm coupon.
    detail["right_lane_board_edge_margin_mm"]=qmax-1.75
    checks["right_lane_board_edge_margin_ge_0p20"]=detail["right_lane_board_edge_margin_mm"]>=0.20

    detail["decoupler_via_board_edge_margin_mm"]=qmax-(1.45+r)
    checks["decoupler_via_edge_margin_ge_0p20"]=detail["decoupler_via_board_edge_margin_mm"]>=0.20

    def out_half(v):
        if v<=9.60: return 0.30
        if v>=10.60: return 0.95
        return 0.30+(0.95-0.30)*(v-9.60)
    ss=[10.0,10.25,10.5,10.6,10.9,11.15,11.4]
    detail["output_to_right_lane_gaps_mm"]=[{"v_mm":v,"gap_mm":1.15-out_half(v)} for v in ss]
    detail["min_output_to_right_lane_gap_mm"]=min(x["gap_mm"] for x in detail["output_to_right_lane_gaps_mm"])
    checks["output_to_right_lane_ge_0p20"]=detail["min_output_to_right_lane_gap_mm"]>=0.20-1e-12

    gaps={"C_IN":5.30-4.90,"C_OUT":9.10-8.70,"L1":9.10-8.70,"C_RF":10.90-10.50}
    detail["component_node_gaps_mm"]=gaps
    checks["component_node_gaps_ge_0p40"]=all(x>=0.40-1e-12 for x in gaps.values())

    detail["rf_land_to_paddle_via_barrel_mm"]={
      "RF_IN":(7.0-r)-6.30,
      "RF_OUT":7.70-(7.0+r)}
    checks["rf_land_to_paddle_via_ge_0p20"]=all(x>=0.20 for x in detail["rf_land_to_paddle_via_barrel_mm"].values())

    spoke_centers=[-0.50,0.50,1.00]
    ov=[]
    for q in spoke_centers:
        lo,hi=q-0.10,q+0.10
        overlap=max(0.0,min(hi,1.05)-max(lo,-0.55))
        ov.append({"q_mm":q,"paddle_overlap_mm":overlap})
    detail["ground_spoke_paddle_overlap"]=ov
    checks["ground_spokes_touch_paddle"]=all(x["paddle_overlap_mm"]>0 for x in ov)

    owner={
      "E_UP":(-0.30,0.30,4.40,4.90),
      "P_IN":(-0.125,0.125,5.87,6.30),
      "P_OUT":(-0.125,0.125,7.70,8.13),
      "E_DN":(-0.30,0.30,9.10,9.60),
      "B_VDD":(1.15,1.75,9.60,10.00),
      "B_VBIAS":(-0.625,-0.375,5.87,6.30)}
    detail["port_containment"]=[]
    for p in m["ports"]:
        rr=owner[p["name"]]
        ok=inside(p["q_mm"],rr[0],rr[1]) and inside(p["v_mm"],rr[2],rr[3])
        detail["port_containment"].append({"name":p["name"],"inside":ok})
    checks["six_ports_inside_owned_copper"]=len(detail["port_containment"])==6 and all(x["inside"] for x in detail["port_containment"])
    checks["six_ports_over_backside_ground"]=len(m["ports"])==6 and all(inside(p["q_mm"],-2,2) and inside(p["v_mm"],3,13) for p in m["ports"])
    checks["corrected_port_n_rule"]=m["port_n_mm"]=={"signal":0.0,"ground":-1.0}
    checks["no_differential_port"]=len(m["ports"])==6 and all(p["z0_ohm"]==50 for p in m["ports"])

    detail["package_to_L1_body_v_clearance_mm"]=8.40-8.00
    detail["COUT_to_L1_body_q_clearance_mm"]=1.20-0.25
    checks["component_body_clearances_ge_0p25"]=detail["package_to_L1_body_v_clearance_mm"]>=0.25 and detail["COUT_to_L1_body_q_clearance_mm"]>=0.25

    checks["authority_off"]=m["build_authorized"] is False and m["solve_authorized"] is False
    status="PASS_R4_A0_E1_STATIC_PREBUILD_ARITHMETIC_AUDIT" if all(checks.values()) else "HOLD_R4_A0_E1_STATIC_PREBUILD_ARITHMETIC_AUDIT"
    payload={"schema_version":"0.2.8","status":status,"checks":checks,"detail":detail,
             "note":"Analytical prebuild audit only; CST Boolean/interference checks remain mandatory at build-only gate."}
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(payload,indent=2)+"\n")
    print(json.dumps(payload,indent=2))
    return 0 if status.startswith("PASS_") else 4

if __name__=="__main__":
    raise SystemExit(main())
