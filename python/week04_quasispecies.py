import marimo

__generated_with = "0.23.8"
app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt
    return mo, np, plt


@app.cell
def __(mo):
    mo.md(
        r"""
        # Week 4 — Quasispecies & Mutation Cascades (Ch. 6.2)

        A linear mutation chain: wild-type $x_0$ mutates to $x_1$, then $x_2$, …, $x_n$.
        Each class $x_i$ has fitness $f_i$ and mutates to $x_{i+1}$ with rate $u$.

        $$\dot{x}_i = x_i f_i (1-u) + x_{i-1} f_{i-1} u - \bar{f}\, x_i$$

        where $\bar{f} = \sum_j x_j f_j$ keeps the population normalised.
        """
    )
    return


@app.cell
def __(mo):
    n_sl = mo.ui.slider(3, 12, value=6, step=1, label="Number of clones")
    u_sl = mo.ui.slider(0.01, 0.5, value=0.1, step=0.01, label="Mutation rate $u$")
    fit_sl = mo.ui.slider(1.0, 3.0, value=1.5, step=0.1, label="Fitness per step $r$ (clone $i$ has fitness $r^i$)")
    mo.vstack([n_sl, u_sl, fit_sl])
    return fit_sl, n_sl, u_sl


@app.cell
def __(fit_sl, mo, n_sl, np, plt, u_sl):
    from scipy.integrate import solve_ivp as _solve

    n_clones = n_sl.value
    u = u_sl.value
    r = fit_sl.value
    fitnesses = np.array([r ** i for i in range(n_clones)])

    def quasispecies(t, x):
        f_bar = np.dot(fitnesses, x)
        dx = np.zeros(n_clones)
        dx[0] = fitnesses[0] * (1 - u) * x[0] - f_bar * x[0]
        for i in range(1, n_clones):
            dx[i] = (fitnesses[i] * (1 - u) * x[i]
                     + fitnesses[i - 1] * u * x[i - 1]
                     - f_bar * x[i])
        return dx

    x0 = np.zeros(n_clones)
    x0[0] = 1.0
    sol = _solve(quasispecies, (0, 80), x0, t_eval=np.linspace(0, 80, 800), max_step=0.1)

    fig, ax = plt.subplots(figsize=(9, 5))
    cmap = plt.cm.viridis(np.linspace(0, 1, n_clones))
    for i in range(n_clones):
        ax.plot(sol.t, sol.y[i], color=cmap[i], lw=2, label=f"$x_{{{i}}}$ (f={fitnesses[i]:.2f})")
    ax.set_xlabel("Time")
    ax.set_ylabel("Frequency")
    ax.set_title("Quasispecies mutation cascade")
    ax.legend(fontsize=8, ncol=2)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    mo.output.replace(fig)
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Things to notice

        - With $r > 1$: dominance *waves* through the population, $x_0$ peaks first then $x_1$, etc.
        - High $u$ blurs the waves — clones are created faster but also lost faster.
        - Very high $u$ (~0.4+) causes *error catastrophe*: the fittest clone never dominates.
        - Each wave is a new mutant clone sweeping through a tumour.
        """
    )
    return


if __name__ == "__main__":
    app.run()
