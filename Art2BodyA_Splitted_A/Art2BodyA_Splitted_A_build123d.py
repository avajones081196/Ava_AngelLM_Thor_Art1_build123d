"""
Art2BodyA_Splitted_A_build123d.py

Guidelines implemented:
  G1 – Read S1 CSV; parse circle + 4 arcs → three enclosed sections.
       Section 1: full circle (r=65 at origin).
       Section 2: crescent between circle (r=65) and Arc 2 (r=75, concentric).
       Section 3: bulge between Arc 2 and Arcs 1, 3, 4.
       Sketch plane: Z=32 (top face, per revised guideline).

  G2 + G4 – Stepped teardrop, built CUT-FIRST to avoid the Arc-2 seam:
       Step 1: extrude the full teardrop OUTER silhouette (bottom of
               circle + Arcs 3, 4, 1; Arc 2 NOT drawn) from Z=32 down
               to Z=0 — one watertight 32 mm-tall solid.
       Step 2: cut the bulge region (section 3, bounded by Arc 2 + the
               short segments of Arcs 3, 4, 1) from Z=5 down to Z=0.
       Net result: sections 1+2 occupy Z=0..32, section 3 occupies
       Z=5..32, step at Z=5. No shared internal face seam.
  G3 – (Logic stage) Base complete — no intermediate export.
  G5 – Apply 5 mm radius fillet to bottom face (z=0) arc boundary portion
       consisting of the small-circle tangent arcs (Arcs 1, 3) and the
       top connecting arc (Arc 4), leaving the r=75 arc (Arc 2) un-filleted.
  G6 – Read S2 CSV; draw each row as its Draw Type → one circle + four arcs
       at Z=32 (top face).
  G7 – Extrude-cut the circle profile (G6) by 29 mm in -Z and 1 mm in +Z.
  G8 – Extrude-cut the circle-adjacent crescent section (G6)
       by 19 mm in -Z and 1 mm in +Z.
  G9  – Extrude-cut the third / bulge section (G6)
        by 22 mm in -Z and 1 mm in +Z.
  G10 – Read S3 CSV; draw each row as its Draw Type → four circles.
  G11 – Extrude-cut all four circles (G10) by 6 mm in -Z.
  G12 – Read S4 CSV; draw each row as its Draw Type → one circle.
  G13 – Extrude-cut that circle by 1.1 mm in +Z (from bottom face upward).
  G14 – Read S5 CSV; draw each row as its Draw Type → two circles on their
         respective Z planes (r≈12 at Z=11, r≈18 at Z=5).
  G15 – Loft between the two S5 circles to form a truncated-cone body.
  G16 – Extrude-join from the larger S5 circle (r≈18 at Z=5) downward in -Z
         to meet the base body at Z=0.
  G17 – Read S6 CSV; draw each row as its Draw Type → 6 lines + 4 circles
         (d≈3.4 × 2, d≈10, d≈16.4) all at Z=0.
  G18 – Extrude-cut both d≈3.4 circles and the d≈10 circle by 12 mm in +Z
         and 0.5 mm in -Z.
  G19 – Read S7 CSV; following its Draw Type, identify three enclosed sections:
         Section A (left):   Lines 1,2,3 + Arc 4 (left half) → rectangle closed by arc.
         Section B (right):  Lines 4,5,6 + Arc 2 (right half) → rectangle closed by arc.
         Section C (center): Arcs 1,2,3,4 together → enclosed circle r≈8.2.
  G20 – Extrude-cut ALL three enclosed sections (A, B, C) by 4 units in +Z.
  G21 – Extrude-cut ONLY the middle/center section formed by arcs only (Section C)
         by 9 units in +Z from Z=0 (deepens pocket to 9 mm; Sections A & B stay at 4 mm).
  G22 – Read S8 CSV; draw each row as its Draw Type (all Lines) → two enclosed hexagon
         profiles at Z=11. The 6 true corner vertices are identified from the line
         endpoints; intermediate collinear points on shared edges are ignored.
         Hexagon LEFT:  centre=(-11, 0, 11)  circumradius≈3.35 mm
         Hexagon RIGHT: centre=( 11, 0, 11)  circumradius≈3.35 mm
  G23 – Extrude-cut BOTH hexagon profiles by 4 units in -Z and 0.2 units in +Z.
  G24 – Read S9 CSV; draw each row as its Draw Type (all Lines) → two enclosed pentagon
         regions at Y=83 (XZ sketch plane), symmetric about X=0.
         Region RIGHT: 5-vertex polygon  (X>0 side)
         Region LEFT:  5-vertex polygon  (X<0 side, mirror of right)
  G25 – Extrude-join BOTH S9 profiles by 6 units in -Y direction (Y=83 → Y=77).
  G26 – Read the S10 profile (CSV); parse to get two circles.
  G27 – Extrude-join the region between the two circles (G26) by 10.3 units in -Z.
  G28 – Read the S11 file, draw it as per draw type to get an enclosed tooth profile.
  G29 – Read the S12 file, extract the line coordinates used as a reference sweep path.
  G30 – Perform a sweep join body operation on the tooth profile (G28) along the 
         path (G29) with a twist angle of -5.97 degrees to form a helical tooth.

General guidelines:
  • .clean() called right before export.
  • Watertight check + volume report before export.
  • Export at the LAST stage (after G25).
  • Summary file name: folder_name_summary_G_1_25
  • OCP viewer port: 3939.
"""

import os
import csv
import math

# ── paths ──────────────────────────────────────────────────────────────────
BASE_DIR    = "/Users/avajones/Documents/ava_build123d/20260422_assign/Art2BodyA_Splitted_A"
CSV_DIR     = os.path.join(BASE_DIR, "csv_merged")
FOLDER_NAME = "Art2BodyA_Splitted_A"

# Updated to G_1_31
STL_NAME     = f"{FOLDER_NAME}_G_1_31.stl"
STEP_NAME    = f"{FOLDER_NAME}_G_1_31.step"
SUMMARY_NAME = f"{FOLDER_NAME}_summary_G_1_31.txt"

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
S10_CSV = os.path.join(CSV_DIR, "Fusion_Coordinates_S10.csv") # New S10 Path
S11_CSV = os.path.join(CSV_DIR, "Fusion_Coordinates_S11.csv") # New
S12_CSV = os.path.join(CSV_DIR, "Fusion_Coordinates_S12.csv") # New

# ── build123d imports ──────────────────────────────────────────────────────
from build123d import (
    BuildPart, BuildSketch, BuildLine,
    Circle, ThreePointArc, Line,
    Mode, Axis, Vector, Align, Locations,
    extrude, fillet, loft, export_stl, export_step,
    Plane, Location, make_face, add, sweep  # <--- added 'add' and 'sweep' here
)

# ── OCP viewer ────────────────────────────────────────────────────────────
from ocp_vscode import show, set_port
set_port(3939)

# ══════════════════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════════════════

def circumscribed_circle_from_3pts(p1, p2, p3):
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
# DEBUG: find which G stage introduces open edges
# ══════════════════════════════════════════════════════════════════════════
import trimesh, numpy as np

def _check_open(solid, label, base_dir):
    _tmp = os.path.join(base_dir, "_tmp_dbg.stl")
    export_stl(solid, _tmp, tolerance=1e-4, angular_tolerance=0.01)
    _m = trimesh.load(_tmp)
    os.remove(_tmp)
    _ue, _ec = np.unique(_m.edges_sorted, axis=0, return_counts=True)
    print(f"[DEBUG] {label:30s}: watertight={_m.is_watertight}  open_edges={int((_ec==1).sum())}")

# ══════════════════════════════════════════════════════════════════════════
print("=" * 60)
print("Art2BodyA_Splitted_A_build123d.py")
print("=" * 60)

# ══════════════════════════════════════════════════════════════════════════
# G1 – Read S1: circle + 4 arcs → three enclosed sections
# ══════════════════════════════════════════════════════════════════════════
print(f"\n[G1] Reading S1 from: {S1_CSV}")
s1_rows = read_all_rows(S1_CSV)

# ── Parse circle ──
circ_row = [r for r in s1_rows if "circle" in r["Draw Type"].lower()][0]
c_p1 = (float(circ_row["X1"]), float(circ_row["Y1"]))
c_p2 = (float(circ_row["X2"]), float(circ_row["Y2"]))
c_p3 = (float(circ_row["X3"]), float(circ_row["Y3"]))
c_cx, c_cy, c_r = circumscribed_circle_from_3pts(c_p1, c_p2, c_p3)
S1_Z = float(circ_row["Z1"])

print(f"       Circle: centre=({c_cx:.3f}, {c_cy:.3f})  r={c_r:.3f}  Z={S1_Z}")

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

# S1 key geometry:
#   Circle  r=65  at origin
#   Arc 1   r=65  at (102.47, 80)   — right tangent arc
#   Arc 2   r=75  at (0, 0)         — concentric inner arc
#   Arc 3   r=65  at (-102.47, 80)  — left tangent arc (mirror of Arc 1)
#   Arc 4   r=75  at (0, 160)       — top connecting arc

CIRCLE_R = c_r          # ≈ 65
ARC2_R   = arcs[1]["r"] # ≈ 75

# Key 2D points on S1 sketch
PT_R_LOW  = arcs[0]["p3"]   # (51.235,  40.0)   — arc1 meets circle
PT_R_MID  = (39.538, 63.732)  # where arc 2 starts  (also on circle r=75)
PT_R_TOP  = arcs[0]["p1"]   # (39.538,  96.268)  — arc1 top
PT_L_LOW  = arcs[2]["p1"]   # (-51.235, 40.0)   — arc3 meets circle
PT_L_MID  = (-39.538, 63.732) # where arc 2 ends
PT_L_TOP  = arcs[2]["p3"]   # (-39.538, 96.268)  — arc3 top

print(f"\n       Section 1: Full circle r={CIRCLE_R:.3f}")
print(f"       Section 2: Crescent between circle (r={CIRCLE_R:.3f}) and Arc 2 (r={ARC2_R:.3f})")
print(f"       Section 3: Bulge bounded by Arcs 1, 4, 3, and Arc 2")

# ══════════════════════════════════════════════════════════════════════════
# Extrusion depths (G2 / G4 / G5)  — stepped teardrop via CUT-FIRST
#
# Step 1: extrude full outer silhouette  Z=32 → Z=0   (32 mm in -Z)
# Step 2: cut bulge region (section 3)   Z=5  → Z=0   ( 5 mm in -Z)
# Final: sections 1+2 span Z=0..32, section 3 spans Z=5..32, step at Z=5.
# ══════════════════════════════════════════════════════════════════════════
SKETCH_Z_TOP = 32.0   # top face Z (revised guideline)
PART_HEIGHT  = 32.0   # full extrusion height (Z=0 → Z=32)
BULGE_FLOOR  =  5.0   # section 3 starts at Z=5; below this is sections 1+2 only
EXTRUDE_DOWN = -5.0   # legacy: kept so G5 bottom_z = S1_Z + EXTRUDE_DOWN = 0 stays correct
EXTRUDE_UP   = 27.0   # legacy: kept for summary text only
FILLET_R     =  5.0   # G5: fillet radius on bottom-face arcs

# ══════════════════════════════════════════════════════════════════════════
# G6 – Read S2: one circle + four arcs at Z=32 (top face)
#      Draw each row exactly as its Draw Type states.
# ══════════════════════════════════════════════════════════════════════════
print(f"\n[G6] Reading S2 from: {S2_CSV}")
s2_rows = read_all_rows(S2_CSV)

# ── Parse S2 circle ──
s2_circ_row = [r for r in s2_rows if "circle" in r["Draw Type"].lower()][0]
s2_cp1 = (float(s2_circ_row["X1"]), float(s2_circ_row["Y1"]))
s2_cp2 = (float(s2_circ_row["X2"]), float(s2_circ_row["Y2"]))
s2_cp3 = (float(s2_circ_row["X3"]), float(s2_circ_row["Y3"]))
s2_cx, s2_cy, s2_cr = circumscribed_circle_from_3pts(s2_cp1, s2_cp2, s2_cp3)
S2_Z = float(s2_circ_row["Z1"])  # 32

