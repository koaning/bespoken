# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
#     "altair==5.5.0",
#     "numpy",
#     "pandas",
# ]
# ///
import marimo

__generated_with = "0.14.10"
app = marimo.App(width="columns")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _(mo):
    mo.md(
        r"""
    # The Monty Hall Problem Simulator

    A famous probability puzzle: You pick one of 3 doors (car behind one, goats behind two). The host opens a door with a goat, then asks if you want to switch.

    **The counterintuitive answer:** Always switch! You get a **66.7%** chance of winning vs **33.3%** if you stay.

    Use the controls below to see this in action!
    """
    )
    return


@app.cell
def _():
    import random
    import numpy as np
    import altair as alt
    import pandas as pd
    return alt, random, pd


@app.cell
def _(mo):
    mo.md("""## 🎮 Simulation Controls""")
    return


@app.cell
def _(mo):
    # Interactive controls
    num_simulations = mo.ui.slider(
        start=100, 
        stop=10000, 
        step=100, 
        value=1000,
        label="Number of simulations:"
    )

    run_simulation = mo.ui.button(
        label="Run Simulation",
        kind="success"
    )

    mo.vstack([
        mo.md("Choose how many games to simulate, then click the button to run:"),
        num_simulations, 
        run_simulation
    ])
    return num_simulations, run_simulation


@app.cell
def _(mo):
    mo.md("""## 🎯 Game Logic""")
    return


@app.cell
def _(random):
    def monty_hall_game(switch_strategy=True):
        """
        Simulate a single Monty Hall game
        Returns True if the player wins, False otherwise
        """
        # Setup: randomly place the car behind one of three doors (0, 1, or 2)
        car_door = random.randint(0, 2)

        # Player initially picks door 0 (doesn't matter which one due to symmetry)
        player_choice = 0

        # Host opens a door that:
        # 1. Is not the player's choice
        # 2. Does not have the car behind it
        available_doors = [door for door in [0, 1, 2] if door != player_choice and door != car_door]
        host_opens = random.choice(available_doors)

        # Remaining door (the one the player can switch to)
        remaining_door = [door for door in [0, 1, 2] if door != player_choice and door != host_opens][0]

        if switch_strategy:
            # Player switches to the remaining door
            final_choice = remaining_door
        else:
            # Player stays with original choice
            final_choice = player_choice

        # Player wins if their final choice matches the car door
        return final_choice == car_door

    return (monty_hall_game,)


@app.cell
def _(mo):
    mo.md("""## 📊 Results""")
    return


@app.cell
def _(mo, monty_hall_game, num_simulations, run_simulation):
    if run_simulation.value:
        # Run simulations for both strategies
        n_sims = num_simulations.value

        # Strategy 1: Always stay
        stay_wins = sum(monty_hall_game(switch_strategy=False) for _ in range(n_sims))
        stay_win_rate = stay_wins / n_sims

        # Strategy 2: Always switch  
        switch_wins = sum(monty_hall_game(switch_strategy=True) for _ in range(n_sims))
        switch_win_rate = switch_wins / n_sims

        # Display results
        results_text = f"""
        ### Simulation Results ({n_sims:,} games)

        **🚪 Stay Strategy:**
        - Wins: {stay_wins:,} out of {n_sims:,}
        - Win Rate: {stay_win_rate:.1%}

        **🔄 Switch Strategy:**
        - Wins: {switch_wins:,} out of {n_sims:,}  
        - Win Rate: {switch_win_rate:.1%}

        **📖 Theoretical Probabilities:**
        - Stay: 33.33% (1/3)
        - Switch: 66.67% (2/3)

        ---

        💡 **Why does switching work?** When you first pick a door, there's a 1/3 chance the car is behind it and a 2/3 chance it's behind one of the other two doors. When the host eliminates one of those doors (always showing a goat), that 2/3 probability transfers entirely to the remaining door!
        """

        simulation_results = {
            'stay_wins': stay_wins,
            'switch_wins': switch_wins,
            'stay_rate': stay_win_rate,
            'switch_rate': switch_win_rate,
            'n_sims': n_sims
        }
    else:
        results_text = "👆 Click **'Run Simulation'** above to see results!"
        simulation_results = None

    mo.md(results_text)
    return (simulation_results,)


@app.cell
def _(mo, alt, pd, simulation_results):
    if simulation_results:
        # Create data for bar chart
        bar_data = pd.DataFrame({
            'Strategy': ['Stay', 'Stay', 'Switch', 'Switch'],
            'Type': ['Simulation', 'Theoretical', 'Simulation', 'Theoretical'],
            'Win Rate': [simulation_results['stay_rate'], 1/3, simulation_results['switch_rate'], 2/3]
        })

        # Create bar chart
        bar_chart = alt.Chart(bar_data).mark_bar().encode(
            x='Strategy',
            y='Win Rate',
            color='Type',
            column='Strategy'
        ).properties(
            title='Monty Hall: Win Rates Comparison'
        )

        # Add text labels
        text = bar_chart.mark_text(
            align='center',
            baseline='bottom',
            dy=-5
        ).encode(
            text=alt.Text('Win Rate:Q', format='.1%')
        )

        # Combine bar chart and text
        win_rate_chart = (bar_chart + text).properties(width=200)

        # Create data for pie chart
        pie_data = pd.DataFrame({
            'Outcome': ['Stay Wins', 'Switch Wins'],
            'Value': [simulation_results['stay_wins'], simulation_results['switch_wins']]
        })

        # Create pie chart
        pie_chart = alt.Chart(pie_data).mark_arc().encode(
            theta='Value',
            color='Outcome',
            tooltip=['Outcome', 'Value']
        ).properties(
            title=f'Distribution of Wins ({simulation_results["n_sims"]:,} total games)',
            width=300,
            height=300
        )

        # Combine charts
        final_chart = alt.hconcat(win_rate_chart, pie_chart)

        mo.vspace(1)
        mo.altair_chart(final_chart)
    else:
        mo.md("*Visualization will appear after running simulation*")
    return


if __name__ == "__main__":
    app.run()
