def read_animals(filename):
    animals = []
    try:
        with open(filename, 'r') as file:
            for line in file:
                animal = line.strip().lower()
                if animal:
                    animals.append(animal)
        return animals
    except FileNotFoundError:
        print(f"Oops! Could not find '{filename}'.")
        return []

def display_animals(animals):
    print("\n--- Favorite Animals ---")
    for i, animal in enumerate(animals, 1):
        print(f"  {i}. {animal.capitalize()}")
    print(f"\nTotal: {len(animals)}")

def search_animals(animals, search_term):
    term = search_term.strip().lower()
    return [a for a in animals if term in a]

def main():
    print("Welcome to the Favorite Animals Reader!")
    animals = read_animals("animals.txt")
    if not animals:
        print("No animals found!")
        return
    display_animals(animals)
    while True:
        print("\nOptions:\n  1. Search\n  2. Quit")
        choice = input("Enter choice: ").strip()
        if choice == '1':
            term = input("Search for: ")
            matches = search_animals(animals, term)
            if matches:
                for m in matches:
                    print(f"  - {m.capitalize()}")
            else:
                print(f"No matches for '{term}'.")
        elif choice == '2':
            break

if __name__ == "__main__":
    main()
