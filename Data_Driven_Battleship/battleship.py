import csv

GRID_SIZE = 5
EMPTY, HIT, MISS = '~', 'H', 'M'

def load_ships(filename):
    ships = {}
    try:
        with open(filename, 'r') as f:
            for row in csv.DictReader(f):
                name = row['ship_name']
                r1, c1 = int(row['row1']), int(row['col1'])
                r2, c2 = int(row['row2']), int(row['col2'])
                positions = set()
                if r1 == r2:
                    for c in range(min(c1,c2), max(c1,c2)+1):
                        positions.add((r1, c))
                else:
                    for r in range(min(r1,r2), max(r1,r2)+1):
                        positions.add((r, c1))
                ships[name] = {'positions': positions, 'hits': set()}
        print(f"  Loaded {len(ships)} ships from file.")
        return ships
    except FileNotFoundError:
        print("  ships.csv not found. Using default ships.")
        return {
            'Destroyer':  {'positions': {(0,0),(0,1)},       'hits': set()},
            'Cruiser':    {'positions': {(2,3),(3,3)},       'hits': set()},
            'Submarine':  {'positions': {(4,1),(4,2),(4,3)}, 'hits': set()}
        }

