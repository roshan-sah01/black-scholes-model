import streamlit as st
from Black_Scholes import blackscholes, blackscholes_greek

#Page Title
st.set_page_config(page_title="Black-Scholes Model", layout="centered")

st.title("Black-Scholes Option Pricing Model")

st.markdown(
    """
    Interactive pricing and risk analysis for European options using the Black–Scholes model.
    """
)

#Sidebar Inputs
st.sidebar.header("Model Inputs")

S = st.sidebar.number_input("Spot Price (S): ", min_value=0.01, value= 100.0, step = 0.5, help="Underlying Price in Dollars")
K = st.sidebar.number_input("Strike Price (K): ", min_value=0.01, value=100.00, step = 0.5, help="Strike Price in Dollars")

t_col, unit_col = st.sidebar.columns([2,1])
T_unit = unit_col.selectbox("Unit: ", ["Days", "Years"], )
if T_unit == "Days":
    T_value = t_col.number_input("Time to Maturity (T): ", min_value=1.0, value=365.0, step=1.0, help = "Days until expiry")
    T = T_value/365.0
else: 
    T = t_col.number_input("Time to Maturity (T): ", min_value=1e-6, value=1.0, step=0.05, help="Years (e.g. 0.5 = 6 months)")


r_dec = st.sidebar.number_input("Risk-Free Rate (r): ", min_value=-10.0, max_value=100.0, value=5.0, step=0.5, help="Annualized continuously-compounded rate in %.") 
r=r_dec/100
sigma_dec = st.sidebar.number_input("Volatility (σ)", min_value=0.0001, max_value=500.0, value=20.0, step=1.0, help="Annualized volatility in %.")
sigma = sigma_dec/100

#pricing
call_price=blackscholes(S, K, T, r, sigma, option_type="call")
put_price=blackscholes(S, K, T, r, sigma, option_type="put")

st.subheader("Option Prices")

col1, col2 = st.columns(2)
col1.metric("Call Price", f"${call_price:.4f}")
col2.metric("Put Price", f"${put_price:.4f}")

#greeks
greeks_call = blackscholes_greek(S, K, T, r, sigma, option_type="call")
greeks_put = blackscholes_greek(S, K, T, r, sigma, option_type="put")

st.subheader("Greeks")

delta_type = st.radio(
    "Delta shown for:",
    ["Call", "Put"],
    horizontal=True
)

delta_value = (
    greeks_call["delta"]
    if delta_type == "Call"
    else greeks_put["delta"]
)

st.caption(
    "Gamma and Vega are identical for calls and puts under Black–Scholes."
)

col3, col4, col5 = st.columns(3)

col3.metric("Delta", f"{delta_value:.6f}")
col4.metric("Gamma", f"{greeks_call['gamma']:.6f}")
col5.metric("Vega", f"{greeks_call['vega']:.6f}")


st.caption(
    "Model assumptions: European options, constant volatility and interest rate, no dividends."
)

st.caption("Unit-tested with pytest (5 tests passing): call-put parity, delta bounds, Greeks vs finite differences, etc.")