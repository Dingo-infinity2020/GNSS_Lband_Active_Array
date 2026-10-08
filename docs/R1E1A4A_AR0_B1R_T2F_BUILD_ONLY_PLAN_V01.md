# AR0-B1R-T2F Canonical Transition Fixture Build-Only Plan V0.1

Status: BUILD AUTHORIZED; SOLVE FORBIDDEN

Parent:
T1 artifact SHA256 3144672323cbd4123d6413e7d9ae8f4842b78707d3a71b641748c7250ca2a8f6

Build:
1. hash-check and copy parent;
2. inventory parent;
3. delete every solid except Pol-A P/N prongs, P/N signal traces and P/N T1 taper-ground;
4. verify retained-solid volumes match parent exactly;
5. add one 100-ohm differential discrete port at v=0;
6. add two 50-ohm signal-to-ground discrete ports at v=10 mm;
7. immediate port/object audit;
8. save;
9. fresh reopen;
10. repeat object/port/endpoint audit;
11. verify solver result tree empty;
12. stop.

No solver.
No monitor.
No sweep.
No geometry optimization.
No silent retry.