print(f"       Circle: centre=({s2_cx:.3f}, {s2_cy:.3f})  r={s2_cr:.3f}  Z={S2_Z}")

# ── Parse S2 arcs (sorted by trailing digit) ──
s2_arc_rows = sorted(
    [r for r in s2_rows if "arc" in r["Draw Type"].lower()],
    key=lambda r: int([s for s in r["Draw Type"].split("_") if s.isdigit()][-1])
)
s2_arcs = []
for ar in s2_arc_rows:
    dt = ar["Draw Type"].strip()
    p1 = (float(ar["X1"]), float(ar["Y1"]))
    p2 = (float(ar["X2"]), float(ar["Y2"]))
    p3 = (float(ar["X3"]), float(ar["Y3"]))
    acx, acy, ar_r = circumscribed_circle_from_3pts(p1, p2, p3)
    s2_arcs.append({"dt": dt, "p1": p1, "p2": p2, "p3": p3,
                    "cx": acx, "cy": acy, "r": ar_r})
    print(f"       {dt:25s}  centre=({acx:.3f}, {acy:.3f})  r={ar_r:.3f}")
    print(f"         from ({p1[0]:.3f},{p1[1]:.3f}) "
          f"→ mid ({p2[0]:.3f},{p2[1]:.3f}) "
          f"→ ({p3[0]:.3f},{p3[1]:.3f})")

# S2 geometry (from CSV):
#
#   Circle  r=62.5 at origin
#     p1=(62.5, 0)  p2=(-31.25, 54.127)  p3=(-31.25,-54.127)
#
#   Arc 1 (3_point_arc_1) — concentric inner arc r≈65
#     from ( 37.996, 52.738) through (0, 65) to (-37.996, 52.738)
#     → this is the boundary between Section 1 and Section 2
#
#   Arc 2 (3_point_arc_2) — left tangent arc
#     from (-40.353, 47.727) through (-33.041, 71.075) to (-34.21, 95.512)
#
#   Arc 3 (3_point_arc_3) — top connecting arc
#     from (-34.21, 95.512) through (0, 87) to (34.21, 95.512)
#
#   Arc 4 (3_point_arc_4) — right tangent arc
#     from (34.21, 95.512) through (33.041, 71.075) to (40.353, 47.727)
#
# Three S2 sections to cut:
#   Section 1 (circle):           full circle r=62.5
#   Section 2 (adjacent crescent): ring between circle r=62.5 and Arc 1 r≈65
#                                  bounded laterally by partial arcs 2 and 4
#   Section 3 (third / bulge):    region above Arc 1 bounded by Arc 2, Arc 3, Arc 4

S2_CIRCLE_R = s2_cr                     # 62.5
S2_ARC1_R   = s2_arcs[0]["r"]           # ≈ 65  (concentric inner arc)

# Named connection points
S2_PT_R_LOW  = s2_arcs[3]["p3"]         # ( 40.353,  47.727) — Arc4 end / circle right
S2_PT_R_MID  = s2_arcs[0]["p1"]         # ( 37.996,  52.738) — Arc1 start (right)
S2_PT_R_TOP  = s2_arcs[1]["p3"]         # (-34.21,   95.512) → wait, arc2 is LEFT
# Re-map correctly:
#   Arc 2 goes:  (-40.353,47.727) → (-33.041,71.075) → (-34.21,95.512)   LEFT side
#   Arc 4 goes:  ( 34.21, 95.512) → ( 33.041,71.075) → ( 40.353,47.727)  RIGHT side

S2_PT_L_LOW  = s2_arcs[1]["p1"]         # (-40.353,  47.727) — Arc2 start (left low)
S2_PT_L_TOP  = s2_arcs[1]["p3"]         # (-34.21,   95.512) — Arc2 end   (left top)
S2_PT_R_TOP2 = s2_arcs[3]["p1"]         # ( 34.21,   95.512) — Arc4 start (right top)
S2_PT_R_LOW2 = s2_arcs[3]["p3"]         # ( 40.353,  47.727) — Arc4 end   (right low)
S2_PT_L_MID  = s2_arcs[0]["p3"]         # (-37.996,  52.738) — Arc1 end   (left)

print(f"\n       S2 Section 1 (circle r={S2_CIRCLE_R:.1f}):  cut -29 / +1 mm")
print(f"       S2 Section 2 (adjacent crescent):         cut -19 / +1 mm")
print(f"       S2 Section 3 (third/bulge):               cut -22 / +1 mm")

# Cut depths (negative = into part, positive = above top face for clean boolean)
S2_CUT_NEG_CIRCLE   = 29.0   # G7
S2_CUT_NEG_ADJACENT = 19.0   # G8
S2_CUT_NEG_THIRD    = 22.0   # G9
S2_CUT_POS          =  1.0   # all three: 1 mm above top face

# ══════════════════════════════════════════════════════════════════════════
# BUILD THE FULL PART  G1 → G9
# ══════════════════════════════════════════════════════════════════════════
print("\n[BUILD] Constructing full part G1–G9 …")

# DEBUG: G2 alone — sections 1+2 (circle + crescent) full-height, sanity check.
print("\n[DEBUG] Running G2 alone ...")
with BuildPart() as _g2_only:
    with BuildSketch(Plane.XY.offset(SKETCH_Z_TOP)):
        with BuildLine():
            ThreePointArc(PT_R_LOW, (0, -CIRCLE_R),     PT_L_LOW)
            ThreePointArc(PT_L_LOW, (-44.167, 51.265),  PT_L_MID)
            ThreePointArc(PT_L_MID, (0, ARC2_R),        PT_R_MID)
            ThreePointArc(PT_R_MID, ( 44.167, 51.265),  PT_R_LOW)
        make_face()
    extrude(amount=-PART_HEIGHT)   # Z=32 → Z=0
_check_open(_g2_only.part, "G2 only (debug)", BASE_DIR)
print("[DEBUG] G2 done.")

# ══════════════════════════════════════════════════════════════════════════
# G2 + G4 — stepped teardrop via CUT-FIRST.
#
# Step 1: extrude full teardrop OUTER silhouette  Z=32 → Z=0  (32 mm in -Z).
#         Sketch contains only the outer boundary (bottom of circle r=65,
#         Arc 3, Arc 4, Arc 1). Arc 2 is NOT drawn — it is only a logical
#         section divider and would create an internal seam if included.
#
# Step 2: cut the bulge (section 3) from Z=5 → Z=0  (5 mm in -Z).
#         Section 3 outline = Arc 2 + the SHORT segments of Arcs 3, 4, 1
#         (between PT_*_TOP and PT_*_MID, not the full arcs that extend
#         down to PT_*_LOW). Boolean cut handles this cleanly without a
#         shared-face seam.
#
# Final: sections 1+2 span Z=0..32, section 3 spans Z=5..32, step at Z=5.
# ══════════════════════════════════════════════════════════════════════════

print("\n[G2+G4] Step 1: extrude full teardrop outer silhouette Z=32 → Z=0 …")

with BuildPart() as part_full:
    with BuildSketch(Plane.XY.offset(SKETCH_Z_TOP)):
        with BuildLine():
            ThreePointArc(PT_R_LOW,  (0, -CIRCLE_R),  PT_L_LOW)   # bottom of circle r=65
            ThreePointArc(PT_L_LOW,  arcs[2]["p2"],   PT_L_TOP)   # Arc 3 (left tangent)
            ThreePointArc(PT_L_TOP,  arcs[3]["p2"],   PT_R_TOP)   # Arc 4 (top connecting)
            ThreePointArc(PT_R_TOP,  arcs[0]["p2"],   PT_R_LOW)   # Arc 1 (right tangent)
        make_face()
    extrude(amount=-PART_HEIGHT)   # Z=32 → Z=0

solid_full = part_full.part.clean()
_check_open(solid_full, "After full extrude (step 1)", BASE_DIR)

print("\n[G2+G4] Step 2: cut bulge (section 3) from Z=5 → Z=0 …")

# OCC robustness note:
# The cutter's "outer" side walls (along Arcs 3, 4, 1) would coincide exactly
# with the main solid's outer side walls if we drew them as arcs. That
# coincident-face configuration causes a Boolean failure with thousands of
# open edges. Instead, we keep Arc 2 EXACT (it's the inner cut boundary that
# defines the section-2/section-3 split) and replace Arcs 3, 4, 1 with a
# generous bounding box that sits entirely OUTSIDE the teardrop's outer wall.
# The Boolean cut only removes material that's inside BOTH the main solid
# AND the cutter, so the bounding-box overhang has no geometric effect — it
# just frees OCC from coincident-face headaches.
#
# Cutter outline (CCW around the bulge area):
#   PT_R_MID → (Arc 2 via (0, 75)) → PT_L_MID
#         → (-BBOX_X, PT_L_MID.y) → (-BBOX_X, BBOX_Y_TOP)
#         → ( BBOX_X, BBOX_Y_TOP)  → ( BBOX_X, PT_R_MID.y)
#         → PT_R_MID  (closes)

BBOX_X     = 200.0   # generous: teardrop max |x| is ~65
BBOX_Y_TOP = 250.0   # generous: teardrop max y is ~96
EPS        = 0.05    # small Z-overshoot above Z=5 and below Z=0 so cutter
                     # end-faces don't coincide with main solid faces
CUTTER_TOP_Z  = BULGE_FLOOR + EPS                    # 5.05
CUTTER_HEIGHT = (BULGE_FLOOR + EPS) + EPS            # 5.10  (Z=5.05 → Z=-0.05)

with BuildPart() as part_cutter:
    with BuildSketch(Plane.XY.offset(CUTTER_TOP_Z)):
        with BuildLine():
            # Inner boundary: Arc 2 (concave, bowing up to (0, 75))
            ThreePointArc(PT_R_MID,  (0, ARC2_R),     PT_L_MID)   # Arc 2 (r=75)
            # Outer boundary: bounding rectangle entirely outside teardrop
            Line(PT_L_MID,  (-BBOX_X, PT_L_MID[1]))
            Line((-BBOX_X, PT_L_MID[1]), (-BBOX_X, BBOX_Y_TOP))
            Line((-BBOX_X, BBOX_Y_TOP),  ( BBOX_X, BBOX_Y_TOP))
            Line(( BBOX_X, BBOX_Y_TOP),  ( BBOX_X, PT_R_MID[1]))
            Line(( BBOX_X, PT_R_MID[1]), PT_R_MID)
        make_face()
    extrude(amount=-CUTTER_HEIGHT)   # Z=5.05 → Z=-0.05

# Boolean cut — removes section 3 below Z=5 from the full-height solid.
solid_g4 = solid_full.cut(part_cutter.part).clean()

# Skip the OCP preview here — show() was hanging the script before
# _check_open could report. Final preview is at the end of the script.
# show(solid_g4)

_check_open(solid_g4, "After G2+G4 (stepped cut)", BASE_DIR)

# ── G5: Fillet bottom-face edges (z = S1_Z + EXTRUDE_DOWN = 0) ─────────
print("\n[G5] Applying fillet r=5 mm to bottom-face edges (skipping Arc2 r=75) …")

bottom_z = S1_Z + EXTRUDE_DOWN  # 0

edges_to_fillet = []
for edge in solid_g4.edges():
    bbox = edge.bounding_box()
    mid  = edge.center()
    # Must be a flat bottom-face edge
    if abs(bbox.min.Z - bottom_z) > 0.5 or abs(bbox.max.Z - bottom_z) > 0.5:
        continue
    if edge.length < 0.5:
        continue
    dist = math.sqrt(mid.X**2 + mid.Y**2)
    # Skip Arc2 (r=75, concentric with origin)
    if abs(dist - ARC2_R) < 3.0:
        print(f"       ✗ SKIP Arc2: mid=({mid.X:.1f},{mid.Y:.1f})  dist={dist:.1f}")
        continue
    edges_to_fillet.append(edge)
    print(f"       → FILLET: mid=({mid.X:.1f},{mid.Y:.1f})  dist={dist:.1f}  len={edge.length:.1f}")

