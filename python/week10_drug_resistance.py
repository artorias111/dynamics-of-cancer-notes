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
        # Week 10 — Drug Resistance (Ch. 15)

        Resistant mutants arise stochastically *before* treatment starts.
        The Luria-Delbrück result: once tumour size $N > 1/u$, resistance is nearly certain.

        Expected resistant cells at treatment:
        $$E[R] \approx \frac{u \cdot N}{\ln(N \cdot r)}$$

        so $P(\text{resistance}) \approx 1 - e^{-E[R]}$.
        """
    )
    return


@app.cell
def __(mo):
    N_sl = mo.ui.slider(100, 10000, value=1000, step=100, label="Treat at tumour size $N$")
    u_sl = mo.ui.slider(1e-5, 1e-2, value=1e-4, step=1e-5, label="Mutation rate $u$")
    runs_sl = mo.ui.slider(100, 2000, value=500, step=100, label="Simulation runs")
    b_sl = mo.ui.slider(0.5, 2.0, value=1.2, step=0.1, label="Birth rate $b$")
    d_sl = mo.ui.slider(0.1, 1.0, value=0.2, step=0.1, label="Death rate $d$")
    run_btn = mo.ui.run_button(label="Simulate")
    mo.vstack([N_sl, u_sl, b_sl, d_sl, runs_sl, run_btn])
    return N_sl, b_sl, d_sl, run_btn, runs_sl, u_sl


@app.cell
def __(N_sl, b_sl, d_sl, mo, np, plt, run_btn, runs_sl, u_sl):
    run_btn
    N_treat = N_sl.value
    u = u_sl.value
    b = b_sl.value
    d = d_sl.value
    n_runs = runs_sl.value
    rng = np.random.default_rng(0)

    def simulate_one():
        sens, res = 1, 0
        while sens + res < N_treat:
            total = (b + d) * (sens + res)
            if total == 0: return 0
            if rng.random() < b / (b + d):
                if rng.random() < sens / (sens + res):
                    if rng.random() < u: res += 1
                    else: sens += 1
                else:
                    res += 1
            else:
                if rng.random() < sens / (sens + res): sens -= 1
                else: res -= 1
            if sens + res == 0: return 0
        return res

    results = np.array([simulate_one() for _ in range(n_runs)])
    prob_resist = (results > 0).mean()
    r_net = b - d
    ld_expected = u * N_treat / np.log(max(N_treat * r_net, 2)) if r_net > 0 else 0
    prob_theory = 1 - np.exp(-ld_expected)

    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    axes[0].hist(results[results > 0], bins=30, color="#d62728", edgecolor="white", alpha=0.8)
    axes[0].set_xlabel("Resistant cells at treatment")
    axes[0].set_ylabel("Count")
    axes[0].set_title(f"Jackpot distribution ({(results>0).sum()}/{n_runs} runs with resistance)")

    N_range = np.logspace(1, np.log10(N_treat * 5), 40).astype(int)
    probs_th = 1 - np.exp(-u * N_range / np.log(np.maximum(N_range * r_net, 2)))
    axes[1].semilogx(N_range, probs_th, color="#1f77b4", lw=2, label="Luria-Delbrück")
    axes[1].axvline(N_treat, color="gray", ls="--", label=f"N={N_treat}")
    axes[1].axhline(prob_resist, color="#d62728", ls="--", label=f"Sim: {prob_resist:.2f}")
    axes[1].set_xlabel("Tumour size N")
    axes[1].set_ylabel("P(resistance exists)")
    axes[1].set_title("Pre-existing resistance probability")
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)
    plt.tight_layout()
    mo.vstack([fig, mo.md(f"Simulation: {prob_resist:.3f}  |  Theory: {prob_theory:.3f}")])
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Things to notice

        - Below $N \sim 1/u$: resistance unlikely to pre-exist, treatment works.
        - Above threshold: resistance almost guaranteed *before treatment starts*.
        - The jackpot distribution: most runs have few resistant cells, but occasionally
          many — depending on when in the lineage the mutation arose.
        """
    )
    return


if __name__ == "__main__":
    app.run()
