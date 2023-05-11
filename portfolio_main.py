import datetime
import sqlite3
import requests
import tkinter as tk
from tkinter import messagebox
import bcrypt
import matplotlib.pyplot as plt
import matplotlib.backends.backend_tkagg as tkagg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas_datareader as web
import datetime as dt
import requests

current_time = datetime.datetime.now()
current_time_string = current_time.strftime("%Y-%m-%d %H:%M")

# Importing the sqlite3 module and connecting to the database:
conn = sqlite3.connect('crypto.sqlite')
cur = conn.cursor()
logged_in_user_id= None


# Create the User table
cur.executescript('''
CREATE  TABLE IF NOT EXISTS  User (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE,
    password TEXT
);

CREATE TABLE IF NOT EXISTS Token (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    user_id INTEGER NOT NULL,
    symbol TEXT NOT NULL,
    amount REAL NOT NULL,
    FOREIGN KEY (user_id) REFERENCES User (id)
);
CREATE  TABLE IF NOT EXISTS  past_value (
    user_id INTEGER NOT NULL,
    token  TEXT,
    price REAL NOT NULL,
    amount REAL NOT NULL,
    holdings$ REAL NOT NULL,
    date DATETIME,
    FOREIGN KEY (user_id) REFERENCES User (id)

);
CREATE TABLE IF NOT EXISTS past_portfolio_worth (
    user_id INTEGER NOT NULL,
    total_worth REAL NOT NULL,
    date DATETIME,
    FOREIGN KEY (user_id) REFERENCES User (id)


)

''')

# DEFINING LOGIN FUNCTION
# (The login function takes two arguments: nick and pasw. 
# It uses the execute method of the cursor cur to query the User table for a user # with the given username and password.
# The query results are stored in the result variable. If the result is not None, it means the user with the given username and # password was found,
#  and we set the logged_in_user_id to the user's ID, which is stored in the first column (index 0) of the result. 
# Finally, the function returns True if the user was found, and False otherwise.)

def graf():
    # Retrieve data from the database
    cur.execute("""
    SELECT * FROM past_portfolio_worth WHERE user_id=?
    """, (logged_in_user_id,))
    results = cur.fetchall()


    # Create two lists for the X and Y axes
    amount = []
    date = []
    for result in results:
        zaokruzen = round(result[1], 2)
        amount.append(zaokruzen)
        date.append(result[2])

        
    import matplotlib.dates as mdates

    # Create the line chart
    fig1 = plt.figure(figsize=(6, 4), dpi=100)
    plt.plot(date, amount)
    plt.xlabel("Days")
    plt.ylabel("Amount of $")

    # Format x-axis ticks as days only
    days = mdates.DayLocator(interval=1)
    days_fmt = mdates.DateFormatter('%d')
    plt.gca().xaxis.set_major_locator(days)
    plt.gca().xaxis.set_major_formatter(days_fmt)

    # Rest of the code
    tickers=[]
    amount=[]
    prices=[]
    total=[]
    cur.execute("""
    SELECT * FROM Token WHERE user_id=?
    """, (logged_in_user_id,))
    results = cur.fetchall()
    print(f'results{results[0][2]}')
    for index,result in enumerate(results):
        print(f'result{result[2]}')
        tickers.append(result[2].strip('\''))
        amount.append(result[3])
        prices.append(get_price(tickers[index]))
    print(prices)
    print(tickers)
    for x in range(len(tickers)):
        total.append(amount[x]*prices[x])

    fig2, ax= plt.subplots(figsize=(4,4))
    ax.set_facecolor('white')
    ax.figure.set_facecolor('white')
    ax.tick_params(axis="x", color="black")
    ax.tick_params(axis="y", color="black")
    ax.set_title("",color="red",fontsize=20)

    _, texts, _ = ax.pie(total, labels=tickers, autopct='%1.1f%%', pctdistance=0.8)
    [text.set_color('black')for text in texts]
    krug=plt.Circle((0,0),0.55,color="white")
    plt.gca().add_artist(krug)

    # Create the Tkinter GUI
    graf = tk.Tk()
    graf.geometry("1280x720")
    graf.configure(bg="white")
    graf.title("Crypto Portfolio Chart")

    # Add the line chart to the GUI
    canvas1 = FigureCanvasTkAgg(fig1, master=graf)
    canvas1.draw()
    canvas1.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Add the pie chart to the GUI
    canvas2 = tk.Canvas(graf)
    canvas2.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    fig_agg = tkagg.FigureCanvasTkAgg(fig2, master=canvas2)
    fig_agg.draw()
    fig_agg.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    # Run the GUI
    tk.mainloop()


