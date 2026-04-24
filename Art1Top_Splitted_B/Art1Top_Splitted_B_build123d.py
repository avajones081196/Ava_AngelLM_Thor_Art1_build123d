"""
Art1Top_Splitted_B_build123d.py

Guidelines implemented:
  G1 – Read S1 CSV; parse three 3-point circles (inner, middle, outer) on one plane.
  G2 – Extrude inner-to-middle annulus -6 mm (-Z) and +7 mm (+Z).
       Extrude inner-to-outer annulus +7 mm (+Z) as join.
  G3 – (Logic stage) Ring complete — no intermediate export.
  G4 – Read S2 CSV; parse one 3-point circle (bolt hole).
  G5 – Extrude-cut the S2 circle 15 mm in Z to make a through-hole.
  G6 – Circular pattern of G5 hole × 6 around global Z axis.

General guidelines:
  • .clean() called right before export.
  • Watertight check + volume report before export.
  • Export at the LAST stage (after G6).
  • OCP viewer port: 3939.
"""

import os
import csv
import math

# ── paths ──────────────────────────────────────────────────────────────────
BASE_DIR    = "/Users/avajones/Documents/ava_build123d/20260422_assign/Art1Top_Splitted_B"
CSV_DIR     = os.path.join(BASE_DIR, "csv_merged")
FOLDER_NAME = "Art1Top_Splitted_B"

STL_NAME     = f"{FOLDER_NAME}_G_1_6.stl"
STEP_NAME    = f"{FOLDER_NAME}_G_1_6.step"
SUMMARY_NAME = f"{FOLDER_NAME}_summary_G_1_6.txt"

STL_PATH     = os.path.join(BASE_DIR, STL_NAME)
STEP_PATH    = os.path.join(BASE_DIR, STEP_NAME)
SUMMARY_PATH = os.path.join(BASE_DIR, SUMMARY_NAME)

S1_CSV = os.path.join(CSV_DIR, "Fusion_Coordinates_S1.csv")
S2_CSV = os.path.join(CSV_DIR, "Fusion_Coordinates_S2.csv")

