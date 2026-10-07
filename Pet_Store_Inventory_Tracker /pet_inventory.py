# Project 5: Pet Store Inventory Tracker — Level 1 Capstone
import sqlite3
import matplotlib.pyplot as plt

COLORS = ['#FF6B6B','#4ECDC4','#FFE66D','#A8E6CF','#FF8B94','#B5EAD7','#C7CEEA']

def read_pets(filename):
    pet_counts = {}
    try:
        with open(filename, 'r') as f:
            for line in f:
                pet = line.strip().lower()
                if pet:
                    pet_counts[pet] = pet_counts.get(pet, 0) + 1
        return pet_counts
    except FileNotFoundError:
        print(f"Error: '{filename}' not found.")
        return {}

def sort_pets(pet_counts):
    return sorted(pet_counts.items(), key=lambda x: (-x[1], x[0]))

def show_chart(sorted_pets):
    names  = [p.capitalize() for p, _ in sorted_pets]
    counts = [c for _, c in sorted_pets]
    colors = [COLORS[i % len(COLORS)] for i in range(len(names))]
    plt.figure(figsize=(10, 6))
    bars = plt.bar(names, counts, color=colors, edgecolor='white', linewidth=1.5)
    for bar, count in zip(bars, counts):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
                 str(count), ha='center', va='bottom', fontsize=12, fontweight='bold')
    plt.title("Pet Store Inventory", fontsize=16, fontweight='bold')
    plt.xlabel("Pet Type")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.show()

def save_to_database(sorted_pets):
    conn = sqlite3.connect("pet_inventory.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS inventory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pet TEXT, count INTEGER,
        updated TEXT DEFAULT (datetime('now')))''')
    c.execute("DELETE FROM inventory")
    c.executemany("INSERT INTO inventory (pet, count) VALUES (?, ?)",
                  [(p, cnt) for p, cnt in sorted_pets])
    conn.commit()
    conn.close()
    print("  Inventory saved to pet_inventory.db!")

def main():
    print("="*50)
    print("   Pet Store Inventory Tracker — Level 1 Capstone")
    print("="*50)
    print("\n[Step 1] Reading pets from file...")
    pet_counts = read_pets("pets.txt")
    if not pet_counts:
        return
    print("[Step 2] Sorting by popularity...")
    sorted_pets = sort_pets(pet_counts)
    for pet, count in sorted_pets:
        print(f"  {pet.capitalize():<12} {'#'*count} ({count})")
    print("\n[Step 3] Drawing chart...")
    show_chart(sorted_pets)
    print("[Step 4] Saving to database...")
    save_to_database(sorted_pets)
    print("\nAll done!")

if __name__ == "__main__":
    main()
