# Project 3: Snack Popularity Chart
import matplotlib.pyplot as plt

COLORS = ['#FF6B6B', '#4ECDC4', '#FFE66D', '#A8E6CF', '#FF8B94', '#B5EAD7']

def collect_snacks():
    snacks = {}
    print("Welcome to the Snack Popularity Chart!")
    print("Type 'done' when finished.\n")
    while True:
        snack = input("Snack name (or 'done'): ").strip().lower()
        if snack == 'done':
            break
        if not snack or snack in snacks:
            continue
        while True:
            try:
                votes = int(input(f"  Votes for {snack}? "))
                if votes >= 0:
                    snacks[snack] = votes
                    break
                print("  Can't be negative!")
            except ValueError:
                print("  Enter a whole number!")
    return snacks

def show_chart(snacks):
    if not snacks:
        return
    sorted_s = dict(sorted(snacks.items(), key=lambda x: x[1], reverse=True))
    names  = list(sorted_s.keys())
    votes  = list(sorted_s.values())
    colors = [COLORS[i % len(COLORS)] for i in range(len(names))]

    plt.figure(figsize=(10, 6))
    bars = plt.bar(names, votes, color=colors, edgecolor='white', linewidth=1.5)
    for bar, vote in zip(bars, votes):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                 str(vote), ha='center', va='bottom', fontsize=12, fontweight='bold')
    plt.title("Snack Popularity Chart", fontsize=18, fontweight='bold', pad=20)
    plt.xlabel("Snacks", fontsize=13)
    plt.ylabel("Votes", fontsize=13)
    plt.xticks(rotation=30, ha='right')
    plt.tight_layout()
    plt.show()
    print(f"\nMost popular: {names[0].capitalize()} with {votes[0]} votes!")

def main():
    show_chart(collect_snacks())

if __name__ == "__main__":
    main()
