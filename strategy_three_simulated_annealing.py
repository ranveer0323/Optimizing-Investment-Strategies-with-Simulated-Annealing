import random
import math
import numpy as np

# Function to calculate portfolio return
def portfolio_return(weights, returns):
    return sum(weights[i] * returns[i] for i in range(len(weights)))

# Function to calculate portfolio risk (standard deviation)
def portfolio_risk(weights, cov_matrix):
    return math.sqrt(sum(weights[i] * weights[j] * cov_matrix[i][j] for i in range(len(weights)) for j in range(len(weights))))

# Function to calculate covariance matrix based on risk and returns
def calculate_cov_matrix(returns):
    num_stocks = len(returns)
    cov_matrix = np.zeros((num_stocks, num_stocks))
    
    for i in range(num_stocks):
        for j in range(num_stocks):
            if i == j:
                cov_matrix[i][j] = (returns[i] / 100)**2  # Converting returns to decimal
            else:
                cov_matrix[i][j] = 0.5 * returns[i] * returns[j] / 10000  # Converting returns to decimal
        
    return cov_matrix

# Simulated Annealing algorithm with random initial weights
def simulated_annealing_minimize_risk(returns, num_iterations, cooling_rate, initial_temperature):
    best_risk = float('inf')
    best_weights = []

    temperature = initial_temperature

    for _ in range(num_iterations):
        # Generate random initial weights
        current_weights = [random.random() for _ in range(len(returns))]
        total_weights = sum(current_weights)
        current_weights = [w / total_weights for w in current_weights]

        # Calculate initial portfolio risk
        current_risk = portfolio_risk(current_weights, cov_matrix)

        for _ in range(num_iterations):
            # Generate a new candidate solution by perturbing the current weights
            new_weights = current_weights.copy()

            # Perturb weights
            for j in range(len(new_weights)):
                new_weights[j] += random.uniform(-0.02, 0.02)  # Tighter range for perturbation
                if new_weights[j] < 0:
                    new_weights[j] = 0

            # Normalize weights
            total_weights = sum(new_weights)
            new_weights = [w / total_weights for w in new_weights]

            # Calculate the new portfolio risk
            new_risk = portfolio_risk(new_weights, cov_matrix)

            # Calculate the difference in risk
            delta_risk = new_risk - best_risk  # Difference from best risk found so far

            # Calculate the cost based on minimizing risk
            cost = delta_risk

            # Accept the new solution if it results in lower risk or with a probability
            if new_risk < best_risk or random.random() < math.exp(-cost / temperature):
                current_weights = new_weights
                current_risk = new_risk

                # Update the best solution if needed
                if new_risk < best_risk:
                    best_weights = new_weights
                    best_risk = new_risk

        # Update the temperature
        temperature *= 1 - cooling_rate

    return best_weights, best_risk

# Define returns for the stocks
returns = [21.22, 41.75, 27.13, 0.81, 5.33, 6.68, 34.69, 18.5, 41.9, 23.81]  # Example returns for the stocks

# Calculate the covariance matrix based on the returns
cov_matrix = calculate_cov_matrix(returns)

# Define optimization parameters
num_iterations = 1000
cooling_rate = 0.003
initial_temperature = 1000  # Initial temperature for simulated annealing

# Run the simulated annealing algorithm
best_weights, best_risk = simulated_annealing_minimize_risk(returns, num_iterations, cooling_rate, initial_temperature)

# Calculate risk and return for initial weights
initial_weights = [1 / len(returns) for _ in returns]
initial_portfolio_return = portfolio_return(initial_weights, returns)
initial_portfolio_risk = portfolio_risk(initial_weights, cov_matrix) * 100  # Convert to percentage

# Calculate risk and return for optimized weights
optimized_portfolio_return = portfolio_return(best_weights, returns)
optimized_portfolio_risk = best_risk * 100  # Convert to percentage

# Print the results
print("Initial Portfolio Weights:", [round(w, 4) for w in initial_weights])
print("Initial Portfolio Return:", round(initial_portfolio_return, 4))
print("Initial Portfolio Risk:", round(initial_portfolio_risk, 4), "%")
print("---------------------------------------------")
print("Optimized Portfolio Weights:", [round(w, 4) for w in best_weights])
print("Optimized Portfolio Return:", round(optimized_portfolio_return, 4))
print("Optimized Portfolio Risk:", round(optimized_portfolio_risk, 4), "%")
