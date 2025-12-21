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

#Implementing Greeks 
def blackscholes_greek(S, K, T, r, sigma, option_type = "call"):
    if T <= 0 or sigma <= 0:
        return ValueError("Time to Maturity and Volatility must be positive.")

    option_type = option_type.strip().lower()

    d_1 = (np.log(S/K)+(r+0.5*sigma**2)*T)/(sigma*np.sqrt(T))

    d_2 = d_1-sigma*np.sqrt(T)

    #delta
    if option_type == "call":
        delta = st.norm.cdf(d_1)
    
    elif option_type == "put":
        delta = st.norm.cdf(d_1) - 1

    else:
        return ValueError("Option type must be call or put.")
    
    gamma = (st.norm.pdf(d_1))/(S*sigma*np.sqrt(T))

    vega = S*st.norm.pdf(d_1)*np.sqrt(T)

    return {
        "delta": float(delta),
        "gamma": float(gamma),
        "vega": float(vega),
        "d1": float(d_1),
        "d2": float(d_2),
    }



def finite_diff_greeks(S, K, T, r, sigma, option_type= "call", eps_S= 1e-4, eps_sigma = 1e-4):
    """
    Numerical approximations of greeksusing central differences. 
    eps_S is the small relative bump of spot price. 
    eps_sigma is the small absolute bump of volatility.
    """

    option_type = option_type.strip().lower()

    dS = S * eps_S
    dsigma = eps_sigma

    V_up = blackscholes(S + dS, K, T, r, sigma, option_type)    #Price after bump up
    V_down = blackscholes(S - dS, K, T, r, sigma, option_type)  #Price after bump down
    V_0 = blackscholes(S, K, T, r, sigma, option_type)                 #Original price

    delta_num = (V_up - V_down)/(2*dS)                            #Delta is the first derivative.
    gamma_num = (V_up - 2*V_0 + V_down) / (dS**2)               #Gamma is the second derivative

    Vol_up = blackscholes(S, K, T, r, sigma + dsigma, option_type)
    Vol_down = blackscholes(S, K, T, r, sigma - dsigma, option_type)
    vega_num = (Vol_up - Vol_down) / (2 * dsigma)

    return{
        "delta": float(delta_num),
        "gamma": float(gamma_num),
        "vega": float(vega_num)
    }


#function to allow users to input the parameters
if __name__ == "__main__":
    S = float(input("Enter Spot Price: ")) #Taking S from user as input

    K = float(input("Enter Strike Price: ")) 

    T_days = float(input("Enter Time of Maturity(in Days): "))
    T = float(T_days/365) #Convert days to year

    r = float(input("Enter Risk-Free Interest Rate: "))

    sigma = float(input('Enter Volatility: '))

    option_type = str(input("Enter option type(call/put):").strip().lower()) #Take input while removing any spaces and converting to lower case.

    price = blackscholes(S, K, T, r, sigma, option_type)
    print(f"European {option_type.capitalize()} Price: ${price:.4f}")

    greeks = blackscholes_greek(K, S, T, r, sigma, option_type)
    print("Greeks: ", {k: round(v, 6) for k, v in greeks.items() if k in ("delta", "gamma", "vega")})

    #compare the analytical and numerical greeks
    analytical = blackscholes_greek(S, K, T, r, sigma, option_type)
    numerical = finite_diff_greeks(S, K, T, r, sigma, option_type)

    print("\nAnalytical greeks:", {k: round(v, 6) for k, v in analytical.items() if k in ("delta", "gamma", "vega")})
    print("Numerical greeks:", {k: round(v, 6) for k, v in numerical.items()})

    print("\nAbsolute diff:", {k: round(abs(analytical[k] - numerical[k]), 10) for k in ("delta", "gamma", "vega")})