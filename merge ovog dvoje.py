import tkinter as tk
import sqlite3
import matplotlib.pyplot as plt
import matplotlib.backends.backend_tkagg as tkagg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas_datareader as web
import datetime as dt
import requests
# Connect to the database
conn = sqlite3.connect('crypto.sqlite')
cur = conn.cursor()
logged_in_user_id = 1

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
