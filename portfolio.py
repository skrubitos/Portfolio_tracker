import sqlite3

conn = sqlite3.connect('dbase.sqlite')
cur = conn.cursor()

# Create the User table
cur.executescript('''
CREATE  TABLE IF NOT EXISTS  User (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE,
    password TEXT
);
''')


def login(nick, pasw):
    cur.execute('SELECT * FROM User WHERE name = ? AND password = ?', (nick, pasw))
    result = cur.fetchone()
    if result:
        return result[0]
    else:
        return False

def delete_user(nick, pasw):
    user_id = login(nick, pasw)
    if user_id:
        cur.execute('DELETE FROM User WHERE name = ?', (nick,))
        conn.commit()
        print(f'Success: user "{nick}" has been deleted.')
        return True
    else:
        print('Error: invalid password. User deletion failed.')
        return False


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



cur.executescript('''CREATE TABLE IF NOT EXISTS Token (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    user_id INTEGER NOT NULL,
    symbol TEXT NOT NULL,
    amount REAL NOT NULL,
    FOREIGN KEY (user_id) REFERENCES User (id)
);
''')

def add_token(user_id, symbol, amount):
    cur.execute('INSERT INTO Token (user_id, symbol, amount) VALUES (?, ?,?)', (user_id, symbol, amount))
    conn.commit()
    print(f'Success: token "{symbol}" has been added to the portfolio.')


def show_tokens(user_id):
    cur.execute('SELECT symbol, amount FROM Token WHERE user_id = ?', (user_id,))
    tokens = cur.fetchall()
    if tokens:
        print('Here are your tokens:')
        for token in tokens:
            print(f'- {token[0]}: {token[1]}')
    else:
        print('You have no tokens in your portfolio.')