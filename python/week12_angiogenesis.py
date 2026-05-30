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
        # Week 12 — Angiogenesis (Ch. 8)

        Tumours beyond ~1–2 mm must recruit blood vessels. The Hahnfeldt model:

        $$\frac{dV}{dt} = aV \ln\!\left(\frac{K}{V}\right), \qquad
          \frac{dK}{dt} = bV - cV^{2/3} K - dK$$

        $V$ = tumour volume, $K$ = vascular carrying capacity.
        $K$ evolves dynamically — the tumour can only grow as fast as it recruits vessels.
        The *angiogenic switch* fires when stimulation ($b$) overtakes inhibition ($c$).
        """
    )
    return


@app.cell
def __(mo):
    a_sl = mo.ui.slider(0.1, 1.0, value=0.3, step=0.05, label="Growth rate $a$")
    b_sl = mo.ui.slider(0.5, 5.0, value=2.0, step=0.1, label="Stimulation $b$")
    c_sl = mo.ui.slider(0.1, 2.0, value=0.8, step=0.05, label="Inhibition $c$")
    d_sl = mo.ui.slider(0.0, 0.5, value=0.05, step=0.01, label="Inhibitor decay $d$")
    mo.vstack([a_sl, b_sl, c_sl, d_sl])
    return a_sl, b_sl, c_sl, d_sl


@app.cell
def __(a_sl, b_sl, c_sl, d_sl, mo, np, plt, solve_ivp):
    a, b, c, d = a_sl.value, b_sl.value, c_sl.value, d_sl.value

    def angio(t, y):
        V, K = max(y[0], 1e-6), max(y[1], 1e-6)
        return [a * V * np.log(K / V), b * V - c * V**(2/3) * K - d * K]

    ics = [(1.0, 5.0), (1.0, 50.0), (1.0, 200.0), (10.0, 20.0)]
    colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"]
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))

    for ic, col in zip(ics, colors):
        sol = solve_ivp(angio, (0, 60), list(ic), t_eval=np.linspace(0, 60, 600), max_step=0.2)
        lbl = f"V₀={ic[0]}, K₀={ic[1]}"
        axes[0].plot(sol.t, sol.y[0], color=col, lw=2, label=lbl)
        axes[0].plot(sol.t, sol.y[1], color=col, lw=2, ls="--")
        axes[1].plot(sol.y[0], sol.y[1], color=col, lw=2, label=lbl)
        axes[1].plot(*ic, "o", color=col, ms=6)

    axes[0].set_xlabel("Time")
    axes[0].set_ylabel("Size")
    axes[0].set_title("V (solid) and K (dashed) over time")
    axes[0].legend(fontsize=8)
    axes[0].grid(True, alpha=0.3)
    axes[1].set_xlabel("Tumour volume V")
    axes[1].set_ylabel("Carrying capacity K")
    axes[1].set_title("Phase portrait (V, K)")
    axes[1].legend(fontsize=8)
    axes[1].grid(True, alpha=0.3)
    plt.tight_layout()
    mo.output.replace(fig)
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Things to notice

        - $K > V$: tumour grows (spare vascular capacity). $K < V$: tumour shrinks.
        - Dormant micrometastases: stable equilibrium at low $V \approx K$.
        - Increasing $b$ raises steady-state size. Anti-angiogenic drugs raise $c$ or lower $b$.
        - The angiogenic switch: when $bV > cV^{2/3}K$, stimulation overtakes inhibition.
        """
    )
    return


if __name__ == "__main__":
    app.run()
