"""
Question 2 - Divide and Conquer system using Merge Sort and Binary Search.
Run normally for the CLI menu: python q2_transactions_divide_conquer.py
Run demo mode for report output: python q2_transactions_divide_conquer.py --demo
"""
from dataclasses import dataclass
from datetime import date
import time
import sys
import matplotlib.pyplot as plt

@dataclass
class Transaction:
    transaction_id: int
    customer_name: str
    product_name: str
    amount: float
    transaction_date: date

    def __str__(self):
        return (f"TX{self.transaction_id:04d} | {self.customer_name:<12} | {self.product_name:<18} | "
                f"RM{self.amount:>7.2f} | {self.transaction_date.isoformat()}")

class MergeSortStats:
    def __init__(self):
        self.recursive_calls = 0
        self.comparisons = 0

def merge_sort(transactions, key=lambda t: t.transaction_id, stats=None):
    if stats is not None:
        stats.recursive_calls += 1
    if len(transactions) <= 1:
        return transactions[:]
    mid = len(transactions) // 2
    left = merge_sort(transactions[:mid], key, stats)
    right = merge_sort(transactions[mid:], key, stats)
    return merge(left, right, key, stats)

def merge(left, right, key, stats=None):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if stats is not None:
            stats.comparisons += 1
        if key(left[i]) <= key(right[j]):
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

def binary_search(sorted_transactions, target_id):
    low, high = 0, len(sorted_transactions) - 1
    comparisons = 0
    while low <= high:
        comparisons += 1
        mid = (low + high) // 2
        mid_id = sorted_transactions[mid].transaction_id
        if mid_id == target_id:
            return sorted_transactions[mid], comparisons
        if target_id < mid_id:
            high = mid - 1
        else:
            low = mid + 1
    return None, comparisons

def linear_search(transactions, target_id):
    comparisons = 0
    for item in transactions:
        comparisons += 1
        if item.transaction_id == target_id:
            return item, comparisons
    return None, comparisons

def sample_transactions():
    return [
        Transaction(1028, "Alicia", "Keyboard", 129.90, date(2026, 5, 2)),
        Transaction(1003, "Brian", "Mouse", 59.90, date(2026, 5, 4)),
        Transaction(1055, "Carmen", "Monitor", 699.00, date(2026, 5, 5)),
        Transaction(1012, "Daniel", "USB-C Hub", 89.50, date(2026, 5, 7)),
        Transaction(1039, "Evelyn", "Laptop Stand", 75.00, date(2026, 5, 9)),
        Transaction(1007, "Fikri", "Webcam", 155.00, date(2026, 5, 11)),
        Transaction(1064, "Grace", "SSD 1TB", 389.90, date(2026, 5, 12)),
        Transaction(1021, "Hafiz", "Headset", 119.90, date(2026, 5, 15)),
        Transaction(1048, "Irene", "Printer", 349.00, date(2026, 5, 18)),
        Transaction(1018, "Jason", "Router", 188.00, date(2026, 5, 20)),
        Transaction(1072, "Kelly", "Tablet", 999.00, date(2026, 5, 23)),
        Transaction(1031, "Lucas", "Power Bank", 79.90, date(2026, 5, 25)),
    ]

def display(transactions):
    print("Transaction records:")
    for item in transactions:
        print(item)

def compare_search_performance(transactions, target_existing=1048, target_missing=1999, rounds=3000):
    sorted_records = merge_sort(transactions)
    rows = []
    for target in [target_existing, target_missing]:
        start = time.perf_counter_ns()
        for _ in range(rounds):
            binary_search(sorted_records, target)
        binary_time = (time.perf_counter_ns() - start) / rounds
        start = time.perf_counter_ns()
        for _ in range(rounds):
            linear_search(transactions, target)
        linear_time = (time.perf_counter_ns() - start) / rounds
        _, bc = binary_search(sorted_records, target)
        _, lc = linear_search(transactions, target)
        rows.append((target, binary_time, linear_time, bc, lc))
    return rows

