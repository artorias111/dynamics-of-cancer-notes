import marimo

__generated_with = "0.23.8"
app = marimo.App()


app._unparsable_cell(
    r"""
    import marimo as mo
    imort numpy as np
    import matplotlib.pyplot as plt

    from scipy.integrate import solve_ivp
    """,
    name="_"
)


@app.function
def logistic_growth(t, W, a, K):
    """
    Model logistic growth of a tumor growth process. Required parameters are t, W, a and K. 
    """
    # Equation 4.3: dW/dt = a*W *(1-W/K)
    return a * W * (1.0 - W / K)


@app.function
def gompertz_growth(t, W, a, b):
    """
    define the function here
    """
    # E


if __name__ == "__main__":
    app.run()
