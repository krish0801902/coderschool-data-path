# Project 2: Simple Sorter — Toy Box Organizer

CATEGORIES = ['action figure', 'board game', 'building blocks',
              'stuffed animal', 'vehicle', 'other']

def collect_toys():
    toys = []
    print("Welcome to the Toy Box Organizer!")
    print("Type 'done' when finished.\n")
    while True:
        name = input("Toy name (or 'done'): ").strip().lower()
        if name == 'done':
            break
        if not name:
            continue
        print("Categories:", ', '.join(CATEGORIES))
        cat = input(f"Category for '{name}': ").strip().lower()
        if cat not in CATEGORIES:
            cat = 'other'
        toys.append({'name': name, 'category': cat})
        print(f"  Added: {name.title()} ({cat})\n")
    return toys

def sort_by_name(toys):
    return sorted(toys, key=lambda t: t['name'])

def sort_by_category(toys):
    grouped = {}
    for toy in toys:
        cat = toy['category']
        if cat not in grouped:
            grouped[cat] = []
        grouped[cat].append(toy['name'])
    for cat in grouped:
        grouped[cat] = sorted(grouped[cat])
    return grouped

def main():
    toys = collect_toys()
    if not toys:
        print("No toys entered!")
        return
    print("\n--- Toys A to Z ---")
    for i, toy in enumerate(sort_by_name(toys), 1):
        print(f"  {i}. {toy['name'].title()} [{toy['category']}]")
    print("\n--- By Category ---")
    for cat, names in sorted(sort_by_category(toys).items()):
        print(f"\n  {cat.title()}:")
        for n in names:
            print(f"    - {n.title()}")

if __name__ == "__main__":
    main()
