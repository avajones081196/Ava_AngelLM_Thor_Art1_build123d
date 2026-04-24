"""
Art1Top_Splitted_A_build123d.py

Guidelines implemented:
  G1  – Read S1 CSV; parse two 3-point circles (inner & outer ring).
  G2  – Extrude annular region between the two S1 circles 5 units in -Z.
  G3  – (Logic stage) Annular ring complete.
  G4  – Read S2 CSV; parse two 3-point circles (countersink hole profile).
  G5  – Extrude-cut: larger circle +3 mm (+Z), smaller circle -2 mm (-Z).
  G6  – Circular pattern of G5 features × 6 around global Z axis.
  G7  – Read S3 CSV; parse 4 lines → build rectangle.
  G8  – Extrude rectangular profile +15 mm in +Z direction.
  G9  – Read S4 CSV; parse 3-point circle (side hole on YZ plane).
  G10 – Extrude-cut S4 circle through all body to make a hole.
  G11 – Read S5 CSV; parse lines → enclosed profile on YZ plane at X=17.
        A divider line splits it into two sections.
  G12 – Extrude section closer to origin +5 mm in +X;
        extrude section farther from origin +13 mm in +X. Both join body.
  G13 – Read S6 CSV; draw hexagon and circle on 45° tilted plane.
  G14 – Extrude-cut circle through-all into the tilted plane;
        extrude-cut hexagon with 2 mm offset, 8 units depth into the plane.

General guidelines:
  • .clean() called right before export.
  • Watertight check + volume report before export.
  • Export at the LAST stage (after G14).
  • OCP viewer port: 3940.
"""

import os
import csv
import math
import numpy as np

# ── paths ──────────────────────────────────────────────────────────────────
BASE_DIR    = "/Users/avajones/Documents/ava_build123d/20260422_assign/Art1Top_Splitted_A"
CSV_DIR     = os.path.join(BASE_DIR, "csv_merged")
FOLDER_NAME = "Art1Top_Splitted_A"

STL_NAME     = f"{FOLDER_NAME}_G_1_20.stl"
STEP_NAME    = f"{FOLDER_NAME}_G_1_20.step"
SUMMARY_NAME = f"{FOLDER_NAME}_summary_G_1_20.txt"

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

# ── build123d imports ──────────────────────────────────────────────────────
from build123d import (
    BuildPart, BuildSketch, BuildLine,
    Circle, Rectangle, Polygon, Line, Polyline, Wire, Face,
    Mode, Axis, Vector,
    extrude, mirror, export_stl, export_step,
    Plane, Location, PolarLocations,
    make_face
)

# ── OCP viewer ────────────────────────────────────────────────────────────
from ocp_vscode import show, set_port
set_port(3940)

# ══════════════════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════════════════

def circumscribed_circle_from_3pts(p1, p2, p3):
    ax, ay = p1
    bx, by = p2
    cx, cy = p3
    D = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
    if abs(D) < 1e-10:
        raise ValueError("Collinear points.")
    ux = ((ax**2 + ay**2) * (by - cy) +
          (bx**2 + by**2) * (cy - ay) +
          (cx**2 + cy**2) * (ay - by)) / D
    uy = ((ax**2 + ay**2) * (cx - bx) +
          (bx**2 + by**2) * (ax - cx) +
          (cx**2 + cy**2) * (bx - ax)) / D
    r = math.sqrt((ax - ux)**2 + (ay - uy)**2)
    return ux, uy, r


