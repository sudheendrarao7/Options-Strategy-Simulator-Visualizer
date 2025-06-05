# strategies/basic.py

import numpy as np

def long_call(prices, strike, premium):
    """
    Payoff = max(S - K, 0) - Premium
    """
    return np.maximum(prices - strike, 0) - premium

def short_call(prices, strike, premium):
    """
    Payoff = -max(S - K, 0) + Premium
    """
    return -1 * (np.maximum(prices - strike, 0) - premium)

def long_put(prices, strike, premium):
    """
    Payoff = max(K - S, 0) - Premium
    """
    return np.maximum(strike - prices, 0) - premium

def short_put(prices, strike, premium):
    """
    Payoff = -max(K - S, 0) + Premium
    """
    return -1 * (np.maximum(strike - prices, 0) - premium)
