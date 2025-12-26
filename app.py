import numpy as np
import matplotlib.pyplot as plt

import streamlit as st
from Black_Scholes import blackscholes, blackscholes_greek


#Page Title
st.set_page_config(page_title="Black-Scholes Model", layout="wide")

st.title("Black-Scholes Option Pricing Model")

st.markdown(
    """
    Interactive pricing and risk analysis for European options using the Black–Scholes model.
    """
)

#Sidebar Inputs
st.sidebar.header("Model Inputs")

S = st.sidebar.number_input("Spot Price (S) [$]: ", min_value=0.01, value= 100.0, step = 0.5, help="Underlying Price in Dollars")
K = st.sidebar.number_input("Strike Price (K) [$]: ", min_value=0.01, value=100.00, step = 0.5, help="Strike Price in Dollars")

t_col, unit_col = st.sidebar.columns([5,3])
T_unit = unit_col.selectbox("Unit: ", ["Days", "Years"], )
if T_unit == "Days":
    T_value = t_col.number_input("Time to Maturity (T):", min_value=1.0, value=365.0, step=1.0, help = "Days until expiry")
    T = T_value/365.0
else: 
    T = t_col.number_input("Time to Maturity (T): ", min_value=1e-6, value=1.0, step=0.05, help="Years (e.g. 0.5 = 6 months)")


r_dec = st.sidebar.number_input("Risk-Free Rate (r) [%]: ", min_value=-10.0, max_value=100.0, value=5.0, step=0.5, help="Annualized continuously-compounded rate in %.") 
r=r_dec/100
sigma_dec = st.sidebar.number_input("Volatility (σ) [%]", min_value=0.1, max_value=500.0, value=20.0, step=1.0, help="Annualized volatility in %.")
sigma = sigma_dec/100

#pricing
call_price = blackscholes(S, K, T, r, sigma, option_type="call")
put_price=blackscholes(S, K, T, r, sigma, option_type="put")

st.header("Option Prices")

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

#Heatmap Sidebar Inputs
st.sidebar.header("Heatmap Settings")

s_max = st.sidebar.number_input("Max Spot Price [$] ", min_value=0.01, value=S * 1.2, step=1.0)
s_min = st.sidebar.number_input("Min Spot Price [$] ", min_value=0.01, value=max(0.01, S * 0.8), step=1.0)
max_vol_pct = st.sidebar.slider("Max Volatility", min_value = 0.01, max_value=300.0, value = sigma * 100 * 1.2, step=0.5)
min_vol_pct = st.sidebar.slider("Min Volatility", min_value=0.01, max_value=300.0, value=max(0.1, sigma * 100 * 0.8), step=0.5)

max_vol = max_vol_pct / 100.0
min_vol = min_vol_pct / 100.0

if s_max <= s_min:
    st.sidebar.error("Max Spot Price must be > Min Spot Price.")
    st.stop()

if max_vol <= min_vol:
    st.sidebar.error("Max Volatility must be > Min Volatility.")
    st.stop()


#HEATMAP
st.title("Interactive Heatmap")
st.caption("Option price as a function of Spot Price (S) and Volatility (σ), holding K, T, r constant.")
N = 10
#Axes Values
s_vals = np.linspace(s_min, s_max, N)
vol_vals = np.linspace(min_vol, max_vol, N)

#Price Grid, Rows = Volatility, Columns = Spot Price
call_grid = np.zeros((N, N))
put_grid = np.zeros((N, N))

for i, v in enumerate(vol_vals):
    for j, s in enumerate(s_vals):
        call_grid[i, j] = blackscholes(s, K, T, r, v, "call")
        put_grid[i, j] = blackscholes(s, K, T, r, v, "put")

def plot_heatmap(grid, s_vals, vol_vals):
    fig, ax = plt.subplots(figsize = (12, 10), dpi=140)
    im = ax.imshow(grid, origin="lower", aspect="auto", interpolation="nearest")

    ax.set_xticks(range(N))
    ax.set_yticks(range(N))
    ax.set_xticklabels([f"{x:.1f}" for x in s_vals], fontsize=18)
    ax.set_yticklabels([f"{v*100:.1f}" for v in vol_vals], fontsize=18)

    ax.set_xlabel("Spot Price (S)", fontsize=20)
    ax.set_ylabel("Volatility (σ) [%]", fontsize=20)

    #Numbers in each cell
    for i in range(N):
        for j in range(N):
            val = grid[i, j]

            # Get the RGBA color of this cell from the colormap
            r_, g_, b_, _ = im.cmap(im.norm(val))

            # Perceived brightness (luminance)
            luminance = 0.2126 * r_ + 0.7152 * g_ + 0.0722 * b_

            text_color = "black" if luminance > 0.55 else "white"

            ax.text(j, i, f"{grid[i, j]:.2f}", ha="center", va="center", fontsize=15, color=text_color)
    
    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)    
    cbar.ax.tick_params(labelsize=16)               # tick number size
    fig.tight_layout()
    return fig

#Plot
callplot, putplot = st.columns(2, gap="large")
with callplot:
    st.header("Call Price Heatmap")
    fig1 = plot_heatmap(call_grid, s_vals, vol_vals)
    st.pyplot(fig1, use_container_width=True, clear_figure=True)

with putplot:
    st.header("Put Price Heatmap")
    fig2 = plot_heatmap(put_grid, s_vals, vol_vals)
    st.pyplot(fig2, use_container_width=True, clear_figure=True)

#Test and Assumptions
st.caption("Unit-tested with pytest (5 tests passing): call-put parity, delta bounds, Greeks vs finite differences, etc.")

st.caption(
    "Model assumptions: European options, constant volatility and interest rate, no dividends."
)

