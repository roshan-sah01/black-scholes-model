"""
Black-Scholes European Option Pricing Model

Description:
Prices European call and put options using the Black-Scholes formula.
User inputs spot price, strike, maturity, risk-free rate, and volatility.
"""

#for data manipulation
import numpy as np

#for statistics
from scipy import stats as st 

#Define the Black Scholes Model formula:
def blackscholes(S, K, T, r, sigma, option_type="call"):
    """
    Parameters/Variables
    S (float)= Spot Price (Current Strike Price)
    K (float)= Strike Price
    T (float)= Time of Maturity (Years)
    r (float)= Risk free interest rate
    sigma (float)= Volatility/Standard Deviation
    type (str)= 'call' or 'put'

    Returns: String
    """

    if T <= 0 and sigma <= 0:
        raise ValueError("Time to maturity and volatility must be positive.")

    d_1 = (np.log(S/K)+(r+0.5*sigma**2)*T)/(sigma*np.sqrt(T))
    d_2 = d_1-sigma*np.sqrt(T)

    if option_type == 'call':
        price = S*st.norm.cdf(d_1, loc=0, scale=1)-K*np.exp(-r*T)*st.norm.cdf(d_2, loc=0, scale=1)
    
    elif option_type == 'put':
        price = K*np.exp(-r*T)*st.norm.cdf(-d_2, loc=0, scale=1)-S*st.norm.cdf(-d_1, loc=0, scale=1)
        
    else:
        raise ValueError("Invalid option type. Must be 'call' or 'put'.")
    
    return price

#function to allow users to input the parameters
if __name__ == "__main__":
    S = float(input("Enter Spot Price: ")) #Taking S from user as input

    K = float(input("Enter Strike Price: ")) 

    T_days = float(input("Enter Time of Maturity(in Days): "))
    T = float(T_days/365) #Convert days to year

    r = float(input("Enter Risk-Free Interest Rate: "))

    sigma = float(input('Enter Volatiliy: '))

    option_type = str(input("Enter option type(call/put):").strip().lower()) #Take input while removing any spaces and converting to lower case.

    price = blackscholes(S, K, T, r, sigma, option_type)
    print(f"European {option_type.capitalize()} Price: ${price:.4f}")