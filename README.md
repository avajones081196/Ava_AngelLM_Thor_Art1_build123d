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

> **All 3 parts: 🟢 EXCELLENT across every metric.**

⏱ **Total time: 5 hrs 10 min**

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
└── Art1Top_Splitted_B/
    ├── csv_data_Art1Top_Splitted_B/
    ├── csv_merged/                        ← S1–S2 cleaned CSVs
    ├── 0_preprocess_csvs.py
    ├── Art1Top_Splitted_B_build123d.py    ← 6 guidelines (G1–G6)
    ├── Art1Top_Splitted_B_compare_stl_files.py
    ├── Art1Top_Splitted_B_G_1_6.stl
    ├── Art1Top_Splitted_B_G_1_6.step
    └── Art1Top_Splitted_B_original.stl
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

**The magic line** — always applied before export to remove accumulated geometric scars:
```python
final_solid = final_solid.clean()
```

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
pip install build123d==0.7.0 ocp_vscode==3.3.4 numpy-stl trimesh manifold3d rtree
```

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

---

## 📦 Dependencies

```
build123d==0.7.0
ocp_vscode==3.3.4
numpy-stl
trimesh
manifold3d
rtree
```

---

## 🗺️ Roadmap

- [x] `Art1Top_1_Stopper` — 🟢 EXCELLENT (0.008% vol error) — 1 hr
- [x] `Art1Top_Splitted_A` — 🟢 EXCELLENT (0.023% vol error) — 3.5 hrs
- [x] `Art1Top_Splitted_B` — 🟢 EXCELLENT (0.030% vol error) — 40 min
- [ ] `Art2BodyA_Splitted_A` — 🔧 In progress

---

## 📄 License

This reconstruction project is open source. The original Thor design files belong to [AngelLM](https://github.com/AngelLM/Thor) under their respective license.

---

## 🙏 Credits

- **[AngelLM](https://github.com/AngelLM)** — original Thor robot arm design
- **[build123d](https://github.com/gumyr/build123d)** — the Python CAD library powering all reconstructions
- **[OCP CAD Viewer](https://github.com/bernhard-42/vscode-ocp-cad-viewer)** — VS Code 3D preview
- **[trimesh](https://trimesh.org/)** + **[manifold3d](https://github.com/elalish/manifold)** — STL comparison engine
