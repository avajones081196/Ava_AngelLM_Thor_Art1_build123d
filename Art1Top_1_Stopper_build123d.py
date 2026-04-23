"""
Art1Top_1_Stopper_build123d.py

Build the Art1Top_1_Stopper part using build123d.
Reference STL: https://github.com/AngelLM/Thor/blob/main/mods/stl/Art1Top_1_Stopper.stl

S1 CSV geometry (Fusion_Coordinates_S1.csv):
  Row 1 — 3_point_circle_1 : (61.6, 0.0, 6.3), (54.7, 3.984, 6.3), (54.7, -3.984, 6.3)
           → circle centre = (57.175, 0.0, 6.3), radius ≈ 4.425 mm, sketch Z = 6.3
  Row 2 — Line : (61.349, -1.5, 6.3) → (52.651, -1.5, 6.3)  [chord at Y = -1.5]
  Row 3 — Line : (52.651,  1.5, 6.3) → (61.349,  1.5, 6.3)  [chord at Y = +1.5]

Three enclosed regions created by the two parallel chords inside the circle:
  Region A : strip between the two lines  (Y ∈ [-1.5, +1.5] ∩ circle)
  Region B : arc segment above Y = +1.5
  Region C : arc segment below Y = -1.5

Guidelines executed (in logical order):
  G1 : Read S1 CSV → derive circle (centre, radius, Z) and two chord Y-values
       → identify the three enclosed regions A, B, C.
  G2 : Extrude Region A by 1.0 unit in +Z;
       extrude full disc (A+B+C) by 1.2 units in -Z;
       combine into one solid.
  G3 : Clean → watertight check → export STL + STEP → write summary.

Execution order: G1, G2, G3
"""

import os
import csv
import math
from datetime import datetime

from build123d import *
from ocp_vscode import show, set_port

# ── PATHS & NAMING ────────────────────────────────────────────────────────
FOLDER_NAME = "Art1Top_1_Stopper"
BASE_DIR    = f"/Users/avajones/Documents/ava_build123d/20260422_assign/{FOLDER_NAME}"
CSV_DIR     = os.path.join(BASE_DIR, "csv_merged")

G_START   = 1
G_END     = 3
STL_NAME  = f"{FOLDER_NAME}_G_{G_START}_{G_END}.stl"
STEP_NAME = f"{FOLDER_NAME}_G_{G_START}_{G_END}.step"
LOG_NAME  = f"{FOLDER_NAME}_summary_G_{G_START}_{G_END}.txt"


# ════════════════════════════════════════════════════════════════════════════
# CSV READER
# ════════════════════════════════════════════════════════════════════════════

def read_csv(filename):
    filepath = os.path.join(CSV_DIR, filename)
    if not os.path.exists(filepath):
        print(f"⚠️  Warning: {filename} not found at {filepath}")
        return []
    rows = []
    with open(filepath, "r") as f:
        for row in csv.DictReader(f):
            def _f(v):
                v = v.strip()
                return None if v in ("", "NA") else float(v)

            x1, y1, z1 = _f(row["X1"]), _f(row["Y1"]), _f(row["Z1"])
            x2, y2, z2 = _f(row["X2"]), _f(row["Y2"]), _f(row["Z2"])
            x3, y3, z3 = _f(row["X3"]), _f(row["Y3"]), _f(row["Z3"])

            parsed = {
                "draw_type": row["Draw Type"].strip().lower(),
                "p1": (x1, y1, z1) if x1 is not None else None,
                "p2": (x2, y2, z2) if x2 is not None else None,
                "p3": (x3, y3, z3) if x3 is not None else None,
            }
            rows.append(parsed)
    return rows


# ════════════════════════════════════════════════════════════════════════════
# GEOMETRY HELPERS
# ════════════════════════════════════════════════════════════════════════════

def circumscribed_circle_xy(p1, p2, p3):
    """
    Circumscribed circle through three coplanar XY points (same Z).
    Returns (cx, cy, cz, radius).
    """
    ax, ay = p1[0], p1[1]
    bx, by = p2[0], p2[1]
    cx, cy = p3[0], p3[1]
    z      = p1[2]

    D = 2.0 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
    if abs(D) < 1e-12:
        raise ValueError("Three points are collinear – cannot determine circle.")

    ux = ((ax**2 + ay**2) * (by - cy) +
          (bx**2 + by**2) * (cy - ay) +
          (cx**2 + cy**2) * (ay - by)) / D
    uy = ((ax**2 + ay**2) * (cx - bx) +
          (bx**2 + by**2) * (ax - cx) +
          (cx**2 + cy**2) * (bx - ax)) / D

    r = math.sqrt((ux - ax)**2 + (uy - ay)**2)
    return ux, uy, z, r