# ── build123d imports ──────────────────────────────────────────────────────
from build123d import (
    BuildPart, BuildSketch, Circle, Mode,
    extrude, export_stl, export_step, Plane, Location,
    PolarLocations
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


# ══════════════════════════════════════════════════════════════════════════
print("=" * 60)
print("Art1Top_Splitted_B_build123d.py")
print("=" * 60)

# ══════════════════════════════════════════════════════════════════════════
# G1 – Read S1: three circles
# ══════════════════════════════════════════════════════════════════════════
print(f"\n[G1] Reading S1 circles from: {S1_CSV}")
s1_circles = read_circles_from_csv(S1_CSV)

if len(s1_circles) < 3:
    raise RuntimeError(f"Expected 3 circles in S1, found {len(s1_circles)}.")

# Sort by radius to identify inner, middle, outer
s1_sorted = sorted(s1_circles, key=lambda c: c["radius"])
c_inner  = s1_sorted[0]
c_middle = s1_sorted[1]
c_outer  = s1_sorted[2]
s1_z     = c_inner["cz"]

for label, c in [("Inner", c_inner), ("Middle", c_middle), ("Outer", c_outer)]:
    print(f"       {label:8s}: centre=({c['cx']:.4f}, {c['cy']:.4f}, {c['cz']:.4f})  r={c['radius']:.4f}")

print(f"\n       Sketch plane Z : {s1_z:.4f} mm")

# ══════════════════════════════════════════════════════════════════════════
# G2 – Extrude annular regions
# ══════════════════════════════════════════════════════════════════════════
print("\n[G2] Building annular extrusions …")

# Annulus 1: inner-to-middle → -6 mm (-Z) and +7 mm (+Z)
# Annulus 2: inner-to-outer  → +7 mm (+Z) join
# Combined: the middle-to-outer ring only goes +7 in +Z
#           the inner-to-middle ring goes -6 in -Z AND +7 in +Z

INNER_MID_DOWN = -6.0   # inner-to-middle annulus, -Z
INNER_MID_UP   =  7.0   # inner-to-middle annulus, +Z
INNER_OUT_UP   =  7.0   # inner-to-outer annulus, +Z (join)

# ══════════════════════════════════════════════════════════════════════════
# G3 – Ring complete (logic stage)
# ══════════════════════════════════════════════════════════════════════════

# ══════════════════════════════════════════════════════════════════════════
# G4 – Read S2: bolt hole circle
# ══════════════════════════════════════════════════════════════════════════
print(f"\n[G4] Reading S2 circle from: {S2_CSV}")
s2_circles = read_circles_from_csv(S2_CSV)
s2_c = s2_circles[0]
s2_r = s2_c["radius"]
s2_z = s2_c["cz"]
bolt_circle_r = math.sqrt(s2_c["cx"]**2 + s2_c["cy"]**2)

print(f"       Circle centre: ({s2_c['cx']:.4f}, {s2_c['cy']:.4f})  Z={s2_z:.1f}  r={s2_r:.4f}")
print(f"       Bolt-circle radius: {bolt_circle_r:.4f}")

HOLE_DEPTH = 15.0  # through-hole depth in Z
HOLE_COUNT = 6

# Determine start angle from S2 circle position
s2_angle = math.degrees(math.atan2(s2_c["cy"], s2_c["cx"]))
print(f"       Start angle: {s2_angle:.1f}°")

# ══════════════════════════════════════════════════════════════════════════
# BUILD THE FULL PART
# ══════════════════════════════════════════════════════════════════════════
print("\n[BUILD] Constructing full part G1-G6 …")

with BuildPart() as part:
    # ── G2: Inner-to-middle annulus: -6 in -Z ──
    with BuildSketch(Plane.XY.offset(s1_z)):
        Circle(c_middle["radius"])
        Circle(c_inner["radius"], mode=Mode.SUBTRACT)
    extrude(amount=INNER_MID_DOWN)

    # ── G2: Inner-to-middle annulus: +7 in +Z ──
    with BuildSketch(Plane.XY.offset(s1_z)):
        Circle(c_middle["radius"])
        Circle(c_inner["radius"], mode=Mode.SUBTRACT)
    extrude(amount=INNER_MID_UP)

    # ── G2: Inner-to-outer annulus: +7 in +Z (join) ──
    with BuildSketch(Plane.XY.offset(s1_z)):
        Circle(c_outer["radius"])
        Circle(c_inner["radius"], mode=Mode.SUBTRACT)
    extrude(amount=INNER_OUT_UP)

    # ── G5-G6: Bolt holes × 6 ──
    with BuildSketch(Plane.XY.offset(s2_z)):
        with PolarLocations(bolt_circle_r, HOLE_COUNT, start_angle=s2_angle):
            Circle(s2_r)
    extrude(amount=HOLE_DEPTH, both=True, mode=Mode.SUBTRACT)

solid_final = part.part

print("\n[OCP] Sending preview to OCP VS Code viewer on port 3939 …")
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
    f"Summary  :  {FOLDER_NAME}_summary_G_1_6",
    "Guidelines covered: G1–G6",
    "=" * 60,
    "",
    "── G1-G2 : Annular ring (S1, 3 circles) ──",
    f"  Inner radius    : {c_inner['radius']:.4f} mm",
    f"  Middle radius   : {c_middle['radius']:.4f} mm",
    f"  Outer radius    : {c_outer['radius']:.4f} mm",
    f"  Sketch plane Z  : {s1_z:.4f} mm",
    f"  Inner-to-middle : {INNER_MID_DOWN} mm (-Z), +{INNER_MID_UP} mm (+Z)",
    f"  Inner-to-outer  : +{INNER_OUT_UP} mm (+Z) join",
    "",
    "── G4-G6 : Bolt holes × 6 (S2) ──",
    f"  Hole radius      : {s2_r:.4f} mm",
    f"  Bolt-circle r    : {bolt_circle_r:.4f} mm",
    f"  Hole depth       : {HOLE_DEPTH} mm (both directions)",
    f"  Hole count       : {HOLE_COUNT}",
    f"  Start angle      : {s2_angle:.1f}°",
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