import threading


def login(nick, pasw):
    global logged_in_user_id
    cur.execute('SELECT * FROM User WHERE name = ?', (nick,))
    result = cur.fetchone()
    if result:
        # Retrieve the stored hashed password and salt for the given username
        stored_hashed_password = result[2]
        stored_salt = result[3]
        # Hash the input password using the same salt and compare with the stored hashed password
        input_hashed_password = bcrypt.hashpw(pasw.encode('utf-8'), stored_salt)
        if input_hashed_password == stored_hashed_password:
            logged_in_user_id = result[0]
            print(f'Success: "{nick}" has been logged in.')
            # Return True indicating that the login was successful
            root.destroy()
            graf()

            

            return True
    print('Name or password wrong')
    messagebox.showwarning("Error", f'Wrong username or password')
    # Return False indicating that the login was not successful
    return False

# DEFINING DELITE USER 
# The delete_user function takes two arguments: nick and pasw.
#  It first calls the login function to check if the user with the given username and password exists. 
# If the login function returns True, it means the user was found and the user_id variable is set to the user's ID. 
# In this case, the function uses the execute method of the cursor cur to delete the user from the User table. Finally,

def delete_user(nick, pasw):
    user_id = login(nick, pasw)
    global logged_in_user_id
    logged_in_user_id = None

    if user_id:
        cur.execute('DELETE FROM User WHERE name = ?', (nick,))
        conn.commit()
        print(f'Success: user "{nick}" has been deleted.')
        return True
    else:
        print('Error: invalid password. User deletion failed.')
        return False

def new_user(nick, pasw):
    # Check if the given username already exists in the User table
    cur.execute('SELECT * FROM User WHERE name = ?', (nick,))
    result = cur.fetchone()
    if len(pasw)<5 and len(nick)<3:
                messagebox.showwarning("No data", f'Password must have min. 5 characters, and username must have atleast 3 characters.')
                result=False

    elif len(pasw)<5 :
        result= False
        messagebox.showwarning("Password too short", f'Please choose a stronger password (min 5 characters).')
    elif len(nick)<3:
        result= False
        messagebox.showwarning("Username too short", f'Username must have atleast 3 characters.')
        

    if result:
        print(f'Error: username "{nick}" is already taken.')
        messagebox.showwarning("Name already taken", f'Error:{nick} is already taken. Please choose a different username.')
        # Return False indicating that the user could not be created due to duplicate username
        return False
    if result is None:
        # If the username is available, generate a salt and hash the password using bcrypt
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(pasw.encode('utf-8'), salt)
        # Check if the salt column exists in the User table
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='User' AND sql LIKE '%salt%'")
        salt_column_exists = bool(cur.fetchone())
        if not salt_column_exists:
            # If the salt column does not exist, add it to the User table
            cur.execute('ALTER TABLE User ADD COLUMN salt TEXT')
            cur.execute('ALTER TABLE User ADD COLUMN timestamp DATETIME')
        # Insert a new user into the User table with the given username and hashed password
        cur.execute('INSERT INTO User (name, password, salt,timestamp) VALUES (?, ?, ?,?)', (nick, hashed_password, salt,current_time_string))
        conn.commit()
        print(f'Success: username "{nick}" has been created.')
        messagebox.showinfo("Registration Successful", "User registered successfully!")
        return True

def show_user():    
    cur.execute("SELECT name, timestamp FROM user")
    result = cur.fetchall()
    if len(result) < 1:
        messagebox.showinfo("User List", "No users yet")
    else:
        user_data = ""
        for j in range(len(result)):
            user_data += f"User {j+1}: {result[j][0]} (Registered: {result[j][1]})\n"
        user_window = tk.Toplevel(root)
        user_window.title("User List")
        user_label = tk.Label(user_window, text=user_data, justify="left")
        user_label.pack(padx=10, pady=10)

