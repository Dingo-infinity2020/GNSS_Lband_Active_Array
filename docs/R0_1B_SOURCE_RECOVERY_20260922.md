# R0.1B source recovery — official IEICE full text found

Date: 2026-09-22
Design-side status: **PRIMARY SOURCE RECOVERED**

H01 correctly stopped because its DOI/metadata route did not expose the paper. The design side subsequently verified that the publisher's IEICE Proceedings page provides a direct 1.3 MB PDF download.

## Official publisher links

Landing/summary page:

https://www.ieice.org/publications/proceedings/summary.php?expandable=13&iconf=ISAP&number=1571143655&session_num=Pos1&year=2025

Direct publisher PDF endpoint:

https://www.ieice.org/publications/proceedings/bin/pdf_link.php?fname=1571143655.pdf&iconf=ISAP&lang=E&number=1571143655&vol=98&year=2025

DOI:

https://doi.org/10.34385/proc.98.1571143655

The PDF is a 2-page ISAP 2025 proceeding and contains the required Fig. 1(a) simulation model and Fig. 2(a) fabricated active antenna.

## Repository policy

The source PDF and its raw figures remain copyrighted publisher material.

For R0.1B2, H01 MAY:

- download/open the official PDF locally for inspection;
- save it only in a local temporary/git-ignored location;
- make temporary local crops/zoom views for measurement;
- use those views to produce project-owned notes, measurements and redrawn schematics.

H01 MUST NOT:

- commit the PDF;
- commit raw screenshots/crops of the publisher figures;
- embed the publisher figures into repository documentation.

Only project-owned textual extraction, measurement tables, coordinate notes, and redrawn interpretation schematics may be committed.

## Design-side verification of paper text

The paper explicitly states that:

- the antenna is based on a dipole over a ground plane;
- a square PCB with a "4-petal" configuration is used;
- a passive ring is integrated around the antenna;
- low field intensity near the centre allows a small area to be removed for feed points/electronics;
- the centre impedance is tunable by physical dimensions and gap separations;
- the height over ground is 200 mm;
- the antenna naturally produces a balanced signal and directly feeds a pair of LNAs;
- in the active implementation, a small ground plane is beneath the petal feed points and the LNA circuits are mounted on top.

These statements do not by themselves resolve the exact centre geometry. The figure audit is still required.

## Next action

Repeat the centre/feed provenance extraction as task:

`R0.1B2-CENTER-FEED-SOURCE-RECOVERY-H01`

Use the official publisher PDF above. No CST and no solver are authorized.