def get_volume(solid):
    if hasattr(solid, "volume"):
        v = solid.volume
        return v() if callable(v) else v
    elif hasattr(solid, "__iter__"):
        return sum(s.volume for s in solid)
    return 0.0


def watertight_check(solid, log_fn):
    from OCP.BRepBuilderAPI import BRepBuilderAPI_Sewing
    from OCP.TopAbs         import TopAbs_FACE
    from OCP.TopExp         import TopExp_Explorer

    sewer    = BRepBuilderAPI_Sewing(0.01)
    explorer = TopExp_Explorer(solid.wrapped, TopAbs_FACE)
    face_count = 0
    while explorer.More():
        sewer.Add(explorer.Current())
        face_count += 1
        explorer.Next()
    sewer.Perform()
    free_edges = sewer.NbFreeEdges()

    log_fn(f"   Faces in solid : {face_count}")
    log_fn(f"   Free edges     : {free_edges}")
    if free_edges == 0:
        log_fn("   🟢 SUCCESS: Mesh is watertight!")
    else:
        log_fn(f"   🔴 WARNING: {free_edges} free edge(s) — mesh is NOT watertight.")
    return free_edges


# ════════════════════════════════════════════════════════════════════════════
# MAIN
# ════════════════════════════════════════════════════════════════════════════

