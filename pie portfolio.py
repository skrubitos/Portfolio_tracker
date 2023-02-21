import datetime as dt
import matplotlib.pyplot as plt
import pandas_datareader as web

tickers=["BTC","ETH","LTC","DOGE"]
amount=[0.5,10,40,30000]
prices=[24000,1500,98,0.08]
total=[]

for x in range(len(tickers)):
    total.append(amount[x]*prices[x])


print(total)
print(sum(total))

fig, ax= plt.subplots(figsize=(16,8))

ax.set_facecolor('black')
ax.figure.set_facecolor('#121212')

#postavljanje boja x osi
ax.tick_params(axis="x", color="white")
#postavljanje boja y osi
ax.tick_params(axis="y", color="white")

#postavljanje naziva 
ax.set_title("PORTFOLIO ",color="red",fontsize=20)

#kreiranje PIE-a, total=sta se gleda, labels= sta ce bit u imenu svake(tickers), autopct=kako ce bit prikazani postotci, pctdistance=koliko ce biti udaljeni postotci od sredine  koji ide od 0 do 1
_,texts,_= ax.pie(total,labels=tickers, autopct='%1.1f%%',pctdistance=0.8)
#odredivanje koje ce bit boje tekst
[text.set_color('white')for text in texts]

#kreiranje kruga tako da izgleda kao ring
krug=plt.Circle((0,0),0.55,color="black")
#određivanje radijusa kruga
plt.gca().add_artist(krug)

ax.text(-2,1, "OVERVIEW",fontsize=12, color='orange',verticalalignment="center",horizontalalignment='center')
ax.text(-2,0.80, f'Total USD Amount: {sum(total):.2f}$',fontsize=10,color="white",verticalalignment="center",horizontalalignment='center')

oduzimanje=0.15

for ticker in tickers:
    ax.text(-2,0.8-oduzimanje,f'{ticker}:{total[tickers.index(ticker)]}',color='white',fontsize=12,verticalalignment="center",horizontalalignment='center')
    oduzimanje+= 0.15

plt.show()