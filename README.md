# STAT5030_Numerical_Methods_Group_Project
STAT5030NumericalMethodsGroupProject: Prepayment Modelling
# Introduction：
This project implements a full pipeline for Mortgage-Backed Securities (MBS) valuation under stochastic interest rate dynamics. It is structured in four parts: Part 1 constructs a U.S. Treasury yield curve from live FRED data using three interpolation methods (Piecewise Constant, Cubic Spline, and the area-preserving quadratic spline APQS method). Part 2 calibrates a 2-Factor Hull-White model to the fitted curve and simulates short-rate paths via Monte Carlo. Part 3 models nonlinear prepayment (CPR) behavior across all simulated paths. Part 4 discounts the resulting cash flows using the simulated rates to compute a theoretical MBS price via Monte Carlo pricing.

---
# Part 1: Construct the Yield Curve
This part constructs a U.S. Treasury yield curve using real-time data from the Federal Reserve Economic Data (FRED) database, and provides three interpolation methods for curve fitting and rate extraction.

---

## Features

- **Live FRED Data Ingestion** — Fetches the latest available Treasury yields across 11 maturities (1-month to 30-year)
- **Three Interpolation Methods:**
  - Piecewise Constant: Returns the yield of the nearest tenor node to the left. Forward rates are constant within each interval, derived analytically from consecutive discount factors.
  - Cubic Spline: Uses SciPy's `CubicSpline` with natural boundary conditions fitted directly to the observed yields. Produces a smooth, twice-differentiable yield curve.
  - Area-Preserving Quadratic Spline (APQS)(Hagan, 2018): Forward rates are represented as 
  
  **quadratic** within each interval. Solves a banded linear system to determine forward rate node values (`f_nodes`). The integral of the forward curve exactly reproduces the observed discount factors (area-preserving). Avoids the oscillation artifacts common in cubic spline forward curves. 

- **Rate Extraction Utilities** — Forward rates, discount factors, and zero rates for any maturity
- **Visualization** — Side-by-side comparison plot of all three interpolation methods

---

## Structure

```
├── 1. get_treasury_yields_from_fred()   # FRED data ingestion
├── 2. class YieldCurve                  # Interpolation engine
│   ├── __init__(self, maturities, yields)
        # Builds discount factors & piecewise forward rates
│   ├── get_interpolation(method)        # Returns callable yield curve function
│   ├── _build_apq_spline()              # APQS (Hagan) spline construction
│   ├── get_forward_rate(t, method)      # Instantaneous forward rate f(t)
│   ├── get_discount_factor(t, method)   # Discount factor P(0,t)
│   └── get_zero_rate(t, method)         # Zero/spot rate y(t)
└── 3. Visualization                     # Interpolation comparison plot
```

---



# Part 2: Calibrate and Simulate Interest Rate Paths



# Part 3: Model Nonlinear Prepayment Behavior under changing interest rate conditions



# Part 4: MBS Valuation







# Citations：
Hagan, P. S. (2018). Building curves using area preserving quadratic splines https://onlinelibrary.wiley.com/doi/abs/10.1002/wilm.10676