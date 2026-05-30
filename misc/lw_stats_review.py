import marimo

__generated_with = "0.23.8"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Lander-Waterman statistics for genome assembly
    """)
    return


app._unparsable_cell(
    r"""
    def bernoulli()
    """,
    name="_"
)


app._unparsable_cell(
    r"""
    def binomial()
    """,
    name="_"
)


app._unparsable_cell(
    r"""
    def poisson()
    """,
    name="_"
)


app._unparsable_cell(
    r"""
    def geometric()
    """,
    name="_"
)


app._unparsable_cell(
    r"""
    def exponential()
    """,
    name="_"
)


if __name__ == "__main__":
    app.run()
