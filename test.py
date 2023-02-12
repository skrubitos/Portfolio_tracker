import requests

def get_price(symbol):
    url = f"https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?symbol={symbol}&convert=USD"
    headers = {
        'Accepts': 'application/json',
        'X-CMC_Pro_API_Key': '9bb7d0ec-030e-42f0-804f-8778b7507e0b'
    }

    response = requests.get(url, headers=headers).json()
    price = response['data'][symbol]['quote']['USD']['price']
    return price

symbol = input("Enter the symbol of the cryptocurrency: ")
price = get_price(symbol.upper())
print(f"The price of {symbol} is ${price:.2f}")
