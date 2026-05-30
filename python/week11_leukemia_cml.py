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
        # Week 11 — CML Drug Resistance (Ch. 16)

        CML is driven by BCR-ABL. Imatinib blocks it, but resistance mutations arise.
        A single drug needs only *one* hit to be escaped.
        Combination therapy needs *two simultaneous* hits — probability scales as $(uN)^2$.

        Single-drug escape: $P \approx 1 - e^{-uN/\ln N}$

        Combination escape: $P \approx 1 - e^{-(uN)^2 / (2\ln^2 N)}$
        """
    )
    return


@app.cell
def __(mo):
    u_sl = mo.ui.slider(1e-8, 1e-5, value=1e-7, step=1e-8, label="Mutation rate $u$")
    N_sl = mo.ui.slider(1e6, 1e10, value=1e8, step=1e6, label="Tumour size $N$")
    runs_sl = mo.ui.slider(100, 1000, value=300, step=100, label="Runs")
    run_btn = mo.ui.run_button(label="Simulate")
    mo.vstack([u_sl, N_sl, runs_sl, run_btn])
    return N_sl, run_btn, runs_sl, u_sl


@app.cell
def __(N_sl, mo, np, plt, run_btn, runs_sl, u_sl):
    run_btn
    u = u_sl.value
    N = int(N_sl.value)
    n_runs = runs_sl.value
    rng = np.random.default_rng(1)

    def exp_single(N, u): return u * N / np.log(max(N * 0.9, 2))
    def exp_double(N, u):
        lnN = np.log(max(N, 2))
        return (u**2) * (N**2) / (2 * lnN**2)

    single_escape = np.array([rng.poisson(exp_single(N, u)) > 0 for _ in range(n_runs)])
    combo_escape  = np.array([rng.poisson(exp_double(N, u)) > 0 for _ in range(n_runs)])
    p_single, p_combo = single_escape.mean(), combo_escape.mean()

    N_range = np.logspace(5, 11, 60)
    p_s_th = 1 - np.exp(-u * N_range / np.log(np.maximum(N_range * 0.9, 2)))
    p_c_th = 1 - np.exp(-(u**2) * N_range**2 / (2 * np.log(np.maximum(N_range, 2))**2))

    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    axes[0].bar(["Single drug", "Combination"], [p_single, p_combo],
                color=["#d62728", "#2ca02c"], alpha=0.8, edgecolor="white")
    axes[0].set_ylim(0, 1)
    axes[0].set_ylabel("P(treatment escape)")
    axes[0].set_title(f"N={N:.1e}, u={u:.1e}")
    for j, val in enumerate([p_single, p_combo]):
        axes[0].text(j, val + 0.02, f"{val:.3f}", ha="center", fontsize=11)

    axes[1].loglog(N_range, p_s_th, color="#d62728", lw=2, label="Single drug")
    axes[1].loglog(N_range, p_c_th, color="#2ca02c", lw=2, label="Combination")
    axes[1].axvline(N, color="gray", ls="--", label=f"N={N:.1e}")
    axes[1].set_xlabel("Tumour size N")
    axes[1].set_ylabel("P(escape)")
    axes[1].set_title("Escape probability vs tumour size")
    axes[1].legend()
    axes[1].grid(True, alpha=0.3, which="both")
    plt.tight_layout()
    mo.vstack([fig, mo.md(f"Single: {p_single:.3f}  |  Combination: {p_combo:.4f}")])
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Things to notice

        - Single drug: once $N > 1/u$, escape is certain.
        - Combination: requires two simultaneous hits, probability $\propto (uN)^2$ — much lower.
        - The crossover: below $N \sim 1/u^2$, both strategies work. Treat early!
        - Real CML: imatinib alone fails ~30% eventually. Second-gen inhibitors close the gap.
        """
    )
    return


if __name__ == "__main__":
    app.run()