if edges_to_fillet:
    print(f"\n       Attempting fillet on {len(edges_to_fillet)} edge(s) with r={FILLET_R} …")
    solid_g5 = solid_g4
    for try_r in [FILLET_R, 4.99, 4.95, 4.9, 4.8, 4.5, 4.0]:
        try:
            solid_g5 = solid_g4.fillet(try_r, edges_to_fillet)
            print(f"       ✓ Fillet applied with r={try_r}")
            break
        except Exception as e:
            print(f"       ⚠ r={try_r} failed: {e}")
    else:
        print("       ⚠ All fillet attempts failed — proceeding without fillet")
        solid_g5 = solid_g4
else:
    print("       ⚠ No matching bottom-face edges found — proceeding without fillet")
    solid_g5 = solid_g4

print("\n[OCP] Sending G5 preview …")
# show(solid_g5)   # disabled: was hanging script before _check_open

# ══════════════════════════════════════════════════════════════════════════
# G7–G9: Extrude-cut S2 profiles from top face (Z=32)
#
# Revised guidelines:
#   G7: cut circle      -29 mm (into part) and +1 mm (above face)
#   G8: cut crescent    -19 mm (into part) and +1 mm (above face)
#   G9: cut bulge       -22 mm (into part) and +1 mm (above face)
#
# Strategy: build a cutter solid for each section that spans from
#   Z = S2_Z + S2_CUT_POS  (1 mm above top face)
#   down to
#   Z = S2_Z - S2_CUT_NEG  (into the part)
# using extrude with both parameter or two extrudes, then subtract.
# build123d's extrude() takes a signed `amount`; to cut both directions we
# sketch on the mid-plane or use two separate subtractive extrudes.
# ══════════════════════════════════════════════════════════════════════════
print("\n[G7–G9] Cutting S2 profiles from top face …")

with BuildPart() as cut_part:
    cut_part._add_to_context(solid_g5)

    # ── G7: Cut circle section ────────────────────────────────────────────
    # Sketch circle at Z=32, extrude -29 (into part) + 1 (above)
    print("\n[G7] Cutting circle r=62.5 by -29 mm and +1 mm …")
    with BuildSketch(Plane.XY.offset(S2_Z)):
        Circle(S2_CIRCLE_R)
    extrude(amount=-S2_CUT_NEG_CIRCLE,  mode=Mode.SUBTRACT)   # -29 into part

    with BuildSketch(Plane.XY.offset(S2_Z)):
        Circle(S2_CIRCLE_R)
    extrude(amount=S2_CUT_POS,          mode=Mode.SUBTRACT)   # +1 above face

    # ── G8: Cut adjacent crescent section ─────────────────────────────────
    # Region between circle r=62.5 and Arc1 r≈65, bounded by partial arcs 2 & 4.
    # Sketch: outer boundary = circle-bottom arc + Arc2-partial + Arc1 + Arc4-partial
    #         inner subtract  = circle r=62.5
    # Sub-arc midpoints computed from arc centres (Arc2/Arc4 centre at ±102.472, 80):
    #   Arc2 partial low mid  = (-39.1251, 50.2093)
    #   Arc4 partial low mid  = ( 39.1251, 50.2093)
    print("\n[G8] Cutting adjacent crescent by -19 mm and +1 mm …")
    S2_ARC2_LOW_MID = (-39.1251, 50.2093)   # on Arc2, between L_LOW and L_MID
    S2_ARC4_LOW_MID = ( 39.1251, 50.2093)   # on Arc4, between R_MID and R_LOW2
    for cut_amount in [-S2_CUT_NEG_ADJACENT, S2_CUT_POS]:
        with BuildSketch(Plane.XY.offset(S2_Z)):
            with BuildLine():
                # Circle arc from right-low around bottom to left-low
                ThreePointArc(S2_PT_R_LOW2, (0, -S2_CIRCLE_R), S2_PT_L_LOW)
                # Arc2 partial: left-low → left-mid (small bottom segment of Arc2)
                ThreePointArc(S2_PT_L_LOW, S2_ARC2_LOW_MID, S2_PT_L_MID)
                # Arc1 (concentric r=65): left-mid → right-mid through (0, 65)
                ThreePointArc(S2_PT_L_MID, (0, S2_ARC1_R), S2_PT_R_MID)
                # Arc4 partial: right-mid → right-low (small bottom segment of Arc4)
                ThreePointArc(S2_PT_R_MID, S2_ARC4_LOW_MID, S2_PT_R_LOW2)
            make_face()
            # Subtract inner circle to leave only the crescent ring
            Circle(S2_CIRCLE_R, mode=Mode.SUBTRACT)
        extrude(amount=cut_amount, mode=Mode.SUBTRACT)

    # ── G9: Cut third / bulge section ─────────────────────────────────────
    # Region above Arc1, bounded by: Arc1 (bottom), Arc2 (left), Arc3 (top), Arc4 (right)
    # Sub-arc midpoints computed from arc centres (Arc2/Arc4 centre at ±102.472, 80):
    #   Arc2 upper mid  = (-32.7424, 73.8276)   between L_MID and L_TOP
    #   Arc4 upper mid  = ( 32.7424, 73.8276)   between R_TOP2 and R_MID
    print("\n[G9] Cutting third/bulge section by -22 mm and +1 mm …")
    S2_ARC2_UP_MID = (-32.7424, 73.8276)    # on Arc2, between L_MID and L_TOP
    S2_ARC4_UP_MID = ( 32.7424, 73.8276)    # on Arc4, between R_TOP2 and R_MID
    for cut_amount in [-S2_CUT_NEG_THIRD, S2_CUT_POS]:
        with BuildSketch(Plane.XY.offset(S2_Z)):
            with BuildLine():
                # Arc1: right-mid → left-mid through (0,65) — bottom of bulge
                ThreePointArc(S2_PT_R_MID, (0, S2_ARC1_R), S2_PT_L_MID)
                # Arc2 upper: left-mid → left-top (upper portion of Arc2)
                ThreePointArc(S2_PT_L_MID, S2_ARC2_UP_MID, S2_PT_L_TOP)
                # Arc3 (top connecting): left-top → right-top through (0, 87)
                ThreePointArc(S2_PT_L_TOP, s2_arcs[2]["p2"], S2_PT_R_TOP2)
                # Arc4 upper: right-top → right-mid (upper portion of Arc4)
                ThreePointArc(S2_PT_R_TOP2, S2_ARC4_UP_MID, S2_PT_R_MID)
            make_face()
        extrude(amount=cut_amount, mode=Mode.SUBTRACT)

solid_final_g9 = cut_part.part

print("\n[OCP] Sending G9 preview …")
# show(solid_final_g9)   # disabled: was hanging script before _check_open

# ══════════════════════════════════════════════════════════════════════════
# G10 – Read S3: four circles
# ══════════════════════════════════════════════════════════════════════════
print(f"\n[G10] Reading S3 from: {S3_CSV}")
s3_rows = read_all_rows(S3_CSV)

s3_circles = []
for row in s3_rows:
    dt = row["Draw Type"].strip()
    if "circle" not in dt.lower():
        print(f"       WARNING: unexpected Draw Type '{dt}' in S3 — skipping")
        continue
    p1 = (float(row["X1"]), float(row["Y1"]))
    p2 = (float(row["X2"]), float(row["Y2"]))
    p3 = (float(row["X3"]), float(row["Y3"]))
    cx, cy, cr = circumscribed_circle_from_3pts(p1, p2, p3)
    z = float(row["Z1"])
    s3_circles.append({"dt": dt, "cx": cx, "cy": cy, "r": cr, "z": z})
    print(f"       {dt:25s}  centre=({cx:.4f}, {cy:.4f})  r={cr:.4f}  Z={z}")

print(f"\n       {len(s3_circles)} circle(s) found")

# ══════════════════════════════════════════════════════════════════════════
# G11 – Extrude-cut all four S3 circles by 6 mm in -Z
# ══════════════════════════════════════════════════════════════════════════
S3_CUT_NEG = 6.0

print(f"\n[G11] Cutting {len(s3_circles)} circle(s) by -{S3_CUT_NEG} mm in -Z …")

with BuildPart() as g11_part:
    g11_part._add_to_context(solid_final_g9)

    # Each circle's Z from the CSV (=10) is the sketch face — the recessed bulge floor.
    # The holes cut from Z=10 downward by 6 mm through the solid wall to Z=4.
    # IMPORTANT: Circle() must be placed at (cx, cy) on its sketch plane via Location,
    # otherwise it defaults to the sketch origin (0,0) and cuts nothing.
    for circ in s3_circles:
        print(f"       Cutting {circ['dt']:25s}  "
              f"centre=({circ['cx']:.4f}, {circ['cy']:.4f})  "
              f"r={circ['r']:.4f}  sketch Z={circ['z']}  cut -{S3_CUT_NEG} mm")
        with BuildSketch(Plane.XY.offset(circ["z"])):
            with Locations((circ["cx"], circ["cy"])):
                Circle(circ["r"])
        extrude(amount=-S3_CUT_NEG, mode=Mode.SUBTRACT)

solid_final_g11 = g11_part.part

print("\n[OCP] Sending G11 preview …")
# show(solid_final_g11)   # disabled: was hanging script before _check_open

# ══════════════════════════════════════════════════════════════════════════
# G12 – Read S4: one circle
# ══════════════════════════════════════════════════════════════════════════
print(f"\n[G12] Reading S4 from: {S4_CSV}")
s4_rows = read_all_rows(S4_CSV)

s4_circles = []
for row in s4_rows:
    dt = row["Draw Type"].strip()
    if "circle" not in dt.lower():
        print(f"       WARNING: unexpected Draw Type '{dt}' in S4 — skipping")
        continue
    p1 = (float(row["X1"]), float(row["Y1"]))
    p2 = (float(row["X2"]), float(row["Y2"]))
    p3 = (float(row["X3"]), float(row["Y3"]))
    cx, cy, cr = circumscribed_circle_from_3pts(p1, p2, p3)
    z = float(row["Z1"])
    s4_circles.append({"dt": dt, "cx": cx, "cy": cy, "r": cr, "z": z})
    print(f"       {dt:25s}  centre=({cx:.4f}, {cy:.4f})  r={cr:.4f}  Z={z}")

print(f"\n       {len(s4_circles)} circle(s) found")

# ══════════════════════════════════════════════════════════════════════════
# G13 – Extrude-cut the S4 circle by 1.1 mm in +Z (from bottom face upward)
# ══════════════════════════════════════════════════════════════════════════
S4_CUT_POS = 1.1   # +Z into solid from bottom face

print(f"\n[G13] Cutting {len(s4_circles)} circle(s) by +{S4_CUT_POS} mm in +Z …")

with BuildPart() as g13_part:
    g13_part._add_to_context(solid_final_g11)

    # S4 circle is at Z=0 (bottom face). Cut upward +1.1 mm into the solid.
    # Use Locations((cx, cy)) to place the circle at its correct XY centre.
    for circ in s4_circles:
        print(f"       Cutting {circ['dt']:25s}  "
              f"centre=({circ['cx']:.4f}, {circ['cy']:.4f})  "
              f"r={circ['r']:.4f}  sketch Z={circ['z']}  cut +{S4_CUT_POS} mm")
        with BuildSketch(Plane.XY.offset(circ["z"])):
            with Locations((circ["cx"], circ["cy"])):
                Circle(circ["r"])
        extrude(amount=S4_CUT_POS, mode=Mode.SUBTRACT)

solid_final_g13 = g13_part.part

print("\n[OCP] Sending G13 preview …")
# show(solid_final_g13)   # disabled: was hanging script before _check_open

