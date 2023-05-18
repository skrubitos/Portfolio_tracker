# Crypto Portfolio Tracker

This program is a simple crypto portfolio tracker that allows users to manage their cryptocurrency holdings and view their portfolio performance.

## Features

- User registration: Users can create an account by providing a username and password. The password is hashed and stored securely using bcrypt.
- User login: Registered users can log in to their account using their username and password.
- User deletion: Users can delete their account by providing their username and password. The account will be permanently removed from the database.
- Token management: Users can add tokens to their portfolio by specifying the token symbol and the amount owned. The program retrieves the current price of the token from the CoinMarketCap API and calculates the total value of the holdings.
- Portfolio visualization: Users can view their portfolio performance through line and pie charts. The line chart shows the value of the portfolio over time, while the pie chart shows the distribution of holdings among different tokens.
- Data storage: User data, including account information, token holdings, and portfolio history, is stored in an SQLite database.

## Dependencies

- `datetime`: Used to handle date and time-related operations.
- `sqlite3`: Provides functionality for interacting with SQLite databases.
- `requests`: Used to send HTTP requests to the CoinMarketCap API.
- `tkinter`: Used to create the graphical user interface (GUI) for the program.
- `bcrypt`: Used for password hashing.
- `matplotlib`: Used for data visualization.
- `pandas_datareader`: Used to retrieve token prices from the CoinMarketCap API.

## How to Use

1. Clone the repository or download the source code.
2. Make sure you have Python 3.x installed on your system.
3. Install the required dependencies by running the following command:
   ```
   pip install -r requirements.txt
   ```
4. Run the program by executing the `crypto_portfolio_tracker.py` file:
   ```
   python crypto_portfolio_tracker.py
   ```
5. The GUI will appear, allowing you to register a new user, log in, manage your tokens, and view portfolio performance.

Note: To retrieve current token prices, the program uses the CoinMarketCap API. You need to sign up on their website and obtain an API key. Replace the placeholder API key in the code with your actual API key for the program to work correctly.

## Limitations

- The program relies on the CoinMarketCap API to retrieve token prices. If the API is unavailable or the token symbol is not recognized, the program will not be able to fetch the current price.
- The program assumes a single user environment and does not support concurrent user sessions.
- The user interface is basic and may not be aesthetically pleasing. You can modify the code to improve the design according to your preferences.

## Future Enhancements

- Implement error handling for API requests to handle network or API-related issues gracefully.
- Add support for multiple user accounts and concurrent user sessions.
- Improve the user interface by using more advanced GUI frameworks or libraries.
- Allow users to set target prices or alerts for tokens and provide notifications when the prices reach the desired levels.
- Implement additional portfolio performance metrics, such as return on investment (ROI) and price change percentages.

Feel free to modify and enhance the program according to your needs and preferences. Happy tracking!
