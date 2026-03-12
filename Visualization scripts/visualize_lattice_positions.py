import os
import sys
from typing import List, Optional
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap, BoundaryNorm

# Defaults
NG_DEFAULT = 200        # lattice size (200x200), fixed
X_DEFAULT = 100         # partition row between layers, fixed
STEP_DEFAULT = 20000    # timestep spacing used when writing LatticePositions
DOT_SIZE = 14           # scatter dot size (points^2)
OUTDIR_DEFAULT = "AntPosition"
INPUT_DEFAULT = "LatticePositions"


def load_positions(path: str) -> List[List[int]]:
    """Load timesteps from LatticePositions file.
    Each non-empty line contains NANT integer indices (or -1 for escaped).
    """
    timesteps: List[List[int]] = []
    with open(path, "r") as f:
        for ln in f:
            ln = ln.strip()
            if not ln:
                continue
            parts = ln.split()
            row: List[int] = []
            for p in parts:
                try:
                    row.append(int(p))
                except ValueError:
                    # ignore malformed tokens
                    pass
            timesteps.append(row)
    return timesteps


def plot_timestep(indices: List[int], NG: int, title: str, outpath: str, x: Optional[int] = None) -> None:
    """Scatter ants (indices >= 0) as dots on an NG x NG grid and save to outpath."""
    # Keep only ants inside the lattice: 0 <= index < NG*NG
    max_index = NG * NG
    in_lattice = [idx for idx in indices if isinstance(idx, int) and 0 <= idx < max_index]
    if in_lattice:
        xs = [idx % NG for idx in in_lattice]   # columns (horizontal)
        ys = [idx // NG for idx in in_lattice]  # rows (vertical)
    else:
        xs, ys = [], []

    fig, ax = plt.subplots(figsize=(6, 6), dpi=300)
    # Build a grid image where each cell corresponds to a lattice site
    # 0 = empty, 1 = bottom-layer ant, 2 = top-layer ant (if x provided)
    grid = np.zeros((NG, NG), dtype=np.uint8)
    if in_lattice:
        for idx in in_lattice:
            c = idx % NG
            r = idx // NG
            if x is None:
                grid[r, c] = 1
            else:
                grid[r, c] = 1 if r < x else 2
    if x is None:
        cmap = ListedColormap(["white", "black"])  # empty, ant
        bounds = [0, 0.5, 1.5]
    else:
        cmap = ListedColormap(["white", "red", "blue"])  # empty, bottom, top
        bounds = [0, 0.5, 1.5, 2.5]
    norm = BoundaryNorm(bounds, cmap.N)
    ax.imshow(grid, cmap=cmap, norm=norm, origin="lower", interpolation="nearest")
    ax.set_aspect("equal")
    ax.axis("off")
    # Optional: title; comment out if not needed
    # ax.set_title(title)

    plt.tight_layout(pad=0)
    os.makedirs(os.path.dirname(outpath) or ".", exist_ok=True)
    plt.savefig(outpath, bbox_inches="tight", pad_inches=0)
    plt.close(fig)


def main():
    # Parse args: infile [step] [outdir]
    infile = sys.argv[1] if len(sys.argv) > 1 else INPUT_DEFAULT
    step = int(sys.argv[2]) if len(sys.argv) > 2 else STEP_DEFAULT
    outdir = sys.argv[3] if len(sys.argv) > 3 else OUTDIR_DEFAULT
    NG = NG_DEFAULT
    x: Optional[int] = X_DEFAULT  # always color-code: rows < 100 red, >= 100 blue

    if not os.path.isfile(infile):
        print(f"Input file not found: {infile}")
        sys.exit(1)

    timesteps = load_positions(infile)

    for t_index, indices in enumerate(timesteps):
        # Compute the actual time label assuming first line is t=0
        t_val = t_index * step
        filename = f"t={t_val}.png"
        outpath = os.path.join(outdir, filename)
        plot_timestep(indices, NG, title=f"t = {t_val}", outpath=outpath, x=x)

    print(f"Wrote {len(timesteps)} frames to '{outdir}' (NG={NG}, x={x}) with names like t=0.png, t={step}.png ...")


if __name__ == "__main__":
    main()
