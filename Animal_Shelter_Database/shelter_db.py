# Project 4: Animal Shelter Database — SQLite Pet Keeper
import sqlite3

def connect():
    conn = sqlite3.connect("shelter.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS animals (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            name     TEXT NOT NULL,
            species  TEXT NOT NULL,
            age      INTEGER NOT NULL,
            available INTEGER DEFAULT 1
        )
    ''')
    cursor.execute("SELECT COUNT(*) FROM animals")
    if cursor.fetchone()[0] == 0:
        starters = [
            ('Buddy','dog',3), ('Whiskers','cat',2),
            ('Goldie','fish',1), ('Thumper','rabbit',4),
            ('Spike','hamster',1), ('Pepper','dog',5), ('Luna','cat',3)
        ]
        cursor.executemany(
            "INSERT INTO animals (name, species, age) VALUES (?, ?, ?)", starters)
        print("Shelter database created with starter animals!")
    conn.commit()
    return conn

def view_animals(conn, species=None):
    c = conn.cursor()
    if species:
        c.execute("SELECT id,name,species,age FROM animals WHERE available=1 AND species=?",
                  (species.lower(),))
    else:
        c.execute("SELECT id,name,species,age FROM animals WHERE available=1 ORDER BY species,name")
    rows = c.fetchall()
    if not rows:
        print("  No animals available!")
        return
    print(f"\n  {'ID':<5} {'Name':<15} {'Species':<12} Age")
    print("  " + "-"*40)
    for r in rows:
        print(f"  {r[0]:<5} {r[1]:<15} {r[2]:<12} {r[3]} yrs")

def add_animal(conn, name, species, age):
    conn.cursor().execute(
        "INSERT INTO animals (name,species,age) VALUES (?,?,?)",
        (name.title(), species.lower(), age))
    conn.commit()
    print(f"  Added {name.title()} the {species.lower()}!")

def adopt_animal(conn, animal_id):
    c = conn.cursor()
    c.execute("SELECT name,species FROM animals WHERE id=? AND available=1", (animal_id,))
    a = c.fetchone()
    if not a:
        print(f"  No animal with ID {animal_id}.")
        return
    c.execute("UPDATE animals SET available=0 WHERE id=?", (animal_id,))
    conn.commit()
    print(f"  {a[0]} the {a[1]} has been adopted!")

def shelter_stats(conn):
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM animals WHERE available=1")
    av = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM animals WHERE available=0")
    ad = c.fetchone()[0]
    print(f"\n  Available: {av} | Adopted: {ad}")

def main():
    print("="*45)
    print("   Animal Shelter Database")
    print("="*45)
    conn = connect()
    while True:
        print("\n  1.View all  2.Search  3.Add  4.Adopt  5.Stats  6.Exit")
        ch = input("\nChoice (1-6): ").strip()
        if   ch == '1': view_animals(conn)
        elif ch == '2':
            sp = input("  Species: ").strip()
            view_animals(conn, sp)
        elif ch == '3':
            nm = input("  Name: ").strip()
            sp = input("  Species: ").strip()
            try:
                ag = int(input("  Age: "))
                add_animal(conn, nm, sp, ag)
            except ValueError:
                print("  Invalid age!")
        elif ch == '4':
            view_animals(conn)
            try:
                adopt_animal(conn, int(input("\n  ID to adopt: ")))
            except ValueError:
                print("  Invalid ID!")
        elif ch == '5': shelter_stats(conn)
        elif ch == '6':
            print("  Goodbye!")
            break
    conn.close()

if __name__ == "__main__":
    main()
