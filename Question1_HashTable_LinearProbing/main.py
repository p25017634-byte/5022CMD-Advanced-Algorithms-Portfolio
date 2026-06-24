"""
Question 1 - Pharmacy Inventory System using Hash Table with Linear Probing.
Run normally for the CLI menu: python q1_pharmacy_hash_linear_probing.py
Run demo mode for report output: python q1_pharmacy_hash_linear_probing.py --demo
"""
from dataclasses import dataclass
import random
import time
import csv
import sys

DELETED = object()

@dataclass
class Medicine:
    medicine_id: str
    name: str
    category: str
    price: float
    quantity: int

    def __str__(self) -> str:
        return (f"ID: {self.medicine_id} | Name: {self.name} | Category: {self.category} | "
                f"Price: RM{self.price:.2f} | Qty: {self.quantity}")

class LinearProbingHashTable:
    def __init__(self, size: int = 101):
        self.size = size
        self.table = [None] * size
        self.count = 0

    def hash_function(self, key: str) -> int:
        numeric = int(key[1:])
        return numeric % self.size

    def _probe_index(self, key: str, for_insert: bool = False):
        start = self.hash_function(key)
        first_deleted = None
        for step in range(self.size):
            index = (start + step) % self.size
            item = self.table[index]
            if item is None:
                if for_insert and first_deleted is not None:
                    return first_deleted
                return index if for_insert else None
            if item is DELETED:
                if for_insert and first_deleted is None:
                    first_deleted = index
                continue
            if item.medicine_id == key:
                return index
        return first_deleted if for_insert else None

    def insert(self, medicine: Medicine) -> bool:
        if self.count >= self.size:
            raise OverflowError("Hash table is full")
        index = self._probe_index(medicine.medicine_id, for_insert=True)
        if index is None:
            raise OverflowError("No slot available")
        existing = self.table[index]
        if existing not in (None, DELETED) and existing.medicine_id == medicine.medicine_id:
            return False
        self.table[index] = medicine
        self.count += 1
        return True

    def search(self, medicine_id: str):
        index = self._probe_index(medicine_id, for_insert=False)
        return None if index is None else self.table[index]

    def edit(self, medicine_id: str, name=None, category=None, price=None, quantity=None) -> bool:
        med = self.search(medicine_id)
        if med is None:
            return False
        if name: med.name = name
        if category: med.category = category
        if price is not None: med.price = float(price)
        if quantity is not None: med.quantity = int(quantity)
        return True

    def delete(self, medicine_id: str) -> bool:
        index = self._probe_index(medicine_id, for_insert=False)
        if index is None:
            return False
        self.table[index] = DELETED
        self.count -= 1
        return True

    def records(self):
        return [item for item in self.table if item not in (None, DELETED)]

    def display_table(self):
        for i, item in enumerate(self.table):
            if item is None:
                print(f"Slot {i:03}: EMPTY")
            elif item is DELETED:
                print(f"Slot {i:03}: DELETED")
            else:
                print(f"Slot {i:03}: {item}")

    def export_csv(self, filename="pharmacy_inventory.csv"):
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Slot", "Medicine ID", "Name", "Category", "Price", "Quantity"])
            for i, item in enumerate(self.table):
                if item not in (None, DELETED):
                    writer.writerow([i, item.medicine_id, item.name, item.category, item.price, item.quantity])
        return filename

def generate_id(used_ids: set) -> str:
    while True:
        mid = f"M{random.randint(10000, 99999)}"
        if mid not in used_ids:
            used_ids.add(mid)
            return mid

def sample_data():
    data = [
        ("Paracetamol", "Tablet", 6.50, 120), ("Amoxicillin", "Capsule", 18.90, 80),
        ("Vitamin C", "Supplement", 12.00, 100), ("Cough Syrup", "Syrup", 9.90, 65),
        ("Antacid", "Tablet", 7.40, 95), ("Ibuprofen", "Tablet", 10.50, 75),
        ("Allergy Relief", "Tablet", 14.20, 60), ("Saline Spray", "Spray", 11.30, 55),
        ("Omega 3", "Supplement", 25.90, 40), ("Probiotic", "Supplement", 31.50, 35),
        ("Wound Cream", "Cream", 8.60, 70), ("Eye Drops", "Drops", 13.80, 45),
    ]
    fixed_ids = ["M12001", "M12012", "M12023", "M12034", "M12045", "M12056", "M12067", "M12078", "M12089", "M12100", "M12111", "M12122"]
    return [Medicine(mid, name, cat, price, qty) for mid, (name, cat, price, qty) in zip(fixed_ids, data)]

