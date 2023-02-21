import sqlite3
import matplotlib.pyplot as plt


conn = sqlite3.connect('crypto.sqlite')
cur = conn.cursor()
logged_in_user_id= 1

cur.execute("""
SELECT * FROM past_portfolio_worth WHERE user_id=?""",(logged_in_user_id,))

results = cur.fetchall()
print(results)


amount=[]
date=[]
for result in results:
    zaokruzen= round(result[1],2)
    amount.append(zaokruzen)
    date.append(result[2])


plt.plot(date,amount)
plt.xlabel("Days")
plt.ylabel("Amount of $")

plt.show()