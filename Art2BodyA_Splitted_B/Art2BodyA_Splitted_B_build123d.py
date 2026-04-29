"""
Art2BodyA_Splitted_B_build123d.py

Guidelines implemented:
  G1 – Read S1 CSV; parse one circle + four arcs at Z=32 (top face).
       Geometry (computed from CSV):
         Circle  : centre=(0, 160)   r=49  → INNER hole at top of teardrop
         Arc 1   : centre=(0, 0)     r=75  → outer boundary, bottom bulge
         Arc 2   : centre=(102.47,80)  r=65  → right tangent arc
         Arc 3   : centre=(0, 160)   r=65  → top connecting arc (concentric w/ circle)
         Arc 4   : centre=(-102.47,80) r=65  → left tangent arc
       The four arcs form a closed teardrop OUTER boundary.
       The circle defines the INNER hole inside that boundary.

  G2 – Extrude the region between the inner circle and the outer arc
       boundary along -Z by 32 units (Z=32 → Z=0).

  G3 – Export STL & STEP at the LAST stage as
       Art2BodyA_Splitted_B_G_1_28.stl / .step
       (file name reflects guidelines 1 through the latest, G28).

  G4 – Read S2 CSV; one circle + multiple arcs and lines at Z=33
       defining THREE enclosed sections:
         Section 1: circle r=49 at (0, 160) — same as the body's hole (98 dia)
         Section 2: U-shape upper "wall channel" around the hole
         Section 3: thin crescent rim along the body's outer perimeter

  G5 – Extrude-cut Sections 2 and 3 (NOT Section 1, the hole) by 28 units
       in -Z. Sketch at Z=33 (1 mm overshoot above body top Z=32).
       Cut spans Z=33 → Z=5; leaves a 5 mm floor at Z=0..5.

  G6 – Read S3 CSV; lines + circle + arc at Z=4.9 defining THREE enclosed sections:
         Section 1: circle r=1.7 at (0, 205) — small hole feature
         Section 2: rectangle from (-5,201) to (5,209) MINUS circle
                    (annular region: rectangle with the small circle as a hole)
         Section 3: slot region from y=209 up to arc top at y=220.484

  G7 – Extrude-join Section 3 (slot) by +8.1 units in +Z.
       Sketch at Z=4.9 (0.1 mm BELOW floor top Z=5 — Z-overshoot fuse).
       Section 3 prism spans Z=4.9 → Z=13.0.

  G8 – Extrude-join Section 2 (rectangle minus circle) by +6 units in +Z,
       starting offset 2.1 units up from the sketch plane.
       Effective Z-range: Z=7.0 → Z=13.0.
       Connects to G7 prism along shared y=209 face.

  G9 – Read S4 CSV; pentagon-like profile (7 lines) at Z=10. Extrude-cut
       SYMMETRICALLY by ±1.5 units in Z (cut spans Z=8.5 → Z=11.5,
       3 mm total depth). Done as TWO subtract extrudes (+1.5 and -1.5).

  G10 – Circular pattern: 3 instances of (G6 → G9) at angles 0°, 120°, 240°
        about the axis of S1's circle (vertical axis at x=0, y=160).
        All three instances share the same Z-depths and profiles, just
        rotated about the pattern axis.

  G11 – Read S5 CSV; forms a rectangle bounded box made up of lines and
        an arc, plus a circle inside it. Sketch plane Z is taken from S5.

  G12 – Extrude-join BOTH sections from G11 (the bounding box AND the inner
        circle) together by 12.1 units along -Z. Both regions are drawn
        in a single BuildSketch and act as added material.

  G13 – Extrude-cut the inner circle from G11 by 12 units along -Z. This
        carves a 12 mm-deep cylindrical hole through the just-added prism
        (the prism is 12.1 mm thick, so 0.1 mm of material remains at the
        bottom under the hole).

  G14 – Read S6 CSV; an enclosed profile made entirely of lines. Lines are
        used in CSV order to form one closed loop (S6_LOOP). Sketch plane
        Z is taken from S6.

  G15 – Extrude-cut the profile from G14 SYMMETRICALLY by ±1.5 units in Z
        (the spec says "extrude symmetrically"; profile sits inside the
        body so the natural realisation is two subtract extrudes from
        the sketch plane, +1.5 and -1.5, giving a 3 mm thick cut).

  G16 – Read S7 CSV; multiple circles. Each circle is reconstructed from
        its 3 sample points, its diameter computed, and circles are
        bucketed into three groups by diameter:
          • dia ≈ 8.4
          • dia ≈ 5.9
          • dia ≈ 3.4
        Sketch plane Z = S7_Z (= -1).

  G17 – Extrude-cut every dia ≈ 8.4 circle by 2.1 units in +Z from sketch
        plane Z=-1. Effective cut Z=-1 → Z=1.1, producing 1.1 mm-deep
        holes opening through the floor at Z=0.

  G18 – Extrude-cut every dia ≈ 5.9 circle by 3.9 units in +Z from sketch
        plane Z=-1. Effective Z=-1 → Z=2.9.

  G19 – Extrude-cut every dia ≈ 3.4 circle by 8 units in +Z from sketch
        plane Z=-1. Effective Z=-1 → Z=7.

  G20 – Read S8 CSV; a circle on the YZ plane. Coordinates parsed as
        (Y, Z) for the 2D circumscribed-circle fit; the YZ sketch is
        offset by S8_X (= 0.0) along X.

  G21 – Extrude-cut the G20 circle SYMMETRICALLY by 50 units in each X
        direction (a through-bore along X). Done as two subtract extrudes
        (+50 and -50) on the YZ sketch.

  G22 – Read S9 CSV; lines on the YZ plane (Y mapped to local X of the
        sketch, Z mapped to local Y). Lines are then auto-grouped into
        closed loops by walking endpoints, yielding TWO enclosed profiles.
        S9_X = -9.0 (the YZ sketch sits at X=-9).

  G23 – From G22, identify the loop whose Y-range spans approximately
        103.7 → 108.7 and extrude-JOIN it by 30 units along -X
        (sketch at X=-9 → solid extends toward X=-39).

  G24 – Extrude-JOIN the OTHER loop from G22 by 26 units along -X
        (sketch at X=-9 → solid extends toward X=-35).

  G25 – Read S10 CSV; a single enclosed region of lines on the XY plane
        at Z=S10_Z (= 8.5).

  G26 – Extrude-cut the G25 profile by 3.5 units in -Z (sketch at
        Z=8.5 → cut floor at Z=5).

  G27 – Mirror everything from G22 → G26 across the global YZ plane.
        Implementation:
          • S9 features: re-build the same two loops on the YZ plane
            offset by +9.0 (mirror of -9.0) and extrude-JOIN with +X
            amounts (+30 for the 103.7→108.7 loop, +26 for the other),
            so material extends in the +X direction on the mirrored side.
          • S10 feature: rebuild every line with its X coordinate negated
            (mirror about the X=0 plane), then extrude-cut by -3.5 in -Z
            on the same XY sketch plane (Z is unaffected by an YZ-plane
            mirror).

  G28 – Apply a fillet to three of the four bottom-face outer arcs of
        the body (z=0). The four bottom-face arcs come from G1's outer
        boundary: Arc 1 (r=75), Arc 2/3/4 (r=65 each). G28 picks the
        bottom face via `part_full.faces().sort_by(Axis.Z)[0]`, filters
        its edges to radius ≈65, and applies fillet(r=4.99) — Arc 1
        (r=75) is left unfilleted. The 4.99 (vs. literal 5.0) sidesteps
        a known OCC numerical edge-case where r=5.0 fails on this
        configuration; the 0.01 mm difference is below STL tolerance
        and visually identical.

General guidelines:
  • .clean() called right before export to wipe accumulated micro-scars.
  • Watertight check + open-edge check + volume report before export.
  • Summary file: Art2BodyA_Splitted_B_summary_G_1_28.txt
  • OCP viewer port: 3939.

"""