def build_table():
    ht = LinearProbingHashTable(size=23)
    for med in sample_data():
        ht.insert(med)
    return ht

def linear_search(array, medicine_id: str):
    for item in array:
        if item.medicine_id == medicine_id:
            return item
    return None

def compare_performance(rounds=2000):
    ht = build_table()
    array = ht.records()
    existing_keys = [array[0].medicine_id, array[len(array)//2].medicine_id, array[-1].medicine_id]
    missing_keys = ["M99991", "M99992", "M99993"]
    keys = existing_keys + missing_keys
    results = []
    for key in keys:
        start = time.perf_counter_ns()
        for _ in range(rounds):
            ht.search(key)
        hash_time = (time.perf_counter_ns() - start) / rounds
        start = time.perf_counter_ns()
        for _ in range(rounds):
            linear_search(array, key)
        array_time = (time.perf_counter_ns() - start) / rounds
        results.append((key, "Existing" if key in existing_keys else "Missing", hash_time, array_time))
    return results

def insert_flow(ht, used_ids):
    name = input("Enter medicine name: ")
    category = input("Enter category: ")
    price = float(input("Enter price: "))
    quantity = int(input("Enter quantity: "))
    mid = generate_id(used_ids)
    ht.insert(Medicine(mid, name, category, price, quantity))
    print(f"Medicine inserted successfully. Assigned ID: {mid}")

def menu():
    ht = build_table()
    used_ids = {m.medicine_id for m in ht.records()}
    while True:
        print("\n===== Pharmacy Inventory System =====")
        print("1. Display all medicines")
        print("2. Insert medicine")
        print("3. Search medicine")
        print("4. Edit medicine")
        print("5. Delete medicine")
        print("6. Performance comparison")
        print("7. Export CSV")
        print("0. Exit")
        choice = input("Enter choice: ").strip()
        if choice == "1": ht.display_table()
        elif choice == "2": insert_flow(ht, used_ids)
        elif choice == "3":
            med = ht.search(input("Enter medicine ID: ").strip().upper())
            print(med if med else "Medicine not found")
        elif choice == "4":
            mid = input("Enter medicine ID to edit: ").strip().upper()
            med = ht.search(mid)
            if not med: print("Medicine not found"); continue
            print("Current:", med)
            name = input("New name (blank keep): ").strip() or None
            category = input("New category (blank keep): ").strip() or None
            price_in = input("New price (blank keep): ").strip()
            qty_in = input("New quantity (blank keep): ").strip()
            ht.edit(mid, name, category, float(price_in) if price_in else None, int(qty_in) if qty_in else None)
            print("Medicine updated successfully")
        elif choice == "5":
            print("Medicine deleted successfully" if ht.delete(input("Enter medicine ID: ").strip().upper()) else "Medicine not found")
        elif choice == "6":
            print("Key       Type      HashTable(ns)   Array(ns)")
            for row in compare_performance():
                print(f"{row[0]:<9} {row[1]:<9} {row[2]:>12.2f} {row[3]:>10.2f}")
        elif choice == "7": print("Exported to", ht.export_csv())
        elif choice == "0": break
        else: print("Invalid choice")

def demo():
    ht = build_table()
    print("Sample pharmacy hash table created with", len(ht.records()), "records.")
    print("\nSearch existing M12045:")
    print(ht.search("M12045"))
    print("\nSearch missing M99999:")
    print(ht.search("M99999") or "Medicine not found")
    print("\nPerformance comparison:")
    print("Key       Type      HashTable(ns)   Array(ns)")
    for row in compare_performance(rounds=1000):
        print(f"{row[0]:<9} {row[1]:<9} {row[2]:>12.2f} {row[3]:>10.2f}")

if __name__ == "__main__":
    if "--demo" in sys.argv:
        demo()
    else:
        menu()
