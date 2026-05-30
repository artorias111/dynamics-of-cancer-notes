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
        # Week 1 — Single-Species Tumor Growth (Ch. 4)

        Two classic models describe how a tumor grows toward a carrying capacity $K$:

        **Logistic** (Eq 4.3):
        $$\frac{dW}{dt} = aW\!\left(1 - \frac{W}{K}\right)$$

        **Gompertz** (Eq 4.6):
        $$\frac{dW}{dt} = aW - bW\ln W$$

        Both produce S-shaped curves, but Gompertz decelerates *earlier* — it better fits
        observed tumor data because large tumors slow down faster than logistic predicts.

        Set $b = a / \ln K$ so both models share the same asymptote $K$.
        """
    )
    return


@app.cell
def __(mo):
    a_slider = mo.ui.slider(0.1, 2.0, value=0.5, step=0.05, label="Growth rate $a$")
    K_slider = mo.ui.slider(50, 2000, value=500, step=50, label="Carrying capacity $K$")
    W0_slider = mo.ui.slider(1, 50, value=5, step=1, label="Initial size $W_0$")
    mo.vstack([a_slider, K_slider, W0_slider])
    return a_slider, K_slider, W0_slider


@app.cell
def __(a_slider, K_slider, W0_slider, np, plt, solve_ivp):
    a = a_slider.value
    K = K_slider.value
    W0 = W0_slider.value
    b = a / np.log(K)

    def logistic(t, W):
        return [a * W[0] * (1.0 - W[0] / K)]

    def gompertz(t, W):
        w = max(W[0], 1e-10)
        return [a * w - b * w * np.log(w)]

    t_span = (0, 40)
    t_eval = np.linspace(0, 40, 400)

    sol_log = solve_ivp(logistic, t_span, [W0], t_eval=t_eval, max_step=0.1)
    sol_gom = solve_ivp(gompertz, t_span, [W0], t_eval=t_eval, max_step=0.1)

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(sol_log.t, sol_log.y[0], label="Logistic (Eq 4.3)", color="#2ca02c", lw=2)
    ax.plot(sol_gom.t, sol_gom.y[0], label="Gompertz (Eq 4.6)", color="#d62728", lw=2, ls="--")
    ax.axhline(K, color="gray", ls=":", lw=1, label=f"K = {K}")
    ax.set_xlabel("Time (days)")
    ax.set_ylabel("Tumor size W")
    ax.set_title("Logistic vs Gompertz growth")
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    fig
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Things to notice

        - With small $W_0$, both curves look exponential early on — the carrying capacity
          doesn't matter until the tumor is large.
        - Increase $a$: both curves rise faster but still saturate at $K$.
        - The Gompertz curve always bends away from the logistic *before* $K/2$.
          That's the signature of early deceleration.

        **Question to think about**: if you only had a few data points from a growing tumor,
        could you tell which model fits better?  What would you need?
        """
    )
    return


if __name__ == "__main__":
    app.run()
