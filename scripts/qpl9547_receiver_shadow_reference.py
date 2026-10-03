#!/usr/bin/env python3
"""Traceable QPL9547 GammaOpt -> Zopt reference calculation for R1E1A4A.

This script does NOT map differential antenna Z_active to either LNA.
That mapping is intentionally blocked until the balanced reference plane is frozen.
"""
from __future__ import print_function
import csv, cmath, math, os

ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH=os.path.join(ROOT,"circuit","qpl9547","QPL9547_NOISE_REFERENCE_1P1_1P7.csv")
Z0=50.0

def z_from_gamma(mag,deg):
    g=mag*cmath.exp(1j*math.radians(deg))
    return Z0*(1.0+g)/(1.0-g)

def main():
    rows=list(csv.DictReader(open(PATH,newline="")))
    worst=0.0
    for r in rows:
        z=z_from_gamma(float(r["gammaopt_mag"]),float(r["gammaopt_deg"]))
        zr=float(r["zopt_re_ohm"]); zi=float(r["zopt_im_ohm"])
        err=abs(z-complex(zr,zi)); worst=max(worst,err)
        if err>1e-4:
            raise SystemExit("HOLD_QPL9547_ZOPT_REFERENCE_MISMATCH")
        print("%s GHz Zopt=%.4f%+.4fj ohm"%(r["freq_ghz"],z.real,z.imag))
    print("PASS_QPL9547_ZOPT_REFERENCE")
    print("MAX_TABLE_ERROR_OHM=%.9g"%worst)
    print("DIFFERENTIAL_MAPPING_FROZEN=NO")

if __name__=="__main__":
    main()