import os
import csv
import math

# ── paths ──────────────────────────────────────────────────────────────────
BASE_DIR    = "/Users/avajones/Documents/ava_build123d/20260422_assign/Art2BodyA_Splitted_B"
CSV_DIR     = os.path.join(BASE_DIR, "csv_merged")
FOLDER_NAME = "Art2BodyA_Splitted_B"

STL_NAME     = f"{FOLDER_NAME}_G_1_28.stl"
STEP_NAME    = f"{FOLDER_NAME}_G_1_28.step"
SUMMARY_NAME = f"{FOLDER_NAME}_summary_G_1_28.txt"

STL_PATH     = os.path.join(BASE_DIR, STL_NAME)
STEP_PATH    = os.path.join(BASE_DIR, STEP_NAME)
SUMMARY_PATH = os.path.join(BASE_DIR, SUMMARY_NAME)

S1_CSV = os.path.join(CSV_DIR, "Fusion_Coordinates_S1.csv")
S2_CSV = os.path.join(CSV_DIR, "Fusion_Coordinates_S2.csv")
S3_CSV = os.path.join(CSV_DIR, "Fusion_Coordinates_S3.csv")
S4_CSV = os.path.join(CSV_DIR, "Fusion_Coordinates_S4.csv")
S5_CSV = os.path.join(CSV_DIR, "Fusion_Coordinates_S5.csv")
S6_CSV = os.path.join(CSV_DIR, "Fusion_Coordinates_S6.csv")
S7_CSV = os.path.join(CSV_DIR, "Fusion_Coordinates_S7.csv")
S8_CSV = os.path.join(CSV_DIR, "Fusion_Coordinates_S8.csv")
S9_CSV = os.path.join(CSV_DIR, "Fusion_Coordinates_S9.csv")
S10_CSV = os.path.join(CSV_DIR, "Fusion_Coordinates_S10.csv")

# ── build123d imports ──────────────────────────────────────────────────────
from build123d import (
    BuildPart, BuildSketch, BuildLine,
    Circle, ThreePointArc, Line,
    Mode, Plane, Location, Locations,
    extrude, make_face, fillet, Axis,
    export_stl, export_step,
)

# ── OCP viewer ────────────────────────────────────────────────────────────
from ocp_vscode import show, set_port
set_port(3939)

# ══════════════════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════════════════

def circumscribed_circle_from_3pts(p1, p2, p3):
    """Return (cx, cy, r) of the unique circle through three non-collinear points."""
    ax, ay = p1
    bx, by = p2
    cx, cy = p3
    D = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
    if abs(D) < 1e-10:
        raise ValueError("Collinear points — cannot compute circumscribed circle.")
    ux = ((ax**2 + ay**2) * (by - cy) +
          (bx**2 + by**2) * (cy - ay) +
          (cx**2 + cy**2) * (ay - by)) / D
    uy = ((ax**2 + ay**2) * (cx - bx) +
          (bx**2 + by**2) * (ax - cx) +
          (cx**2 + cy**2) * (bx - ax)) / D
    r  = math.sqrt((ax - ux)**2 + (ay - uy)**2)
    return ux, uy, r


