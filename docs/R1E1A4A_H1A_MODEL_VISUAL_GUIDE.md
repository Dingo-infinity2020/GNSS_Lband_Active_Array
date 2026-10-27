# R1E1A4A-H1A Model Visual Guide

Status: GEOMETRY GUIDE — H1A SOLVE REMAINS NUMERICAL HOLD

## Side view (not to scale)

```text
                    +z / sky

        TopCopper: radiator metallization
        ==================================  z = 58.177857 mm
        |                                |
        |         1.000 mm FR4           |
        |                                |
        ==================================  z = 57.142857 mm
             |                    |
             |  ideal P1A/P1B     |       <- no physical metal pin in H1A
             |  discrete ports    |
             |                    |
             |<-- 2.000 mm air -->|
             |                    |
        ----------------------------------  z = 55.142857 mm
        H1A_OFFSET_LOCAL_GROUND
        10 x 10 x 0.035 mm PEC
        ----------------------------------  z = 55.107857 mm
```

Port electrical length from top-copper terminal plane to local-ground top:
3.035 mm.

## Top view of the 10 x 10 mm local-ground diagnostic footprint

```text
             y
             ^
             |
        +----+----+
        |    .    |
        | P1A .   |    P1A terminal center:
        |  x  .   |    (+2.1213,+2.1213) mm
        |     .   |
        |.....+.........> x
        |   .     |
        |  .  x   |     P1B terminal center:
        | .  P1B  |     (-2.1213,-2.1213) mm
        |    .    |
        +---------+

        local-ground outline = 10 x 10 mm
        centered at x=y=0
```

## What is physically modeled

- 94-mm periodic unit-cell ground/backplane;
- 70.714-mm-class radiator FR4 board from the qualified P094 lineage;
- top radiator copper;
- one centered 10 x 10 x 0.035 mm offset PEC local-ground sheet;
- two 50-ohm single-ended lumped/discrete P1 ports.

## What is intentionally NOT modeled yet

- no PEEK/PTFE spacer;
- no daughterboard dielectric;
- no signal pins/vias;
- no antipads;
- no QPL9547 package;
- no bias or output traces;
- no RF shield;
- no carrier to the main backplane.

Therefore H1A answers only:
"What happens if the same local-ground footprint is moved 2 mm away from the radiator underside?"

It is not yet the manufacturing model. H1B is reserved for the manufacturable daughterboard/feed-transition structure after H1A is numerically qualified.
