import sqlite3

conn = sqlite3.connect('dbase.sqlite')
cur = conn.cursor()

# Make some fresh tables using executescript()
cur.executescript('''
DROP TABLE IF EXISTS User;

CREATE TABLE User (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE,
    password TEXT
);
''')



def login(nick, pasw):
    cur.execute('SELECT * FROM User WHERE name = ? AND password = ?', (nick, pasw))
    result = cur.fetchone()
    if result:
        return True
    else:
        return False

def delete_user(nick, pasw):
    if check_credentials(nick, pasw):
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


while True:
    choice=input('''What do you want to do?
    1) Log in
    2) Create Account
    3) Delite Account \n''')
    
    
    nick=('Input your nick: ')
    pasw= input('Input your passwsss1ord:')

if choice== 1:
    login()
if choice==2:
    new_user()
if choice==3:
    delete_user()
else:
    print('You need to select numbers')
