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

def display_board(board):
    print("\n     "+"  ".join(str(i)for i in range(GRID_SIZE))) 
    print("   " +"-"*(GRID_SIZE*3+1))
    for i ,row in enumerate(board):
        print(f'  {i} | '+"  ".join(row))

def show_stats(log, ships):
    hits = sum(1 for s in log if s ["result"] == HIT)
    acc = (hits / len(log)*100) if log else 0  
    print(f'\n{"="*30}')
    print(f'  shots: {len(log)} | hits {hits } | accuracy {acc:.1f}%')
    for name,d in ships.items():
        sunk = d["positions"]==d["hits"]
        print(f'  {name}: {"sunk" if sunk else "survived"} ')
    print("="*30)

def main():
    print("welcome to battleship\n")
    ships = load_ships('ships.csv')
    board = [[EMPTY]*GRID_SIZE for _ in range(GRID_SIZE)]
    all_pos = {pos: name for name, d in ships.items() for pos in d['positions']}
    total = len(all_pos)
    hits_total = 0
    shots_num = 0
    log = []
    guessed = set()
    print(f"Grid: {GRID_SIZE}x{GRID_SIZE} | Ships: {len(ships)} | Type 'quit' to end\n")
    while hits_total < total:
        display_board(board) 
        guess = input('\nfire at row, column: ').strip().lower()
        if guess == 'quit':
            break 
        try:
            r,c = map(int,guess.split(','))
            if not(0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE):
                print("invalid row and column")
                continue
        except ValueError:
            print("incorrect format")
            continue
        if (r,c) in guessed:
            print("already fired")
            continue
        guessed.add((r,c))
        shots_num += 1 
        if (r,c) in all_pos:
            ship_name = all_pos[(r,c)]
            ships [ship_name]['hits'].add((r,c))
            board[r][c]=HIT
            hits_total += 1
            log.append({'shot':shots_num, 'row':r, 'col':c, 'result':'HIT', 'ship_hit':ship_name})
            print(f"You hit {ship_name}")
            if ships[ship_name]['positions'] == ships[ship_name]['hits']:
                print(f"You sunk {ship_name}!")
        else:
            board[r][c] = MISS
            log.append({'shot':shots_num, 'row':r, 'col':c, 'result':'MISS', 'ship_hit':''})
            print(" Miss!")
    if hits_total == total:
        display_board(board)
        print("You Win!")
    show_stats(log, ships)

if __name__ == "__main__":
    main()
