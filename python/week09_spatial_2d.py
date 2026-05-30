import marimo

__generated_with = "0.23.8"
app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.colors as mcolors
    return mo, mcolors, np, plt


@app.cell
def __(mo):
    mo.md(
        r"""
        # Week 9 — 2D Contact Process (Ch. 14)

        The **contact process** places cells on a 2D grid where each site is
        empty (0), normal (1), or mutant (2). Cells divide into empty neighbours;
        they can also die, leaving gaps. Unlike the Moran process, population size
        is not fixed — tumours grow into vacant space.

        This creates *cluster islands* rather than well-mixed competition, with
        direct clinical relevance: spatial heterogeneity makes biopsy unreliable.
        """
    )
    return


@app.cell
def __(mo):
    grid_sl = mo.ui.slider(30, 100, value=60, step=10, label="Grid size")
    steps_sl = mo.ui.slider(1000, 50000, value=10000, step=1000, label="Steps")
    fit_mut_sl = mo.ui.slider(1.0, 3.0, value=1.5, step=0.1, label="Mutant fitness")
    death_sl = mo.ui.slider(0.0, 0.5, value=0.1, step=0.05, label="Death rate $d$")
    run_btn = mo.ui.run_button(label="Run simulation")
    mo.vstack([grid_sl, steps_sl, fit_mut_sl, death_sl, run_btn])
    return death_sl, fit_mut_sl, grid_sl, run_btn, steps_sl


@app.cell
def __(death_sl, fit_mut_sl, grid_sl, mo, mcolors, np, plt, run_btn, steps_sl):
    run_btn

    N = grid_sl.value
    n_steps = steps_sl.value
    d = death_sl.value
    rng = np.random.default_rng(42)

    grid = np.ones((N, N), dtype=np.int8)
    cx, cy = N // 2, N // 2
    grid[cx-2:cx+2, cy-2:cy+2] = 2

    def neighbours(r, c, n):
        return [(r+dr, c+dc) for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]
                if 0 <= r+dr < n and 0 <= c+dc < n]

    for _ in range(n_steps):
        r, c = rng.integers(0, N, size=2)
        cell = grid[r, c]
        if cell == 0:
            continue
        if rng.random() < d:
            grid[r, c] = 0
            continue
        empty = [(nr, nc) for nr, nc in neighbours(r, c, N) if grid[nr, nc] == 0]
        if not empty:
            continue
        nr, nc = empty[rng.integers(len(empty))]
        grid[nr, nc] = cell

    mutant_frac = (grid == 2).sum() / (grid > 0).sum() if (grid > 0).any() else 0.0
    cmap = mcolors.ListedColormap(["white", "#4daf4a", "#e41a1c"])
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.imshow(grid, cmap=cmap, vmin=0, vmax=2, interpolation="nearest")
    ax.set_title(f"After {n_steps} steps  |  mutant fraction = {mutant_frac:.2%}")
    ax.axis("off")
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(color="white", ec="gray", label="Empty"),
                       Patch(color="#4daf4a", label="Normal"),
                       Patch(color="#e41a1c", label="Mutant")],
              loc="lower right", fontsize=9)
    plt.tight_layout()
    mo.output.replace(fig)
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Things to notice

        - Mutant cells form **compact islands** — they must grow outward from the founding cluster.
        - Increase death rate: empty patches appear and growth fragments.
        - A well-mixed fitter mutant would sweep instantly; spatially it takes much longer.
        - This is why a single biopsy can miss entire subclonal populations.
        """
    )
    return


if __name__ == "__main__":
    app.run()