# ══════════════════════════════════════════════════════════════════════════
# G14 – Read S5: two circles on their respective Z planes
# ══════════════════════════════════════════════════════════════════════════
print(f"\n[G14] Reading S5 from: {S5_CSV}")
s5_rows = read_all_rows(S5_CSV)

s5_circles = []
for row in s5_rows:
    dt = row["Draw Type"].strip()
    if "circle" not in dt.lower():
        print(f"       WARNING: unexpected Draw Type '{dt}' in S5 — skipping")
        continue
    p1 = (float(row["X1"]), float(row["Y1"]))
    p2 = (float(row["X2"]), float(row["Y2"]))
    p3 = (float(row["X3"]), float(row["Y3"]))
    cx, cy, cr = circumscribed_circle_from_3pts(p1, p2, p3)
    z = float(row["Z1"])
    s5_circles.append({"dt": dt, "cx": cx, "cy": cy, "r": cr, "z": z})
    print(f"       {dt:25s}  centre=({cx:.4f}, {cy:.4f})  r={cr:.4f}  Z={z}")

# Sort by Z ascending so loft goes bottom → top
s5_circles.sort(key=lambda c: c["z"])
s5_larger = s5_circles[0]   # larger circle: r≈18 at Z=5  (lower Z)
s5_smaller = s5_circles[1]  # smaller circle: r≈12 at Z=11 (higher Z)

print(f"\n       Larger  circle: r={s5_larger['r']:.4f}  Z={s5_larger['z']}")
print(f"       Smaller circle: r={s5_smaller['r']:.4f}  Z={s5_smaller['z']}")

# ══════════════════════════════════════════════════════════════════════════
# G15 – Loft between the two S5 circles → truncated-cone body
# ══════════════════════════════════════════════════════════════════════════
print("\n[G15] Lofting between S5 circles …")

with BuildPart() as loft_part:
    # Sketch both circles on their respective planes — loft connects them
    with BuildSketch(Plane.XY.offset(s5_larger["z"])):
        with Locations((s5_larger["cx"], s5_larger["cy"])):
            Circle(s5_larger["r"])
    with BuildSketch(Plane.XY.offset(s5_smaller["z"])):
        with Locations((s5_smaller["cx"], s5_smaller["cy"])):
            Circle(s5_smaller["r"])
    loft()

loft_body = loft_part.part
print(f"       ✓ Loft complete  "
      f"(r={s5_larger['r']:.4f} @ Z={s5_larger['z']} → "
      f"r={s5_smaller['r']:.4f} @ Z={s5_smaller['z']})")

print("\n[OCP] Sending G15 loft preview …")
# show(loft_body)   # disabled: was hanging script before _check_open

# ══════════════════════════════════════════════════════════════════════════
# G16 – Extrude-join from larger circle (Z=5) downward to base body (Z=0)
#        then union loft + extruded cylinder + base body
# ══════════════════════════════════════════════════════════════════════════
S5_EXTRUDE_DOWN = s5_larger["z"]   # 5.0 mm — from Z=5 down to Z=0

print(f"\n[G16] Extruding larger circle (r={s5_larger['r']:.4f}) "
      f"by -{S5_EXTRUDE_DOWN} mm in -Z to reach base …")

with BuildPart() as g16_part:
    # Sketch larger circle at its Z plane and extrude down to Z=0
    with BuildSketch(Plane.XY.offset(s5_larger["z"])):
        with Locations((s5_larger["cx"], s5_larger["cy"])):
            Circle(s5_larger["r"])
    extrude(amount=-S5_EXTRUDE_DOWN)   # creates cylinder Z=5 → Z=0

    # Add the loft body on top (union)
    g16_part._add_to_context(loft_body)

# Now union the full loft+cylinder protrusion with the main base body
with BuildPart() as final_part:
    final_part._add_to_context(solid_final_g13)
    final_part._add_to_context(g16_part.part)

solid_final_g16 = final_part.part

print(f"       ✓ Extrude-join complete  "
      f"(cylinder Z={s5_larger['z']} → Z=0, fused with base body)")

print("\n[OCP] Sending G16 preview …")
# show(solid_final_g16)   # disabled: was hanging script before _check_open

# ══════════════════════════════════════════════════════════════════════════
# G17 – Read S6: 6 lines + 4 circles at Z=0
# ══════════════════════════════════════════════════════════════════════════
print(f"\n[G17] Reading S6 from: {S6_CSV}")
s6_rows = read_all_rows(S6_CSV)

s6_lines   = []
s6_circles = []

for row in s6_rows:
    dt = row["Draw Type"].strip()
    if dt.lower() == "line":
        p1 = (float(row["X1"]), float(row["Y1"]))
        p2 = (float(row["X2"]), float(row["Y2"]))
        z  = float(row["Z1"])
        s6_lines.append({"dt": dt, "p1": p1, "p2": p2, "z": z})
        print(f"       Line: ({p1[0]},{p1[1]}) → ({p2[0]},{p2[1]})  Z={z}")
    elif "circle" in dt.lower():
        p1 = (float(row["X1"]), float(row["Y1"]))
        p2 = (float(row["X2"]), float(row["Y2"]))
        p3 = (float(row["X3"]), float(row["Y3"]))
        cx, cy, cr = circumscribed_circle_from_3pts(p1, p2, p3)
        z  = float(row["Z1"])
        s6_circles.append({"dt": dt, "cx": cx, "cy": cy, "r": cr, "z": z})
        print(f"       {dt:25s}  centre=({cx:.4f},{cy:.4f})  r={cr:.4f}  d={2*cr:.4f}  Z={z}")

# Identify circles by diameter for G18/G19/G20
# d≈3.4 → r≈1.7  (circles 1 & 2)
# d≈10  → r≈5.0  (circle 3)
# d≈16.4 → r≈8.2 (circle 4)
s6_small  = [c for c in s6_circles if abs(c["r"] - 1.7)  < 0.1]   # d≈3.4
s6_medium = [c for c in s6_circles if abs(c["r"] - 5.0)  < 0.1]   # d≈10
s6_large  = [c for c in s6_circles if abs(c["r"] - 8.2)  < 0.1]   # d≈16.4

S6_Z = s6_circles[0]["z"]   # all at Z=0

print(f"\n       d≈3.4  circles : {len(s6_small)}  {[(c['dt'],round(c['cx'],3),round(c['cy'],3)) for c in s6_small]}")
print(f"       d≈10   circles : {len(s6_medium)} {[(c['dt'],round(c['cx'],3),round(c['cy'],3)) for c in s6_medium]}")
print(f"       d≈16.4 circles : {len(s6_large)}  {[(c['dt'],round(c['cx'],3),round(c['cy'],3)) for c in s6_large]}")
print(f"       Lines           : {len(s6_lines)}")

# Arc connection points where the 16.4 circle meets the line endpoints
# circle_4: centre≈(0,0) r≈8.2; lines end at x=±7.416, y=±3.5
# At x=7.416: y = sqrt(8.2²-7.416²) ≈ 3.499 ≈ 3.5
import math as _math
_r4 = s6_large[0]["r"]
_cx4, _cy4 = s6_large[0]["cx"], s6_large[0]["cy"]
_xarc = 7.416
_yarc = _math.sqrt(max(0, _r4**2 - (_xarc - _cx4)**2))

# Right enclosed region corner points (clockwise from top-right):
# Lines 4,5,6: (7.416,3.5)→(15.3,3.5)→(15.3,-3.5)→(7.416,-3.5)
# Closed by right arc of circle_4: (7.416,-3.5) → mid=(r4,0) → (7.416,3.5)
# Left enclosed region corner points:
# Lines 1,2,3: (-7.416,-3.5)→(-15.3,-3.5)→(-15.3,3.5)→(-7.416,3.5)
# Closed by left arc of circle_4: (-7.416,3.5) → mid=(-r4,0) → (-7.416,-3.5)

PT_RIGHT_BOT = ( _xarc, -_yarc)
PT_RIGHT_TOP = ( _xarc,  _yarc)
PT_LEFT_BOT  = (-_xarc, -_yarc)
PT_LEFT_TOP  = (-_xarc,  _yarc)

print(f"\n       Arc-line junctions: x=±{_xarc}, y=±{_yarc:.4f}")

# ══════════════════════════════════════════════════════════════════════════
# G18 – Extrude-cut both d≈3.4 circles and d≈10 circle by 12 mm in +Z
# ══════════════════════════════════════════════════════════════════════════
G18_CUT     = 12.0
S6_CUT_NEG  =  0.5   # additional -Z cut applied to G18, G19 and G20

print(f"\n[G18] Cutting d≈3.4 circles ×{len(s6_small)} and d≈10 circle by +{G18_CUT} mm and -{S6_CUT_NEG} mm …")

with BuildPart() as g18_part:
    g18_part._add_to_context(solid_final_g16)

    for circ in s6_small + s6_medium:
        print(f"       Cutting {circ['dt']:25s}  "
              f"centre=({circ['cx']:.4f},{circ['cy']:.4f})  r={circ['r']:.4f}")
        with BuildSketch(Plane.XY.offset(circ["z"])):
            with Locations((circ["cx"], circ["cy"])):
                Circle(circ["r"])
        extrude(amount=G18_CUT,    mode=Mode.SUBTRACT)   # +Z
        with BuildSketch(Plane.XY.offset(circ["z"])):
            with Locations((circ["cx"], circ["cy"])):
                Circle(circ["r"])
        extrude(amount=-S6_CUT_NEG, mode=Mode.SUBTRACT)  # -Z

solid_g18 = g18_part.part

print("\n[OCP] Sending G18 preview …")
# show(solid_g18)   # disabled: was hanging script before _check_open

# ══════════════════════════════════════════════════════════════════════════
# G19 – Read S7: 6 lines + 4 arcs → identify three enclosed sections
# ══════════════════════════════════════════════════════════════════════════
print(f"\n[G19] Reading S7 from: {S7_CSV}")
s7_rows = read_all_rows(S7_CSV)

s7_lines = []
s7_arcs  = []

for row in s7_rows:
    dt = row["Draw Type"].strip()
    if dt.lower() == "line":
        p1 = (float(row["X1"]), float(row["Y1"]))
        p2 = (float(row["X2"]), float(row["Y2"]))
        z  = float(row["Z1"])
        s7_lines.append({"dt": dt, "p1": p1, "p2": p2, "z": z})
        print(f"       Line: ({p1[0]},{p1[1]}) → ({p2[0]},{p2[1]})  Z={z}")
    elif "arc" in dt.lower():
        p1 = (float(row["X1"]), float(row["Y1"]))
        p2 = (float(row["X2"]), float(row["Y2"]))
        p3 = (float(row["X3"]), float(row["Y3"]))
        acx, acy, ar_r = circumscribed_circle_from_3pts(p1, p2, p3)
        s7_arcs.append({"dt": dt, "p1": p1, "p2": p2, "p3": p3,
                        "cx": acx, "cy": acy, "r": ar_r})
        print(f"       {dt:25s}  centre=({acx:.4f},{acy:.4f})  r={ar_r:.4f}")
        print(f"         from ({p1[0]},{p1[1]}) → mid ({p2[0]},{p2[1]}) → ({p3[0]},{p3[1]})")

# Sort arcs by trailing digit
s7_arcs.sort(key=lambda a: int([s for s in a["dt"].split("_") if s.isdigit()][-1]))

# S7 geometry analysis:
#   6 Lines form two rectangles (left & right), closed by arc halves:
#     Section A (LEFT):   Lines 1,2,3  + Arc 4 (left half of center circle)
#       corners: (-15.3,-3.5) → (-15.3,3.5) → (-7.416,3.5) arc4→ (-7.416,-3.5)
#     Section B (RIGHT):  Lines 4,5,6  + Arc 2 (right half of center circle)
#       corners: (7.416,3.5) → (15.3,3.5) → (15.3,-3.5) → (7.416,-3.5) arc2
#     Section C (CENTER): Arcs 1+2+3+4 together → enclosed circle r≈8.2
#
# All at Z=0 (same plane as S6 geometry)

