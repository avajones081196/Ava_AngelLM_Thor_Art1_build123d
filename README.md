# Ava_AngelLM_Thor_Art1_build123d

> **Reconstructing the [AngelLM Thor open-source robot arm](https://github.com/AngelLM/Thor) parts from scratch using [build123d](https://github.com/gumyr/build123d) — with automated STL comparison against the original Fusion 360 exports.**

---

## 🤖 What is This Project?

[Thor](https://github.com/AngelLM/Thor) is a fully open-source, 3D-printable robotic arm designed by AngelLM. This project takes each Thor part and **reconstructs it programmatically** using Python + build123d, driven entirely by coordinate data exported from Fusion 360.

The goal: prove that every part can be rebuilt to **near-perfect geometric accuracy** from first principles — no manual CAD, no guesswork.

---

## ✅ Parts Completed

| # | Part | Volume (mm³) | Vol Error | Sym Diff | Overlap | Bounding Box | Time | Rating |
|---|------|-------------|-----------|----------|---------|-------------|------|--------|
| 1 | `Art1Top_1_Stopper` | 106.87 | 0.008% | 0.009% | 99.999% | ✅ PASS | 1 hr | 🟢 EXCELLENT |
| 2 | `Art1Top_Splitted_A` | 107,906.06 | 0.023% | 0.030% | 99.973% | ✅ PASS | 3.5 hrs | 🟢 EXCELLENT |
| 3 | `Art1Top_Splitted_B` | 45,416.29 | 0.030% | 0.065% | 99.952% | ✅ PASS | 40 min | 🟢 EXCELLENT |
| 4 | `Art2BodyA_Splitted_A` | 102,778.90 | 0.199% | 0.579% | 99.613% | ✅ PASS | 17 hrs | 🟢 EXCELLENT |
| 5 | `Art2BodyA_Splitted_B` | — | — | — | — | — | 🔧 in progress | — |

> **All 4 completed parts: 🟢 EXCELLENT across every metric.**

⏱ **Total time: 22 hrs 10 min**

---

## 📊 Art2BodyA_Splitted_A — Detailed Results

### What the part looks like

The most complex part yet — a stepped teardrop body with a **60-tooth helical gear ring**:

- **Stepped teardrop base**: sections 1+2 (circle + crescent) span Z=0..32; section 3 (bulge) sits on top from Z=5..32
- **Multi-depth pockets** on top face (sections cut to depths -29, -19, -22 mm)
- **4 small bores** (Ø3.4 mm) in bulge floor; central counterbore (Ø10 mm) and through-bore (Ø16.4 mm) clusters
- **Two hexagonal recesses** at Z=11 (circumradius ≈ 3.35 mm)
- **Truncated cone boss** (loft from r=18 @ Z=5 to r=12 @ Z=11), extruded to base
- **Two pentagonal extrusions** on the YZ side face at Y=83 (joined by 6 mm in -Y)
- **60-tooth helical gear ring**: each tooth swept along Z=13→Z=3 with 5.97° twist, patterned around global Z-axis (radial range r=57.5 → 62.92 mm)

### Guidelines breakdown (31 guidelines, G1–G31)

| Guideline | Description | CSV |
|-----------|-------------|-----|
| G1 | Read S1; sketch circle + 4 arcs at Z=32 → 3 enclosed sections | S1 |
| G2 + G4 | **Stepped teardrop via cut-first**: full silhouette extrude Z=32→0, then Boolean cut for bulge below Z=5 | S1 |
| G3 | (Logic stage) Base complete | — |
| G5 | Fillet bottom-face arcs r=5 mm (skip Arc 2 r=75) | — |
| G6–G9 | S2 cuts on top face (circle / crescent / bulge: -29 / -19 / -22 mm) | S2 |
| G10–G11 | 4 small bores in bulge floor (-6 mm) | S3 |
| G12–G13 | S4 single circle from bottom face (+1.1 mm) | S4 |
| G14–G16 | S5 loft + extrude-join (truncated cone) | S5 |
| G17–G18 | S6 holes & slot cluster on bottom face | S6 |
| G19–G21 | S7 three sections, two depths (4 mm and 9 mm) | S7 |
| G22–G23 | S8 two hexagon recesses at Z=11 | S8 |
| G24–G25 | S9 two pentagon extrude-joins on YZ plane | S9 |
| G26–G27 | S10 ring extrude-join (Z=13 → Z=2.7) | S10 |
| G28–G29 | S11 tooth profile + S12 sweep path | S11, S12 |
| G30 | Helical tooth via 21-slice rotated loft (twist +5.97°) | — |
| G31 | Circular pattern × 60 around global Z-axis | — |

### Comparison scorecard

```
███████████████████████████████████████████████████████████
  STL COMPARISON: Build123d  vs  Fusion 360 Original
███████████████████████████████████████████████████████████

  Build123d volume    : 102,778.90 mm³
  Fusion 360 volume   : 102,979.85 mm³
  Absolute difference :    -204.77 mm³
  % error             :     0.199%      🟢 EXCELLENT

  Symmetric diff      :     596.42 mm³
  Sym diff %          :     0.579%      🟢 EXCELLENT
  Overlap coverage    :    99.613%      🟢 EXCELLENT

  Bounding box        : ✅ ALL 6 AXES PASS  (max deviation 0.010 mm)

  ─────────────────────────────────────────────────────────
  SUMMARY SCORECARD
  ─────────────────────────────────────────────────────────
  Volume % error          0.199%   🟢 EXCELLENT
  Symmetric diff % error  0.579%   🟢 EXCELLENT
  Overlap coverage       99.61%    🟢 EXCELLENT
  Bounding box             PASS    ✅
```

### Lessons learned (the 17-hour debug arc)

This part exposed several Boolean-kernel pitfalls that the simpler Art1 parts didn't hit. The key fixes — written up as universal rules in [`build123d_short_prompts.md`](./build123d_short_prompts.md) — are:

1. **Never share a sketch curve between two extrudes that get fused.** G2 + G4 originally extruded sections 1+2 and all-3-sections separately, both containing Arc 2 in their sketches. The fuse left Arc 2 as an internal seam → 14 open edges. **Fix**: build the full outer silhouette in one extrude, then Boolean-cut the bulge below Z=5.
2. **Avoid coincident faces between cutter and host.** First cut attempt produced 1483 open edges because the cutter's side walls (Arcs 3, 4, 1) sat exactly coincident with the host's outer walls. **Fix**: replace those arcs with a generous bounding rectangle that lies entirely outside the host. Boolean only acts where they overlap, so the rectangle's overhang is geometrically free.
3. **Z-inset for swept teeth.** Tooth path of exact Z=13→Z=3 produced 9 open edges where tooth end-faces coincided with the ring's top/bottom faces. **Fix**: shrink path 0.05 mm at each end (Z=12.95 → Z=3.05). Each tooth ends 0.05 mm *inside* the ring at top and bottom — invisible because the ring's flat top/bottom faces project over those gaps, and the Boolean fuse is now isolated from coincident-face conflicts.
4. **Three-gate STL validator before export.** trimesh's `is_watertight=True` does NOT guarantee Fusion will accept the STL — Fusion also checks face-orientation consistency and positive signed volume. **Fix**: always run `trimesh.repair.fix_winding()` + `fix_normals()` before export, then gate on three checks: watertight + positive volume + volume matches BREP within 1%.

---

## 📊 Art1Top_Splitted_B — Detailed Results

### What the part looks like

A stepped annular ring with three concentric circles defining two regions:

- **Inner ring** (r25→r35): extends both upward (+7 mm) and downward (-6 mm) from the sketch plane
- **Outer flange** (r25→r47): extends upward (+7 mm) only
- **6 bolt holes** (r≈1.7 mm) on a 30 mm bolt circle, evenly spaced

### Guidelines breakdown (6 guidelines, G1–G6)

| Guideline | Description | CSV |
|-----------|-------------|-----|
| G1 | Read 3 concentric circles (inner r=25, middle r=35, outer r=47) | S1 |
| G2 | Extrude inner-to-middle -6 mm (-Z) and +7 mm (+Z); inner-to-outer +7 mm (+Z) join | S1 |
| G3 | (Logic stage) Ring complete | — |
| G4 | Read bolt hole circle (r≈1.7 mm at radius 30 mm) | S2 |
| G5 | Extrude-cut hole 15 mm through-all | S2 |
| G6 | Circular pattern × 6 around global Z axis | — |

### Comparison scorecard

```
███████████████████████████████████████████████████████████
  STL COMPARISON: Build123d  vs  Fusion 360 Original
███████████████████████████████████████████████████████████

  Build123d volume    : 45,416.29 mm³
  Fusion 360 volume   : 45,429.81 mm³
  Absolute difference :    −13.52 mm³
  % error             :     0.030%      🟢 EXCELLENT

  Symmetric diff      :     29.74 mm³
  Sym diff %          :     0.065%      🟢 EXCELLENT
  Overlap coverage    :    99.952%      🟢 EXCELLENT

  Bounding box        : ✅ ALL 6 AXES PASS  (max deviation 0.015 mm)

  ─────────────────────────────────────────────────────────
  SUMMARY SCORECARD
  ─────────────────────────────────────────────────────────
  Volume % error          0.030%   🟢 EXCELLENT
  Symmetric diff % error  0.065%   🟢 EXCELLENT
  Overlap coverage       99.95%    🟢 EXCELLENT
  Bounding box             PASS    ✅
```

---

## 📊 Art1Top_Splitted_A — Detailed Results

### What the part looks like

A large annular disc (inner radius 25 mm, outer radius 75 mm) with multiple features:

- **6 countersink holes** on a 30 mm bolt circle (counterbore + through-bore)
- **4 rectangular bosses** with side holes, pentagon slots, and wedge extrusions (mirrored in 4 quadrants)
- **Tilted hex + circle cuts** on 45° angled faces
- **Curved cutout profiles** at wedge bases
- **Bottom-face pocket** (circle cut from Z=0)

### Guidelines breakdown (20 guidelines, G1–G20)

| Guideline | Description | CSV |
|-----------|-------------|-----|
| G1–G3 | Annular ring (inner/outer circles, extrude −5 mm) | S1 |
| G4–G6 | Countersink holes × 6 (counterbore +3, through-bore −2, circular pattern) | S2 |
| G7–G8 | Rectangular boss (10×23 mm, extrude +15 mm) | S3 |
| G9–G10 | Side hole through rectangular boss | S4 |
| G11–G12_1 | Wedge profile extrusions (triangle +13, polygon +5) | S5 |
| G12_2–G12_3 | Curved cutout at wedge base (+30 mm cut) | S9 |
| G13–G14 | Hexagon + circle cut on 45° tilted plane | S6 |
| G15–G16 | Pentagon slot cut (±1.5 mm symmetric) | S7 |
| G17 | Mirror G7–G16 across YZ plane (X → −X) | — |
| G18 | Mirror G7–G17 across XZ plane (Y → −Y) | — |
| G19–G20 | Bottom-face circle pocket (r=5 mm, 2 mm deep) | S8 |

### Comparison scorecard

```
  Build123d volume    : 107,906.06 mm³
  Fusion 360 volume   : 107,931.29 mm³
  % error             :     0.023%      🟢 EXCELLENT

  Symmetric diff %    :     0.030%      🟢 EXCELLENT
  Overlap coverage    :    99.973%      🟢 EXCELLENT
  Bounding box        : ✅ ALL 6 AXES PASS
```

---

## 📊 Art1Top_1_Stopper — Detailed Results

### What the part looks like

A circular disc (radius ≈ 4.4 mm) with a raised central strip — two parallel chord lines inside the circle divide it into three regions:

```
        ╭─────────────────╮
        │   Region B (arc)│   ← flat
        ├─────────────────┤   ← chord at Y = +1.5
        │   Region A      │   ← raised +1.0 mm (the "stopper" ridge)
        ├─────────────────┤   ← chord at Y = -1.5
        │   Region C (arc)│   ← flat
        ╰─────────────────╯
```

### Comparison scorecard

```
  Build123d volume    : 106.87 mm³
  Fusion 360 volume   : 106.86 mm³
  % error             :   0.008%       🟢 EXCELLENT

  Symmetric diff %    :   0.009%       🟢 EXCELLENT
  Overlap coverage    :  99.999%       🟢 EXCELLENT
  Bounding box        : ✅ ALL 6 AXES PASS
```

---

## 🗂️ Project Structure

Each part lives in its own folder under `20260422_assign/`:

```
20260422_assign/
├── Art1Top_1_Stopper/
│   ├── csv_data_Art1Top_1_Stopper/
│   ├── csv_merged/
│   ├── 0_preprocess_csvs.py
│   ├── Art1Top_1_Stopper_build123d.py
│   ├── Art1Top_1_Stopper_compare_stl_files.py
│   ├── Art1Top_1_Stopper_G_1_3.stl
│   ├── Art1Top_1_Stopper_G_1_3.step
│   └── Art1Top_1_Stopper_original.stl
│
├── Art1Top_Splitted_A/
│   ├── csv_data_Art1Top_Splitted_A/
│   ├── csv_merged/                        ← S1–S9 cleaned CSVs
│   ├── 0_preprocess_csvs.py
│   ├── Art1Top_Splitted_A_build123d.py    ← 20 guidelines (G1–G20)
│   ├── Art1Top_Splitted_A_compare_stl_files.py
│   ├── Art1Top_Splitted_A_G_1_20.stl
│   ├── Art1Top_Splitted_A_G_1_20.step
│   └── Art1Top_Splitted_A_original.stl
│
├── Art1Top_Splitted_B/
│   ├── csv_data_Art1Top_Splitted_B/
│   ├── csv_merged/                        ← S1–S2 cleaned CSVs
│   ├── 0_preprocess_csvs.py
│   ├── Art1Top_Splitted_B_build123d.py    ← 6 guidelines (G1–G6)
│   ├── Art1Top_Splitted_B_compare_stl_files.py
│   ├── Art1Top_Splitted_B_G_1_6.stl
│   ├── Art1Top_Splitted_B_G_1_6.step
│   └── Art1Top_Splitted_B_original.stl
│
└── Art2BodyA_Splitted_A/
│   ├── csv_data_Art2BodyA_Splitted_A/
│   ├── csv_merged/                        ← S1–S12 cleaned CSVs
│   ├── 0_preprocess_csvs.py
│   ├── Art2BodyA_Splitted_A_build123d.py  ← 31 guidelines (G1–G31)
│   ├── Art2BodyA_Splitted_A_compare_stl_files.py
│   ├── Art2BodyA_Splitted_A_G_1_31.stl
│   ├── Art2BodyA_Splitted_A_G_1_31.step
│   └── Art2BodyA_Splitted_A_original.stl
│
└── Art2BodyA_Splitted_B/                 ← 🔧 in progress
    └── Art2BodyA_Splitted_B_original.stl  (reference from Thor repo)
```

---

## 🔧 How It Works

### The Pipeline (3 scripts per part)

```
Raw Fusion CSVs
      ↓
[0_preprocess_csvs.py]     → cleans duplicates, merges split files → csv_merged/
      ↓
[PartName_build123d.py]    → reads CSVs, builds 3D geometry, exports STL + STEP
      ↓
[PartName_compare_stl_files.py]  → compares built STL vs Fusion original
```

---

### Script 1 — `0_preprocess_csvs.py`

Reads raw Fusion 360 coordinate CSVs and produces clean, deduplicated versions:

- Handles split files (e.g. `S25_1.csv + S25_2.csv → S25.csv`)
- Removes geometry-aware duplicates:
  - Lines: `A→B == B→A` (direction-invariant)
  - Triangles: `A,B,C == B,C,A` (rotation-invariant)
  - Points: exact match
- Renumbers `Steps` column sequentially
- **Incremental** — skips shapes already in `csv_merged/` (safe to re-run)

---

### Script 2 — `PartName_build123d.py`

Rebuilds the part using [build123d](https://github.com/gumyr/build123d). Each script follows a numbered guideline system:

| Guideline | Always means |
|-----------|-------------|
| **G1** | Read CSV(s), extract geometry (circles, lines, polygons) |
| **G2–Gn** | Perform extrusions, cuts, sweeps, patterns, mirrors etc. |
| **Last G** | Always last — `clean()` → watertight check → export STL + STEP → write summary |

**File naming convention:**
```
PartName_G_1_N.stl          ← STL output  (N = last guideline number)
PartName_G_1_N.step         ← STEP output
PartName_summary_G_1_N.txt  ← Build log
```

**Pre-export validator (since Art2BodyA_Splitted_A)** — replaces the simple watertight check, gates on three conditions:

```python
trimesh.repair.fix_winding(mesh)   # consistent CCW winding
trimesh.repair.fix_normals(mesh)   # outward-pointing normals

wt      = mesh.is_watertight
pos_vol = mesh.volume > 0
vol_ok  = abs(mesh.volume - brep_vol) / abs(brep_vol) < 0.01

if wt and pos_vol and vol_ok:
    mesh.export(STL_PATH)          # ship validated mesh
```

This eliminates the *"mesh not oriented / not positive volume"* error Fusion would intermittently throw on import — Fusion checks face orientation in addition to manifoldness, and `is_watertight=True` alone doesn't guarantee that.

---

### Script 3 — `PartName_compare_stl_files.py`

Compares the built STL against the original Fusion 360 STL across four metrics:

| Metric | What it measures |
|--------|-----------------|
| **Volume % error** | How close the total volume is |
| **Symmetric difference** | Spatial overlap quality — how well the shapes align in 3D space |
| **Overlap coverage** | What % of the original is covered by the reconstruction |
| **Bounding box** | Whether all 6 axis extents match within ±0.1 mm |

Ratings: 🟢 EXCELLENT / 🟡 GOOD / 🟠 ACCEPTABLE / 🔴 POOR

---

## 🛠️ Environment Setup

### Requirements

- Python 3.11
- macOS (tested on MacBook Air, Apple Silicon)
- VS Code + [OCP CAD Viewer extension](https://github.com/bernhard-42/vscode-ocp-cad-viewer)

### Create the master environment

```bash
python3.11 -m venv ~/Documents/ava_build123d/build123d_master_env
source ~/Documents/ava_build123d/build123d_master_env/bin/activate
pip install --upgrade pip
pip install build123d==0.7.0 ocp_vscode==3.3.4 numpy-stl trimesh manifold3d rtree networkx
```

> `networkx` is optional — used by trimesh for boundary-loop stitching during mesh repair. Recommended.

### Add a handy shell alias (optional but recommended)

```bash
echo 'alias buildenv="source ~/Documents/ava_build123d/build123d_master_env/bin/activate"' >> ~/.zshrc
source ~/.zshrc
```

Now you can just type `buildenv` to activate.

---

## 🚀 Running a Part (Master Startup Checklist)

### 🔧 One-Time Per Project Folder

1. **Open project folder** in VS Code: `File` → `Open Folder`
2. **Lock the interpreter:**
   ```bash
   mkdir -p .vscode && cat > .vscode/settings.json << 'EOF'
   {
       "python.defaultInterpreterPath": "/Users/avajones/Documents/ava_build123d/build123d_master_env/bin/python"
   }
   EOF
   ```

### ▶️ Every Session

3. **Open OCP viewer:** `Cmd+Shift+P` → `OCP CAD Viewer: Open Viewer`
   - If interpreter prompt appears → click `yes` → pick `build123d_master_env`
4. **Check port:** read bottom-right corner `OCP: XXXX` — match in script's `set_port(XXXX)`
5. **Tab 2 — run scripts:**
   ```bash
   buildenv
   cd ~/Documents/ava_build123d/20260422_assign/PartName
   python 0_preprocess_csvs.py
   python PartName_build123d.py
   python PartName_compare_stl_files.py
   ```

> **Port note:** The OCP viewer port varies per session. Always check `OCP: XXXX` in the bottom-right corner of VS Code and match `set_port()` accordingly.

---

## 🐛 Known Gotchas

| Issue | Cause | Fix |
|-------|-------|-----|
| `Connection refused Errno 61` | OCP server not running | Open OCP viewer panel before running script |
| Geometry not showing | Script port ≠ viewer port | Match `set_port()` to bottom-right `OCP: XXXX` |
| Script runs old version | Unsaved file (● dot on tab) | `Cmd+S` — confirm dot disappears |
| `No module named ocp_vscode` | VS Code using wrong Python | Run `.vscode/settings.json` fix once per folder |
| `Location()` on `Plane.YZ` misplaced | `Location` uses **global** coords, not local | Use `Location((0, Y, Z))` not `Location((Y, Z, 0))` |
| Thin surface artifact on cuts | Sketch plane sits exactly on body face | Use `both=True` to cut in both directions |
| `Location` context manager error | `with Location(...)` not supported | Use `Plane.move(Location(...))` instead |
| `open_edges = 14` after fuse | Two extrudes share a sketch curve → internal seam | Single outer-silhouette extrude + Boolean cut |
| `open_edges` = 1000+ after cut | Cutter side walls coincident with host walls | Replace cutter outline with bounding rectangle outside host |
| Fusion: *"mesh not oriented"* on import | trimesh `is_watertight` doesn't check face orientation | Always run `fix_winding` + `fix_normals` before export |
| Script hangs mid-run | Intermediate `show()` blocking | Comment out all but final `show()` |

---

## 📦 Dependencies

```
build123d==0.7.0
ocp_vscode==3.3.4
numpy-stl
trimesh
manifold3d
rtree
networkx          # optional — trimesh boundary-loop stitching
```

---

## 🗺️ Roadmap

- [x] `Art1Top_1_Stopper` — 🟢 EXCELLENT (0.008% vol error) — 1 hr
- [x] `Art1Top_Splitted_A` — 🟢 EXCELLENT (0.023% vol error) — 3.5 hrs
- [x] `Art1Top_Splitted_B` — 🟢 EXCELLENT (0.030% vol error) — 40 min
- [x] `Art2BodyA_Splitted_A` — 🟢 EXCELLENT (0.199% vol error) — 17 hrs
- [ ] `Art2BodyA_Splitted_B` — 🔧 in progress

---

## 📄 License

This reconstruction project is open source. The original Thor design files belong to [AngelLM](https://github.com/AngelLM/Thor) under their respective license.

---

## 🙏 Credits

- **[AngelLM](https://github.com/AngelLM)** — original Thor robot arm design
- **[build123d](https://github.com/gumyr/build123d)** — the Python CAD library powering all reconstructions
- **[OCP CAD Viewer](https://github.com/bernhard-42/vscode-ocp-cad-viewer)** — VS Code 3D preview
- **[trimesh](https://trimesh.org/)** + **[manifold3d](https://github.com/elalish/manifold)** — STL comparison engine
