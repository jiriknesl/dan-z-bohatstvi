import numpy as np
import matplotlib.pyplot as plt

# Parameters
num_simulations = 1000
num_years = 30
initial_value = 1000000  # Initial portfolio value for each asset

# Asset returns (annual) and their risk profiles (standard deviation)
assets = {
    "SP500": {"return": 0.08, "std_dev": 0.18},
    "Land": {"return": 0.03, "std_dev": 0.10},
    "Rental_Property": {"return": 0.07, "std_dev": 0.15},
    "Business": {"return": 0.10, "std_dev": 0.25},
    "Balanced_Portfolio": {"return": (0.08 + 0.03 + 0.07 + 0.10) / 4, "std_dev": (0.18 + 0.10 + 0.15 + 0.25) / 4}  # Average return and standard deviation
}

# Other parameters
inflation_rate = 0.03
wealth_tax_rate = 0.035

# Function to run the Monte Carlo simulation
def monte_carlo_simulation(initial_value, assets, num_simulations, num_years, inflation_rate, wealth_tax_rate):
    results = {asset: np.zeros((num_simulations, num_years)) for asset in assets}
    time_to_half_value = {asset: [] for asset in assets}
    total_wealth_tax = {asset: 0 for asset in assets}
    total_inflation = {asset: 0 for asset in assets}

    for asset in assets:
        for i in range(num_simulations):
            portfolio_value = initial_value
            for year in range(num_years):
                annual_return = np.random.normal(assets[asset]["return"], assets[asset]["std_dev"])  # Using specific standard deviation for each asset
                initial_portfolio_value = portfolio_value
                portfolio_value *= (1 + annual_return)
                portfolio_value_after_inflation = portfolio_value * (1 - inflation_rate)
                total_inflation[asset] += portfolio_value - portfolio_value_after_inflation
                portfolio_value = portfolio_value_after_inflation
                portfolio_value_after_wealth_tax = portfolio_value * (1 - wealth_tax_rate)
                total_wealth_tax[asset] += portfolio_value - portfolio_value_after_wealth_tax
                portfolio_value = portfolio_value_after_wealth_tax
                results[asset][i, year] = portfolio_value
                
                if portfolio_value <= 500000 and len(time_to_half_value[asset]) < i + 1:
                    time_to_half_value[asset].append(year + 1)  # Year + 1 because year is 0-indexed

    avg_time_to_half_value = {asset: np.mean(time_to_half_value[asset]) if time_to_half_value[asset] else np.inf for asset in assets}
    
    return results, avg_time_to_half_value, total_wealth_tax, total_inflation

# Run the simulation
simulation_results, avg_time_to_half_value, total_wealth_tax, total_inflation = monte_carlo_simulation(initial_value, assets, num_simulations, num_years, inflation_rate, wealth_tax_rate)

# Plotting the results
for asset in assets:
    plt.figure(figsize=(12, 8))
    for i in range(num_simulations):
        plt.plot(simulation_results[asset][i], alpha=0.1, color='grey')
    plt.plot(np.mean(simulation_results[asset], axis=0), label=f'Average {asset}', color='blue')
    plt.axhline(y=500000, color='red', linestyle='--')
    plt.xlabel('Years')
    plt.ylabel('Portfolio Value (EUR)')
    plt.title(f'Monte Carlo Simulation of {asset} Development\nAverage Time to Reach 500,000 EUR: {avg_time_to_half_value[asset]:.2f} years')
    plt.legend()
    plt.show()

# Calculate average return and the impact of wealth tax and inflation for each asset
for asset in assets:
    avg_return = np.mean(simulation_results[asset][:, -1]) / initial_value - 1
    total_value_created = initial_value * (1 + avg_return)
    total_wealth_tax_collected = total_wealth_tax[asset] / num_simulations
    total_inflation_impact = total_inflation[asset] / num_simulations
    percent_wealth_tax = (total_wealth_tax_collected / total_value_created) * 100
    percent_inflation = (total_inflation_impact / total_value_created) * 100

    print(f'Asset: {asset}')
    print(f'  - Average return over {num_years} years: {avg_return * 100:.2f}%')
    print(f'  - Average time to reach 500,000 EUR: {avg_time_to_half_value[asset]:.2f} years')
    print(f'  - Total wealth tax collected: {total_wealth_tax_collected:.2f} EUR ({percent_wealth_tax:.2f}% of total value created)')
    print(f'  - Total impact of inflation: {total_inflation_impact:.2f} EUR ({percent_inflation:.2f}% of total value created)')
