# STAT5030_Numerical_Methods_Group_Project
# Introduction：
This project prices Mortgage-Backed Securities by simulating prepayment behavior under realistic interest rate conditions. It is structured in four parts: Part 1 constructs a U.S. Treasury yield curve from live FRED data using three interpolation methods (Piecewise Constant, Cubic Spline, and the area-preserving quadratic spline APQS method). Part 2 calibrates a 2-Factor Hull-White model to the fitted curve and simulates short-rate paths via Monte Carlo. Part 3 models nonlinear prepayment (CPR) behavior across all simulated paths. Part 4 discounts the resulting cash flows using the simulated rates to compute a theoretical MBS price via Monte Carlo pricing. At the end, we show the nuainces of pricing methologies using different interet rate models as a result.

---
# Part 1: Construct the Yield Curve
This part constructs a U.S. Treasury yield curve using real-time data from the Federal Reserve Economic Data (FRED) database, and provides three interpolation methods for curve fitting and rate extraction.


---

## Features

- **Live FRED Data Ingestion** — Fetches the latest available Treasury yields across 11 maturities (1-month to 30-year)
- **Three Interpolation Methods:**
  - Piecewise Constant: Returns the yield of the nearest tenor node to the left. Forward rates are constant within each interval, derived analytically from consecutive discount factors.
  - Cubic Spline: Uses SciPy's `CubicSpline` with natural boundary conditions fitted directly to the observed yields. Produces a smooth, twice-differentiable yield curve.
  - Area-Preserving Quadratic Spline (APQS)(Hagan, 2018): Forward rates are represented as quadratic within each interval. Solves a tridiagonal linear system to determine forward rate node values (`f_nodes`). The integral of the forward curve exactly reproduces the observed discount factors (area-preserving). In theory, avoids the "double hump" artifacts common in smart quadratic methods by enforcing continuity of the derivative at each node. In practice, performance depends on data quality and node spacing.

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



# Part 3: Model Nonlinear Prepayment Behavior under changing interest rate conditions (Using Monte Carlo Prepayment Methodologies)

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
Now we have Annualized CPR, where based on textbook: "Bond Markets, Analysis and Strategies", the conditional prepayment rate follows S-Curve where as the mortgage rate at first accelates as there is a boudnary in the middle of the curve that is attractive for borrowers to refinance and make large prepayments. However, as the market rate continues to go up higher, the S-curve smooths out as it becomes less attractive for borrowers to make large prepaymetns due to the unattractive high mortgage rate.
[Image]
To model this S-curve refinance relationship of prepayment and market mortgage rate, logistic curve is our decision to use to project the ideal future prepayment rate. For this computation, we use:

As we have the Annualzied CPR of each bonds at that period of time, then we look at the distribution of our annualized CPR so we can compute the future projected CPR (Conditional Prepayment Rate) where we use the equations based on CPR min and max.

CPR (t) = Future Conditional Prepayment Rate = CPR(min) + (CPR max - CPR min) * (1/1+e^-k(It-x0))

where I(t) = c - r(t):
I(t): refiannce sentiment
c: the original rate that the bond was issued that the mortage owner has been prepaying
r(t): the current market rate that if the bond holder refinancees, then they will use this current market rate as the new mortage rate.

For the CPR min, this is the bottom distribution's minimum CPR based on our data distribution and vice versa for CPR max.

k: sensitivity / tolerance level of the model that refines how fast or slow it captures the CPR increases.
x0: threshhold -> minimum threshold that distinguishes the decision to refinance or not.

To project the prepayment, we decided to use Monte Carlo Method's application of Boostrap methodology. While the traditional Monte Carlo method simulates from a simulation of randomized distribution that is not drawing from the original data set, the Bootstrap methodology draws from an actual data as distribution.

In the bootstrap sampling methods, to compute minimum CPR, we take the 20 percent bottom distribution of the CPR data and resample uniformly from the observed data points to capture real CPR data set that may not be normally distributed but rather realisically skewed due as CPR follows S curve relationship with refiannce behavior. This approach approximates CPR's low mean value better than just finding the edge of the dataset and cutting the minimum part of the dataset which can be abrupt in capturing the distribution. Similarly, we do run the same botstramp sampling methods for high CPR located in 20 percent top of the distribution in CPR.

*Applying what we learned in class, this strategy avoids having a deterministics min and max cpr to Monte Carlo Method that captures the distribution of CPR. 
Now that we have both min CPR and max CPR, we combine our datasets with the projected interest rate from White Hull scenarios given from Hull White Model given as r(t) to compute the I(t)  as refinance sentiment and we now have all the satisified inputs. Then, we now project the Future conditional Prepayment Rate. 

Our result indicates that

Given the projected CPR, 
It is resampling uniformly from the observed data points. 


# Part 4: MBS Valuation
This part implements Mortgage-Backed Security (MBS) valuation using simulated short rate paths from a Hull-White model and CPR projections from a refinancing model. It supports single- and multi-coupon pricing with pathwise discounting.

1. For the MBS valuation process, we now have two key inputs: short rate paths and CPR paths.

2. Now, our future cash flows follow the equation:

$$CF_t = \text{Interest}_t + \text{Scheduled Principal}_t + \text{Prepayment}_t$$

Where:
- $Interest_t = Balance_{t-1} \times q$ (where $q = Coupon Rate / 12$)
- $Scheduled Principal_t = \min(PMT - Interest_t, B_{t-1})$
- $Prepayment_t = SMM_t \times (B_{t-1} - Scheduled Principal_t)$

3. We discount the cash flows back using the discount factors ($DF_t$) derived from the Hull-White short-rate paths:

$$PV = \sum_{t=1}^{T} CF_t \times DF_t$$

4. Finally, we compute the average Present Value across all $N$ simulated paths to get the price of MBS:

$$\text{Value} = \frac{1}{N} \sum_{i=1}^{N} PV_i$$

---

## Features

**Simulated Short Rate Integration** — Uses Hull-White simulated short rate paths (`hw_rates`) with shape `(M × N+1)` for monthly discounting

**CPR Path Selection** — Retrieves path-specific CPR projections from `refi_df` based on the MBS coupon rate, pivoted to a `(M × N+1)` matrix

**Monte Carlo Pricing** — Returns the MBS price as the average of all path present values

**Multi-Coupon Support** — Prices multiple coupon rates in batch for sensitivity analysis

---

## Structure

```
├── 1. calculate_mbs_price()            # Core Monte Carlo pricing logic
│   ├── Compute monthly payment         # pmt = B0 × (q(1+q)^N) / ((1+q)^N - 1)
│   ├── Loop over each Monte Carlo path
│   └── Return average price + path PVs
│
├── 2. run_mbs_valuation()              # Wrapper to orchestrate simulation
│   ├── Load/simulate hw_rates          # Hull-White short rate paths (M × N+1)
│   ├── Load refi_df with CPR projections
│   ├── Call calculate_mbs_price()
│   └── Return price and path PVs
│
└── 3. Analysis & Visualization         # Coupon sensitivity plotting
```
---


# Citations：
Hagan, P. S. (2018). Building curves using area preserving quadratic splines https://onlinelibrary.wiley.com/doi/abs/10.1002/wilm.10676
