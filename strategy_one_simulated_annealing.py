import random
import math

# Function to calculate portfolio return
def portfolio_return(weights, returns):
    return sum(weights[i] * returns[i] for i in range(len(weights)))

def simulated_annealing_high_growth(initial_weights, returns, cooling_rate=0.003, num_iterations=1000):
    """
    Simulated Annealing algorithm for optimizing portfolio weights for the High Growth Stocks Portfolio.

    Args:
    - initial_weights: List of initial weights for the stocks.
    - returns: List of returns for the stocks.
    - cooling_rate: Rate of cooling for the simulated annealing algorithm (default: 0.003).
    - num_iterations: Number of iterations for the algorithm (default: 1000).

    Returns:
    - Tuple containing:
        - List of optimized portfolio weights rounded to 4 decimal places.
        - Optimized portfolio return.
    """

    initial_cost = portfolio_return(initial_weights, returns)
    temperature = 1000

    # Define the best weights and cost
    best_weights = initial_weights.copy()
    best_cost = initial_cost

    for _ in range(num_iterations):
        # Generate a new candidate solution by perturbing the current weights
        new_weights = initial_weights.copy()

        # Perturb weights for each sector
        for j in range(len(new_weights)):
            new_weights[j] += random.uniform(-0.01, 0.01)
            if new_weights[j] < 0:
                new_weights[j] = 0

        # Normalize to ensure the weights add up to 1
        total_weights = sum(new_weights)
        new_weights = [w / total_weights for w in new_weights]

        # Calculate the new cost (portfolio return)
        new_cost = portfolio_return(new_weights, returns)

        # Calculate the difference in cost
        delta_cost = new_cost - initial_cost

        # Acceptance probability
        acceptance_prob = math.exp(delta_cost / temperature)

        # Accept the new solution with a probability
        if delta_cost > 0 or random.random() < acceptance_prob:
            initial_weights = new_weights
            initial_cost = new_cost

            # Update the best solution if needed
            if new_cost > best_cost:
                best_weights = new_weights
                best_cost = new_cost

        # Update the temperature
        temperature *= 1 - cooling_rate

    # Round the optimized weights to 4 decimal places
    rounded_weights = [round(w, 4) for w in best_weights]

    return rounded_weights, best_cost


# Example usage
initial_weights = [0.2, 0.2, 0.2, 0.15, 0.15, 0.03, 0.02, 0.02, 0.02, 0.01]  
returns = [21.22, 41.75, 27.13, 0.81, 5.33, 6.68, 34.69, 18.5, 41.9, 23.81]  

# Print initial weights and returns
print("Initial Weights:", initial_weights)
print("Initial Portfolio Return:", portfolio_return(initial_weights, returns))
print()

# Run simulated annealing for high growth portfolio
optimized_weights, optimized_return = simulated_annealing_high_growth(initial_weights, returns)

# Print optimized results
print("Optimized Weights:", optimized_weights)
print("Optimized Portfolio Return:", optimized_return)
