# Importing the sqlite3 module and connecting to the database:
import sqlite3
import requests

conn = sqlite3.connect('dbase.sqlite')
cur = conn.cursor()
logged_in_user_id= None

# Create the User table
cur.executescript('''
CREATE  TABLE IF NOT EXISTS  User (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE,
    password TEXT
);
''')


# DEFINING LOGIN FUNCTION
# (The login function takes two arguments: nick and pasw. 
# It uses the execute method of the cursor cur to query the User table for a user # with the given username and password.
# The query results are stored in the result variable. If the result is not None, it means the user with the given username and # password was found,
#  and we set the logged_in_user_id to the user's ID, which is stored in the first column (index 0) of the result. 
# Finally, the function returns True if the user was found, and False otherwise.)

def login(nick, pasw):
    global logged_in_user_id
    cur.execute('SELECT * FROM User WHERE name = ? AND password = ?', (nick, pasw))
    result = cur.fetchone()
    if result:
        logged_in_user_id = result[0]
        return True
    else:
        print('Name or password wrong')
        return False


# DEFINING DELITE USER 
# The delete_user function takes two arguments: nick and pasw.
#  It first calls the login function to check if the user with the given username and password exists. 
# If the login function returns True, it means the user was found and the user_id variable is set to the user's ID. 
# In this case, the function uses the execute method of the cursor cur to delete the user from the User table. Finally,

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
    # Check if the given username already exists in the User table
    cur.execute('SELECT * FROM User WHERE name = ?', (nick,))
    result = cur.fetchone()
    if result:
        print(f'Error: username "{nick}" is already taken.')
        # Return False indicating that the user could not be created due to duplicate username
        return False
    else:
        # If the username is available, insert a new user into the User table with the given username and password
        cur.execute('INSERT INTO User (name, password) VALUES (?, ?)', (nick, pasw))
        conn.commit()
        # Return True indicating that the user was successfully created
        print(f'Success: username "{nick}" has been created.')
        return True

def show_user():
    cur.execute("SELECT name FROM User")
    result= cur.fetchall()
    for j in range(len(result)):
        print(f"User {j+1}: {result[j][0]}")

cur.executescript('''CREATE TABLE IF NOT EXISTS Token (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    user_id INTEGER NOT NULL,
    symbol TEXT NOT NULL,
    amount REAL NOT NULL,
    FOREIGN KEY (user_id) REFERENCES User (id)
);
''')
#it adds token with parametars symbol and amount and to select function add token we first need to pas log in function to get user id
#which we need in order to select which tokens we are choosing
def add_token(symbol, amount):
    if not amount.isdigit():
        print("Error: amount must be a integer.")
        return 
    cur.execute('SELECT amount FROM Token WHERE user_id = ? AND symbol = ?', (logged_in_user_id, symbol))
    result = cur.fetchone()
    if result:
        new_amount = result[0] + float (amount)
        cur.execute('UPDATE Token SET amount = ? WHERE user_id = ? AND symbol = ?', (new_amount, logged_in_user_id, symbol))
        conn.commit()
        print(f'Success: token "{symbol}" has been updated in the portfolio. Total amount is {new_amount}.')
    else:
        cur.execute('INSERT INTO Token (user_id, symbol, amount) VALUES (?, ?,?)', (logged_in_user_id, symbol, amount))
        conn.commit()
        print(f'Success: token "{symbol}" has been added to the portfolio.')


#if user id is in variable logged_in_user_id then it will show list of tokens
def show_tokens():
    if logged_in_user_id is None:
        print('Error: you need to log in first.')
        return
    cur.execute('SELECT symbol, amount FROM Token WHERE user_id = ?', (logged_in_user_id,))
    tokens = cur.fetchall()
    if tokens:
        print('Here are your tokens:')
        for token in tokens:
            print(f'- {token[0]}: {token[1]}')
    else:
        print('You have no tokens in your portfolio.')

def get_price(symbol):
    url = f"https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?symbol={symbol}&convert=USD"
    headers = {
        'Accepts': 'application/json',
        'X-CMC_Pro_API_Key': '9bb7d0ec-030e-42f0-804f-8778b7507e0b'
    }

    response = requests.get(url, headers=headers).json()
    try:
        price = response['data'][symbol]['quote']['USD']['price']
        return price
    except KeyError:
        return False
    

"""
login("skrubitos","admin")

while True:
    symbol= input("simbol: ").upper()
    amount=input("amount: ")
    
    add_token(symbol,amount)
"""    


