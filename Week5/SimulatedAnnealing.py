import random
import math
import time
import pandas as pd


def initialize_board(n=8):
    return [random.randint(0, n - 1) for _ in range(n)]


def calculate_cost(board):
    attacking_pairs = 0
    n = len(board)

    for i in range(n):
        for j in range(i + 1, n):
            if board[i] == board[j] or abs(board[i] - board[j]) == j - i:
                attacking_pairs += 1
    return attacking_pairs


def generate_neighbor(board):
    n = len(board)
    new_board = board[:]
    row = random.randint(0, n - 1)
    new_board[row] = random.randint(0, n - 1)
    return new_board


def simulated_annealing(schedule, max_time=10, n=8, T0=100, alpha=0.9, beta=1.0, gamma=1.0):
    start_time = time.time()
    board = initialize_board(n)
    current_cost = calculate_cost(board)
    best_board = board[:]
    best_cost = current_cost
    k = 0

    while time.time() - start_time < max_time:
        T = schedule(T0, k, alpha, beta, gamma)
        if T == 0:
            break

        new_board = generate_neighbor(board)
        new_cost = calculate_cost(new_board)

        if new_cost < current_cost:
            board = new_board[:]
            current_cost = new_cost
        else:
            p = math.exp(-(new_cost - current_cost) / T)
            if random.random() < p:
                board = new_board[:]
                current_cost = new_cost

        if current_cost < best_cost:
            best_board = board[:]
            best_cost = current_cost

        k += 1

    return best_board, best_cost, time.time() - start_time


def exponential_schedule(T0, k, alpha, beta, gamma):
    return T0 * (alpha ** k)


def linear_schedule(T0, k, alpha, beta, gamma):
    return max(0, T0 - beta * k)


def logarithmic_schedule(T0, k, alpha, beta, gamma):
    return T0 / (1 + gamma * math.log(1 + k))

def run_experiments():
    schedules = {
        "Exponential": exponential_schedule,
        "Linear": linear_schedule,
        "Logarithmic": logarithmic_schedule
    }

    execution_times = [10, 50, 100]
    results = []
    best_overall_result = None

    for schedule_name, schedule_fn in schedules.items():
        for max_time in execution_times:
            best_board, best_cost, total_time = simulated_annealing(schedule_fn, max_time=max_time)
            results.append((schedule_name, max_time, best_cost, total_time))
            print(f"Schedule: {schedule_name}, Time: {max_time}s, Best Cost: {best_cost}, Total Time: {total_time:.2f}s")

            # Track the best result across all experiments
            if best_overall_result is None or best_cost < best_overall_result[2]:
                # Update best if this has a lower cost
                best_overall_result = (schedule_name, max_time, best_cost, total_time, best_board)
            elif best_cost == best_overall_result[2] and total_time < best_overall_result[3]:
                # If costs are equal, choose the one with the lower time
                best_overall_result = (schedule_name, max_time, best_cost, total_time, best_board)

    return results, best_overall_result


results, best_overall_result = run_experiments()

df = pd.DataFrame(results, columns=["Schedule", "Execution Time (s)", "Best Cost", "Total Time (s)"])
print("\nFinal Results:")
print(df)

if best_overall_result:
    print(f"\nBest Overall Result:\nSchedule: {best_overall_result[0]}, "
          f"Time: {best_overall_result[1]}s, Best Cost: {best_overall_result[2]}, "
          f"Total Time: {best_overall_result[3]:.2f}s, Board: {best_overall_result[4]}")