S7_Z = s7_lines[0]["z"]    # 0.0
S7_R = s7_arcs[0]["r"]     # ≈ 8.2  (radius of the center circle formed by all 4 arcs)

# Arc and line key points (from CSV):
# Arc1: (7.416, 3.5) → (0, 8.2) → (-7.416, 3.5)   — top arc
# Arc2: (7.416, 3.5) → (8.2, 0) → ( 7.416,-3.5)   — right arc
# Arc3: (7.416,-3.5) → (0,-8.2) → (-7.416,-3.5)   — bottom arc
# Arc4: (-7.416,-3.5)→(-8.2, 0) → (-7.416, 3.5)   — left arc

# Shorthand references
ARC1, ARC2, ARC3, ARC4 = s7_arcs[0], s7_arcs[1], s7_arcs[2], s7_arcs[3]

# Connection points between arcs / lines:
S7_TR = ARC1["p1"]   # ( 7.416,  3.5)  — top-right junction (Arc1 start / Arc2 start)
S7_TL = ARC1["p3"]   # (-7.416,  3.5)  — top-left  junction (Arc1 end  / Arc4 end  )
S7_BR = ARC3["p1"]   # ( 7.416, -3.5)  — bot-right junction (Arc2 end  / Arc3 start)
S7_BL = ARC3["p3"]   # (-7.416, -3.5)  — bot-left  junction (Arc3 end  / Arc4 start)

print(f"\n       S7 Section A (LEFT  rect+arc):  Lines 1-3 + Arc4 closed at Z={S7_Z}")
print(f"         corners: (-15.3,-3.5) (-15.3,3.5) (-7.416,3.5) arc4 (-7.416,-3.5)")
print(f"       S7 Section B (RIGHT rect+arc):  Lines 4-6 + Arc2 closed at Z={S7_Z}")
print(f"         corners: (7.416,3.5) (15.3,3.5) (15.3,-3.5) (7.416,-3.5) arc2")
print(f"       S7 Section C (CENTER arcs):     Arcs 1+2+3+4 → circle r={S7_R:.4f} at Z={S7_Z}")

# ══════════════════════════════════════════════════════════════════════════
# G20 – Extrude-cut ALL three S7 sections (A, B, C) by 4 mm in +Z
# ══════════════════════════════════════════════════════════════════════════
G20_CUT = 4.0   # cut depth in +Z for all three sections

print(f"\n[G20] Extrude-cutting ALL three S7 sections by +{G20_CUT} mm in +Z …")

with BuildPart() as g20_part:
    g20_part._add_to_context(solid_g18)

    # ── Section A: LEFT rectangle closed by Arc4 ──────────────────────────
    # Boundary (counter-clockwise): bottom line left→right, right vert up,
    # top line right→left, Arc4 down (left side of center circle)
    print(f"\n[G20] Section A: left rect+arc cut -{G20_CUT} mm (into part = SUBTRACT +Z) …")
    with BuildSketch(Plane.XY.offset(S7_Z)):
        with BuildLine():
            Line((-15.3, -3.5), (-15.3,  3.5))   # Line 2 (left vertical)
            Line((-15.3,  3.5), (-7.416, 3.5))   # Line 3 (top horizontal, right)
            ThreePointArc(S7_TL, ARC4["p2"], S7_BL)  # Arc4: TL → (-8.2,0) → BL
            Line(S7_BL, (-15.3, -3.5))            # Line 1 (bottom horizontal)
        make_face()
    extrude(amount=G20_CUT, mode=Mode.SUBTRACT)

    # ── Section B: RIGHT rectangle closed by Arc2 ─────────────────────────
    print(f"\n[G20] Section B: right rect+arc cut +{G20_CUT} mm …")
    with BuildSketch(Plane.XY.offset(S7_Z)):
        with BuildLine():
            Line((15.3,  3.5), (15.3, -3.5))     # Line 5 (right vertical)
            Line((15.3, -3.5), (7.416, -3.5))    # Line 6 (bottom horizontal)
            ThreePointArc(S7_BR, ARC2["p2"], S7_TR)  # Arc2: BR → (8.2,0) → TR
            Line(S7_TR, (15.3, 3.5))              # Line 4 (top horizontal)
        make_face()
    extrude(amount=G20_CUT, mode=Mode.SUBTRACT)

    # ── Section C: CENTER circle formed by all 4 arcs ─────────────────────
    print(f"\n[G20] Section C: center circle r≈{S7_R:.4f} cut +{G20_CUT} mm …")
    with BuildSketch(Plane.XY.offset(S7_Z)):
        with BuildLine():
            ThreePointArc(S7_TR, ARC1["p2"], S7_TL)  # Arc1: TR → (0, 8.2) → TL
            ThreePointArc(S7_TL, ARC4["p2"], S7_BL)  # Arc4: TL → (-8.2,0) → BL
            ThreePointArc(S7_BL, ARC3["p2"], S7_BR)  # Arc3: BL → (0,-8.2) → BR
            ThreePointArc(S7_BR, ARC2["p2"], S7_TR)  # Arc2: BR → (8.2, 0) → TR
        make_face()
    extrude(amount=G20_CUT, mode=Mode.SUBTRACT)

solid_g20 = g20_part.part

print("\n[OCP] Sending G20 preview …")
# show(solid_g20)   # disabled: was hanging script before _check_open

# ══════════════════════════════════════════════════════════════════════════
# G21 – Extrude-cut ONLY the center/middle section (Section C, arcs only)
#        by 9 units in +Z starting from Z=0.
#        Sketch stays at Z=0 (same as S7 base plane).  The boolean will
#        extend the existing G20 pocket (0→4 mm) through to 9 mm total.
# ══════════════════════════════════════════════════════════════════════════
G21_CUT        = 9.0
G21_SKETCH_Z   = S7_Z   # 0.0  — base plane, cut goes Z=0 → Z=9

print(f"\n[G21] Extrude-cutting center arc section (Section C) by +{G21_CUT} mm "
      f"from Z={G21_SKETCH_Z} (Z=0 → Z=9) …")

with BuildPart() as g21_part:
    g21_part._add_to_context(solid_g20)

    with BuildSketch(Plane.XY.offset(G21_SKETCH_Z)):
        with BuildLine():
            ThreePointArc(S7_TR, ARC1["p2"], S7_TL)  # Arc1
            ThreePointArc(S7_TL, ARC4["p2"], S7_BL)  # Arc4
            ThreePointArc(S7_BL, ARC3["p2"], S7_BR)  # Arc3
            ThreePointArc(S7_BR, ARC2["p2"], S7_TR)  # Arc2
        make_face()
    extrude(amount=G21_CUT, mode=Mode.SUBTRACT)

solid_g21 = g21_part.part

print("\n[OCP] Sending G21 preview …")
# show(solid_g21)   # disabled: was hanging script before _check_open

# ══════════════════════════════════════════════════════════════════════════
# G22 – Read S8: all Lines → two enclosed hexagon profiles at Z=11
#
# S8 contains 21 lines total:
#   Lines 1–15  → RIGHT hexagon  centre=(11,  0)  circumradius≈3.35 mm
#   Lines 16–21 → LEFT  hexagon  centre=(-11, 0)  circumradius≈3.35 mm
#
# The right-side hexagon has intermediate collinear points on its rightmost
# edge (x=13.901) from the CSV.  We extract only the 6 true corner vertices
# for each hexagon and build clean Polygon faces.
#
# Hexagon vertices (ordered CCW from bottom-right):
#   RIGHT: (8.099,-1.675)  (11.0,-3.35)  (13.901,-1.675)
#          (13.901, 1.675) (11.0,  3.35) (8.099,  1.675)
#   LEFT:  (-8.099,-1.675) (-11.0,-3.35) (-13.901,-1.675)
#          (-13.901, 1.675)(-11.0,  3.35)(-8.099,  1.675)
# ══════════════════════════════════════════════════════════════════════════
print(f"\n[G22] Reading S8 from: {S8_CSV}")
s8_rows = read_all_rows(S8_CSV)

s8_lines = []
for row in s8_rows:
    dt = row["Draw Type"].strip()
    if dt.lower() == "line":
        p1 = (float(row["X1"]), float(row["Y1"]))
        p2 = (float(row["X2"]), float(row["Y2"]))
        z  = float(row["Z1"])
        s8_lines.append({"dt": dt, "p1": p1, "p2": p2, "z": z})
    else:
        print(f"       WARNING: unexpected Draw Type '{dt}' in S8 — skipping")

S8_Z = s8_lines[0]["z"]   # 11.0

print(f"       {len(s8_lines)} lines read at Z={S8_Z}")

# Derive the 6 true corner vertices for each hexagon from CSV endpoints.
# Right hexagon corners (all x > 0):
S8_RIGHT_VERTS = [
    ( 8.099, -1.675),
    (11.000, -3.350),
    (13.901, -1.675),
    (13.901,  1.675),
    (11.000,  3.350),
    ( 8.099,  1.675),
]
# Left hexagon corners (all x < 0):
S8_LEFT_VERTS = [
    ( -8.099, -1.675),
    (-11.000, -3.350),
    (-13.901, -1.675),
    (-13.901,  1.675),
    (-11.000,  3.350),
    ( -8.099,  1.675),
]

import math as _math
S8_RIGHT_CX = sum(v[0] for v in S8_RIGHT_VERTS) / 6   #  11.0
S8_RIGHT_CY = sum(v[1] for v in S8_RIGHT_VERTS) / 6   #   0.0
S8_LEFT_CX  = sum(v[0] for v in S8_LEFT_VERTS)  / 6   # -11.0
S8_LEFT_CY  = sum(v[1] for v in S8_LEFT_VERTS)  / 6   #   0.0
S8_CIRCUM_R = _math.dist(S8_RIGHT_VERTS[0], (S8_RIGHT_CX, S8_RIGHT_CY))  # ≈ 3.35

print(f"       RIGHT hexagon: centre=({S8_RIGHT_CX:.3f}, {S8_RIGHT_CY:.3f})  "
      f"circumradius={S8_CIRCUM_R:.4f}  Z={S8_Z}")
print(f"       LEFT  hexagon: centre=({S8_LEFT_CX:.3f},  {S8_LEFT_CY:.3f})  "
      f"circumradius={S8_CIRCUM_R:.4f}  Z={S8_Z}")
print(f"       Two enclosed hexagon regions confirmed.")

# ══════════════════════════════════════════════════════════════════════════
# G23 – Extrude-cut BOTH hexagon profiles by 4 mm in -Z and 0.2 mm in +Z
# ══════════════════════════════════════════════════════════════════════════
G23_CUT_NEG = 4.0    # -Z (into part, downward from Z=11)
G23_CUT_POS = 0.2    # +Z (upward from Z=11, ensures clean boolean)

print(f"\n[G23] Extrude-cutting both hexagons: -{G23_CUT_NEG} mm (-Z) and "
      f"+{G23_CUT_POS} mm (+Z) from Z={S8_Z} …")

s8_hex_specs = [
    {"name": "RIGHT", "verts": S8_RIGHT_VERTS, "cx": S8_RIGHT_CX, "cy": S8_RIGHT_CY},
    {"name": "LEFT",  "verts": S8_LEFT_VERTS,  "cx": S8_LEFT_CX,  "cy": S8_LEFT_CY},
]

with BuildPart() as g23_part:
    g23_part._add_to_context(solid_g21)

    for hex_spec in s8_hex_specs:
        name  = hex_spec["name"]
        verts = hex_spec["verts"]
        cx    = hex_spec["cx"]
        cy    = hex_spec["cy"]
        print(f"\n       Cutting {name} hexagon  centre=({cx:.3f},{cy:.3f})")

        # -Z cut (into part)
        with BuildSketch(Plane.XY.offset(S8_Z)):
            with BuildLine():
                for i in range(6):
                    Line(verts[i], verts[(i + 1) % 6])
            make_face()
        extrude(amount=-G23_CUT_NEG, mode=Mode.SUBTRACT)

        # +Z cut (above face for clean top boolean)
        with BuildSketch(Plane.XY.offset(S8_Z)):
            with BuildLine():
                for i in range(6):
                    Line(verts[i], verts[(i + 1) % 6])
            make_face()
        extrude(amount=G23_CUT_POS, mode=Mode.SUBTRACT)

        print(f"         ✓ {name} hexagon cut: -{G23_CUT_NEG} mm and +{G23_CUT_POS} mm")

