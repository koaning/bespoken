# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "altair==5.5.0",
#     "marimo",
#     "matplotlib==3.10.3",
#     "numpy==2.3.1",
#     "pandas==2.3.0",
# ]
# ///

import marimo

__generated_with = "0.14.10"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import random
    import pandas as pd
    import altair as alt
    return alt, mo, pd, random


@app.cell
def _(mo):
    mo.md(
        r"""
        # The Monty Hall Problem Analysis 🎲

    A famous probability puzzle: You pick one of 3 doors (car behind one, goats behind two). The host opens a door with a goat, then asks if you want to switch.

    **The counterintuitive answer:** Always switch! You get a **66.7%** chance of winning vs **33.3%** if you stay.

        Let's analyze the results of a simulation to understand this better.
        """
    )
    return


@app.cell
def _(mo):
    mo.md("## 🎯 Game Logic and Simulation")
    return


if __name__ == "__main__":
    app.run()
