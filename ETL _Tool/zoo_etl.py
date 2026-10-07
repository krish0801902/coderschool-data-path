# Project 1: ETL Tool — Zoo Animal Data Processor
import csv

def extract(filename):
    animals = []
    try:
        with open(filename, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    animals.append({
                        'species': row['species'].strip().lower(),
                        'name':    row['name'].strip().title(),
                        'weight':  float(row['weight']),
                        'age':     int(row['age'])
                    })
                except (ValueError, KeyError):
                    print(f"  Skipping bad row: {row}")
        print(f"  Extracted {len(animals)} animals.")
        return animals
    except FileNotFoundError:
        print(f"Error: '{filename}' not found.")
        return []

def transform(animals):
    species_data = {}
    for a in animals:
        sp = a['species']
        if sp not in species_data:
            species_data[sp] = {'count': 0, 'total_weight': 0, 'heaviest': None, 'max_w': 0}
        species_data[sp]['count'] += 1
        species_data[sp]['total_weight'] += a['weight']
        if a['weight'] > species_data[sp]['max_w']:
            species_data[sp]['heaviest'] = a['name']
            species_data[sp]['max_w'] = a['weight']
    summary = []
    for sp, d in sorted(species_data.items()):
        avg = round(d['total_weight'] / d['count'], 1)
        summary.append({
            'species': sp.capitalize(), 'count': d['count'],
            'avg_weight_kg': avg, 'heaviest': d['heaviest']
        })
    return summary

def load(summary, out_file):
    with open(out_file, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=['species','count','avg_weight_kg','heaviest'])
        w.writeheader()
        w.writerows(summary)
    print(f"  Saved to '{out_file}'.")

def main():
    print("Zoo Animal Data Processor — ETL Tool\n")
    animals = extract("zoo_animals.csv")
    if not animals:
        return
    summary = transform(animals)
    print(f"\n  {'Species':<14} {'Count':<8} {'Avg Wt (kg)':<14} Heaviest")
    print("  " + "-"*50)
    for r in summary:
        print(f"  {r['species']:<14} {r['count']:<8} {r['avg_weight_kg']:<14} {r['heaviest']}")
    load(summary, "zoo_summary.csv")
    print("\nETL complete!")

if __name__ == "__main__":
    main()
