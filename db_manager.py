import sqlite3
import datetime

rendszamok = ['JJL839',
              'DEF456',
              'GHI789',
              'AAAA123',
              'NAI3NRU',
              'GXI5OGJ',
              'APO5JEO',
              'KHO5ZZK',
              'FJI4ZHY',
              'NAS4KGJ',
              'BG65USJ',
              'AK64DMV'
              ]
datumok = ['2024-03-17',
           '2024-03-18',
           '2024-03-19',
           '2025-01-01',
           '2025-01-01',
           '2025-01-01',
           '2025-01-01',
           '2024-12-21',
           '2024-11-11',
           '2024-10-10',
           '2024-10-10',
           '2023-01-01'
           ]


def connect(name):
    return sqlite3.connect(name)

def create_tables(conn):
    # Kapcsolódás az adatbázishoz
    c = conn.cursor() 

    c.execute("""CREATE TABLE IF NOT EXISTS tickets(
    id INTEGER PRIMARY KEY,
    plate TEXT NOT NULL,
    date DATE DEFAULT (date('now')),
    end_of_validity Text NOT NULL
    )""")

    upload_db(c)
    conn.commit()
    conn.close()

def upload_db(c):
    # Adatok beszúrása
    for rendszam, datum in zip(rendszamok, datumok):
        c.execute("INSERT INTO tickets (plate, end_of_validity) VALUES (?, ?)", (rendszam, datum))

def drop_table(db, table):
    conn = sqlite3.connect(db)
    c = conn.cursor() 

    c.execute("DROP TABLE IF EXISTS "+table)
    conn.commit()
    conn.close()

# videos:
    #https://youtu.be/iXYeb2artTE?t=774
    #https://youtu.be/JrAiefGNUq8?t=254


def check(plate2):
    plate = plate2.strip()
    connection = connect('database.db')
    c = connection.cursor()

    # Rendszám, dátum és lejárat dátumának lekérése az adatbázisból
    c.execute('SELECT date, end_of_validity FROM tickets WHERE plate = ?', (plate,))
    result = c.fetchone()

    if result:
        # Mai dátum lekérése
        today = datetime.datetime.now().date()
        
        # Dátumok lekérése az adatbázisból
        start_date = datetime.datetime.strptime(result[0], "%Y-%m-%d").date()
        end_date = datetime.datetime.strptime(result[1], "%Y-%m-%d").date()
        #test(start_date, today, end_date)

        # Ellenőrzés, hogy a mai dátum az adatbázisban található kezdő és befejező dátumok között van-e
        if start_date <= today <= end_date:
            return 'Ervenyes matrica'
        else:
            return 'Ervenytelen matrica'
    else:
        return 'Nem talalhato'
    
def test(a,b,c):
    print("----------\nKezdő dátum: ",a,"\nMa:",b,"\nBefejező dátum: ",c)

#GUI
def add_row(plate, end_of_validity):
    print("ezt kellene hozzáadni: "+plate+",  "+end_of_validity)
    conn = connect("database.db")
    c = conn.cursor() 
    try:
        # SQL INSERT parancs végrehajtása az adatokkal
        c.execute("INSERT INTO tickets (plate, end_of_validity) VALUES (?, ?)", (plate, end_of_validity))
        print("Sor hozzáadva az adatbázishoz: ", plate, ", ", end_of_validity)
        conn.commit()  # Tranzakció mentése
    except sqlite3.Error as e:
        print("Hiba az adatok beszúrásakor:", e)
    finally:
        conn.close()  # Adatbáziskapcsolat lezárása

def delete_row(plate):
    print("ezt kellene kitörölni:", plate)
    conn = connect("database.db")
    c = conn.cursor() 
    try:
        # SQL DELETE parancs végrehajtása a megadott rendszámra
        c.execute("DELETE FROM tickets WHERE plate = ?", (plate,))
        print("Sor törölve az adatbázisból:", plate)
        conn.commit()  # Tranzakció mentése
    except sqlite3.Error as e:
        print("Hiba a sor törlésekor:", e)
    finally:
        conn.close()  # Adatbáziskapcsolat lezárása