def draw_search_graph(transactions):
    rows = compare_search_performance(transactions, rounds=3000)

    targets = [f"TX{row[0]}" for row in rows]

    binary_times = [row[1] for row in rows]
    linear_times = [row[2] for row in rows]

    binary_comps = [row[3] for row in rows]
    linear_comps = [row[4] for row in rows]

    x = range(len(targets))
    width = 0.35

    # -------------------------
    # Graph 1 : Execution Time
    # -------------------------
    plt.figure(figsize=(8,5))

    plt.bar(
        [i - width/2 for i in x],
        binary_times,
        width,
        label="Binary Search"
    )

    plt.bar(
        [i + width/2 for i in x],
        linear_times,
        width,
        label="Linear Search"
    )

    plt.title("Execution Time Comparison")
    plt.xlabel("Target Transaction")
    plt.ylabel("Average Execution Time (ns)")
    plt.xticks(list(x), targets)
    plt.legend()
    plt.grid(axis="y", linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.show()

    # -------------------------
    # Graph 2 : Comparisons
    # -------------------------
    plt.figure(figsize=(8,5))

    plt.bar(
        [i - width/2 for i in x],
        binary_comps,
        width,
        label="Binary Search"
    )

    plt.bar(
        [i + width/2 for i in x],
        linear_comps,
        width,
        label="Linear Search"
    )

    plt.title("Number of Comparisons")
    plt.xlabel("Target Transaction")
    plt.ylabel("Comparisons")
    plt.xticks(list(x), targets)
    plt.legend()
    plt.grid(axis="y", linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.show()

def insert_transaction(records):
    tid = int(input("Enter transaction ID: "))
    name = input("Enter customer name: ")
    product = input("Enter product name: ")
    amount = float(input("Enter amount: "))
    y, m, d = map(int, input("Enter date YYYY-MM-DD: ").split("-"))
    records.append(Transaction(tid, name, product, amount, date(y, m, d)))
    print("Transaction inserted successfully")

def menu():
    records = sample_transactions()
    sorted_records = None
    while True:
        print("\n===== Online Shopping Transaction System =====")
        print("1. Display all transactions")
        print("2. Sort by transaction ID using Merge Sort")
        print("3. Search transaction using Binary Search")
        print("4. Search transaction using Linear Search")
        print("5. Insert new transaction")
        print("6. Sort by amount")
        print("7. Display complexity table")
        print("8. Compare search performance")
        print("0. Exit")
        choice = input("Enter choice: ").strip()
        if choice == "1": display(records)
        elif choice == "2":
            stats = MergeSortStats()
            sorted_records = merge_sort(records, stats=stats)
            display(sorted_records)
            print(f"Recursive calls: {stats.recursive_calls}, Comparisons: {stats.comparisons}")
        elif choice == "3":
            if sorted_records is None: sorted_records = merge_sort(records)
            target = int(input("Enter transaction ID: "))
            found, comps = binary_search(sorted_records, target)
            print(found if found else "Transaction not found")
            print("Comparisons:", comps)
        elif choice == "4":
            target = int(input("Enter transaction ID: "))
            found, comps = linear_search(records, target)
            print(found if found else "Transaction not found")
            print("Comparisons:", comps)
        elif choice == "5": insert_transaction(records); sorted_records = None
        elif choice == "6": display(merge_sort(records, key=lambda t: t.amount))
        elif choice == "7": print("Merge Sort: O(n log n) | Binary Search: O(log n) | Linear Search: O(n)")
        elif choice == "8":
            print("Target   Binary(ns)   Linear(ns)   Binary comps   Linear comps")
            rows = compare_search_performance(records)
            for row in rows:
                print(f"{row[0]:<8} {row[1]:>10.2f} {row[2]:>11.2f} {row[3]:>13} {row[4]:>13}")
            draw_search_graph(records)
        elif choice == "0": break
        else: print("Invalid choice")

def demo():
    records = sample_transactions()
    print("Before sorting:")
    display(records[:5])
    stats = MergeSortStats()
    sorted_records = merge_sort(records, stats=stats)
    print("\nAfter sorting by transaction ID:")
    display(sorted_records[:5])
    print(f"\nRecursive calls: {stats.recursive_calls}, Comparisons: {stats.comparisons}")
    print("\nBinary Search existing TX1048:")
    print(binary_search(sorted_records, 1048))
    print("\nBinary Search missing TX1999:")
    print(binary_search(sorted_records, 1999))
    print("\nPerformance comparison:")
    print("Target   Binary(ns)   Linear(ns)   Binary comps   Linear comps")
    rows = compare_search_performance(records, rounds=1000)
    for row in rows:
        print(f"{row[0]:<8} {row[1]:>10.2f} {row[2]:>11.2f} {row[3]:>13} {row[4]:>13}")
    draw_search_graph(records)

if __name__ == "__main__":
    if "--demo" in sys.argv:
        demo()
    else:
        menu()