def add_token(symbol, amount=0):
    try:
        if not isinstance(amount, float) and not isinstance(amount, int):
            print("Amount must be a float.")
            return 
        cur.execute('SELECT amount FROM Token WHERE user_id = ? AND symbol = ?', (logged_in_user_id, symbol))
        result = cur.fetchone()
        if get_price(symbol)== None:
            print("This token does not exist")
            show_tokens()
            result=False
            return False

        if result:
            new_amount = result[0] + float (amount)
            cur.execute('UPDATE Token SET amount = ? WHERE user_id = ? AND symbol = ?', (new_amount, logged_in_user_id, symbol))
            conn.commit()
            print(f'Success: token "{symbol}" has been updated in the portfolio. Total amount is {new_amount}.')
            show_tokens()

        
        else:
            cur.execute('INSERT INTO Token (user_id, symbol, amount) VALUES (?, ?,?)', (logged_in_user_id, symbol, amount))
            conn.commit()
            print(f'Success: token "{symbol}" has been added to the portfolio.')
            show_tokens()
        price_of_token=get_price(symbol)
        price_of_token = round(price_of_token, 2)            
        holdingsS= price_of_token* float(amount)
        total_worth =price_of_token*holdingsS 
        
        cur.execute('INSERT INTO past_value (user_id, token,price, amount,holdings$, date) VALUES (?,?,?,?,?,?)', (logged_in_user_id,symbol,price_of_token, amount,   total_worth, current_time_string))

        conn.commit()
    except SyntaxError:
        print("Something went wrong. Make sure that you use integer or float number ex. (1.2)")

#if user id is in variable logged_in_user_id then it will show list of tokens
def show_tokens():
    if logged_in_user_id is None:
        print('Error: you need to log in first.')
        return
    cur.execute('SELECT symbol, amount FROM Token WHERE user_id = ?', (logged_in_user_id,))
    tokens = cur.fetchall()
    
    if tokens:
        total_worth= 0
        print('\t Here are your tokens')
        for token in tokens:
            price_of_token=get_price(token[0])
            price_of_token = round(price_of_token, 2)            
            holdingsS= price_of_token* float(token[1])
            total_worth+= float(holdingsS)
            print(f'{token[0]}: {token[1]} \t  {holdingsS:,.2f}$')
            cur.execute('INSERT INTO past_value (user_id, token,price, amount,holdings$, date) VALUES (?,?,?,?,?,?)', (logged_in_user_id,token[0],price_of_token, token[1],   holdingsS, current_time_string))

            conn.commit()

      
        print(f"Your portfolio is worth: {total_worth:,.2f}$")
        cur.execute('INSERT INTO past_portfolio_worth(user_id, total_worth,date) VALUES (?,?,?)', (logged_in_user_id,total_worth ,current_time_string))

        conn.commit()

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
        if len(response['data']) < 1:
            pass
        else:
            return price
    except KeyError:
        return None
'+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
#GUI
# Create a new Tkinter window
root = tk.Tk()
root.geometry("500x700")
root.title("User Login System")
root.configure(background="white")
#icon = tk.PhotoImage(file="main_icon.png")
#root.iconphoto(False, icon)

boja=0
#ovo dodat widget za dark mode
def darkmod():
    global boja
    if boja%2==0:
        root.configure(background="black")
        boja+=1
    else:
        root.configure(background="white")
        boja+=1

# Create a frame for the input fields and buttons
input_frame = tk.Frame(root)
input_frame.pack(pady=200)

# Create a label for the username field
username_label = tk.Label(input_frame, text="Username:")
username_label.grid(row=0, column=0, padx=10, pady=10)

# Create an entry field for the username
username_entry = tk.Entry(input_frame)
username_entry.grid(row=0, column=1, padx=10, pady=10)

# Create a label for the password field
password_label = tk.Label(input_frame, text="Password:")
password_label.grid(row=1, column=0, padx=10, pady=10)

# Create an entry field for the password
password_entry = tk.Entry(input_frame, show="*")
password_entry.grid(row=1, column=1, padx=10, pady=10)


# Create a button to change to dark mode
dark_mode = tk.Button(input_frame, text="Dark Mode", command=lambda: darkmod())
dark_mode.grid(row=2, column=0, padx=0, pady=0)


# Create a button to submit the login information
login_button = tk.Button(input_frame, text="Login", command=lambda: login(username_entry.get(), password_entry.get()))
login_button.grid(row=0, column=2, padx=10, pady=10)

# Create a button to register the user
register_button = tk.Button(input_frame, text="Register", command=lambda: new_user(username_entry.get(), password_entry.get()))
register_button.grid(row=2, column=1, padx=10, pady=10)

# Create a button to show the users
show_users_button = tk.Button(input_frame, text="Show Users", command=show_user)
show_users_button.grid(row=2, column=2, padx=10, pady=10)

# Create a frame for the buttons
button_frame = tk.Frame(root)
button_frame.pack(side="right", padx=10, pady=10)

# Create a label to display the user data
user_data_label = tk.Label(button_frame, text="", justify="left", width=50, wraplength=400)
user_data_label.pack(pady=2)

# Start the Tkinter event loop
root.mainloop()

'+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
#VIZUALIZACIJA
'import matplotlib.pyplot as web'
