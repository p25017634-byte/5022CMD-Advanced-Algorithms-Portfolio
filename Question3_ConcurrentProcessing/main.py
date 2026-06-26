"""
Question 3 - Factorial calculation using multithreading and single-thread comparison.
Run: python q3_factorial_concurrent_processing.py
"""
import threading
import time
import statistics
import matplotlib.pyplot as plt

NUMBERS = [50, 100, 200]
ROUNDS = 10

def factorial(n: int) -> int:
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def worker(n: int, results: dict):
    results[n] = factorial(n)

def run_multithreaded(numbers=NUMBERS):
    results = {}
    threads = [threading.Thread(target=worker, args=(n, results)) for n in numbers]
    start = time.perf_counter_ns()
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    end = time.perf_counter_ns()
    return end - start, results

def run_single_threaded(numbers=NUMBERS):
    results = {}
    start = time.perf_counter_ns()
    for n in numbers:
        results[n] = factorial(n)
    end = time.perf_counter_ns()
    return end - start, results

def draw_graph(mt_times, st_times):
    rounds = list(range(1, len(mt_times) + 1))

    plt.figure(figsize=(10, 6))

    plt.plot(
        rounds,
        mt_times,
        marker='o',
        linewidth=2,
        label='Multithreading'
    )

    plt.plot(
        rounds,
        st_times,
        marker='s',
        linewidth=2,
        label='Single-thread'
    )

    plt.title("Execution Time Comparison: Multithreading vs Single-threaded")
    plt.xlabel("Round")
    plt.ylabel("Execution Time (ns)")
    plt.xticks(rounds)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend()
    plt.tight_layout()

    plt.show()

def draw_average_graph(mt_times, st_times):
    avg_mt = statistics.mean(mt_times)
    avg_st = statistics.mean(st_times)

    plt.figure(figsize=(6,5))

    plt.bar(
        ["Multithreading", "Single-thread"],
        [avg_mt, avg_st]
    )

    plt.ylabel("Average Execution Time (ns)")
    plt.title("Average Execution Time Comparison")

    plt.tight_layout()
    plt.show()

def experiment(rounds=ROUNDS):
    mt_times, st_times = [], []
    print("===== Factorial Timing Experiment =====")
    print("Round   Multithreading(ns)   Single-thread(ns)")
    for r in range(1, rounds + 1):
        mt_time, mt_results = run_multithreaded()
        st_time, st_results = run_single_threaded()
        assert mt_results == st_results
        mt_times.append(mt_time)
        st_times.append(st_time)
        print(f"{r:<7} {mt_time:>18}   {st_time:>17}")
    print("\nAverage multithreading time (ns):", round(statistics.mean(mt_times), 2))
    print("Average single-thread time (ns):", round(statistics.mean(st_times), 2))
    print("Fastest multithreading time (ns):", min(mt_times))
    print("Fastest single-thread time (ns):", min(st_times))
    print("\nSample result lengths:")
    for n, value in st_results.items():
        print(f"{n}! contains {len(str(value))} digits")

    draw_graph(mt_times, st_times)
    draw_average_graph(mt_times, st_times)

if __name__ == "__main__":
    experiment()