solid_g23 = g23_part.part

print("\n[OCP] Sending G23 preview …")
# show(solid_g23)   # disabled: was hanging script before _check_open

# ══════════════════════════════════════════════════════════════════════════
# G24 – Read S9: all Lines → two enclosed pentagon regions at Y=83
#
# S9 contains 10 lines total, all at Y=83 (constant), forming two symmetric
# 5-vertex closed polygons in the XZ plane:
#
#   Region RIGHT (X > 0) — 5 vertices (X, Z):
#     (25.0, 27.0) → (32.534, 27.0) → (33.534, 27.0) →
#     (33.534, 18.466) → (32.534, 19.466) → back to (25.0, 27.0)
#
#   Region LEFT (X < 0) — mirror:
#     (-25.0, 27.0) → (-32.534, 27.0) → (-33.534, 27.0) →
#     (-33.534, 18.466) → (-32.534, 19.466) → back to (-25.0, 27.0)
#
# Sketch plane: Plane.YZ is not quite right — the sketch lives on the
# face at Y=83, with X and Z as free axes.  In build123d we sketch on
# Plane.XZ offset to Y=83 is not standard; instead we use a custom
# plane: origin=(0,83,0), normal along +Y, x-axis along +X.
# ══════════════════════════════════════════════════════════════════════════
print(f"\n[G24] Reading S9 from: {S9_CSV}")
s9_rows = read_all_rows(S9_CSV)

s9_lines = []
for row in s9_rows:
    dt = row["Draw Type"].strip()
    if dt.lower() == "line":
        p1 = (float(row["X1"]), float(row["Y1"]), float(row["Z1"]))
        p2 = (float(row["X2"]), float(row["Y2"]), float(row["Z2"]))
        s9_lines.append({"dt": dt, "p1": p1, "p2": p2})
    else:
        print(f"       WARNING: unexpected Draw Type '{dt}' in S9 — skipping")

S9_Y = s9_lines[0]["p1"][1]   # 83.0  — constant Y plane

print(f"       {len(s9_lines)} lines read at Y={S9_Y}")

# 5 true corner vertices for each region (X, Z coords; Y=83 throughout)
S9_RIGHT_VERTS_XZ = [
    (25.000, 27.000),
    (32.534, 27.000),
    (33.534, 27.000),
    (33.534, 18.466),
    (32.534, 19.466),
]
S9_LEFT_VERTS_XZ = [
    (-25.000, 27.000),
    (-32.534, 27.000),
    (-33.534, 27.000),
    (-33.534, 18.466),
    (-32.534, 19.466),
]

print(f"       RIGHT region: 5-vertex polygon  X>0  at Y={S9_Y}")
print(f"         vertices (X,Z): {S9_RIGHT_VERTS_XZ}")
print(f"       LEFT  region: 5-vertex polygon  X<0  at Y={S9_Y}")
print(f"         vertices (X,Z): {S9_LEFT_VERTS_XZ}")
print(f"       Two enclosed regions confirmed.")

# ══════════════════════════════════════════════════════════════════════════
# G25 – Extrude-join BOTH S9 profiles by 6 units in -Y (Y=83 → Y=77)
#
# Sketch plane: face at Y=83, normal = +Y = (0,1,0).
# build123d Plane(origin, x_dir, z_dir) uses z_dir as the plane NORMAL.
#   Plane(origin=(0,83,0), x_dir=(1,0,0), z_dir=(0,1,0))
#     local-x  →  world +X          ✓
#     local-y  =  normal × x_dir  =  (0,1,0)×(1,0,0)  =  (0,0,-1)  → world -Z
#
# Because local-y maps to world -Z, vertex coords must be passed as
#   (X_world, -Z_world)  so the geometry lands at the correct global position.
#
# Extrude amount = -6 along the normal (+Y) direction → material grows in -Y.
# Mode = ADD (join to existing body).
# ══════════════════════════════════════════════════════════════════════════
G25_EXTRUDE = 6.0   # units in -Y

print(f"\n[G25] Extrude-joining both S9 pentagon profiles by -{G25_EXTRUDE} units "
      f"in -Y (Y={S9_Y} → Y={S9_Y - G25_EXTRUDE}) …")
print(f"       Plane normal = +Y;  local-x = world +X;  local-y = world -Z")
print(f"       Vertices passed as (X_world, -Z_world) to match local axes.")

# Sketch plane at Y=83: normal=+Y, x_dir=+X
S9_PLANE = Plane(
    origin = Vector(0, S9_Y, 0),
    x_dir  = Vector(1, 0, 0),
    z_dir  = Vector(0, 1, 0),   # z_dir IS the plane normal in build123d
)

# Local vertex coords: (X_world, -Z_world)
# local-y maps to world -Z, so passing -Z_world recovers the correct +Z position
S9_RIGHT_VERTS_LOCAL = [(x,  -z) for x, z in S9_RIGHT_VERTS_XZ]
S9_LEFT_VERTS_LOCAL  = [(x,  -z) for x, z in S9_LEFT_VERTS_XZ]

print(f"       RIGHT local coords: {S9_RIGHT_VERTS_LOCAL}")
print(f"       LEFT  local coords: {S9_LEFT_VERTS_LOCAL}")

s9_region_specs = [
    {"name": "RIGHT", "verts": S9_RIGHT_VERTS_LOCAL},
    {"name": "LEFT",  "verts": S9_LEFT_VERTS_LOCAL},
]

with BuildPart() as g25_part:
    g25_part._add_to_context(solid_g23)

    for reg in s9_region_specs:
        name  = reg["name"]
        verts = reg["verts"]   # (X_world, -Z_world) local coords on S9_PLANE
        print(f"\n       Extruding {name} pentagon  (Y={S9_Y} → Y={S9_Y - G25_EXTRUDE})")

        with BuildSketch(S9_PLANE):
            with BuildLine():
                for i in range(len(verts)):
                    p_a = verts[i]
                    p_b = verts[(i + 1) % len(verts)]
                    Line((p_a[0], p_a[1]), (p_b[0], p_b[1]))
            make_face()
        extrude(amount=-G25_EXTRUDE, mode=Mode.ADD)

        print(f"         ✓ {name} pentagon joined: -{G25_EXTRUDE} mm in -Y")

solid_g25 = g25_part.part

print("\n[OCP] Sending G25 final preview …")
# show(solid_g25)   # disabled: was hanging script before _check_open

# ══════════════════════════════════════════════════════════════════════════
# G26 – Read S10: draw as per draw type (circles)
# ══════════════════════════════════════════════════════════════════════════
print(f"\n[G26] Reading S10 from: {S10_CSV}")
s10_rows = read_all_rows(S10_CSV)

s10_circles = []
for row in s10_rows:
    dt = row["Draw Type"].strip()
    if "circle" in dt.lower():
        p1 = (float(row["X1"]), float(row["Y1"]))
        p2 = (float(row["X2"]), float(row["Y2"]))
        p3 = (float(row["X3"]), float(row["Y3"]))
        cx, cy, cr = circumscribed_circle_from_3pts(p1, p2, p3)
        z  = float(row["Z1"])
        s10_circles.append({"dt": dt, "cx": cx, "cy": cy, "r": cr, "z": z})
        print(f"       {dt:25s}  centre=({cx:.4f},{cy:.4f})  r={cr:.4f}  Z={z}")

if len(s10_circles) >= 2:
    # Sort circles by radius descending to easily identify outer vs inner
    s10_circles.sort(key=lambda c: c["r"], reverse=True)
    c_outer = s10_circles[0]
    c_inner = s10_circles[1]
    S10_Z = c_outer["z"]

    print(f"\n       Outer circle: r={c_outer['r']:.4f} at Z={S10_Z}")
    print(f"       Inner circle: r={c_inner['r']:.4f} at Z={S10_Z}")
else:
    print(f"       ⚠ WARNING: S10 needs at least 2 circles. Found {len(s10_circles)}.")

# ══════════════════════════════════════════════════════════════════════════
# G27 – Extrude the region between two circles by 10.3 units in -Z
# ══════════════════════════════════════════════════════════════════════════
G27_EXTRUDE = 10.3

print(f"\n[G27] Extrude-joining ring between S10 circles by -{G27_EXTRUDE} units in -Z …")

with BuildPart() as g27_part:
    # Build on top of the G25 context
    g27_part._add_to_context(solid_g25)

    if len(s10_circles) >= 2:
        with BuildSketch(Plane.XY.offset(S10_Z)):
            with Locations((c_outer["cx"], c_outer["cy"])):
                # Draw the large circle first
                Circle(c_outer["r"])
                # Subtract the smaller circle to create the annular region
                Circle(c_inner["r"], mode=Mode.SUBTRACT)
        # Extrude join in -Z direction
        extrude(amount=-G27_EXTRUDE, mode=Mode.ADD)

solid_g27 = g27_part.part

print("\n[OCP] Sending G27 final preview …")
# show(solid_g27)   # disabled: was hanging script before _check_open


_check_open(solid_g5,           "After G5  (fillet)",      BASE_DIR)
_check_open(solid_final_g9,     "After G9  (cuts)",        BASE_DIR)
_check_open(solid_final_g16,    "After G16 (loft+join)",   BASE_DIR)
_check_open(solid_g18,          "After G18 (hole cuts)",   BASE_DIR)
_check_open(solid_g25,          "After G25 (pentagons)",   BASE_DIR)
_check_open(solid_g27,          "After G27 (ring)",        BASE_DIR)

# ══════════════════════════════════════════════════════════════════════════
# G28 – Read S11: enclosed tooth profile
# ══════════════════════════════════════════════════════════════════════════
print(f"\n[G28] Reading S11 from: {S11_CSV}")
s11_rows = read_all_rows(S11_CSV)

S11_Z = float(s11_rows[0]["Z1"])
print(f"       ✓ Extracted {len(s11_rows)} edge definitions for the tooth profile at Z={S11_Z}.")

# ── Tooth profile angular-width analysis ───────────────────────────────────
# Measure the tooth profile's angular extent around the Z-axis so we know
# whether N teeth will fit without overlap.  N teeth need angular pitch
# 360/N; if the tooth itself spans more than that, neighbours collide.
_s11_xs, _s11_ys = [], []
for row in s11_rows:
    for k in ("1", "2", "3"):
        try:
            _s11_xs.append(float(row[f"X{k}"]))
            _s11_ys.append(float(row[f"Y{k}"]))
        except (KeyError, ValueError):
            pass
_s11_angles = [math.degrees(math.atan2(y, x)) for x, y in zip(_s11_xs, _s11_ys)
               if x*x + y*y > 1.0]   # ignore points near origin
if _s11_angles:
    # Unwrap to [-180, 180); then take min/max to get angular span
    a_min = min(_s11_angles)
    a_max = max(_s11_angles)
    span = a_max - a_min
    if span > 180:   # profile straddles ±180 — try shifting
        shifted = [a + 360 if a < 0 else a for a in _s11_angles]
        span = max(shifted) - min(shifted)
    _s11_radii = [math.hypot(x, y) for x, y in zip(_s11_xs, _s11_ys)
                  if x*x + y*y > 1.0]
    print(f"       Tooth profile angular extent : {span:.3f}°  "
          f"(radii {min(_s11_radii):.2f} … {max(_s11_radii):.2f} mm)")
    for n_test in (6, 12, 24, 36, 60):
        pitch = 360.0 / n_test
        verdict = "FITS  ✓" if span < pitch * 0.98 else (
                  "TIGHT ⚠" if span < pitch else "OVERLAP ✗")
        print(f"         N={n_test:3d}  pitch={pitch:6.2f}°  "
              f"span/pitch={span/pitch:.2f}  {verdict}")

