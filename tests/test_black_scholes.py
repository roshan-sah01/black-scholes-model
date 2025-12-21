import math
import sys
import os 

#Allow tests to import BlackScholes.py
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from Black_Scholes import blackscholes, blackscholes_greek, finite_diff_greeks

#Check call-put parity
def test_call_put_parity():
    # C - P = S - Ke^{-rT} 
    S, K, T, r, sigma = 100, 100, 1.0, 0.05, 0.2

    call = blackscholes(S, K, T, r, sigma, option_type="call")
    put = blackscholes(S, K, T, r, sigma, option_type="put")

    lhs = call - put
    rhs = S - K*math.exp(-r*T)

    assert abs(lhs-rhs) < 1e-6

#test delta bounds
def test_delta_bounds():
    S, K, T, r, sigma = 100, 100, 1.0, 0.05, 0.2

    call_delta = blackscholes_greek(S, K, T, r, sigma, "call") ["delta"]
    put_delta = blackscholes_greek(S, K, T, r, sigma, "put") ["delta"]

    assert 0.0 <= call_delta <= 1.0
    assert -1.0 <= put_delta <= 0.0

#test gamma positivity
def test_gamma_positive():
    S, K, T, r, sigma = 100, 100, 1.0, 0.05, 0.2

    gamma = blackscholes_greek(S, K, T, r, sigma, "call") ["gamma"]

    assert gamma > 0.0

#test vega positivity
def test_vega_positive():
    S, K, T, r, sigma = 100, 100, 1.0, 0.05, 0.2

    vega = blackscholes_greek(S, K, T, r, sigma, "call") ["vega"]

    assert vega > 0.0

#test analytical vs numerical greeks
def test_greeks_match_finite_difference():
    S, K, T, r, sigma = 100, 100, 1.0, 0.05, 0.2

    numerical = finite_diff_greeks(S, K, T, r, sigma, "call")
    analytical = blackscholes_greek(S, K, T, r, sigma, "call") 

    assert abs(numerical["delta"]-analytical["delta"]) < 1e-6
    assert abs(numerical["gamma"]-analytical["gamma"]) < 1e-6
    assert abs(numerical["vega"]-numerical["vega"]) < 1e-6




