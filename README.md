# STAT5030_Numerical_Methods_Group_Project
STAT5030NumericalMethodsGroupProject: Prepayment Modelling
## Introduction：
## Part 1: Construct the Yield Curve
This part constructs a U.S. Treasury yield curve using real-time data from the Federal Reserve Economic Data (FRED) database, and provides three interpolation methods for curve fitting and rate extraction.

---

# Features

- **Live FRED Data Ingestion** — Fetches the latest available Treasury yields across 11 maturities (1-month to 30-year)
- **Three Interpolation Methods:**
  - Piecewise Constant: Returns the yield of the nearest tenor node to the left. Forward rates are constant within each interval, derived analytically from consecutive discount factors.
  - Cubic Spline: Uses SciPy's `CubicSpline` with natural boundary conditions fitted directly to the observed yields. Produces a smooth, twice-differentiable yield curve.
  - Area-Preserving Quadratic Spline (APQS)(Hagan, 2018): Forward rates are represented as **quadratic** within each interval. Solves a banded linear system to determine forward rate node values (`f_nodes`). The integral of the forward curve exactly reproduces the observed discount factors (area-preserving). Avoids the oscillation artifacts common in cubic spline forward curves. 

- **Rate Extraction Utilities** — Forward rates, discount factors, and zero rates for any maturity
- **Visualization** — Side-by-side comparison plot of all three interpolation methods

# Structure

```
├── 1. get_treasury_yields_from_fred()
│       No inputs
│       Returns: pd.DataFrame with columns Maturity (years) and Yield (%)
│       Fetches the latest non-null business day Treasury yields from FRED
│       across 11 tenors: 1M, 3M, 6M, 1Y, 2Y, 3Y, 5Y, 7Y, 10Y, 20Y, 30Y
│
├── 2. class YieldCurve
│   │
│   ├── __init__(self, maturities, yields)
│   │       maturities : array-like of float  – tenor nodes in years, unsorted ok
│   │       yields     : array-like of float  – zero yields in decimal (e.g. 0.045)
│   │       Internally computes discount factors P(0,T) = exp(-y·T) and
│   │       piecewise constant forward rates A[j] for each interval
│   │
│   ├── get_interpolation(self, method='apqs')
│   │       method : str – 'piecewise' | 'cubic' | 'apqs'  (default: 'apqs')
│   │       Returns: Callable f(t) → yield (decimal) for any maturity t
│   │
│   ├── _build_apq_spline(self)                         [internal]
│   │       No inputs (uses self.A, self.delta, self.T_aug)
│   │       Solves a banded linear system for forward rate nodes f_nodes,
│   │       then returns yield_func(t) and stores forward_func as
│   │       self._apqs_forward_func
│   │
│   ├── get_forward_rate(self, t, method='apqs')
│   │       t      : float or array-like – maturity in years
│   │       method : str – 'apqs' | 'cubic' | 'piecewise'  (default: 'apqs')
│   │       Returns: np.ndarray – instantaneous forward rate f(t) in decimal
│   │
│   ├── get_discount_factor(self, t, method='apqs')
│   │       t      : float or array-like – maturity in years
│   │       method : str – 'apqs' | 'cubic' | 'piecewise'  (default: 'apqs')
│   │       Returns: np.ndarray – P(0,t) = exp(-∫₀ᵗ f(s)ds) in (0, 1]
│   │
│   └── get_zero_rate(self, t, method='apqs')
│           t      : float or array-like – maturity in years
│           method : str – 'apqs' | 'cubic' | 'piecewise'  (default: 'apqs')
│           Returns: np.ndarray – y(t) = -log(P(0,t))/t in decimal
│                    At t=0, approximated as f(1e-8) to avoid division by zero
│
└── 3. Visualization
        Plots yield curves from all three methods against raw FRED market data
        (red dots=market, blue dashed=piecewise, red dash-dot=cubic, black=APQS)
```


## Part 2: Calibrate and Simulate Interest Rate Paths



## Part 3: Model Nonlinear Prepayment Behavior under changing interest rate conditions



## Part 4: MBS Valuation







## Citations：
Hagan, P. S. (2018). Building curves using area preserving quadratic splines https://onlinelibrary.wiley.com/doi/abs/10.1002/wilm.10676