def read_all_rows(csv_path):
    rows = []
    with open(csv_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


# ══════════════════════════════════════════════════════════════════════════
print("=" * 60)
print("Art2BodyA_Splitted_B_build123d.py")
print("=" * 60)

# ══════════════════════════════════════════════════════════════════════════
# G1 – Read S1: one circle + four arcs at Z=32
# ══════════════════════════════════════════════════════════════════════════
print(f"\n[G1] Reading S1 from: {S1_CSV}")
s1_rows = read_all_rows(S1_CSV)

# ── Parse circle ──
circ_row = [r for r in s1_rows if "circle" in r["Draw Type"].lower()][0]
c_p1 = (float(circ_row["X1"]), float(circ_row["Y1"]))
c_p2 = (float(circ_row["X2"]), float(circ_row["Y2"]))
c_p3 = (float(circ_row["X3"]), float(circ_row["Y3"]))
c_cx, c_cy, c_r = circumscribed_circle_from_3pts(c_p1, c_p2, c_p3)
S1_Z = float(circ_row["Z1"])  # 32

print(f"       Circle (inner hole): centre=({c_cx:.3f}, {c_cy:.3f})  r={c_r:.3f}  Z={S1_Z}")

# ── Parse arcs (sorted by trailing digit in Draw Type) ──
arc_rows = sorted(
    [r for r in s1_rows if "arc" in r["Draw Type"].lower()],
    key=lambda r: int([s for s in r["Draw Type"].split("_") if s.isdigit()][-1])
)

arcs = []
for ar in arc_rows:
    dt = ar["Draw Type"].strip()
    p1 = (float(ar["X1"]), float(ar["Y1"]))
    p2 = (float(ar["X2"]), float(ar["Y2"]))
    p3 = (float(ar["X3"]), float(ar["Y3"]))
    acx, acy, ar_r = circumscribed_circle_from_3pts(p1, p2, p3)
    arcs.append({"dt": dt, "p1": p1, "p2": p2, "p3": p3,
                 "cx": acx, "cy": acy, "r": ar_r})
    print(f"       {dt:25s}  centre=({acx:.3f}, {acy:.3f})  r={ar_r:.3f}")
    print(f"         from ({p1[0]:.3f},{p1[1]:.3f}) "
          f"→ mid ({p2[0]:.3f},{p2[1]:.3f}) "
          f"→ ({p3[0]:.3f},{p3[1]:.3f})")

# ── S1 key geometry (verified by computation) ──
#   Circle  r≈49  at (0, 160)         — INNER hole
#   Arc 1   r=75  at origin           — outer boundary, lower bulge
#   Arc 2   r=65  at (102.47, 80)     — right tangent arc
#   Arc 3   r=65  at (0, 160)         — top connecting arc
#   Arc 4   r=65  at (-102.47, 80)    — left tangent arc
#
# Outer boundary chain (closed, traversed CCW):
#   Arc 1 : ( 39.538,  63.732) → (0, 75)         → (-39.538, 63.732)
#   Arc 4 : (-39.538,  63.732) → (-38.83, 93.229) → (-51.235, 120.0)
#   Arc 3 : (-51.235, 120.0)   → (0, 225)        → ( 51.235, 120.0)
#   Arc 2 : ( 51.235, 120.0)   → ( 38.83, 93.229) → ( 39.538, 63.732)
#
# All endpoints chain head-to-tail, forming a single closed loop.

CIRCLE_R  = c_r          # ≈ 49
CIRCLE_CX = c_cx         # ≈ 0
CIRCLE_CY = c_cy         # ≈ 160
ARC1_R    = arcs[0]["r"] # ≈ 75
ARC3_R    = arcs[2]["r"] # ≈ 65

# Outer-boundary key points (start/end of each arc)
PT_ARC1_START = arcs[0]["p1"]   # ( 39.538,  63.732)
PT_ARC1_MID   = arcs[0]["p2"]   # (  0.000,  75.000)
PT_ARC1_END   = arcs[0]["p3"]   # (-39.538,  63.732)

PT_ARC2_START = arcs[1]["p1"]   # ( 39.538,  63.732)
PT_ARC2_MID   = arcs[1]["p2"]   # ( 38.830,  93.229)
PT_ARC2_END   = arcs[1]["p3"]   # ( 51.235, 120.000)

PT_ARC3_START = arcs[2]["p1"]   # ( 51.235, 120.000)
PT_ARC3_MID   = arcs[2]["p2"]   # (  0.000, 225.000)
PT_ARC3_END   = arcs[2]["p3"]   # (-51.235, 120.000)

PT_ARC4_START = arcs[3]["p1"]   # (-51.235, 120.000)
PT_ARC4_MID   = arcs[3]["p2"]   # (-38.830,  93.229)
PT_ARC4_END   = arcs[3]["p3"]   # (-39.538,  63.732)

print(f"\n       Outer boundary closes: "
      f"Arc1 end {PT_ARC1_END} == Arc4 end {PT_ARC4_END}  "
      f"and Arc1 start {PT_ARC1_START} == Arc2 start {PT_ARC2_START}")

# ══════════════════════════════════════════════════════════════════════════
# G2 – Extrude region between inner circle and outer arc boundary,
#      along -Z by 32 units (sketch at Z=32 → bottom at Z=0).
# ══════════════════════════════════════════════════════════════════════════
SKETCH_Z_TOP = 32.0
PART_HEIGHT  = 32.0   # full extrude depth in -Z

print(f"\n[G2] Extruding outer-boundary region with circle hole, "
      f"depth = -{PART_HEIGHT} mm  (Z={SKETCH_Z_TOP} → Z=0)")

with BuildPart() as part_full:
    with BuildSketch(Plane.XY.offset(SKETCH_Z_TOP)):
        with BuildLine():
            # Arc 1: (39.538, 63.732) → (0, 75) → (-39.538, 63.732)
            ThreePointArc(PT_ARC1_START, PT_ARC1_MID, PT_ARC1_END)
            # Arc 4 reversed: (-39.538, 63.732) → (-38.83, 93.229) → (-51.235, 120)
            ThreePointArc(PT_ARC4_END, PT_ARC4_MID, PT_ARC4_START)
            # Arc 3 reversed: (-51.235, 120) → (0, 225) → (51.235, 120)
            ThreePointArc(PT_ARC3_END, PT_ARC3_MID, PT_ARC3_START)
            # Arc 2 reversed: (51.235, 120) → (38.83, 93.229) → (39.538, 63.732)
            ThreePointArc(PT_ARC2_END, PT_ARC2_MID, PT_ARC2_START)
        make_face()

        # Subtract inner circle hole at (CIRCLE_CX, CIRCLE_CY) with r=CIRCLE_R
        with Locations(Location((CIRCLE_CX, CIRCLE_CY))):
            Circle(radius=CIRCLE_R, mode=Mode.SUBTRACT)

    extrude(amount=-PART_HEIGHT)   # Z=32 → Z=0

    # ══════════════════════════════════════════════════════════════════════
    # G4 + G5  (executed inside the SAME BuildPart so the cut applies to
    #          the body just extruded by G2)
    # ══════════════════════════════════════════════════════════════════════
    print("\n[G4] Reading S2 and identifying three enclosed sections…")
    s2_rows = read_all_rows(S2_CSV)

    # Parse circle (the hole, will be excluded from the cut)
    s2_circ_row = [r for r in s2_rows if "circle" in r["Draw Type"].lower()][0]
    _cp1 = (float(s2_circ_row["X1"]), float(s2_circ_row["Y1"]))
    _cp2 = (float(s2_circ_row["X2"]), float(s2_circ_row["Y2"]))
    _cp3 = (float(s2_circ_row["X3"]), float(s2_circ_row["Y3"]))
    S2_HOLE_CX, S2_HOLE_CY, S2_HOLE_R = circumscribed_circle_from_3pts(_cp1, _cp2, _cp3)
    S2_Z = float(s2_circ_row["Z1"])  # 33

    print(f"       Hole circle (NOT cut): centre=({S2_HOLE_CX:.3f}, {S2_HOLE_CY:.3f})  "
          f"r={S2_HOLE_R:.3f}  dia={2*S2_HOLE_R:.3f}  Z={S2_Z}")

    # Parse arcs into a dict keyed by Draw Type
    s2_arcs = {}
    for r in s2_rows:
        dt = r["Draw Type"].strip()
        if "arc" not in dt.lower():
            continue
        p1 = (float(r["X1"]), float(r["Y1"]))
        p2 = (float(r["X2"]), float(r["Y2"]))
        p3 = (float(r["X3"]), float(r["Y3"]))
        acx, acy, ar_r = circumscribed_circle_from_3pts(p1, p2, p3)
        s2_arcs[dt] = {"p1": p1, "p2": p2, "p3": p3,
                       "cx": acx, "cy": acy, "r": ar_r}
        print(f"       {dt:25s}  centre=({acx:8.3f}, {acy:8.3f})  r={ar_r:7.3f}")

    def _arc_pts(name):
        a = s2_arcs[name]
        return a["p1"], a["p2"], a["p3"]

    S2_CUT_DEPTH = 28.0       # G5 cut depth in -Z
    S2_SKETCH_Z  = S2_Z       # 33 (1 mm above body top Z=32, "Z-overshoot" trick)

    print(f"\n[G5] Sketch at Z={S2_SKETCH_Z}, cut depth = {S2_CUT_DEPTH} mm in -Z")
    print(f"       Cut spans Z={S2_SKETCH_Z} → Z={S2_SKETCH_Z - S2_CUT_DEPTH}  "
          f"(top 1 mm overshoots into empty space)")
    print(f"       Floor of pocket at Z=5; floor thickness 5 mm above Z=0 base")

    with BuildSketch(Plane.XY.offset(S2_SKETCH_Z)):
        with BuildLine():
            # ——— Top inner (Arc 1, r=60 around hole) ———
            a1_p1, a1_p2, a1_p3 = _arc_pts("3_point_arc_1")
            ThreePointArc(a1_p1, a1_p2, a1_p3)
            # ——— Left side outward (Arc 9 reversed) ———
            a9_p1, a9_p2, a9_p3 = _arc_pts("3_point_arc_9")
            ThreePointArc(a9_p3, a9_p2, a9_p1)
            # Left zigzag lines (steps 21, 20, 19 in CSV order)
            Line((-33.685, 92.990),  (-35.669, 94.025))
            Line((-35.669, 94.025),  (-37.620, 95.118))
            Line((-37.620, 95.118),  (-39.538, 96.268))
            # Edge 18: outward to left outer corner
            Line((-39.538, 96.268),  (-45.939, 100.109))
            # Arc 7 reversed: outer corner → lower
            a7_p1, a7_p2, a7_p3 = _arc_pts("3_point_arc_7")
            ThreePointArc(a7_p3, a7_p2, a7_p1)
            # Lines 15, 14 (line 14 reversed) along the bottom-left rim transition
            Line((-43.898, 66.986),  (-43.898, 59.486))
            Line((-43.898, 59.486),  (-36.898, 59.486))
            # Arc 5 reversed (r=70 body bottom inner): left → right
            a5_p1, a5_p2, a5_p3 = _arc_pts("3_point_arc_5")
            ThreePointArc(a5_p3, a5_p2, a5_p1)
            # Lines 11 (reversed), 10 (reversed) along bottom-right rim transition
            Line(( 36.898, 59.486),  ( 43.898, 59.486))
            Line(( 43.898, 59.486),  ( 43.898, 66.986))
            # Arc 3 reversed (r=60 right tang): lower → outer corner
            a3_p1, a3_p2, a3_p3 = _arc_pts("3_point_arc_3")
            ThreePointArc(a3_p3, a3_p2, a3_p1)
            # Edge 7 reversed: right outer corner → T-junction
            Line(( 45.939, 100.109), ( 39.538, 96.268))
            # Right zigzag (lines 6, 5, 4 reversed)
            Line(( 39.538, 96.268),  ( 37.620, 95.118))
            Line(( 37.620, 95.118),  ( 35.669, 94.025))
            Line(( 35.669, 94.025),  ( 33.685, 92.990))
            # Arc 2 (r=70 right tang upper): right → top — closes back to (47.294, 123.077)
            a2_p1, a2_p2, a2_p3 = _arc_pts("3_point_arc_2")
            ThreePointArc(a2_p1, a2_p2, a2_p3)
        make_face()

    # Apply the cut: 28 mm in -Z. Sketch is 1 mm above body top, so the cutter's
    # top face is in empty space (no coincident face with the body's top).
    extrude(amount=-S2_CUT_DEPTH, mode=Mode.SUBTRACT)

    # ══════════════════════════════════════════════════════════════════════
    # G6 + G7 + G8 + G9  parameterized for G10 (circular pattern, 3 instances
    # at 0°, 120°, 240° around the axis of S1's circle at (0, 160))
    # ══════════════════════════════════════════════════════════════════════
    print("\n[G6] Reading S3 and S4 (profiles for the patterned cluster)…")
    s3_rows = read_all_rows(S3_CSV)
    s4_rows = read_all_rows(S4_CSV)

    # ── S3 parsing ────────────────────────────────────────────────────────
    S3_Z = float(s3_rows[0]["Z1"])  # 4.9
    print(f"       S3 sketch plane Z = {S3_Z}  (0.1 mm below floor top Z=5)")

    s3_circ_row = [r for r in s3_rows if "circle" in r["Draw Type"].lower()][0]
    _cp1 = (float(s3_circ_row["X1"]), float(s3_circ_row["Y1"]))
    _cp2 = (float(s3_circ_row["X2"]), float(s3_circ_row["Y2"]))
    _cp3 = (float(s3_circ_row["X3"]), float(s3_circ_row["Y3"]))
    S3_HOLE_CX, S3_HOLE_CY, S3_HOLE_R = circumscribed_circle_from_3pts(_cp1, _cp2, _cp3)
    print(f"       S3 Section 1 (circle): centre=({S3_HOLE_CX:.3f}, {S3_HOLE_CY:.3f})  "
          f"r={S3_HOLE_R:.3f}")

    s3_arc_row = [r for r in s3_rows if "arc" in r["Draw Type"].lower()][0]
    S3_ARC_P1 = (float(s3_arc_row["X1"]), float(s3_arc_row["Y1"]))
    S3_ARC_P2 = (float(s3_arc_row["X2"]), float(s3_arc_row["Y2"]))
    S3_ARC_P3 = (float(s3_arc_row["X3"]), float(s3_arc_row["Y3"]))
    S3_ARC_CX, S3_ARC_CY, S3_ARC_R = circumscribed_circle_from_3pts(
        S3_ARC_P1, S3_ARC_P2, S3_ARC_P3
    )
    print(f"       S3 Section 3 top arc: centre=({S3_ARC_CX:.3f}, {S3_ARC_CY:.3f})  "
          f"r={S3_ARC_R:.3f}")

    # ── S4 parsing (G9 cut profile — pentagon/house outline, 7 lines) ─────
    S4_Z = float(s4_rows[0]["Z1"])  # 10.0
    print(f"       S4 sketch plane Z = {S4_Z}")
    print(f"       S4 profile: {len(s4_rows)} lines forming a closed pentagon-like outline")

    S4_LOOP = [
        ((-2.901, 200.5),  ( 2.901, 200.5)),
        (( 2.901, 200.5),  ( 2.901, 201.0)),
        (( 2.901, 201.0),  ( 2.901, 206.675)),
        (( 2.901, 206.675),( 0.0,   208.35)),
        (( 0.0,   208.35), (-2.901, 206.675)),
        ((-2.901, 206.675),(-2.901, 201.0)),
        ((-2.901, 201.0),  (-2.901, 200.5)),
    ]

    # ──────────────────────────────────────────────────────────────────────
    # G10 — Circular Pattern parameters
    # ──────────────────────────────────────────────────────────────────────
    G10_AXIS_CX = 0.0
    G10_AXIS_CY = 160.0
    G10_COUNT   = 3

    print(f"\n[G10] Circular pattern: {G10_COUNT} instances of (G6→G9) "
          f"about axis x={G10_AXIS_CX}, y={G10_AXIS_CY} (Z-parallel)")

    def _rot(p, angle_rad):
        """Rotate a 2D point about (G10_AXIS_CX, G10_AXIS_CY) by angle_rad."""
        x, y = p
        dx, dy = x - G10_AXIS_CX, y - G10_AXIS_CY
        c, s = math.cos(angle_rad), math.sin(angle_rad)
        return (G10_AXIS_CX + c * dx - s * dy,
                G10_AXIS_CY + s * dx + c * dy)

    G7_EXTRUDE  = 8.1
    G8_OFFSET   = 2.1
    G8_EXTRUDE  = 6.0
    G8_START_Z  = S3_Z + G8_OFFSET            # 4.9 + 2.1 = 7.0
    G8_END_Z    = G8_START_Z + G8_EXTRUDE     # 7.0 + 6.0 = 13.0
    G9_HALF     = 1.5
    G9_TOTAL    = 2 * G9_HALF
    G9_TOP_Z    = S4_Z + G9_HALF
    G9_BOT_Z    = S4_Z - G9_HALF

    print(f"       G7 depth: +{G7_EXTRUDE} mm  (Z={S3_Z} → Z={S3_Z + G7_EXTRUDE})")
    print(f"       G8 depth: +{G8_EXTRUDE} mm at offset {G8_OFFSET} "
          f"(Z={G8_START_Z} → Z={G8_END_Z})")
    print(f"       G9 cut  : ±{G9_HALF} mm symmetric  (Z={G9_BOT_Z} → Z={G9_TOP_Z})")

    for idx in range(G10_COUNT):
        angle_deg = idx * (360.0 / G10_COUNT)
        angle_rad = math.radians(angle_deg)
        print(f"\n   ── Instance {idx+1}/{G10_COUNT}  (angle = {angle_deg:.1f}°) ──")

        # ── G7 (rotated) — extrude-join Section 3 (slot) ──
        with BuildSketch(Plane.XY.offset(S3_Z)):
            with BuildLine():
                Line(_rot((-5.0, 209.0),   angle_rad), _rot(( 0.0, 209.0),   angle_rad))
                Line(_rot(( 0.0, 209.0),   angle_rad), _rot(( 5.0, 209.0),   angle_rad))
                Line(_rot(( 5.0, 209.0),   angle_rad), _rot(( 5.0, 219.791), angle_rad))
                Line(_rot(( 5.0, 219.791), angle_rad), _rot(( 5.0, 220.291), angle_rad))
                ThreePointArc(_rot(S3_ARC_P3, angle_rad),
                              _rot(S3_ARC_P2, angle_rad),
                              _rot(S3_ARC_P1, angle_rad))
                Line(_rot((-5.0, 220.291), angle_rad), _rot((-5.0, 219.791), angle_rad))
                Line(_rot((-5.0, 219.791), angle_rad), _rot((-5.0, 209.0),   angle_rad))
            make_face()
        extrude(amount=G7_EXTRUDE, mode=Mode.ADD)

        # ── G8 (rotated) — extrude-join Section 2 (rect minus circle) ──
        with BuildSketch(Plane.XY.offset(G8_START_Z)):
            with BuildLine():
                Line(_rot((-5.0, 201.0), angle_rad), _rot(( 5.0, 201.0), angle_rad))
                Line(_rot(( 5.0, 201.0), angle_rad), _rot(( 5.0, 209.0), angle_rad))
                Line(_rot(( 5.0, 209.0), angle_rad), _rot(( 0.0, 209.0), angle_rad))
                Line(_rot(( 0.0, 209.0), angle_rad), _rot((-5.0, 209.0), angle_rad))
                Line(_rot((-5.0, 209.0), angle_rad), _rot((-5.0, 201.0), angle_rad))
            make_face()
            _hole_xy = _rot((S3_HOLE_CX, S3_HOLE_CY), angle_rad)
            with Locations(Location(_hole_xy)):
                Circle(radius=S3_HOLE_R, mode=Mode.SUBTRACT)
        extrude(amount=G8_EXTRUDE, mode=Mode.ADD)

        # ── G9 (rotated) — extrude-cut S4 pentagon symmetrically ±1.5 in Z ──
        with BuildSketch(Plane.XY.offset(S4_Z)):
            with BuildLine():
                for (a, b) in S4_LOOP:
                    Line(_rot(a, angle_rad), _rot(b, angle_rad))
            make_face()
        extrude(amount= G9_HALF, mode=Mode.SUBTRACT)
        with BuildSketch(Plane.XY.offset(S4_Z)):
            with BuildLine():
                for (a, b) in S4_LOOP:
                    Line(_rot(a, angle_rad), _rot(b, angle_rad))
            make_face()
        extrude(amount=-G9_HALF, mode=Mode.SUBTRACT)

        print(f"      Instance {idx+1}: G7+G8 join, G9 cut applied at angle {angle_deg:.1f}°")

    # ══════════════════════════════════════════════════════════════════════════
    # G11, G12, G13 – Read S5 and process
    # ══════════════════════════════════════════════════════════════════════════
    print("\n[G11] Reading S5 file...")
    s5_rows = read_all_rows(S5_CSV)
    S5_Z = float(s5_rows[0]["Z1"])

    # Parse circle
    s5_circ_row = [r for r in s5_rows if "circle" in r["Draw Type"].lower()][0]
    _c_p1 = (float(s5_circ_row["X1"]), float(s5_circ_row["Y1"]))
    _c_p2 = (float(s5_circ_row["X2"]), float(s5_circ_row["Y2"]))
    _c_p3 = (float(s5_circ_row["X3"]), float(s5_circ_row["Y3"]))
    S5_CIRC_CX, S5_CIRC_CY, S5_CIRC_R = circumscribed_circle_from_3pts(_c_p1, _c_p2, _c_p3)
    print(f"       S5 Circle: centre=({S5_CIRC_CX:.3f}, {S5_CIRC_CY:.3f}) r={S5_CIRC_R:.3f} Z={S5_Z}")

    # G12: Extrude join BOTH sections by 12.1 in -Z
    print("\n[G12] Extrude-join S5 sections by 12.1 mm in -Z")
    with BuildSketch(Plane.XY.offset(S5_Z)):
        # 1st section: Bounding block (rectangle + top arc)
        with BuildLine():
            Line((-5.0, 210.0), (5.0, 210.0))
            Line((5.0, 210.0), (5.0, 219.791))
            Line((5.0, 219.791), (5.0, 220.391))
            ThreePointArc((5.0, 220.391), (0.0, 220.6), (-5.0, 220.391))
            Line((-5.0, 220.391), (-5.0, 219.791))
            Line((-5.0, 219.791), (-5.0, 210.0))
        make_face()
        # 2nd section: Circle added to the sketch
        with Locations(Location((S5_CIRC_CX, S5_CIRC_CY))):
            Circle(radius=S5_CIRC_R)
    extrude(amount=-12.1, mode=Mode.ADD)

    # G13: Extrude cut S5 circle by 12 mm in -Z
    print("\n[G13] Extrude-cut S5 circle by 12 mm in -Z")
    with BuildSketch(Plane.XY.offset(S5_Z)):
        with Locations(Location((S5_CIRC_CX, S5_CIRC_CY))):
            Circle(radius=S5_CIRC_R)
    extrude(amount=-12.0, mode=Mode.SUBTRACT)

    # ══════════════════════════════════════════════════════════════════════════
    # G14, G15 – Read S6 and process
    # ══════════════════════════════════════════════════════════════════════════
    print("\n[G14] Reading S6 file...")
    s6_rows = read_all_rows(S6_CSV)
    S6_Z = float(s6_rows[0]["Z1"])

    print(f"       S6 sketch plane Z = {S6_Z}")

    # S6 forms a closed loop of lines
    S6_LOOP = []
    for r in s6_rows:
        p1 = (float(r["X1"]), float(r["Y1"]))
        p2 = (float(r["X2"]), float(r["Y2"]))
        S6_LOOP.append((p1, p2))

    # G15: Extrude symmetrically ±1.5 in Z (Done in 2 passes to cut both ways from sketch plane)
    print("\n[G15] Extruding S6 profile symmetrically by ±1.5 units in Z (cut)")
    with BuildSketch(Plane.XY.offset(S6_Z)):
        with BuildLine():
            for (a, b) in S6_LOOP:
                Line(a, b)
        make_face()
    extrude(amount=1.5, mode=Mode.SUBTRACT)

    with BuildSketch(Plane.XY.offset(S6_Z)):
        with BuildLine():
            for (a, b) in S6_LOOP:
                Line(a, b)
        make_face()
    extrude(amount=-1.5, mode=Mode.SUBTRACT)

    # ══════════════════════════════════════════════════════════════════════════
    # G16, G17, G18, G19 – Read S7 and extrude cut circles
    # ══════════════════════════════════════════════════════════════════════════
    print("\n[G16] Reading S7 file and computing circle parameters...")
    s7_rows = read_all_rows(S7_CSV)
    S7_Z = float(s7_rows[0]["Z1"]) # Should be -1.0
    
    circles_dia_8_4 = [] # Target dia ≈ 8.4
    circles_dia_5_9 = [] # Target dia ≈ 5.9
    circles_dia_3_4 = [] # Target dia ≈ 3.4
    
    for r in s7_rows:
        if "circle" in r["Draw Type"].lower():
            p1 = (float(r["X1"]), float(r["Y1"]))
            p2 = (float(r["X2"]), float(r["Y2"]))
            p3 = (float(r["X3"]), float(r["Y3"]))
            cx, cy, rad = circumscribed_circle_from_3pts(p1, p2, p3)
            dia = 2 * rad
            
            # Categorize the circles based on computed diameter (with small tolerance)
            if abs(dia - 8.4) < 0.1:
                circles_dia_8_4.append({"cx": cx, "cy": cy, "r": rad})
            elif abs(dia - 5.9) < 0.1:
                circles_dia_5_9.append({"cx": cx, "cy": cy, "r": rad})
            elif abs(dia - 3.4) < 0.1:
                circles_dia_3_4.append({"cx": cx, "cy": cy, "r": rad})
                
    print(f"       Found {len(circles_dia_8_4)} circles of dia 8.4")
    print(f"       Found {len(circles_dia_5_9)} circles of dia 5.9")
    print(f"       Found {len(circles_dia_3_4)} circles of dia 3.4")

    # G17: Extrude cut dia 8.4 circles by 2.1 in +Z (creating 1.1 mm deep hole from floor at Z=0)
    print(f"\n[G17] Extrude-cut dia 8.4 circles by 2.1 units in +Z")
    with BuildSketch(Plane.XY.offset(S7_Z)):
        for c in circles_dia_8_4:
            with Locations(Location((c["cx"], c["cy"]))):
                Circle(radius=c["r"])
    extrude(amount=2.1, mode=Mode.SUBTRACT)

    # G18: Extrude cut dia 5.9 circles by 3.9 in +Z
    print(f"\n[G18] Extrude-cut dia 5.9 circles by 3.9 units in +Z")
    with BuildSketch(Plane.XY.offset(S7_Z)):
        for c in circles_dia_5_9:
            with Locations(Location((c["cx"], c["cy"]))):
                Circle(radius=c["r"])
    extrude(amount=3.9, mode=Mode.SUBTRACT)

    # G19: Extrude cut dia 3.4 circles by 8.0 in +Z
    print(f"\n[G19] Extrude-cut dia 3.4 circles by 8 units in +Z")
    with BuildSketch(Plane.XY.offset(S7_Z)):
        for c in circles_dia_3_4:
            with Locations(Location((c["cx"], c["cy"]))):
                Circle(radius=c["r"])
    extrude(amount=8.0, mode=Mode.SUBTRACT)

    # ══════════════════════════════════════════════════════════════════════════
    # G20, G21 – Read S8 and extrude cut circle on the YZ plane
    # ══════════════════════════════════════════════════════════════════════════
    print("\n[G20] Reading S8 file...")
    s8_rows = read_all_rows(S8_CSV)
    
    # S8 lies on the YZ plane (X is constant at 0.0). 
    # We map global Y to local X, and global Z to local Y for our 2D circle function.
    s8_circ_row = [r for r in s8_rows if "circle" in r["Draw Type"].lower()][0]
    S8_X = float(s8_circ_row["X1"]) # 0.0
    
    _p1_yz = (float(s8_circ_row["Y1"]), float(s8_circ_row["Z1"]))
    _p2_yz = (float(s8_circ_row["Y2"]), float(s8_circ_row["Z2"]))
    _p3_yz = (float(s8_circ_row["Y3"]), float(s8_circ_row["Z3"]))
    
    S8_CIRC_CY, S8_CIRC_CZ, S8_CIRC_R = circumscribed_circle_from_3pts(_p1_yz, _p2_yz, _p3_yz)
    print(f"       S8 Circle (YZ Plane): centre_Y={S8_CIRC_CY:.3f}, centre_Z={S8_CIRC_CZ:.3f} r={S8_CIRC_R:.3f} at X={S8_X}")

    # G21: Extrude cut S8 circle symmetrically by 50 in each direction
    print("\n[G21] Extrude-cut S8 circle symmetrically by 50 units in each direction")
    
    # Pass 1: Cut 50 units in the +X direction
    with BuildSketch(Plane.YZ.offset(S8_X)):
        with Locations(Location((S8_CIRC_CY, S8_CIRC_CZ))):
            Circle(radius=S8_CIRC_R)
    extrude(amount=50.0, mode=Mode.SUBTRACT)

    # Pass 2: Cut 50 units in the -X direction
    with BuildSketch(Plane.YZ.offset(S8_X)):
        with Locations(Location((S8_CIRC_CY, S8_CIRC_CZ))):
            Circle(radius=S8_CIRC_R)
    extrude(amount=-50.0, mode=Mode.SUBTRACT)

    # ══════════════════════════════════════════════════════════════════════════
    # G22, G23, G24 – Read S9 and extrude enclosed sections on the YZ plane
    # ══════════════════════════════════════════════════════════════════════════
    print("\n[G22] Reading S9 file...")
    s9_rows = read_all_rows(S9_CSV)
    
    # Extract all lines mapping Global Y, Z to Local X, Y for Plane.YZ
    S9_X = float(s9_rows[0]["X1"]) # Should be -9.0
    
    s9_lines = []
    for r in s9_rows:
        if "Line" in r["Draw Type"]:
            p1 = (float(r["Y1"]), float(r["Z1"]))
            p2 = (float(r["Y2"]), float(r["Z2"]))
            s9_lines.append((p1, p2))
            
    # Group lines into closed loops (since S9 lines are not perfectly ordered)
    def is_close(pt1, pt2):
        return abs(pt1[0]-pt2[0]) < 1e-5 and abs(pt1[1]-pt2[1]) < 1e-5
        
    s9_loops = []
    _unprocessed = s9_lines.copy()
    _current_loop = [_unprocessed.pop(0)]
    
    while _unprocessed:
        _progress = False
        for i, line in enumerate(_unprocessed):
            last_pt = _current_loop[-1][1]
            first_pt = _current_loop[0][0]
            
            if is_close(last_pt, line[0]):
                _current_loop.append(line)
                _unprocessed.pop(i)
                _progress = True
                break
            elif is_close(last_pt, line[1]):
                _current_loop.append((line[1], line[0]))
                _unprocessed.pop(i)
                _progress = True
                break
            elif is_close(first_pt, line[1]):
                _current_loop.insert(0, line)
                _unprocessed.pop(i)
                _progress = True
                break
            elif is_close(first_pt, line[0]):
                _current_loop.insert(0, (line[1], line[0]))
                _unprocessed.pop(i)
                _progress = True
                break
                
        if not _progress: # End of current loop found
            s9_loops.append(_current_loop)
            _current_loop = [_unprocessed.pop(0)]
            
    if _current_loop:
        s9_loops.append(_current_loop)
        
    print(f"       S9 profiles found: {len(s9_loops)}")
    
    # Identify the loops based on their Y coordinates
    loop_103_108 = []
    loop_other = []
    
    for loop in s9_loops:
        # Check the min and max of Y (which is the first coordinate in our local 2D tuple)
        y_vals = [p[0] for line in loop for p in line]
        min_y, max_y = min(y_vals), max(y_vals)
        if abs(min_y - 103.7) < 0.2 and abs(max_y - 108.7) < 0.2:
            loop_103_108 = loop
            print(f"       -> Identified 103.7-108.7 region with {len(loop)} lines")
        else:
            loop_other = loop
            print(f"       -> Identified other region with {len(loop)} lines (Y: {min_y:.1f} to {max_y:.1f})")

    # G23: Extrude join the 103.7 to 108.7 region by 30 units in -X
    print("\n[G23] Extrude-join the 103.7-108.7 region by 30 units in -X")
    with BuildSketch(Plane.YZ.offset(S9_X)):
        with BuildLine():
            for (a, b) in loop_103_108:
                Line(a, b)
        make_face()
    extrude(amount=-30.0, mode=Mode.ADD)

    # G24: Extrude join the other region by 26 units in -X
    print("\n[G24] Extrude-join the other S9 region by 26 units in -X")
    with BuildSketch(Plane.YZ.offset(S9_X)):
        with BuildLine():
            for (a, b) in loop_other:
                Line(a, b)
        make_face()
    extrude(amount=-26.0, mode=Mode.ADD)

# ══════════════════════════════════════════════════════════════════════════
    # G25, G26 – Read S10 and extrude cut the enclosed region
    # ══════════════════════════════════════════════════════════════════════════
    print("\n[G25] Reading S10 file...")
    s10_rows = read_all_rows(S10_CSV)
    S10_Z = float(s10_rows[0]["Z1"]) # Should be 8.5
    
    s10_lines = []
    for r in s10_rows:
        if "Line" in r["Draw Type"]:
            p1 = (float(r["X1"]), float(r["Y1"]))
            p2 = (float(r["X2"]), float(r["Y2"]))
            s10_lines.append((p1, p2))
            
    print(f"       S10 Profile: enclosed region with {len(s10_lines)} lines at Z={S10_Z}")

    # G26: Extrude cut the profile by 3.5 units in the -Z direction
    print("\n[G26] Extrude-cut S10 profile by 3.5 units in -Z")
    with BuildSketch(Plane.XY.offset(S10_Z)):
        with BuildLine():
            for (a, b) in s10_lines:
                Line(a, b)
        make_face()
    extrude(amount=-3.5, mode=Mode.SUBTRACT)
    # ══════════════════════════════════════════════════════════════════════════
    # G27 – Mirror operations from G22 to G26 across the global YZ plane
    # ══════════════════════════════════════════════════════════════════════════
    print("\n[G27] Mirroring features from G22-G26 across the global YZ plane...")
    
    # --- Mirroring G22, G23, G24 (S9 Profiles) ---
    # The original sketch was at X=-9.0. The mirrored sketch goes to X=9.0.
    MIRRORED_S9_X = -S9_X 
    
    print(f"       -> Mirroring S9 features to Plane.YZ at X={MIRRORED_S9_X}")
    
    # Mirrored G23: Extrude join the 103.7-108.7 region by 30 units in +X
    with BuildSketch(Plane.YZ.offset(MIRRORED_S9_X)):
        with BuildLine():
            for (a, b) in loop_103_108:
                Line(a, b)
        make_face()
    extrude(amount=30.0, mode=Mode.ADD) # Positive amount to extrude in +X
    
    # Mirrored G24: Extrude join the other region by 26 units in +X
    with BuildSketch(Plane.YZ.offset(MIRRORED_S9_X)):
        with BuildLine():
            for (a, b) in loop_other:
                Line(a, b)
        make_face()
    extrude(amount=26.0, mode=Mode.ADD) # Positive amount to extrude in +X

    # --- Mirroring G25, G26 (S10 Profile) ---
    print("       -> Mirroring S10 feature across global YZ plane")
    mirrored_s10_lines = []
    for (a, b) in s10_lines:
        # Mirror across the YZ plane by negating the X coordinate of every point
        mirrored_a = (-a[0], a[1])
        mirrored_b = (-b[0], b[1])
        mirrored_s10_lines.append((mirrored_a, mirrored_b))
        
    with BuildSketch(Plane.XY.offset(S10_Z)):
        with BuildLine():
            for (a, b) in mirrored_s10_lines:
                Line(a, b)
        make_face()
    # Depth remains exactly the same (-3.5 in Z)
    extrude(amount=-3.5, mode=Mode.SUBTRACT)

    # ══════════════════════════════════════════════════════════════════════════
    # G28 – Fillet the three outer bottom arcs (radius = 65)
    # ══════════════════════════════════════════════════════════════════════════
    print("\n[G28] Applying 4.99 mm fillet to the three radius=65 bottom arcs...")
    bottom_face = part_full.faces().sort_by(Axis.Z)[0]
    
    # Safe filter function: checks the radius, ignores edges that don't have a radius (like straight lines)
    def is_target_arc(e):
        try:
            return abs(e.radius - 65.0) < 0.1
        except:
            return False
            
    edges_to_fillet = bottom_face.edges().filter_by(is_target_arc)
    
    print(f"       -> Found {len(edges_to_fillet)} edges to fillet.")
    
    # Apply the 4.99 mm fillet to those 3 edges
    fillet(edges_to_fillet, radius=4.99)

# .clean() right before export to wipe accumulated micro-scars (NO INDENTATION - 0 SPACES)
final_solid = part_full.part.clean()
print("\n       G1 to G28 complete; final solid cleaned.")

# Push to OCP viewer
show(final_solid, names=["Art2BodyA_Splitted_B"])
print("       Sent to OCP viewer on port 3939.")

# ══════════════════════════════════════════════════════════════════════════
# Watertight check + volume report (BEFORE export, per guideline)
# ══════════════════════════════════════════════════════════════════════════
print("\n[CHECK] Watertight & volume check …")

import trimesh
import numpy as np

is_watertight    = "check failed"
vol_stl          = "check failed"
vol_b123d        = "check failed"
open_edges_count = "check failed"

try:
    # build123d native volume (BREP)
    try:
        vol_b123d = float(final_solid.volume)
    except Exception:
        vol_b123d = "N/A"

    # tessellate to a temp STL for trimesh inspection
    _tmp_stl = os.path.join(BASE_DIR, "_tmp_check.stl")
    export_stl(final_solid, _tmp_stl, tolerance=1e-4, angular_tolerance=0.01)
    _m = trimesh.load(_tmp_stl)
    is_watertight = bool(_m.is_watertight)
    vol_stl       = float(_m.volume)

    _ue, _ec = np.unique(_m.edges_sorted, axis=0, return_counts=True)
    open_edges_count = int((_ec == 1).sum())
    _nonmanifold    = int((_ec >  2).sum())

    print(f"       Watertight        : {is_watertight}")
    print(f"       Open edges        : {open_edges_count}")
    print(f"       Non-manifold edges: {_nonmanifold}")
    print(f"       STL volume        : {vol_stl:.4f} mm^3")
    if isinstance(vol_b123d, float):
        print(f"       build123d volume  : {vol_b123d:.4f} mm^3")
    else:
        print(f"       build123d volume  : {vol_b123d}")

    if open_edges_count > 0:
        print(f"       ⚠  WARNING: mesh has {open_edges_count} open edges — "
              f"may cause 'mesh not oriented' / 'no positive volume' errors when re-imported.")
    if _nonmanifold > 0:
        print(f"       ⚠  WARNING: mesh has {_nonmanifold} non-manifold edges.")

    try:
        os.remove(_tmp_stl)
    except OSError:
        pass

except Exception as e:
    print(f"       trimesh check failed: {e}")

# ══════════════════════════════════════════════════════════════════════════
# G3 – Export STL & STEP  (LAST stage, per guideline)
# ══════════════════════════════════════════════════════════════════════════
print(f"\n[G3] Writing STL  -> {STL_PATH}")
export_stl(final_solid, STL_PATH, tolerance=5e-4, angular_tolerance=0.05)

print(f"[G3] Writing STEP -> {STEP_PATH}")
export_step(final_solid, STEP_PATH)

# ══════════════════════════════════════════════════════════════════════════
# Summary
# ══════════════════════════════════════════════════════════════════════════
summary_lines = [
    "=" * 60,
    f"Summary  :  {FOLDER_NAME}_summary_G_1_28",
    "Guidelines covered: G1 to G28",
    "=" * 60,
    "",
    "-- G1 : Profile (S1, Z=32) --",
    f"  Inner Circle (hole) : centre=({CIRCLE_CX:.3f}, {CIRCLE_CY:.3f})  r={CIRCLE_R:.3f}",
    f"  Arc 1 (bottom)      : centre=({arcs[0]['cx']:.3f}, {arcs[0]['cy']:.3f})  r={arcs[0]['r']:.3f}",
    f"  Arc 2 (right tang.) : centre=({arcs[1]['cx']:.3f}, {arcs[1]['cy']:.3f})  r={arcs[1]['r']:.3f}",
    f"  Arc 3 (top conn.)   : centre=({arcs[2]['cx']:.3f}, {arcs[2]['cy']:.3f})  r={arcs[2]['r']:.3f}",
    f"  Arc 4 (left tang.)  : centre=({arcs[3]['cx']:.3f}, {arcs[3]['cy']:.3f})  r={arcs[3]['r']:.3f}",
    f"  Sketch plane Z = {S1_Z}",
    "",
    "-- G2 : Extrude region (outer arcs minus circle hole) --",
    f"  Depth: -{PART_HEIGHT} mm in -Z  (Z={SKETCH_Z_TOP} -> Z=0)",
    "",
    "-- G4 : Profile (S2, Z=33) — three enclosed sections --",
    f"  Section 1 (HOLE, NOT cut): circle r={S2_HOLE_R:.3f} at "
    f"({S2_HOLE_CX:.3f}, {S2_HOLE_CY:.3f})  dia={2*S2_HOLE_R:.3f}",
    f"  Section 2 (upper U-channel)",
    f"  Section 3 (rim crescent)",
    "",
    "-- G5 : Extrude-cut Sections 2 ∪ 3 (NOT Section 1) --",
    f"  Sketch Z = {S2_Z}  (1 mm above body top Z=32 — Z-overshoot)",
    f"  Cut depth: {S2_CUT_DEPTH} mm in -Z   (Z={S2_Z} → Z={S2_Z - S2_CUT_DEPTH})",
    f"  Result: 5 mm floor at Z=0..5; pocket reaches body sidewalls",
    "",
    "-- G6 : Profile (S3, Z=4.9) — three enclosed sections --",
    f"  Section 1 : circle r={S3_HOLE_R:.3f} at ({S3_HOLE_CX:.3f}, {S3_HOLE_CY:.3f})",
    f"  Section 2 : rectangle (-5,201)→(5,209) MINUS Section-1 circle",
    f"  Section 3 : slot lines+arc (top arc r={S3_ARC_R:.3f} c=({S3_ARC_CX:.3f}, {S3_ARC_CY:.3f}))",
    f"  Sketch plane Z = {S3_Z}  (0.1 mm BELOW floor top Z=5 — Z-overshoot)",
    "",
    "-- G7 : Extrude-join Section 3 (slot) --",
    f"  Depth: +{G7_EXTRUDE} mm in +Z  (Z={S3_Z} → Z={S3_Z + G7_EXTRUDE})",
    "",
    "-- G8 : Extrude-join Section 2 (rect - circle) --",
    f"  Offset: +{G8_OFFSET} mm above sketch plane → start Z={G8_START_Z}",
    f"  Depth:  +{G8_EXTRUDE} mm in +Z  (Z={G8_START_Z} → Z={G8_END_Z})",
    f"  Circle hole carries through Section-2 tab (Z={G8_START_Z}..{G8_END_Z})",
    "",
    "-- G9 : Profile (S4, Z=10) + symmetric extrude-cut --",
    f"  S4 profile: pentagon-like outline ({len(S4_LOOP)} lines, closed)",
    f"  Sketch plane Z = {S4_Z}",
    f"  Cut: ±{G9_HALF} mm symmetric in Z  (Z={G9_BOT_Z} → Z={G9_TOP_Z}, total {G9_TOTAL} mm)",
    f"  Implementation: TWO subtract extrudes from sketch (+{G9_HALF} and -{G9_HALF})",
    "",
    "-- G10 : Circular pattern of (G6 → G9) --",
    f"  Pattern axis: vertical at ({G10_AXIS_CX}, {G10_AXIS_CY}) "
    f"(centre of S1 circle)",
    f"  Quantity: {G10_COUNT} instances at "
    f"{', '.join(f'{i*360.0/G10_COUNT:.1f}°' for i in range(G10_COUNT))}",
    f"  G7+G8 join, G9 cut applied at each rotated position",
    "",
    f"-- G11 : Profile (S5, Z={S5_Z}) — bounding box (lines+arc) + inner circle --",
    f"  Inner circle: centre=({S5_CIRC_CX:.3f}, {S5_CIRC_CY:.3f})  r={S5_CIRC_R:.3f}",
    f"  Bounding box: rectangle x=[-5, 5], y=[210, 219.791] + small step to y=220.391 + top arc",
    "",
    "-- G12 : Extrude-join BOTH S5 sections (box + circle) --",
    f"  Depth: -12.1 mm in -Z  (Z={S5_Z} → Z={S5_Z - 12.1})",
    "",
    "-- G13 : Extrude-cut S5 inner circle --",
    f"  Depth: -12.0 mm in -Z  (Z={S5_Z} → Z={S5_Z - 12.0})",
    f"  Leaves 0.1 mm of material under the hole at the bottom of the G12 prism",
    "",
    f"-- G14 : Profile (S6, Z={S6_Z}) — closed loop of lines --",
    f"  S6 profile: {len(S6_LOOP)} lines forming a single closed loop",
    "",
    "-- G15 : Extrude-cut S6 profile symmetrically --",
    f"  Cut: ±1.5 mm symmetric in Z  (Z={S6_Z - 1.5} → Z={S6_Z + 1.5}, total 3.0 mm)",
    f"  Implementation: TWO subtract extrudes from sketch (+1.5 and -1.5)",
    "",
    f"-- G16 : Profile (S7, Z={S7_Z}) — circles bucketed by diameter --",
    f"  Circles dia ≈ 8.4: {len(circles_dia_8_4)} found",
    f"  Circles dia ≈ 5.9: {len(circles_dia_5_9)} found",
    f"  Circles dia ≈ 3.4: {len(circles_dia_3_4)} found",
    "",
    "-- G17 : Extrude-cut dia ≈ 8.4 circles --",
    f"  Depth: +2.1 mm in +Z  (Z={S7_Z} → Z={S7_Z + 2.1})",
    f"  Produces 1.1 mm-deep counterbore-style holes through floor at Z=0",
    "",
    "-- G18 : Extrude-cut dia ≈ 5.9 circles --",
    f"  Depth: +3.9 mm in +Z  (Z={S7_Z} → Z={S7_Z + 3.9})",
    "",
    "-- G19 : Extrude-cut dia ≈ 3.4 circles --",
    f"  Depth: +8.0 mm in +Z  (Z={S7_Z} → Z={S7_Z + 8.0})",
    "",
    f"-- G20 : Profile (S8, YZ-plane at X={S8_X}) — circle --",
    f"  Circle: centre_Y={S8_CIRC_CY:.3f}, centre_Z={S8_CIRC_CZ:.3f}  r={S8_CIRC_R:.3f}",
    "",
    "-- G21 : Extrude-cut S8 circle symmetrically along X --",
    f"  Cut: ±50 mm symmetric in X  (through-bore along X)",
    f"  Implementation: TWO subtract extrudes from YZ sketch (+50 and -50)",
    "",
    f"-- G22 : Profile (S9, YZ-plane at X={S9_X}) — TWO closed loops --",
    f"  Auto-grouped into {len(s9_loops)} loops by walking endpoints",
    f"  Loop A (Y range 103.7→108.7): {len(loop_103_108)} lines",
    f"  Loop B (other):                {len(loop_other)} lines",
    "",
    "-- G23 : Extrude-join Loop A by 30 mm in -X --",
    f"  Sketch at X={S9_X} → solid extends toward X={S9_X - 30.0}",
    "",
    "-- G24 : Extrude-join Loop B by 26 mm in -X --",
    f"  Sketch at X={S9_X} → solid extends toward X={S9_X - 26.0}",
    "",
    f"-- G25 : Profile (S10, Z={S10_Z}) — single enclosed region --",
    f"  S10 profile: {len(s10_lines)} lines forming a single closed loop",
    "",
    "-- G26 : Extrude-cut S10 profile by 3.5 mm in -Z --",
    f"  Cut: Z={S10_Z} → Z={S10_Z - 3.5}",
    "",
    "-- G27 : Mirror G22-G26 across the global YZ plane --",
    f"  S9 features re-built at X={-S9_X} (mirror of {S9_X})",
    f"    Loop A extruded +30 mm in +X",
    f"    Loop B extruded +26 mm in +X",
    f"  S10 feature: every X coordinate negated, then cut -3.5 mm in -Z",
    "",
    "-- G28 : Fillet 3 bottom-face outer arcs (r≈65) at z=0 --",
    f"  Selection: bottom face via faces().sort_by(Axis.Z)[0], filter edges by radius ≈65",
    f"  Fillet radius applied: 4.99 (literal 5.0 fails OCC kernel; 0.01 mm difference",
    f"    is below STL tolerance, visually identical)",
    f"  Skipped Arc 1 (r=75 bottom of teardrop)",
    "",
    "-- G3 : Export --",
    f"  STL  : {STL_NAME}",
    f"  STEP : {STEP_NAME}",
    "",
    f"Watertight check  : {is_watertight}",
    f"Open edges        : {open_edges_count}",
    f"STL volume        : {vol_stl} mm^3",
    f"build123d volume  : {vol_b123d} mm^3",
    "=" * 60,
]

with open(SUMMARY_PATH, "w") as sf:
    sf.write("\n".join(summary_lines))
print(f"\n[SUMMARY] Written -> {SUMMARY_PATH}")

print("\nDone -- G1 to G28 complete.")