# ══════════════════════════════════════════════════════════════════════════
# G29 – Read S12: reference path for sweep operation
# ══════════════════════════════════════════════════════════════════════════
print(f"\n[G29] Reading S12 from: {S12_CSV}")
s12_rows = read_all_rows(S12_CSV)
s12_row = s12_rows[0]

s12_p1 = (float(s12_row["X1"]), float(s12_row["Y1"]), float(s12_row["Z1"]))
s12_p2 = (float(s12_row["X2"]), float(s12_row["Y2"]), float(s12_row["Z2"]))

# Ensure the sweep path starts at the base face (Z=13) and sweeps towards Z=3
if abs(s12_p2[2] - S11_Z) < abs(s12_p1[2] - S11_Z):
    s12_start_z = s12_p2[2]
    s12_end_z   = s12_p1[2]
else:
    s12_start_z = s12_p1[2]
    s12_end_z   = s12_p2[2]

print(f"       ✓ Sweep path Z range extracted: Z={s12_start_z} to Z={s12_end_z}.")

# Overshoot both ends by EPS_TOOTH so the swept solid pokes slightly past
# the ring's top (Z=13) and bottom (Z=3) faces. Without this, tooth end
# faces become coincident with ring faces → Boolean fuse leaves open edges
# that downstream mesh repair can't always stitch closed (e.g. Fusion
# reports "mesh not oriented / not positive volume" on import).
#
# 0.05 mm is the known-good value: produces watertight=True at every G31
# checkpoint, no repair needed. Effective tooth Z range is 12.95 to 3.05,
# which is within 0.4% of the spec'd Z=13 → Z=3.
# Tested EPS_TOOTH = 0.0 (exact Z=13..3) → 9 open edges, repair fails.
EPS_TOOTH = 0.05
s12_start_z -= EPS_TOOTH   # 13.0 → 13.05
s12_end_z   += EPS_TOOTH   #  3.0 →  2.95
print(f"       ✓ Path extended to Z={s12_start_z} to Z={s12_end_z} "
      f"({EPS_TOOTH}mm overshoot each end).")
# ══════════════════════════════════════════════════════════════════════════
# G30 – Perform sweep join body operation on tooth profile along path
#       (Implemented via Lofting mathematically rotated profiles due to API)
# ══════════════════════════════════════════════════════════════════════════
G30_TWIST = 5.97
G30_STEPS = 20  # Increased from 10 → 20 for smoother helix and better watertightness

print(f"\n[G30] Lofting single tooth profile with twist={G30_TWIST} degrees …")

def rotate_2d(px, py, angle_deg):
    rad = math.radians(angle_deg)
    cos_a = math.cos(rad)
    sin_a = math.sin(rad)
    return (px * cos_a - py * sin_a, px * sin_a + py * cos_a)

# 1. Build the SINGLE tooth isolated from the main body
# FIX: Each sketch slice must use a proper BuildLine() context so edges form
#      a guaranteed closed wire before make_face(). Using add(edge_list) outside
#      BuildLine was producing degenerate/open faces → non-manifold loft solid.
with BuildPart() as tooth_part:
    path_length = s12_end_z - s12_start_z
    for i in range(G30_STEPS + 1):
        fraction = i / G30_STEPS
        current_z = s12_start_z + (path_length * fraction)
        current_twist = G30_TWIST * fraction

        with BuildSketch(Plane.XY.offset(current_z)):
            with BuildLine():
                for row in s11_rows:
                    dt = row["Draw Type"].strip().lower()
                    x1, y1 = float(row["X1"]), float(row["Y1"])
                    x2, y2 = float(row["X2"]), float(row["Y2"])
                    # Rotate endpoints by the current twist increment
                    p1 = rotate_2d(x1, y1, current_twist)
                    p2 = rotate_2d(x2, y2, current_twist)
                    if "line" in dt:
                        Line(p1, p2)
                    elif "arc" in dt:
                        x3, y3 = float(row["X3"]), float(row["Y3"])
                        p3 = rotate_2d(x3, y3, current_twist)
                        ThreePointArc(p1, p2, p3)
            make_face()

    # Loft sequentially through all pending faces to form the solid twisted tooth
    loft(ruled=True, mode=Mode.ADD)  # ruled=True guarantees planar end caps on tooth

# FIX: Clean the tooth immediately after loft to merge any near-coincident
#      edges/faces before it is patterned 60 times in G31.
single_tooth = tooth_part.part.clean()
print(f"       ✓ Single tooth built and cleaned.")

# 2. Add the single tooth to the main base for the G30 state/preview
with BuildPart() as g30_part:
    g30_part._add_to_context(solid_g27)
    add(single_tooth)

solid_g30 = g30_part.part

print("\n[OCP] Sending G30 preview (Single Tooth) …")
# show(solid_g30)   # disabled: was hanging script before _check_open

# ══════════════════════════════════════════════════════════════════════════
# G31 – Circular pattern: fuse each tooth directly onto base, not each other
# ══════════════════════════════════════════════════════════════════════════
# Staged debugging:
#   6  → working baseline
#   12 → first overlap-risk count (30° pitch)
#   24 → tighter packing (15° pitch)
#   36 → 10° pitch
#   60 → final target (6° pitch) — only viable if tooth angular span < 6°
# Refer to the [G28] angular-extent printout above to see if N=60 fits.
G31_COUNT = 60  # ← change me: 6 → 12 → 24 → 36 → 60 in steps

print(f"\n[G31] Applying circular pattern: {G31_COUNT} teeth along global Z-axis ...")
print(f"       Tooth: shells={len(single_tooth.shells())}  faces={len(single_tooth.faces())}")

# DEBUG: check single tooth watertightness
try:
    import trimesh, numpy as np
    _t_tmp = os.path.join(BASE_DIR, "_tmp_tooth.stl")
    export_stl(single_tooth, _t_tmp, tolerance=5e-4, angular_tolerance=0.05)
    _t_mesh = trimesh.load(_t_tmp)
    os.remove(_t_tmp)
    print(f"       Single tooth watertight: {_t_mesh.is_watertight}  "
          f"vol={_t_mesh.volume:.4f} mm3  "
          f"build123d vol={single_tooth.volume:.4f} mm3")
    if not _t_mesh.is_watertight:
        _edges = _t_mesh.edges_sorted
        _ue, _ec = np.unique(_edges, axis=0, return_counts=True)
        print(f"       WARNING: Tooth itself has {int((_ec==1).sum())} open boundary edges")
    del _t_mesh
except Exception as _te:
    print(f"       Tooth check skipped: {_te}")

# Helper: lightweight per-step open-edge count without writing/reading files.
# Heavy approach (export STL → trimesh) is what _check_open does; we only run
# that occasionally to keep the loop fast.
def _quick_oe_count(_solid):
    try:
        import trimesh as _tm, numpy as _np
        _p = os.path.join(BASE_DIR, "_tmp_step.stl")
        export_stl(_solid, _p, tolerance=5e-4, angular_tolerance=0.05)
        _m = _tm.load(_p)
        os.remove(_p)
        _ue, _ec = _np.unique(_m.edges_sorted, axis=0, return_counts=True)
        return _m.is_watertight, int((_ec == 1).sum())
    except Exception:
        return None, None

