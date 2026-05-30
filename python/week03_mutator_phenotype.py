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
        # Week 3 — The Mutator Phenotype (Ch. 6.1)

        Normal cells spend resources on DNA repair; mutator cells skip repair and replicate faster.
        The trade-off: mutators accumulate deleterious mutations at rate $u$, reducing their
        average fitness.

        Fitness of a **stable** cell: $f_s = 1$ (normalised)

        Fitness of a **mutator** cell (Eq 6.4):
        $$f_m(u) = (1 + s) \cdot (1 - u)^n$$

        - $s > 0$: replication advantage from skipping repair
        - $u$: probability a replication produces a deleterious hit
        - $n$: number of fitness-relevant loci

        Mutators win when $f_m > f_s$, i.e. when $u < u_c$ where:
        $$u_c = 1 - \left(\frac{1}{1+s}\right)^{1/n}$$
        """
    )
    return


@app.cell
def __(mo):
    s_sl = mo.ui.slider(0.01, 0.5, value=0.1, step=0.01, label="Replication advantage $s$")
    n_sl = mo.ui.slider(1, 200, value=50, step=1, label="Number of loci $n$")
    mo.hstack([s_sl, n_sl])
    return n_sl, s_sl


@app.cell
def __(mo, n_sl, np, plt, s_sl):
    s = s_sl.value
    n = n_sl.value

    u_vals = np.linspace(0, 0.5, 500)
    f_m = (1 + s) * (1 - u_vals) ** n
    u_c = 1 - (1 / (1 + s)) ** (1 / n)

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(u_vals, f_m, label="Mutator fitness $f_m(u)$", color="#d62728", lw=2)
    ax.axhline(1.0, color="#1f77b4", lw=2, label="Stable cell fitness $f_s = 1$")
    ax.axvline(u_c, color="gray", ls="--", lw=1.5, label=f"$u_c = {u_c:.3f}$")
    ax.fill_betweenx([0, 1.8], 0, u_c, alpha=0.08, color="green", label="Mutator wins")
    ax.fill_betweenx([0, 1.8], u_c, 0.5, alpha=0.08, color="red", label="Stable wins")
    ax.set_xlim(0, 0.5)
    ax.set_ylim(0, max(f_m.max(), 1.5))
    ax.set_xlabel("Deleterious hit rate per replication $u$")
    ax.set_ylabel("Fitness")
    ax.set_title(f"Mutator threshold  ($s={s}$, $n={n}$)  →  $u_c = {u_c:.4f}$")
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    mo.vstack([fig, mo.md(f"**Critical threshold**: $u_c = {u_c:.4f}$.  "
                          f"For $u < u_c$ mutators are fitter; above it, repair pays off.")])
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Things to notice

        - Larger $n$ makes $u_c$ **smaller** — more loci means skipping repair is riskier.
        - Larger $s$ shifts $u_c$ **up** — a bigger speed advantage tolerates more errors.
        - Real mutation rates: $u \sim 10^{-7}$ normally, up to $\sim 10^{-4}$ in MMR-deficient cells.

        **Question**: what happens to $u_c$ as $n \to \infty$?  What does that mean biologically?
        """
    )
    return


if __name__ == "__main__":
    app.run()
