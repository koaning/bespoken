import marimo

__generated_with = "0.14.0"
app = marimo.App(width="columns")


@app.cell
def __():
    import marimo as mo
    return mo,


@app.cell
def __(mo):
    mo.md(
        r"""
        # The Monty Hall Problem Simulator 🎲

        A famous probability puzzle: You pick one of 3 doors (car behind one, goats behind two). The host opens a door with a goat, then asks if you want to switch.

        **The counterintuitive answer:** Always switch! You get a **66.7%** chance of winning vs **33.3%** if you stay.

        Use the controls below to see this in action!
        """
    )
    return


@app.cell
def __():
    import random
    import numpy as np
    import matplotlib.pyplot as plt
    import pandas as pd
    return random, np, plt, pd





@app.cell
def __(mo):
    mo.md("## 🎮 Simulation Controls")
    return


@app.cell
def __(mo):
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
def __(mo):
    mo.md("## 🎯 Game Logic")
    return


@app.cell
def __(random):
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
    
    return monty_hall_game,


@app.cell
def __(mo):
    mo.md("## 📊 Results")
    return


@app.cell
def __(run_simulation, num_simulations, monty_hall_game, np, mo):
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
    return simulation_results, results_text, stay_wins, switch_wins, stay_win_rate, switch_win_rate


@app.cell
def __(simulation_results, plt, mo):
    if simulation_results:
        # Create visualization
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # Bar chart of win rates
        strategies = ['Stay', 'Switch']
        win_rates = [simulation_results['stay_rate'], simulation_results['switch_rate']]
        theoretical_rates = [1/3, 2/3]
        
        x = range(len(strategies))
        width = 0.35
        
        ax1.bar([i - width/2 for i in x], win_rates, width, label='Simulation', alpha=0.8, color='skyblue')
        ax1.bar([i + width/2 for i in x], theoretical_rates, width, label='Theoretical', alpha=0.8, color='lightcoral')
        
        ax1.set_ylabel('Win Rate')
        ax1.set_title('Monty Hall: Win Rates Comparison')
        ax1.set_xticks(x)
        ax1.set_xticklabels(strategies)
        ax1.legend()
        ax1.set_ylim(0, 1)
        
        # Add percentage labels on bars
        for i, (sim_rate, theo_rate) in enumerate(zip(win_rates, theoretical_rates)):
            ax1.text(i - width/2, sim_rate + 0.01, f'{sim_rate:.1%}', ha='center', va='bottom')
            ax1.text(i + width/2, theo_rate + 0.01, f'{theo_rate:.1%}', ha='center', va='bottom')
        
        # Pie chart showing the advantage of switching
        labels = ['Stay Wins', 'Switch Wins']
        sizes = [simulation_results['stay_wins'], simulation_results['switch_wins']]
        colors = ['lightcoral', 'skyblue']
        
        ax2.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        ax2.set_title(f'Distribution of Wins\n({simulation_results["n_sims"]:,} total games)')
        
        plt.tight_layout()
        mo.mpl.output(fig)
    else:
        mo.md("*Visualization will appear after running simulation*")
    return ax1, ax2, fig, strategies, theoretical_rates, win_rates, x, width





if __name__ == "__main__":
    app.run()