def main():
    log_lines = []
    ts_start  = datetime.now()

    def log(msg=""):
        print(msg)
        log_lines.append(msg)

    log("=" * 65)
    log(f"  {FOLDER_NAME}_build123d.py")
    log(f"  Started : {ts_start.strftime('%Y-%m-%d %H:%M:%S')}")
    log("=" * 65)

    # ══════════════════════════════════════════════════════════════════════
    # G1 : Read S1 → circle + two chord lines → three regions
    # ══════════════════════════════════════════════════════════════════════
    log("\n-> [G1] Reading S1 (Fusion_Coordinates_S1.csv) ...")
    s1_rows = read_csv("Fusion_Coordinates_S1.csv")

    s1_circles = [r for r in s1_rows if "circle" in r["draw_type"]]
    s1_lines   = [r for r in s1_rows if "line"   in r["draw_type"]]

    if not s1_circles:
        raise RuntimeError("No circle row found in S1 CSV.")
    if len(s1_lines) < 2:
        raise RuntimeError(f"Expected ≥2 line rows in S1 CSV; got {len(s1_lines)}.")

    # ── Circle ────────────────────────────────────────────────────────────
    cr = s1_circles[0]
    cx, cy, cz, radius = circumscribed_circle_xy(cr["p1"], cr["p2"], cr["p3"])
    log(f"   → Circle centre  = ({cx:.4f}, {cy:.4f}, {cz:.4f})")
    log(f"   → Circle radius  = {radius:.4f} mm")
    log(f"   → Sketch plane Z = {cz:.4f} mm")

    # ── Two chord lines ───────────────────────────────────────────────────
    # Both lines are horizontal chords (constant Y per line).
    line_ys = []
    for lr in s1_lines[:2]:
        y_val = lr["p1"][1]   # Y is the same at both endpoints for each line
        line_ys.append(y_val)
        log(f"   → Chord line Y = {y_val:.4f}  "
            f"[({lr['p1'][0]:.3f},{lr['p1'][1]:.3f}) → "
            f"({lr['p2'][0]:.3f},{lr['p2'][1]:.3f})]")

    y_low  = min(line_ys)   # -1.5 — bottom edge of Region A strip
    y_high = max(line_ys)   # +1.5 — top edge of Region A strip

    log(f"   → Region A (strip) : Y ∈ [{y_low:.3f}, {y_high:.3f}] ∩ circle")
    log(f"   → Region B (arc)   : Y > {y_high:.3f} ∩ circle")
    log(f"   → Region C (arc)   : Y < {y_low:.3f} ∩ circle")
    log("--- [G1] Complete ✓ ---")

    # ══════════════════════════════════════════════════════════════════════
    # G2 : Extrusions
    # ══════════════════════════════════════════════════════════════════════
    log("\n-> [G2] Building extrusions ...")

    # The sketch plane sits at the circle centre at Z = cz, normal = +Z.
    sketch_plane = Plane(origin=(cx, cy, cz), z_dir=(0, 0, 1))

    # ── Full disc (Regions A + B + C) extruded 1.2 mm in -Z ───────────────
    log("   → Extruding full disc (A+B+C) by 1.2 mm in -Z ...")
    with BuildPart() as disc_part:
        with BuildSketch(sketch_plane):
            Circle(radius)
        extrude(amount=1.2, dir=(0, 0, -1))

    base_solid = disc_part.part
    log(f"   ✓ Base disc volume = {get_volume(base_solid):.4f} mm³")

    # ── Region A (strip y_low ≤ Y ≤ y_high) extruded 1.0 mm in +Z ────────
    # Strategy: start with a full circle in the sketch, then subtract the
    # two rectangular caps (above y_high and below y_low) to isolate the
    # strip.  The cap rectangles must be in local sketch coordinates
    # (origin = circle centre).
    log(f"   → Extruding Region A (strip Y=[{y_low},{y_high}]) by 1.0 mm in +Z ...")

    # Local y-coordinates relative to circle centre (cy)
    y_low_local  = y_low  - cy   # -1.5 - 0.0 = -1.5
    y_high_local = y_high - cy   # +1.5 - 0.0 = +1.5

    # Height of each cap to remove
    cap_top_h    = radius - y_high_local   # from y_high up to top of circle
    cap_bottom_h = radius + y_low_local    # from y_low down to bottom  (y_low_local is negative, so + gives correct positive height)

    # Width wider than circle diameter to ensure full coverage
    cap_w = 2 * radius + 2.0

    with BuildPart() as strip_part:
        with BuildSketch(sketch_plane):
            Circle(radius)
            # Subtract top cap  (above y_high_local)
            if cap_top_h > 1e-6:
                with Locations((0, y_high_local + cap_top_h / 2, 0)):
                    Rectangle(cap_w, cap_top_h, mode=Mode.SUBTRACT)
            # Subtract bottom cap  (below y_low_local)
            if cap_bottom_h > 1e-6:
                with Locations((0, y_low_local - cap_bottom_h / 2, 0)):
                    Rectangle(cap_w, cap_bottom_h, mode=Mode.SUBTRACT)
        extrude(amount=1.0, dir=(0, 0, 1))

    strip_solid = strip_part.part
    log(f"   ✓ Strip (Region A) volume = {get_volume(strip_solid):.4f} mm³")

    # ── Combine ───────────────────────────────────────────────────────────
    final_solid = base_solid + strip_solid
    log(f"   ✓ Combined solid volume   = {get_volume(final_solid):.4f} mm³")
    log("--- [G2] Complete ✓ ---")

    # ══════════════════════════════════════════════════════════════════════
    # G3 (FINAL): Clean → Watertight check → Export STL/STEP → Summary
    # ══════════════════════════════════════════════════════════════════════
    log(f"\n{'='*65}")
    log("  [G3]  PRE-EXPORT CHECKS & STL/STEP EXPORT")
    log(f"{'='*65}")

    # The magical clean() — removes accumulated geometric scars
    final_solid = final_solid.clean()

    log("\n-> [G3] Watertight check ...")
    free_edges = watertight_check(final_solid, log)

    final_vol = get_volume(final_solid)
    log(f"\n   Final volume = {final_vol:.4f} mm³")

    # ── STL export ────────────────────────────────────────────────────────
    stl_path = os.path.join(BASE_DIR, STL_NAME)
    try:
        export_stl(final_solid, stl_path, tolerance=0.001, angular_tolerance=0.05)
        stl_kb = os.path.getsize(stl_path) / 1024
        log(f"   ✓ STL saved  : {STL_NAME}  ({stl_kb:.1f} KB)")
    except Exception as e:
        log(f"   ❌ STL export failed: {e}")

    # ── STEP export ───────────────────────────────────────────────────────
    step_path = os.path.join(BASE_DIR, STEP_NAME)
    try:
        export_step(final_solid, step_path)
        step_kb = os.path.getsize(step_path) / 1024
        log(f"   ✓ STEP saved : {STEP_NAME}  ({step_kb:.1f} KB)")
    except Exception as e:
        log(f"   ❌ STEP export failed: {e}")

    ts_end  = datetime.now()
    elapsed = (ts_end - ts_start).total_seconds()

    log(f"\n{'='*65}")
    log("  BUILD COMPLETE — G1 through G3")
    log(f"  Finished : {ts_end.strftime('%Y-%m-%d %H:%M:%S')}  ({elapsed:.1f} s)")
    log(f"{'='*65}")

    # ── Write summary ─────────────────────────────────────────────────────
    log_path = os.path.join(BASE_DIR, LOG_NAME)
    try:
        with open(log_path, "w") as f:
            f.write("\n".join(log_lines))
        print(f"\n📄 Summary saved → {LOG_NAME}")
    except Exception as e:
        print(f"❌ Could not save summary: {e}")

    # ── OCP viewer ────────────────────────────────────────────────────────
    print("\nDisplaying in OCP viewer on port 3939 ...")
    set_port(3940)
    show([final_solid], names=[f"{FOLDER_NAME}_G{G_START}-{G_END}"])


if __name__ == "__main__":
    main()