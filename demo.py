# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo",
#     "numpy==2.3.1",
# ]
# ///

import marimo

__generated_with = "0.14.10"
app = marimo.App(width="columns")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    return mo, np


@app.cell
def _():
    a = 1 
    return (a,)


@app.cell
def _():
    b = 2
    return (b,)


@app.cell
def _(a, b, np, slider):
    c = a + b + slider.value
    np.arange(c)
    return


@app.cell
def _(mo):
    slider = mo.ui.slider(1, 10, 1)
    slider
    return (slider,)


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
