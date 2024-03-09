import random
import math

# Function to calculate portfolio return
def portfolio_return(weights, returns):
    return sum(weights[i] * returns[i] for i in range(len(weights)))

# Function to calculate portfolio risk (standard deviation)
def portfolio_risk(weights, risks):
    return (sum((weights[i] * risks[i]) ** 2 for i in range(len(weights)))) ** 0.5

def simulated_annealing_minimize_risk(returns, risks, target_return=15, cooling_rate=0.003, num_iterations=1000):
    """
    Simulated Annealing algorithm for minimizing portfolio risk while keeping return above target.

    Args:
    - returns: List of returns for the stocks.
    - risks: List of risks (standard deviation) for the stocks.
    - target_return: Minimum desired portfolio return (default: 15).
    - cooling_rate: Rate of cooling for the simulated annealing algorithm (default: 0.003).
    - num_iterations: Number of iterations for the algorithm (default: 1000).

    Returns:
    - Tuple containing:
        - List of optimized portfolio weights rounded to 4 decimal places.
        - Optimized portfolio return.
        - Optimized portfolio risk.
    """

    # Generate random initial weights
    num_stocks = len(returns)
    initial_weights = [random.random() for _ in range(num_stocks)]
    total_weight = sum(initial_weights)
    initial_weights = [round(w / total_weight, 4) for w in initial_weights]

    initial_cost = portfolio_return(initial_weights, returns)
    initial_risk = portfolio_risk(initial_weights, risks)
    print("Initial Weights:", initial_weights)
    print("Initial Portfolio Return:", initial_cost)
    print("Initial Portfolio Risk:", initial_risk)
    print()

    temperature = 1000

    # Define the best weights, cost, and risk
    best_weights = initial_weights.copy()
    best_cost = initial_cost
    best_risk = initial_risk

    for _ in range(num_iterations):
        # Generate a new candidate solution by perturbing the current weights
        new_weights = initial_weights.copy()

        # Perturb weights for each stock
        for j in range(len(new_weights)):
            new_weights[j] += random.uniform(-0.02, 0.02)
            if new_weights[j] < 0:
                new_weights[j] = 0

        # Normalize to ensure the weights add up to 1
        total_weights = sum(new_weights)
        new_weights = [w / total_weights for w in new_weights]

        # Calculate the new cost (portfolio return)
        new_cost = portfolio_return(new_weights, returns)

        # Calculate the new risk (portfolio risk)
        new_risk = portfolio_risk(new_weights, risks)

        # Calculate the difference in cost and risk
        delta_cost = new_cost - target_return
        delta_risk = new_risk - best_risk

        # Accept the new solution if it meets the criteria
        if delta_cost >= 0 and delta_risk < 0:
            initial_weights = new_weights
            best_weights = new_weights
            best_cost = new_cost
            best_risk = new_risk

        # Update the temperature
        temperature *= 1 - cooling_rate

    # Round the optimized weights to 4 decimal places
    rounded_weights = [round(w, 4) for w in best_weights]

    return rounded_weights, best_cost, best_risk

# Example usage
returns = [21.22, 41.75, 27.13, 0.81, 5.33, 6.68, 34.69, 18.5, 41.9, 23.81]  
risks = [25.93, 25.47, 20.98, 19.98, 25.96, 24.02, 28.0, 31.38, 25.23, 27.03]  

# Run simulated annealing for minimizing risk while keeping return at least 15%
optimized_weights, optimized_return, optimized_risk = simulated_annealing_minimize_risk(returns, risks)

# Print optimized results
print("Optimized Weights:", optimized_weights)
print("Optimized Portfolio Return:", optimized_return)
print("Optimized Portfolio Risk:", optimized_risk)
