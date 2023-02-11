import sqlite3

conn = sqlite3.connect('dbase.sqlite')
cur = conn.cursor()

# Make some fresh tables using executescript()
cur.executescript('''


CREATE  TABLE IF NOT EXISTS  User (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE,
    password TEXT
);
''')

def new_user(nick,pasw):   
    cur.execute('SELECT * FROM User WHERE name = ?', (nick,))
    result = cur.fetchone()
    if result:
        print(f'Error: username "{nick}" is already taken.')
        return False
    else:
        cur.execute('INSERT INTO User (name, password) VALUES (?, ?)', (nick, pasw))
        conn.commit()
        print(f'Success: username "{nick}" has been created.')
        return True


        
nick='stojko'
pasw='ivandovic'
new_user(nick,pasw)