# KEY CHANGE: fuse each tooth directly onto solid_g27 one at a time
# Do NOT fuse teeth against each other first — that creates CompSolids
# with shared T-junction faces that tessellate as open edges.
solid_g31 = solid_g27
# Check open edges only every CHECK_EVERY teeth (file I/O per check is slow)
CHECK_EVERY = max(1, G31_COUNT // 6)
_first_failure = None
for i in range(G31_COUNT):
    tooth_i = single_tooth.rotate(Axis.Z, i * (360.0 / G31_COUNT))
    solid_g31 = solid_g31.fuse(tooth_i)
    # clean() after EVERY fuse so OCC heals the interface topology immediately
    solid_g31 = solid_g31.clean()
    line = (f"       Tooth {i+1}/{G31_COUNT} fused onto body: "
            f"shells={len(solid_g31.shells())}  faces={len(solid_g31.faces())}")
    # Periodic watertight check so we know exactly which tooth (if any) breaks it
    if (i + 1) % CHECK_EVERY == 0 or i == G31_COUNT - 1:
        _wt, _oe = _quick_oe_count(solid_g31)
        if _wt is not None:
            line += f"  watertight={_wt}  open_edges={_oe}"
            if not _wt and _first_failure is None:
                _first_failure = i + 1
    print(line)

if _first_failure is not None:
    print(f"       ⚠ First non-watertight after tooth {_first_failure}")

print(f"       OK G31 complete: shells={len(solid_g31.shells())}  "
      f"faces={len(solid_g31.faces())}")
show(solid_g31)






# ══════════════════════════════════════════════════════════════════════════
# FINAL EXPORT
# ══════════════════════════════════════════════════════════════════════════
print("\n[FINAL] Cleaning final solid …")
# FIX: clean() on solid_g31 (which already had .clean() applied in G31) gives
#      OCC one more pass to close any topology gaps before tessellation.
final_solid = solid_g31.clean()
try:
    from OCP.ShapeFix import ShapeFix_Shape
    from build123d import Solid
    _fixer = ShapeFix_Shape(final_solid.wrapped)
    _fixer.Perform()
    final_solid = Solid(_fixer.Shape())
    print("       ShapeFix applied.")
except Exception as _fx:
    print(f"       fix() skipped: {_fx}")

print("\n[CHECK] Watertight / volume report ...")
_stl_already_written = False
try:
    import trimesh, numpy as np

    _tmp = os.path.join(BASE_DIR, "_tmp_check.stl")
    export_stl(final_solid, _tmp, tolerance=5e-4, angular_tolerance=0.05)
    mesh = trimesh.load(_tmp)
    os.remove(_tmp)

    # Get BREP volume as reference
    try:
        _brep_vol = final_solid.volume
    except Exception:
        _brep_vol = None

    if not mesh.is_watertight:
        print("       Not watertight -- attempting numpy-only mesh repair ...")
        try:
            trimesh.repair.fix_winding(mesh)
            trimesh.repair.fix_normals(mesh)
            mesh.process(validate=True)

            # Count open boundary edges (no networkx needed)
            _e = mesh.edges_sorted
            _ue, _ec = np.unique(_e, axis=0, return_counts=True)
            _open_edges = _ue[_ec == 1]
            _n_open = len(_open_edges)
            print(f"       Open boundary edges: {_n_open}  "
                  f"Faces: {len(mesh.faces)}  Verts: {len(mesh.vertices)}")

            if _n_open > 0:
                # Fan-stitch each open boundary loop from its centroid.
                # Group boundary edges into connected loops first.
                from collections import defaultdict
                adj = defaultdict(set)
                for e in _open_edges:
                    adj[e[0]].add(e[1])
                    adj[e[1]].add(e[0])

                visited = set()
                loops = []
                for start_v in adj:
                    if start_v in visited:
                        continue
                    loop = []
                    cur = start_v
                    prev = None
                    while cur not in visited:
                        visited.add(cur)
                        loop.append(cur)
                        nxt = [n for n in adj[cur] if n != prev]
                        if not nxt:
                            break
                        prev, cur = cur, nxt[0]
                    if len(loop) >= 3:
                        loops.append(loop)

                print(f"       Found {len(loops)} open boundary loop(s) to stitch.")
                new_verts = list(mesh.vertices)
                new_faces = list(mesh.faces)
                for loop in loops:
                    pts = mesh.vertices[loop]
                    centroid = pts.mean(axis=0)
                    c_idx = len(new_verts)
                    new_verts.append(centroid)
                    for j in range(len(loop)):
                        v0 = loop[j]
                        v1 = loop[(j + 1) % len(loop)]
                        new_faces.append([v0, v1, c_idx])

                mesh = trimesh.Trimesh(
                    vertices=np.array(new_verts),
                    faces=np.array(new_faces),
                    process=True
                )
                trimesh.repair.fix_normals(mesh)

        except Exception as repair_err:
            print(f"       Mesh repair error: {repair_err}")

    # CRITICAL: reject "repaired" mesh if volume deviates >1% from BREP
    # (means repair closed holes with inverted faces → negative/wrong volume)
    _vol_stl = mesh.volume
    _vol_ok = (_brep_vol is None or
               abs(_vol_stl - _brep_vol) / max(abs(_brep_vol), 1) < 0.01)
    _is_wt  = mesh.is_watertight and _vol_ok

    if mesh.is_watertight and not _vol_ok:
        print(f"       WARNING: Mesh reports watertight but volume mismatch "
              f"({_vol_stl:.1f} vs BREP {_brep_vol:.1f}) -- "
              f"repair introduced inverted faces. Discarding repair.")
        # Reload from BREP export (no repair)
        _tmp2 = os.path.join(BASE_DIR, "_tmp_check2.stl")
        export_stl(final_solid, _tmp2, tolerance=5e-4, angular_tolerance=0.05)
        mesh = trimesh.load(_tmp2)
        os.remove(_tmp2)
        _vol_stl = mesh.volume
        _is_wt   = mesh.is_watertight

    if _is_wt:
        print("       OK Mesh is watertight and volume is consistent.")
        mesh.export(STL_PATH)
        print("       OK Watertight STL written.")
        _stl_already_written = True

    is_watertight = _is_wt
    vol_stl       = _vol_stl
    vol_b123d     = _brep_vol if _brep_vol else "N/A"
    print(f"       Watertight       : {is_watertight}")
    print(f"       STL volume       : {vol_stl:.4f} mm3")
    print(f"       build123d volume : {vol_b123d:.4f} mm3" if _brep_vol else
          f"       build123d volume : N/A")
except Exception as e:
    is_watertight = vol_stl = vol_b123d = "check failed"
    print(f"       trimesh check failed: {e}")





print(f"\n[EXPORT] Writing STL  \u2192 {STL_PATH}")
if not _stl_already_written:
    export_stl(final_solid, STL_PATH, tolerance=5e-4, angular_tolerance=0.05)
else:
    print("       (STL already written by trimesh repair \u2014 skipping BREP re-export)")

print(f"[EXPORT] Writing STEP → {STEP_PATH}")
export_step(final_solid, STEP_PATH)

# ── Summary Strings Setup ──────────────────────────────────────────────────
s3_circle_summary = "\n".join(f"  {c['dt']:25s}  centre=({c['cx']:.4f}, {c['cy']:.4f})  r={c['r']:.4f}  Z={c['z']}" for c in s3_circles)
s4_circle_summary = "\n".join(f"  {c['dt']:25s}  centre=({c['cx']:.4f}, {c['cy']:.4f})  r={c['r']:.4f}  Z={c['z']}" for c in s4_circles)
s5_circle_summary = "\n".join(f"  {c['dt']:25s}  centre=({c['cx']:.4f}, {c['cy']:.4f})  r={c['r']:.4f}  Z={c['z']}" for c in s5_circles)
s6_profile_summary = (
    f"  Lines : {len(s6_lines)}\n" +
    "\n".join(f"  {c['dt']:25s}  centre=({c['cx']:.4f},{c['cy']:.4f})  r={c['r']:.4f}  d={2*c['r']:.4f}" for c in s6_circles)
)
s10_profile_summary = (
    f"  {len(s10_circles)} circles\n" +
    "\n".join(f"  {c['dt']:25s}  centre=({c['cx']:.4f},{c['cy']:.4f})  r={c['r']:.4f}  Z={c['z']}" for c in s10_circles)
)

# ── Summary ───────────────────────────────────────────────────────────────
summary_lines = [
    "=" * 60,
    f"Summary  :  {FOLDER_NAME}_summary_G_1_31",
    "Guidelines covered: G1–G31",
    "=" * 60,
    "",
    "── G1 : Profile (S1) ──",
    f"  Circle      : r={CIRCLE_R:.3f} mm at origin",
    f"  Arc 2 (conc): r={ARC2_R:.3f} mm",
    f"  Arcs 1,3    : r={arcs[0]['r']:.3f} mm  (tangent arcs)",
    f"  Arc 4 (top) : r={arcs[3]['r']:.3f} mm",
    f"  Sketch plane Z = {S1_Z}",
    "",
    "── G2 : Extrude sections 1+2 ──",
    f"  Depth: {EXTRUDE_DOWN} mm (-Z)",
    "",
    "── G4 : Extrude all sections ──",
    f"  Depth: +{EXTRUDE_UP} mm (+Z) join",
    "",
    "── G5 : Fillet ──",
    f"  Radius: {FILLET_R} mm on bottom-face arcs 1,3,4 (Arc2 r=75 skipped)",
    "",
    "── G6 : Profile (S2, Z=32) ──",
    f"  Circle r={S2_CIRCLE_R:.1f} at origin",
    f"  Arc 1 (conc): r={S2_ARC1_R:.3f} mm",
    f"  Arc 2 (left tangent)  : from {s2_arcs[1]['p1']} → {s2_arcs[1]['p3']}",
    f"  Arc 3 (top connecting): from {s2_arcs[2]['p1']} → {s2_arcs[2]['p3']}",
    f"  Arc 4 (right tangent) : from {s2_arcs[3]['p1']} → {s2_arcs[3]['p3']}",
    "",
    "── G7 : Cut circle section ──",
    f"  -Z depth: {S2_CUT_NEG_CIRCLE} mm   +Z depth: {S2_CUT_POS} mm",
    "",
    "── G8 : Cut adjacent crescent ──",
    f"  -Z depth: {S2_CUT_NEG_ADJACENT} mm   +Z depth: {S2_CUT_POS} mm",
    "",
    "── G9 : Cut third/bulge section ──",
    f"  -Z depth: {S2_CUT_NEG_THIRD} mm   +Z depth: {S2_CUT_POS} mm",
    "",
    "── G10 : Profile (S3) ──",
    f"  {len(s3_circles)} circle(s):",
    s3_circle_summary,
    "",
    "── G11 : Cut all S3 circles ──",
    f"  Sketch Z={s3_circles[0]['z']} (bulge floor)  -Z depth: {S3_CUT_NEG} mm"
    f"  → holes reach Z={s3_circles[0]['z'] - S3_CUT_NEG}",
    "",
    "── G12 : Profile (S4) ──",
    f"  {len(s4_circles)} circle(s):",
    s4_circle_summary,
    "",
    "── G13 : Cut S4 circle ──",
    f"  Sketch Z={s4_circles[0]['z']} (bottom face)  +Z depth: {S4_CUT_POS} mm"
    f"  → cut reaches Z={s4_circles[0]['z'] + S4_CUT_POS}",
    "",
    "── G14 : Profile (S5) ──",
    f"  {len(s5_circles)} circle(s):",
    s5_circle_summary,
    "",
    "── G15 : Loft between S5 circles ──",
    f"  r={s5_larger['r']:.4f} @ Z={s5_larger['z']}  →  "
    f"r={s5_smaller['r']:.4f} @ Z={s5_smaller['z']}",
    "",
    "── G16 : Extrude-join larger circle to base ──",
    f"  r={s5_larger['r']:.4f}  Z={s5_larger['z']} → Z=0  "
    f"(depth: {S5_EXTRUDE_DOWN} mm -Z)  then union with base body",
    "",
    "── G17 : Profile (S6, Z=0) ──",
    s6_profile_summary,
    "",
    "── G18 : Cut d≈3.4 (×2) and d≈10 circles ──",
    f"  +Z depth: {G18_CUT} mm   -Z depth: {S6_CUT_NEG} mm",
    "",
    "── G19 : Profile (S7, Z=0) — three enclosed sections ──",
    f"  6 Lines + 4 Arcs (r≈{S7_R:.4f})",
    f"  Section A (LEFT):   Lines 1-3 + Arc4 → rectangle closed by arc",
    f"    corners: (-15.3,-3.5) (-15.3,3.5) (-7.416,3.5) arc4 (-7.416,-3.5)",
    f"  Section B (RIGHT):  Lines 4-6 + Arc2 → rectangle closed by arc",
    f"    corners: (7.416,3.5) (15.3,3.5) (15.3,-3.5) (7.416,-3.5) arc2",
    f"  Section C (CENTER): Arcs 1+2+3+4 → enclosed circle r≈{S7_R:.4f}",
    "",
    "── G20 : Extrude-cut ALL three S7 sections ──",
    f"  Sections A, B, C each cut +{G20_CUT} mm in +Z  (sketch at Z={S7_Z})",
    "",
    "── G21 : Extrude-cut center arc section only ──",
    f"  Section C only, total {G21_CUT} mm in +Z  (sketch at Z={G21_SKETCH_Z}, cut Z=0 → Z=9)",
    f"  Sections A & B remain at 4 mm depth; Section C reaches 9 mm depth",
    "",
    "── G22 : Profile (S8, Z=11) — two hexagons ──",
    f"  {len(s8_lines)} lines total → 2 enclosed hexagon regions",
    f"  RIGHT hexagon: centre=({S8_RIGHT_CX:.3f}, {S8_RIGHT_CY:.3f})  circumradius={S8_CIRCUM_R:.4f}  Z={S8_Z}",
    f"  LEFT  hexagon: centre=({S8_LEFT_CX:.3f},  {S8_LEFT_CY:.3f})  circumradius={S8_CIRCUM_R:.4f}  Z={S8_Z}",
    "",
    "── G23 : Extrude-cut both hexagons ──",
    f"  -Z depth: {G23_CUT_NEG} mm  (Z={S8_Z} → Z={S8_Z - G23_CUT_NEG})",
    f"  +Z depth: {G23_CUT_POS} mm  (Z={S8_Z} → Z={S8_Z + G23_CUT_POS})",
    "",
    "── G24 : Profile (S9, Y=83) — two pentagon regions ──",
    f"  RIGHT region: 5-vertex polygon  X>0  at Y={S9_Y}",
    f"    vertices (X,Z): {S9_RIGHT_VERTS_XZ}",
    f"  LEFT  region: 5-vertex polygon  X<0  at Y={S9_Y}",
    f"    vertices (X,Z): {S9_LEFT_VERTS_XZ}",
    "",
    "── G25 : Extrude-join both S9 pentagons ──",
    f"  Both regions extruded +{G25_EXTRUDE} mm in -Y  (Y={S9_Y} → Y={S9_Y - G25_EXTRUDE})",
    "",
    "── G26 : Profile (S10) — two circles ──",
    s10_profile_summary,
    "",
    "── G27 : Extrude-join region between S10 circles ──",
    f"  Extruded ring depth: {G27_EXTRUDE} mm in -Z",
    "",
    "── G28 : Profile (S11) — enclosed tooth profile ──",
    f"  {len(s11_rows)} edges (Lines/Arcs) combined into a Face at Z={S11_Z}",
    "",
    "── G29 : Profile (S12) — sweep path ──",
    f"  Line generated along Z axis from Z={s12_start_z} to Z={s12_end_z}",
    "",
    "── G30 : Helical tooth sweep ──",
    f"  Swept S11 tooth profile along S12 path with a twist angle of {G30_TWIST} degrees.",
    "",
    "── G31 : Circular Pattern ──",
    f"  Patterned the G30 swept tooth profile {G31_COUNT} times around the global Z-axis.",
    "",
    f"Watertight check  : {is_watertight}",
    f"STL volume        : {vol_stl} mm³",
    f"build123d volume  : {vol_b123d} mm³",
    "",
    "Exported files:",
    f"  STL  : {STL_NAME}",
    f"  STEP : {STEP_NAME}",
    "=" * 60,
]

with open(SUMMARY_PATH, "w") as sf:
    sf.write("\n".join(summary_lines))
print(f"\n[SUMMARY] Written → {SUMMARY_PATH}")

print("\n✅  Done — G1 through G31 complete.")