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
        # The Monty Hall Paradox: A Probability Puzzle

    Welcome to an exploration of one of the most intriguing probability puzzles in mathematics: The Monty Hall Problem.

    **The Scenario:**
    - You're on a game show, facing three closed doors.
    - Behind one door is a car; behind the others, goats.
    - You pick a door, say No. 1, and the host, who knows what's behind the doors, opens another door, say No. 3, which has a goat.
    - He then asks you: "Do you want to switch to door No. 2?"

    **The Paradox:**
    Intuition might suggest that switching doesn't matter, as you now have a 50/50 chance. However, probability theory tells us otherwise!

    **The Solution:**
    Always switch! By switching, you increase your chances of winning the car from 33.3% to 66.7%.

    Let's dive into a simulation to understand why this counterintuitive result is correct.
        """
    )
    return


@app.cell
def _(mo):
    mo.md("## Game Logic and Simulation")
    return


if __name__ == "__main__":
    app.run()
