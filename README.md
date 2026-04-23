# Ava_AngelLM_Thor_Art1_build123d

> **Reconstructing the [AngelLM Thor open-source robot arm](https://github.com/AngelLM/Thor) parts from scratch using [build123d](https://github.com/gumyr/build123d) — with automated STL comparison against the original Fusion 360 exports.**

---

## 🤖 What is This Project?

[Thor](https://github.com/AngelLM/Thor) is a fully open-source, 3D-printable robotic arm designed by AngelLM. This project takes each Thor part and **reconstructs it programmatically** using Python + build123d, driven entirely by coordinate data exported from Fusion 360.

The goal: prove that every part can be rebuilt to **near-perfect geometric accuracy** from first principles — no manual CAD, no guesswork.

---

## ✅ Parts Completed

| # | Part | Volume (mm³) | Vol Error | Sym Diff | Bounding Box | Rating |
|---|------|-------------|-----------|----------|-------------|--------|
| 1 | `Art1Top_1_Stopper` | 106.8725 | 0.008% | 0.009% | ✅ PASS | 🟢 EXCELLENT |

> More parts in progress — `Art1Top_Splitted_A`, and others to follow.

---

## 🗂️ Project Structure

Each part lives in its own folder under `20260422_assign/`:

```
20260422_assign/
└── Art1Top_1_Stopper/
    ├── csv_data_Art1Top_1_Stopper/        ← Raw Fusion 360 coordinate exports
    │   └── Fusion_Coordinates_S1.csv
    ├── csv_merged/                        ← Cleaned & deduplicated CSVs
    │   └── Fusion_Coordinates_S1.csv
    ├── 0_preprocess_csvs.py               ← Step 1: Clean & merge raw CSVs
    ├── Art1Top_1_Stopper_build123d.py     ← Step 2: Build the part
    ├── Art1Top_1_Stopper_compare_stl_files.py  ← Step 3: Compare vs original
    ├── Art1Top_1_Stopper_G_1_3.stl        ← Output: built STL
    ├── Art1Top_1_Stopper_G_1_3.step       ← Output: built STEP
    ├── Art1Top_1_Stopper_original.stl     ← Reference: Fusion 360 original
    ├── Art1Top_1_Stopper_summary_G_1_3.txt        ← Build log
    └── Art1Top_1_Stopper_build123d_vs_original_G_1_3.txt  ← Comparison report
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
| **G2–Gn** | Perform extrusions, cuts, sweeps, patterns etc. |
| **G3** | Always last — `clean()` → watertight check → export STL + STEP → write summary |

**File naming convention:**
```
PartName_G_1_3.stl          ← STL output
PartName_G_1_3.step         ← STEP output
PartName_summary_G_1_3.txt  ← Build log
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

Extruded:
- **Full disc (A+B+C)**: 1.2 mm downward (−Z)
- **Strip (Region A only)**: additional 1.0 mm upward (+Z)

### Comparison scorecard

```
███████████████████████████████████████████████████████████
  STL COMPARISON: Build123d  vs  Fusion 360 Original
███████████████████████████████████████████████████████████

  Build123d volume    : 106.8725 mm³
  Fusion 360 volume   : 106.8644 mm³
  Absolute difference :  +0.0082 mm³
  % error             :   0.008%       🟢 EXCELLENT

  Symmetric diff      :   0.0092 mm³
  Sym diff %          :   0.009%       🟢 EXCELLENT
  Overlap coverage    :  99.9995%      🟢 EXCELLENT

  Bounding box        : ✅ ALL 6 AXES PASS  (max deviation 0.0007 mm)
  Centre of mass      : (57.000, 0.000, 5.979) mm  ← IDENTICAL
```

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

```bash
# Step 1 — Activate environment
buildenv

# Step 2 — Navigate to part folder
cd ~/Documents/ava_build123d/20260422_assign/Art1Top_1_Stopper

# Step 3 — Set VS Code Python interpreter (once per project folder)
# Cmd+Shift+P → "Python: Select Interpreter"
# → ~/Documents/ava_build123d/build123d_master_env/bin/python3

# Step 4 — Start OCP viewer server (Terminal tab 1 — leave running)
python -m ocp_vscode

# Step 5 — Open second terminal tab, activate env again
buildenv
cd ~/Documents/ava_build123d/20260422_assign/Art1Top_1_Stopper

# Step 6 — Preprocess CSVs
python 0_preprocess_csvs.py

# Step 7 — Build the part
python Art1Top_1_Stopper_build123d.py

# Step 8 — Compare against original
python Art1Top_1_Stopper_compare_stl_files.py
```

> **Port note:** OCP viewer on this machine runs on port **3940**. All scripts use `set_port(3940)`.

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

- [x] `Art1Top_1_Stopper`
- [ ] `Art1Top_Splitted_A`
- [ ] `Art1Top_Splitted_B`
- [ ] More Art1 parts...
- [ ] Art2, Art3, Art4, Art5, Art6 parts

---

## 📄 License

This reconstruction project is open source. The original Thor design files belong to [AngelLM](https://github.com/AngelLM/Thor) under their respective license.

---

## 🙏 Credits

- **[AngelLM](https://github.com/AngelLM)** — original Thor robot arm design
- **[build123d](https://github.com/gumyr/build123d)** — the Python CAD library powering all reconstructions
- **[OCP CAD Viewer](https://github.com/bernhard-42/vscode-ocp-cad-viewer)** — VS Code 3D preview
- **[trimesh](https://trimesh.org/)** + **[manifold3d](https://github.com/elalish/manifold)** — STL comparison engine