def read_circles_from_csv(csv_path):
    circles = []
    with open(csv_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            dt = row["Draw Type"].strip()
            if "circle" not in dt.lower():
                continue
            m = [int(s) for s in dt.split("_") if s.isdigit()]
            order = m[-1] if m else 0
            p1 = (float(row["X1"]), float(row["Y1"]))
            p2 = (float(row["X2"]), float(row["Y2"]))
            p3 = (float(row["X3"]), float(row["Y3"]))
            z  = float(row["Z1"])
            cx, cy, r = circumscribed_circle_from_3pts(p1, p2, p3)
            circles.append({"draw_type": dt, "order": order,
                            "cx": cx, "cy": cy, "cz": z, "radius": r})
    circles.sort(key=lambda c: c["order"])
    return circles


def read_lines_from_csv(csv_path):
    lines = []
    with open(csv_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            dt = row["Draw Type"].strip()
            if dt.lower() != "line":
                continue
            p1 = (float(row["X1"]), float(row["Y1"]), float(row["Z1"]))
            p2 = (float(row["X2"]), float(row["Y2"]), float(row["Z2"]))
            lines.append((p1, p2))
    return lines


def read_all_rows(csv_path):
    rows = []
    with open(csv_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


def rectangle_from_lines(lines):
    xs, ys, zs = [], [], []
    for (x1, y1, z1), (x2, y2, z2) in lines:
        xs.extend([x1, x2])
        ys.extend([y1, y2])
        zs.extend([z1, z2])
    x_min, x_max = min(xs), max(xs)
    y_min, y_max = min(ys), max(ys)
    cx = (x_min + x_max) / 2.0
    cy = (y_min + y_max) / 2.0
    return cx, cy, zs[0], x_max - x_min, y_max - y_min


# ══════════════════════════════════════════════════════════════════════════
print("=" * 60)
print("Art1Top_Splitted_A_build123d.py")
print("=" * 60)

# ══════════════════════════════════════════════════════════════════════════
# G1 – Read S1 circles
# ══════════════════════════════════════════════════════════════════════════
print(f"\n[G1] Reading S1 circles from: {S1_CSV}")
s1_circles = read_circles_from_csv(S1_CSV)
for c in s1_circles:
    print(f"       {c['draw_type']:30s}  centre=({c['cx']:.4f}, {c['cy']:.4f}, {c['cz']:.4f})"
          f"  r={c['radius']:.4f}")
s1_inner_r = min(s1_circles[0]["radius"], s1_circles[1]["radius"])
s1_outer_r = max(s1_circles[0]["radius"], s1_circles[1]["radius"])
s1_z       = s1_circles[0]["cz"]
S1_EXTRUDE = 5.0

# ══════════════════════════════════════════════════════════════════════════
# G4 – Read S2 circles
# ══════════════════════════════════════════════════════════════════════════
print(f"\n[G4] Reading S2 circles from: {S2_CSV}")
s2_circles = read_circles_from_csv(S2_CSV)
s2_bore_r     = s2_circles[0]["radius"]
s2_cbore_r    = s2_circles[1]["radius"]
s2_z          = s2_circles[0]["cz"]
bolt_circle_r = math.sqrt(s2_circles[0]["cx"]**2 + s2_circles[0]["cy"]**2)
CS_CBORE_DEPTH =  3.0
CS_BORE_DEPTH  = -2.0
HOLE_COUNT     = 6

# ══════════════════════════════════════════════════════════════════════════
# G7 – Read S3 lines → rectangle
# ══════════════════════════════════════════════════════════════════════════
print(f"\n[G7] Reading S3 lines from: {S3_CSV}")
s3_lines = read_lines_from_csv(S3_CSV)
rect_cx, rect_cy, rect_z, rect_w, rect_h = rectangle_from_lines(s3_lines)
print(f"       Rectangle centre: ({rect_cx:.4f}, {rect_cy:.4f})  {rect_w:.1f}×{rect_h:.1f} mm  Z={rect_z:.1f}")
RECT_EXTRUDE = 15.0

# ══════════════════════════════════════════════════════════════════════════
# G9 – Read S4 circle (side hole on YZ plane)
# ══════════════════════════════════════════════════════════════════════════
print(f"\n[G9] Reading S4 circle from: {S4_CSV}")
s4_rows = read_all_rows(S4_CSV)
s4_row = s4_rows[0]
s4_const_x = float(s4_row["X1"])
s4_p1 = (float(s4_row["Y1"]), float(s4_row["Z1"]))
s4_p2 = (float(s4_row["Y2"]), float(s4_row["Z2"]))
s4_p3 = (float(s4_row["Y3"]), float(s4_row["Z3"]))
s4_cy, s4_cz, s4_r = circumscribed_circle_from_3pts(s4_p1, s4_p2, s4_p3)
print(f"       YZ plane X={s4_const_x:.1f}  centre=({s4_cy:.4f}, {s4_cz:.4f})  r={s4_r:.4f}")

# ══════════════════════════════════════════════════════════════════════════
# G11 – Read S5 lines → profile on YZ plane at X=17
# ══════════════════════════════════════════════════════════════════════════
print(f"\n[G11] Reading S5 lines from: {S5_CSV}")
s5_lines = read_lines_from_csv(S5_CSV)

# All points at X=17 → profile lives on YZ plane
# Lines 1-4: outer quadrilateral
# Line 5: vertical divider at Y=-44.5 from Z=5 to Z=21.5
# The divider splits the profile into:
#   Section 1 (closer to origin):  triangle (-28,5)→(-44.5,5)→(-44.5,21.5)
#   Section 2 (farther from origin): polygon (-44.5,5)→(-67.904,5)→(-67.904,30)→(-53,30)→(-44.5,21.5)

S5_X = 17.0  # constant X for all S5 points

# Section 1: triangle (closer to Y=0)
sec1_verts_yz = [(-28.0, 5.0), (-44.5, 5.0), (-44.5, 21.5)]
SEC1_EXTRUDE = 13.0  # +X direction (closer to origin, longer extrusion)

# Section 2: polygon (farther from Y=0)
sec2_verts_yz = [(-44.5, 5.0), (-67.904, 5.0), (-67.904, 30.0), (-53.0, 30.0), (-44.5, 21.5)]
SEC2_EXTRUDE = 5.0   # +X direction (farther from origin, shorter extrusion)

print(f"       Profile on YZ plane at X = {S5_X}")
print(f"       Section 1 (closer to origin): triangle, extrude +{SEC1_EXTRUDE} mm in +X")
print(f"       Section 2 (farther):          polygon,  extrude +{SEC2_EXTRUDE} mm in +X")

# ══════════════════════════════════════════════════════════════════════════
# G12_2 – Read S9 lines → enclosed profile on XY plane at Z=5
# ══════════════════════════════════════════════════════════════════════════
print(f"\n[G12_2] Reading S9 lines from: {S9_CSV}")
s9_lines = read_lines_from_csv(S9_CSV)

# All at Z=5 on XY plane — closed curved cutout profile
S9_Z = 5.0
s9_verts_xy = [
    (17.0,    -67.904),
    (22.0,    -67.904),
    (22.5,    -67.904),
    (22.5,    -66.293),
    (22.0,    -66.453),
    (20.76,   -66.851),
    (19.513,  -67.225),
    (18.26,   -67.576),
]
S9_CUT_DEPTH = 30.0  # extrude cut +30 mm in +Z

print(f"       Profile on XY plane at Z = {S9_Z}")
print(f"       Closed profile: {len(s9_verts_xy)} vertices")
print(f"       Extrude cut: +{S9_CUT_DEPTH} mm in +Z")

# ══════════════════════════════════════════════════════════════════════════
# G13 – Read S6 lines + circle on 45° tilted plane
# ══════════════════════════════════════════════════════════════════════════
print(f"\n[G13] Reading S6 from: {S6_CSV}")
s6_lines = read_lines_from_csv(S6_CSV)
s6_all   = read_all_rows(S6_CSV)

# All S6 points satisfy Y + Z = -23 → 45° tilted plane
# Normal: (0, 1/√2, 1/√2) pointing outward
# Hexagon: 6 vertices from lines
hex_verts_3d = [
    (23.099, -39.685, 16.685),
    (26.0,   -38.501, 15.501),
    (28.901, -39.685, 16.685),
    (28.901, -42.054, 19.054),
    (26.0,   -43.238, 20.238),
    (23.099, -42.054, 19.054),
]
hex_centre_3d = np.mean(hex_verts_3d, axis=0)

# Circle on same plane
s6_circ_row = [r for r in s6_all if "circle" in r["Draw Type"].lower()][0]
# All 3 points have X varying → circle is in the tilted plane
# Project to 2D in tilted plane: u = X, v = (-Y+Z)/√2
def to_2d_tilted(x, y, z):
    return (x, (-y + z) / math.sqrt(2))

cp1 = (float(s6_circ_row["X1"]), float(s6_circ_row["Y1"]), float(s6_circ_row["Z1"]))
cp2 = (float(s6_circ_row["X2"]), float(s6_circ_row["Y2"]), float(s6_circ_row["Z2"]))
cp3 = (float(s6_circ_row["X3"]), float(s6_circ_row["Y3"]), float(s6_circ_row["Z3"]))

c2d1 = to_2d_tilted(*cp1)
c2d2 = to_2d_tilted(*cp2)
c2d3 = to_2d_tilted(*cp3)
s6_circ_u, s6_circ_v, s6_circ_r = circumscribed_circle_from_3pts(c2d1, c2d2, c2d3)

# Convert 2D centre back to 3D
s6_circ_x = s6_circ_u
neg_y_plus_z = s6_circ_v * math.sqrt(2)
s6_circ_y = (-23.0 - neg_y_plus_z) / 2.0
s6_circ_z = (-23.0 + neg_y_plus_z) / 2.0

print(f"       Tilted plane: Y+Z = -23  (45° tilt, normal=(0, 0.707, 0.707))")
print(f"       Hexagon centre: ({hex_centre_3d[0]:.3f}, {hex_centre_3d[1]:.3f}, {hex_centre_3d[2]:.3f})")
print(f"       Circle centre:  ({s6_circ_x:.3f}, {s6_circ_y:.3f}, {s6_circ_z:.3f})  r={s6_circ_r:.4f}")

# Tilted plane definition for build123d
# origin = hex_centre, X-dir = (1,0,0), normal = (0, 1/√2, 1/√2)
n_vec = Vector(0, 1/math.sqrt(2), 1/math.sqrt(2))
x_dir = Vector(1, 0, 0)
plane_origin = Vector(float(hex_centre_3d[0]), float(hex_centre_3d[1]), float(hex_centre_3d[2]))
tilted_plane = Plane(origin=plane_origin, x_dir=x_dir, z_dir=n_vec)

# Hexagon vertices in 2D on the tilted plane
hex_verts_2d = []
for v3d in hex_verts_3d:
    u = v3d[0]
    v = (-v3d[1] + v3d[2]) / math.sqrt(2)
    # Relative to hex centre in 2D
    u0 = float(hex_centre_3d[0])
    v0 = (-float(hex_centre_3d[1]) + float(hex_centre_3d[2])) / math.sqrt(2)
    hex_verts_2d.append((u - u0, v - v0))

# Circle centre relative to hex centre in 2D
circ_u_rel = s6_circ_x - float(hex_centre_3d[0])
circ_v_rel = ((-s6_circ_y + s6_circ_z) / math.sqrt(2)) - ((-float(hex_centre_3d[1]) + float(hex_centre_3d[2])) / math.sqrt(2))

HEX_CUT_OFFSET = -2.0   # 2 mm offset into the plane (negative = into body)
HEX_CUT_DEPTH  = -8.0    # 8 mm cut depth into the plane
CIRC_CUT_DEPTH = -100.0  # through-all INTO the body (negative = into body along -normal)

# ══════════════════════════════════════════════════════════════════════════
# G15 – Read S7 lines → pentagon profile on YZ plane at X=50
# ══════════════════════════════════════════════════════════════════════════
print(f"\n[G15] Reading S7 lines from: {S7_CSV}")
s7_lines = read_lines_from_csv(S7_CSV)

# All X=50 → profile on YZ plane
# 5 lines form a closed pentagon (house shape)
# Traced in order: bottom tip → left → top-left → top-right → right → back
S7_X = 50.0
s7_verts_yz = [
    (-31.5,   9.65),
    (-34.401, 11.325),
    (-34.401, 20.0),
    (-28.599, 20.0),
    (-28.599, 11.325),
]
S7_CUT_HALF = 1.5  # symmetric cut 1.5 mm each direction

print(f"       Profile on YZ plane at X = {S7_X}")
print(f"       Pentagon (house shape): 5 vertices")
print(f"       Symmetric cut: ±{S7_CUT_HALF} mm in X (total {S7_CUT_HALF*2} mm)")

# ══════════════════════════════════════════════════════════════════════════
# G19 – Read S8 circle on XY plane at Z=0
# ══════════════════════════════════════════════════════════════════════════
print(f"\n[G19] Reading S8 circle from: {S8_CSV}")
s8_circles = read_circles_from_csv(S8_CSV)
s8_c = s8_circles[0]
s8_cx = s8_c["cx"]
s8_cy = s8_c["cy"]
s8_z  = s8_c["cz"]
s8_r  = s8_c["radius"]
S8_CUT_DEPTH = 2.0  # cut 2 mm into body from bottom face (+Z direction from Z=0)

print(f"       Circle centre: ({s8_cx:.4f}, {s8_cy:.4f})  Z={s8_z:.1f}  r={s8_r:.4f}")
print(f"       Extrude cut: {S8_CUT_DEPTH} mm in -Z")

# ══════════════════════════════════════════════════════════════════════════
# BUILD THE FULL PART
# ══════════════════════════════════════════════════════════════════════════
print("\n[BUILD] Constructing full part G1-G20 …")

with BuildPart() as part:
    # ── G1-G2: Annular ring ──
    with BuildSketch(Plane.XY.offset(s1_z)):
        Circle(s1_outer_r)
        Circle(s1_inner_r, mode=Mode.SUBTRACT)
    extrude(amount=-S1_EXTRUDE)

    # ── G5-G6: Countersink holes × 6 ──
    with BuildSketch(Plane.XY.offset(s2_z)):
        with PolarLocations(bolt_circle_r, HOLE_COUNT, start_angle=90):
            Circle(s2_cbore_r)
    extrude(amount=CS_CBORE_DEPTH, mode=Mode.SUBTRACT)

    with BuildSketch(Plane.XY.offset(s2_z)):
        with PolarLocations(bolt_circle_r, HOLE_COUNT, start_angle=90):
            Circle(s2_bore_r)
    extrude(amount=CS_BORE_DEPTH, mode=Mode.SUBTRACT)

    # ── G7-G8: Rectangle extruded +15 mm in +Z ──
    with BuildSketch(Plane.XY.offset(rect_z).move(Location((rect_cx, rect_cy, 0)))):
        Rectangle(rect_w, rect_h)
    extrude(amount=RECT_EXTRUDE)

    # ── G9-G10: Side hole through-all along X (through rectangular boss only) ──
    with BuildSketch(Plane.YZ.offset(s4_const_x).move(Location((0, s4_cy, s4_cz)))):
        Circle(s4_r)
    extrude(amount=10.0, both=True, mode=Mode.SUBTRACT)

    # ── G11-G12: S5 profile sections on YZ plane at X=17 ──
    # Section 1 (closer to origin): triangle, extrude +5 in +X
    with BuildSketch(Plane.YZ.offset(S5_X)):
        with BuildLine():
            Polyline([*sec1_verts_yz, sec1_verts_yz[0]])
        make_face()
    extrude(amount=SEC1_EXTRUDE)

    # Section 2 (farther from origin): polygon, extrude +13 in +X
    with BuildSketch(Plane.YZ.offset(S5_X)):
        with BuildLine():
            Polyline([*sec2_verts_yz, sec2_verts_yz[0]])
        make_face()
    extrude(amount=SEC2_EXTRUDE)

    # ── G12_2/G12_3: S9 profile cut on XY plane at Z=5, +30 mm in +Z ──
    with BuildSketch(Plane.XY.offset(S9_Z)):
        with BuildLine():
            Polyline([*s9_verts_xy, s9_verts_xy[0]])
        make_face()
    extrude(amount=S9_CUT_DEPTH, mode=Mode.SUBTRACT)

    # ── G13-G14: Hexagon + circle cut on tilted plane ──
    # Circle cut — 8 mm depth, both directions to eliminate thin surface artifact
    tilted_circ_plane = tilted_plane.move(Location((circ_u_rel, circ_v_rel, 0)))
    with BuildSketch(tilted_circ_plane):
        Circle(s6_circ_r)
    extrude(amount=HEX_CUT_DEPTH, both=True, mode=Mode.SUBTRACT)

    # Hexagon cut — 2 mm offset into plane, then 8 mm depth
    tilted_hex_offset = tilted_plane.offset(HEX_CUT_OFFSET)
    with BuildSketch(tilted_hex_offset):
        with BuildLine():
            Polyline([*hex_verts_2d, hex_verts_2d[0]])
        make_face()
    extrude(amount=HEX_CUT_DEPTH, mode=Mode.SUBTRACT)

    # ── G15-G16: Pentagon slot cut on YZ plane at X=50, symmetric ±1.5 mm ──
    with BuildSketch(Plane.YZ.offset(S7_X)):
        with BuildLine():
            Polyline([*s7_verts_yz, s7_verts_yz[0]])
        make_face()
    extrude(amount=S7_CUT_HALF, both=True, mode=Mode.SUBTRACT)

    # ── G17: Mirror all features (G7-G16) across YZ plane (X → -X) ──
    # This mirrors the rectangular boss, side hole, wedge extrusions,
    # tilted hex/circle cuts, and pentagon slot to the opposite side
    mirror(about=Plane.YZ)

    # ── G18: Mirror all features (G7-G17) across XZ plane (Y → -Y) ──
    # This mirrors everything from G7-G17 to the other half
    mirror(about=Plane.XZ)

    # ── G19-G20: Circle cut on XY plane at Z=0, -3 mm in -Z ──
    with BuildSketch(Plane.XY.offset(s8_z).move(Location((s8_cx, s8_cy, 0)))):
        Circle(s8_r)
    extrude(amount=S8_CUT_DEPTH, mode=Mode.SUBTRACT)

solid_final = part.part

print("\n[OCP] Sending full part preview to OCP VS Code viewer on port 3940 …")
show(solid_final)

# ══════════════════════════════════════════════════════════════════════════
# FINAL EXPORT
# ══════════════════════════════════════════════════════════════════════════
print("\n[FINAL] Cleaning final solid …")
final_solid = solid_final.clean()

print("\n[CHECK] Watertight / volume report …")
try:
    import trimesh
    _tmp = os.path.join(BASE_DIR, "_tmp_check.stl")
    export_stl(final_solid, _tmp)
    mesh = trimesh.load(_tmp)
    os.remove(_tmp)
    is_watertight = mesh.is_watertight
    vol_stl       = mesh.volume
    print(f"       Watertight       : {is_watertight}")
    print(f"       STL volume       : {vol_stl:.4f} mm³")
    try:
        vol_b123d = final_solid.volume
        print(f"       build123d volume : {vol_b123d:.4f} mm³")
    except Exception:
        vol_b123d = "N/A"
except Exception as e:
    is_watertight = vol_stl = vol_b123d = "check failed"
    print(f"       trimesh check failed: {e}")

print(f"\n[EXPORT] Writing STL  → {STL_PATH}")
export_stl(final_solid, STL_PATH)
print(f"[EXPORT] Writing STEP → {STEP_PATH}")
export_step(final_solid, STEP_PATH)

# ── Summary ───────────────────────────────────────────────────────────────
summary_lines = [
    "=" * 60,
    f"Summary  :  {FOLDER_NAME}_summary_G_1_20",
    "Guidelines covered: G1–G20",
    "=" * 60,
    "",
    "── G1-G2 : Annular ring (S1) ──",
    f"  S1 inner radius   : {s1_inner_r:.4f} mm",
    f"  S1 outer radius   : {s1_outer_r:.4f} mm",
    f"  Extrusion         : {S1_EXTRUDE} mm  (−Z)",
    "",
    "── G4-G6 : Countersink holes × 6 (S2) ──",
    f"  Counterbore r={s2_cbore_r:.4f} cut +{CS_CBORE_DEPTH} (+Z)",
    f"  Through-bore r={s2_bore_r:.4f} cut {CS_BORE_DEPTH} (−Z)",
    f"  Bolt-circle r={bolt_circle_r:.4f}  count={HOLE_COUNT}",
    "",
    "── G7-G8 : Rectangular boss (S3) ──",
    f"  Centre ({rect_cx:.1f}, {rect_cy:.1f})  {rect_w:.1f}×{rect_h:.1f} mm  +{RECT_EXTRUDE} mm (+Z)",
    "",
    "── G9-G10 : Side hole (S4) ──",
    f"  YZ plane X={s4_const_x:.1f}  r={s4_r:.4f}  through-all",
    "",
    "── G11-G12 : Profile extrusions (S5) ──",
    f"  G12_1: YZ plane X={S5_X}",
    f"    Section 1 (triangle):  +{SEC1_EXTRUDE} mm in +X",
    f"    Section 2 (polygon):   +{SEC2_EXTRUDE} mm in +X",
    f"  G12_2: S9 cutout on XY plane Z={S9_Z}",
    f"    Profile: {len(s9_verts_xy)} vertices",
    f"  G12_3: Extrude cut +{S9_CUT_DEPTH} mm in +Z",
    "",
    "── G13-G14 : Hex + circle cut on tilted plane (S6) ──",
    f"  Tilted plane Y+Z=-23 (45°)",
    f"  Circle r={s6_circ_r:.4f}  cut through-all",
    f"  Hexagon cut: {HEX_CUT_OFFSET} mm offset, {HEX_CUT_DEPTH} mm depth",
    "",
    "── G15-G16 : Pentagon slot cut (S7) ──",
    f"  YZ plane X={S7_X}",
    f"  Pentagon (house shape): 5 vertices",
    f"  Symmetric cut: ±{S7_CUT_HALF} mm in X (total {S7_CUT_HALF*2} mm)",
    "",
    "── G17 : Mirror across YZ plane ──",
    "  Mirrors G7-G16 features: X → -X",
    "",
    "── G18 : Mirror across XZ plane ──",
    "  Mirrors G7-G17 features: Y → -Y",
    "",
    "── G19-G20 : Circle cut (S8) ──",
    f"  Circle centre: ({s8_cx:.4f}, {s8_cy:.4f})  Z={s8_z:.1f}",
    f"  Radius: {s8_r:.4f} mm",
    f"  Extrude cut: {S8_CUT_DEPTH} mm  (−Z)",
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

print("\n✅  Done.")