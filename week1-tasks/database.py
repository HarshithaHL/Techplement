# database_setup.py

import sqlite3

def create_table():
    conn = sqlite3.connect('quotes.db')
    c = conn.cursor()
    c.execute('CREATE TABLE quotes (id INTEGER PRIMARY KEY AUTOINCREMENT, quote TEXT NOT NULL, author TEXT NOT NULL)')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    # create_table()
    create_table()
