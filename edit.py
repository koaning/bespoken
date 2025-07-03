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


@app.cell
def _(random):
    def monty_hall_game(switch_strategy=True):
        """
        Simulate a single Monty Hall game
        Returns True if the player wins, False otherwise
        """
        car_door = random.randint(0, 2)
        player_choice = 0
        available_doors = [door for door in [0, 1, 2] if door != player_choice and door != car_door]
        host_opens = random.choice(available_doors)
        remaining_door = [door for door in [0, 1, 2] if door != player_choice and door != host_opens][0]

        if switch_strategy:
            final_choice = remaining_door
        else:
            final_choice = player_choice

        return final_choice == car_door

    return (monty_hall_game,)


@app.cell
def _(monty_hall_game):
    # Run simulations
    n_sims = 10000

    stay_wins = sum(monty_hall_game(switch_strategy=False) for _ in range(n_sims))
    stay_win_rate = stay_wins / n_sims

    switch_wins = sum(monty_hall_game(switch_strategy=True) for _ in range(n_sims))
    switch_win_rate = switch_wins / n_sims

    simulation_results = {
        'stay_wins': stay_wins,
        'switch_wins': switch_wins,
        'stay_rate': stay_win_rate,
        'switch_rate': switch_win_rate,
        'n_sims': n_sims
    }
    return (simulation_results,)


@app.cell
def _(mo, simulation_results):
    results_text = f"""
    ## 📊 Simulation Results

    We ran a simulation of the Monty Hall problem with {simulation_results['n_sims']:,} games for each strategy. Here are the results:

    **🚪 Stay Strategy:**
    - Wins: {simulation_results['stay_wins']:,} out of {simulation_results['n_sims']:,}
    - Win Rate: {simulation_results['stay_rate']:.1%}

    **🔄 Switch Strategy:**
    - Wins: {simulation_results['switch_wins']:,} out of {simulation_results['n_sims']:,}  
    - Win Rate: {simulation_results['switch_rate']:.1%}

    **📖 Theoretical Probabilities:**
    - Stay: 33.33% (1/3)
    - Switch: 66.67% (2/3)

    As we can see, the simulation results closely match the theoretical probabilities, confirming that switching doors is indeed the optimal strategy in the Monty Hall problem.
    """

    mo.md(results_text)
    return


@app.cell
def _(alt, pd, simulation_results):
    # Prepare data for charts
    win_rates_data = pd.DataFrame({
        'Strategy': ['Stay', 'Switch', 'Stay (Theoretical)', 'Switch (Theoretical)'],
        'Win Rate': [simulation_results['stay_rate'], simulation_results['switch_rate'], 1/3, 2/3],
        'Type': ['Simulation', 'Simulation', 'Theoretical', 'Theoretical']
    })

    # Bar chart of win rates
    win_rates_chart = alt.Chart(win_rates_data).mark_bar().encode(
        x=alt.X('Strategy:N', axis=alt.Axis(labelAngle=0)),
        y=alt.Y('Win Rate:Q', axis=alt.Axis(format='.0%')),
        color='Type:N',
        column=alt.Column('Type:N', header=alt.Header(labelOrient='bottom'))
    ).properties(
        title='Monty Hall: Win Rates Comparison',
        width=200
    )

    # Pie chart of wins distribution
    wins_data = pd.DataFrame({
        'Strategy': ['Stay', 'Switch'],
        'Wins': [simulation_results['stay_wins'], simulation_results['switch_wins']]
    })

    pie_chart = alt.Chart(wins_data).mark_arc().encode(
        theta='Wins:Q',
        color='Strategy:N',
        tooltip=['Strategy', 'Wins']
    ).properties(
        title=f"Distribution of Wins ({simulation_results['n_sims']:,} total games)",
        width=300,
        height=300
    )

    # Display charts
    charts = alt.vconcat(win_rates_chart, pie_chart)
    return


@app.cell
def _(mo):
    mo.md("""
    ## 🧠 Conclusion

    The Monty Hall problem demonstrates a counterintuitive result in probability theory. Our simulation confirms the theoretical prediction:

    1. **Staying with the initial choice** gives a win rate of about 33% (1/3).
    2. **Switching to the other door** gives a win rate of about 67% (2/3).

    This outcome occurs because:

    1. Initially, there's a 1/3 chance the car is behind the chosen door and a 2/3 chance it's behind one of the other two doors.
    2. When the host opens a door with a goat, they're using their knowledge of the car's location, which provides new information.
    3. If you initially chose the car (1/3 chance), switching makes you lose. But if you initially chose a goat (2/3 chance), switching makes you win.

    Therefore, switching doubles your chances of winning from 1/3 to 2/3. This unintuitive result highlights the importance of considering all available information and the power of conditional probability in decision-making.

    Remember: In the Monty Hall problem, always switch for the best chance of winning!
    """)
    return


if __name__ == "__main__":
    app.run()
