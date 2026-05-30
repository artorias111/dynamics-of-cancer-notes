import marimo

__generated_with = "0.23.8"
app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt
    from scipy.integrate import solve_ivp
    return mo, np, plt, solve_ivp


@app.cell
def __(mo):
    mo.md(
        r"""
        # Week 2 — Two-Species Competition (Ch. 5)

        Two clones compete for the same resource (e.g. space, oxygen):

        $$\frac{dx_1}{dt} = x_1\bigl(r_1 - a_{11}x_1 - a_{12}x_2\bigr)$$
        $$\frac{dx_2}{dt} = x_2\bigl(r_2 - a_{21}x_1 - a_{22}x_2\bigr)$$

        $a_{ii}$ = self-suppression (intraspecific), $a_{ij}$ = cross-suppression (interspecific).

        **Competitive exclusion**: if one clone suppresses the other more than it suppresses
        itself, co-existence is unstable — one clone drives the other extinct.
        That is exactly what happens during clonal selection in a tumour.
        """
    )
    return


@app.cell
def __(mo):
    r1_s = mo.ui.slider(0.5, 3.0, value=1.0, step=0.1, label="$r_1$ (clone 1 growth rate)")
    r2_s = mo.ui.slider(0.5, 3.0, value=1.2, step=0.1, label="$r_2$ (clone 2 growth rate)")
    a12_s = mo.ui.slider(0.1, 2.0, value=0.8, step=0.1, label="$a_{12}$ (clone 2 suppresses clone 1)")
    a21_s = mo.ui.slider(0.1, 2.0, value=0.6, step=0.1, label="$a_{21}$ (clone 1 suppresses clone 2)")
    mo.vstack([r1_s, r2_s, a12_s, a21_s])
    return a12_s, a21_s, r1_s, r2_s


@app.cell
def __(a12_s, a21_s, mo, np, plt, r1_s, r2_s, solve_ivp):
    r1, r2 = r1_s.value, r2_s.value
    a11, a22 = 1.0, 1.0
    a12, a21 = a12_s.value, a21_s.value

    def odes(t, y):
        x1, x2 = y
        dx1 = x1 * (r1 - a11 * x1 - a12 * x2)
        dx2 = x2 * (r2 - a21 * x1 - a22 * x2)
        return [dx1, dx2]

    t_span = (0, 30)
    t_eval = np.linspace(0, 30, 400)

    fig, axes = plt.subplots(1, 2, figsize=(12, 4))

    starts = [(0.1, 2.0), (2.0, 0.1), (1.0, 1.0), (0.5, 0.5)]
    colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#9467bd"]
    for ic, col in zip(starts, colors):
        sol = solve_ivp(odes, t_span, list(ic), t_eval=t_eval, max_step=0.1)
        axes[0].plot(sol.t, sol.y[0], color=col, lw=2, label=f"x1₀={ic[0]}")
        axes[0].plot(sol.t, sol.y[1], color=col, lw=2, ls="--")
    axes[0].set_xlabel("Time")
    axes[0].set_ylabel("Population")
    axes[0].set_title("Clone 1 (solid) vs Clone 2 (dashed)")
    axes[0].legend(fontsize=8)
    axes[0].grid(True, alpha=0.3)

    lim = max(r1 / a11, r2 / a22) * 1.2
    x1g = np.linspace(0.01, lim, 20)
    x2g = np.linspace(0.01, lim, 20)
    X1, X2 = np.meshgrid(x1g, x2g)
    U = X1 * (r1 - a11 * X1 - a12 * X2)
    V = X2 * (r2 - a21 * X1 - a22 * X2)
    speed = np.sqrt(U**2 + V**2) + 1e-10
    axes[1].streamplot(X1, X2, U / speed, V / speed, color="lightgray", density=1.2)
    for ic, col in zip(starts, colors):
        sol = solve_ivp(odes, t_span, list(ic), t_eval=t_eval, max_step=0.1)
        axes[1].plot(sol.y[0], sol.y[1], color=col, lw=2)
        axes[1].plot(*ic, "o", color=col, ms=6)
    axes[1].set_xlabel("Clone 1 ($x_1$)")
    axes[1].set_ylabel("Clone 2 ($x_2$)")
    axes[1].set_title("Phase portrait")
    axes[1].set_xlim(0, lim)
    axes[1].set_ylim(0, lim)
    axes[1].grid(True, alpha=0.3)

    x_range = np.linspace(0, lim, 200)
    axes[1].plot(x_range, (r1 - a11 * x_range) / a12, "b--", lw=1.5, label="$x_1$ nullcline")
    axes[1].plot((r2 - a22 * x_range) / a21, x_range, "r--", lw=1.5, label="$x_2$ nullcline")
    axes[1].legend(fontsize=8)

    plt.tight_layout()
    mo.output.replace(fig)
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Things to notice

        - The nullclines (dashed) divide the phase space.  Where they cross is an equilibrium.
        - If $a_{12} > r_1/r_2$ **and** $a_{21} > r_2/r_1$: both clones try to exclude each other
          → *bistability* (which clone wins depends on starting point).
        - If cross-suppression is weak relative to self-suppression: stable coexistence is possible.
        - Try $r_2 > r_1$ with weak $a_{21}$: clone 2 takes over regardless of starting conditions.

        **Cancer relevance**: a fitter mutant clone (higher $r$, lower self-suppression) will
        reliably outcompete normal tissue — the maths makes that inevitable.
        """
    )
    return


if __name__ == "__main__":
    app.run()
