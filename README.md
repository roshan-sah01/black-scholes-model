# Black–Scholes Option Pricing Model (Python)

This project implements a **European Black–Scholes option pricing model** from scratch in Python, including **analytical Greeks**, **numerical verification via finite differences**, and **unit tests** to validate correctness.

The goal of this project is to build a **quantitatively sound and testable pricing engine**.

---

## Features

- European option pricing (Call & Put)
- Analytical Greeks:
  - Delta
  - Gamma
  - Vega
- Numerical Greeks using **central finite differences**
- Validation of analytical Greeks vs numerical approximations
- Unit tests covering:
  - Call–put parity
  - Delta bounds
  - Gamma & Vega positivity
  - Analytical vs numerical Greeks consistency
- Clean, modular code structure designed for extension

---

## 🧠 Model Overview

The Black–Scholes model prices European options under assumptions including:
- Lognormal asset prices
- Constant volatility
- Constant risk-free rate
- No arbitrage and frictionless markets

The pricing formula is implemented directly, with Greeks derived analytically and verified numerically.

---

## Numerical Verification

To ensure correctness, Greeks are validated using **central finite-difference approximations**:

- Delta ≈ ∂V/∂S  
- Gamma ≈ ∂²V/∂S²  
- Vega ≈ ∂V/∂σ  

Analytical and numerical results match to floating-point precision.

---

## Testing

Automated tests are written using `pytest` to ensure:
- Pricing consistency via call–put parity
- Correct bounds on Greeks
- Positive curvature and volatility sensitivity
- Agreement between analytical and numerical Greeks

Run tests from the project root:
```bash
python3 -m pytest