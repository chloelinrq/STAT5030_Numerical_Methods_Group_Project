# STAT5030_Numerical_Methods_Group_Project
STAT5030NumericalMethodsGroupProject: Prepayment Modelling
# Introduction：
This project implements a full pipeline for Mortgage-Backed Securities (MBS) valuation under stochastic interest rate dynamics. It is structured in four parts: Part 1 constructs a U.S. Treasury yield curve from live FRED data using three interpolation methods (Piecewise Constant, Cubic Spline, and the area-preserving quadratic spline APQS method). Part 2 calibrates a 2-Factor Hull-White model to the fitted curve and simulates short-rate paths via Monte Carlo. Part 3 models nonlinear prepayment (CPR) behavior across all simulated paths. Part 4 discounts the resulting cash flows using the simulated rates to compute a theoretical MBS price via Monte Carlo pricing. At the end, we show the nuainces of pricing methologies using different interet rate models as a result. 

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

Data Source: After looking carefully at data source available as free online, we found real prepayment information about aggregated mortgages based in 2019 that has different types of bond cashflows. From here, you can find out: "Supplemental Daily Prepayment Report" where you can find out the real prepayent data. 
https://capitalmarkets.freddiemac.com/mbs/daily-prepayment-report

In terms of the prepayment computation, we first compute to find out each of the bond's Annualized Prepayment Rate (CPR), meaning the percentage you expect for the bond to prepay within an year. For example, given the Annaulzed CPR of 5%, then you expect the bond to prepay 5 percent of the outstanding principal (how much balance is left for the mortgage to be prepaid by the mortgage owners). 

To compute Annualzed CPR, we use: CPR = 1 - (1- SMM)^12, where the amount of principal includes not just principal itself but other financing costs like selling homes and taxes. So SMM is the percentage that we expect the prepayment to be made in a month, accounting for the monthly sentiment of prepayment. so when SMM is 1 percent, we know that 1 percent of the remaining balance was prepayed, rather than yearly. And this amount is driven by the following equation:

SMM = Unscheduled Principal / (Current Loan or Bond balance - Scheduled Principal)

So in our table given, we have: 
Scheduled principal: Originally planned set principal amount. 
Unsheculed principal: Payments that were not part of the original plan like refinancing, home selling, taxation, etc. 

In our data, we match the following as: 
Beginning Balance = "Cohort Current UPB"
Scheduled Principal = "Scheduled Principal"
Principal Reduction Amount = "Unscheduled Principal Reduction Amount"
Unscheduled Principal = "Unscheduled Principal Reduction Amoun"t"

And we compute SMM. Afterwards, we compute CPR using the equation above: CPR = 1 - (1- SMM)^12
Now we have Annualized CPR. 

As we have the Annualzied CPR of each bonds at that period of time, 

# Part 4: MBS Valuation





# Citations：
Hagan, P. S. (2018). Building curves using area preserving quadratic splines https://onlinelibrary.wiley.com/doi/abs/10.1002/wilm.10676