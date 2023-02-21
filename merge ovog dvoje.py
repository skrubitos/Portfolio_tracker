import tkinter as tk
import sqlite3
import matplotlib.pyplot as plt
import matplotlib.backends.backend_tkagg as tkagg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas_datareader as web
import datetime as dt

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

# Create the line chart
fig1 = plt.figure(figsize=(6, 4), dpi=100)
plt.plot(date, amount)
plt.xlabel("Days")
plt.ylabel("Amount of $")

tickers=["BTC","ETH","LTC","DOGE"]
amount=[0.5,10,40,30000]
prices=[24000,1500,98,0.08]
total=[]

for x in range(len(tickers)):
    total.append(amount[x]*prices[x])

fig2, ax= plt.subplots(figsize=(4,4))
ax.set_facecolor('white')
ax.figure.set_facecolor('white')
ax.tick_params(axis="x", color="black")
ax.tick_params(axis="y", color="black")
ax.set_title("",color="red",fontsize=20)
_,texts,_= ax.pie(total,labels=tickers, autopct='%1.1f%%',pctdistance=0.8)
[text.set_color('black')for text in texts]
krug=plt.Circle((0,0),0.55,color="white")
plt.gca().add_artist(krug)

# Create the Tkinter GUI
root = tk.Tk()

root.title("Crypto Portfolio Chart")

# Add the line chart to the GUI
canvas1 = FigureCanvasTkAgg(fig1, master=root)
canvas1.draw()
canvas1.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Add the pie chart to the GUI
canvas2 = tk.Canvas(root)
canvas2.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
fig_agg = tkagg.FigureCanvasTkAgg(fig2, master=canvas2)
fig_agg.draw()
fig_agg.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Run the GUI
tk.mainloop()
