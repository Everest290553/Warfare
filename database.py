import sqlite3 as sq

if __name__ != '__main__':
    with sq.connect('database.db') as con:
        cur = con.cursor()

        cur.execute('''CREATE TABLE IF NOT EXISTS records (
                        id INTEGER PRIMARY KEY,
                        value INTEGER DEFAULT 0
                    )''')
        cur.execute('''CREATE TABLE IF NOT EXISTS weapons (
                        bought INTEGER DEFAULT 0,
                        active INTEGER DEFAULT 0
                    )''')
        check = cur.execute('''SELECT bought FROM weapons''').fetchall()
        if check == []:
            cur.execute('''INSERT INTO weapons (bought) VALUES (0)''')
            cur.execute('''INSERT INTO weapons (active) VALUES (0)''')

def add_result(result):
    with sq.connect('database.db') as con:
        cur = con.cursor()

        cur.execute(f'''INSERT INTO records (value) VALUES ({result})''')

def get_record():
    with sq.connect('database.db') as con:
        cur = con.cursor()

        records = cur.execute('''SELECT value FROM records''').fetchall()
    highest_record = 0
    for record in records:
        if record[0] > highest_record:
            highest_record = record[0]
    return highest_record

def get_points():
    with sq.connect('database.db') as con:
        cur = con.cursor()

        records = cur.execute('''SELECT value FROM records''').fetchall()
    points = 0
    for record in records:
        points += record[0]
    return points

def add_weapon(weapon):
    with sq.connect('database.db') as con:
        cur = con.cursor()

        cur.execute(f'''INSERT INTO weapons (bought) VALUES ({weapon})''')

def is_bought(weapon):
    with sq.connect('database.db') as con:
        cur = con.cursor()

        weapons = cur.execute('''SELECT bought FROM weapons''').fetchall()
    for i in weapons:
        if i[0] == weapon:
            return True

def is_active(weapon):
    with sq.connect('database.db') as con:
        cur = con.cursor()

        weapons = cur.execute('''SELECT active FROM weapons''').fetchall()
    for i in weapons:
        if i[0] == weapon:
            return True

def set_active(weapon):
    with sq.connect('database.db') as con:
        cur = con.cursor()

        cur.execute(f'''UPDATE weapons SET active={weapon}''')
