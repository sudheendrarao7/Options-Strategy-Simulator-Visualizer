# app.py
import streamlit as st
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
from strategies.basic import long_call, long_put, short_call, short_put
from strategies.multi_leg import straddle, strangle, bull_call_spread, bear_put_spread, iron_condor

st.title("📈 Options Strategy Simulator & Visualizer")

top_10_firms = {
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "Amazon": "AMZN",
    "Google (Alphabet)": "GOOGL",
    "Meta (Facebook)": "META",
    "Tesla": "TSLA",
    "NVIDIA": "NVDA",
    "Berkshire Hathaway": "BRK-B",
    "JPMorgan Chase": "JPM",
    "Johnson & Johnson": "JNJ"
}
# Dropdown for top 10 firms
selected_firm = st.selectbox("Select a Firm", list(top_10_firms.keys()))
ticker_symbol = top_10_firms[selected_firm]

ticker = yf.Ticker(ticker_symbol)

# Get option chain for a specific date
expiry_dates = ticker.options
selected_expiry = st.selectbox("Choose Expiry Date", expiry_dates)


chain = ticker.option_chain(selected_expiry)

# Access calls and puts
calls = chain.calls
puts = chain.puts
st.subheader("Option Chain Data")
# View some values
st.write("Calls:")
st.write(calls[['strike', 'lastPrice']].head())

st.write("Puts:")
st.write(puts[['strike', 'lastPrice']].head())


# Strategy selector
strategy = st.selectbox("Choose Strategy", [
    "Long Call", "Short Call", "Long Put", "Short Put",
    "Straddle", "Strangle", "Bull Call Spread", "Bear Put Spread",
    "Iron Condor"
])

# Spot price input (common to all)
spot = st.number_input("Spot Price", min_value=1.0, value=100.0)

# Inputs for single-leg strategies
if strategy in ["Long Call", "Short Call", "Long Put", "Short Put"]:
    strike1 = st.number_input("Strike Price", min_value=1.0, value=(spot))
    premium1 = st.number_input("Premium", min_value=0.0, value=5.0)

# Inputs for Straddle (Call + Put same strike)
elif strategy == "Straddle":
    strike1 = st.number_input("Strike Price (Call & Put)", min_value=1.0, value=float((spot)))
    premium1 = st.number_input("Call Premium", min_value=0.0, value=5.0)
    premium2 = st.number_input("Put Premium", min_value=0.0, value=5.0)

# Inputs for Strangle (Call + Put different strikes)
elif strategy == "Strangle":
    strike_call = st.number_input("Call Strike", min_value=1.0, value=(spot + 5))
    premium_call = st.number_input("Call Premium", min_value=0.0, value=4.0)
    strike_put = st.number_input("Put Strike", min_value=1.0, value=(spot - 5))
    premium_put = st.number_input("Put Premium", min_value=0.0, value=4.0)

# Inputs for Bull Call Spread
elif strategy == "Bull Call Spread":
    long_strike = st.number_input("Buy Call Strike", min_value=1.0, value=(spot - 5))
    long_premium = st.number_input("Buy Call Premium", min_value=0.0, value=6.0)
    short_strike = st.number_input("Sell Call Strike", min_value=1.0, value=(spot + 5))
    short_premium = st.number_input("Sell Call Premium", min_value=0.0, value=2.0)

# Inputs for Bear Put Spread
elif strategy == "Bear Put Spread":
    long_strike = st.number_input("Buy Put Strike", min_value=1.0, value=(spot + 5))
    long_premium = st.number_input("Buy Put Premium", min_value=0.0, value=6.0)
    short_strike = st.number_input("Sell Put Strike", min_value=1.0, value=(spot - 5))
    short_premium = st.number_input("Sell Put Premium", min_value=0.0, value=2.0)


# Inputs for Iron Condor (4 strikes)
elif strategy == "Iron Condor":
    lower_put_strike = st.number_input("Lower Put Strike", min_value=1.0, value=(spot - 20))
    lower_put_premium = st.number_input("Lower Put Premium", min_value=0.0, value=1.0)
    higher_put_strike = st.number_input("Higher Put Strike", min_value=1.0, value=(spot - 10))
    higher_put_premium = st.number_input("Higher Put Premium", min_value=0.0, value=3.0)
    lower_call_strike = st.number_input("Lower Call Strike", min_value=1.0, value=(spot + 10))
    lower_call_premium = st.number_input("Lower Call Premium", min_value=0.0, value=3.0)
    higher_call_strike = st.number_input("Higher Call Strike", min_value=1.0, value=(spot + 20))
    higher_call_premium = st.number_input("Higher Call Premium", min_value=0.0, value=1.0)

# Inputs for Calendar Spread


# Simulate prices
prices = np.linspace(0.5 * spot, 1.5 * spot, 200)

# Calculate payoff
if strategy == "Long Call":
    payoff = long_call(prices, strike1, premium1)

elif strategy == "Short Call":
    payoff = short_call(prices, strike1, premium1)

elif strategy == "Long Put":
    payoff = long_put(prices, strike1, premium1)

elif strategy == "Short Put":
    payoff = short_put(prices, strike1, premium1)

elif strategy == "Straddle":
    payoff = straddle(prices, strike1, premium1, premium2)

elif strategy == "Strangle":
    payoff = strangle(prices, strike_call, premium_call, strike_put, premium_put)

elif strategy == "Bull Call Spread":
    payoff = bull_call_spread(prices, long_strike, long_premium, short_strike, short_premium)

elif strategy == "Bear Put Spread":
    payoff = bear_put_spread(prices, long_strike, long_premium, short_strike, short_premium)

elif strategy == "Butterfly Spread":
    payoff = butterfly_spread(prices, lower_strike, middle_strike, upper_strike, premium_low, premium_mid, premium_up)

elif strategy == "Iron Condor":
    payoff = iron_condor(prices, lower_put_strike, lower_put_premium,
                         higher_put_strike, higher_put_premium,
                         lower_call_strike, lower_call_premium,
                         higher_call_strike, higher_call_premium)




# Plot
st.subheader("Payoff at Expiry")
fig, ax = plt.subplots()
ax.plot(prices, payoff, label="Payoff")
ax.axhline(0, color='black', linestyle='--')
ax.axvline(spot, color='red', linestyle='--', label="Spot Price")
ax.set_xlabel("Stock Price at Expiry")
ax.set_ylabel("Profit / Loss")
ax.legend()
ax.grid(True)
st.pyplot(fig)
