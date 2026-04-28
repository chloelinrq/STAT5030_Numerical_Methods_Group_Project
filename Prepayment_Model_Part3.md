# Part 3: Model Nonlinear Prepayment Behavior under changing interest rate conditions
## Using Monte Carlo Prepayment Methodologies

### 1. Prepayment Computation Framework
The foundational metrics for measuring prepayment speed are derived from the **Single Monthly Mortality (SMM)** and the **Conditional Prepayment Rate (CPR)**.

#### Monthly Prepayment Rate (SMM)
The SMM represents the percentage of the outstanding principal balance (after scheduled payments) that was prepaid in a given month.
$$SMM = \frac{\text{Unscheduled Principal}}{\text{Beginning Balance} - \text{Scheduled Principal}}$$

Based on the Freddie Mac Supplemental Daily Prepayment Report, we map the variables as follows:
* **Beginning Balance:** Cohort Current UPB
* **Scheduled Principal:** Scheduled Principal
* **Unscheduled Principal:** Unscheduled Principal Reduction Amount

#### Annualized Prepayment Rate (CPR)
To annualize the monthly sentiment into a yearly expectation:
$$CPR = 1 - (1 - SMM)^{12}$$

---

### 2. The Logistic Prepayment Model (S-Curve)
Refinancing behavior is non-linear. Homeowners do not respond to interest rate changes linearly; instead, they follow an **S-Curve** relationship. Prepayment speeds accelerate once a specific threshold is hit but plateau (burnout) as the pool of rational refinancers depletes.

To model this, we use the **Logistic Curve** equation:
$$CPR(t) = CPR_{min} + (CPR_{max} - CPR_{min}) \times \left( \frac{1}{1 + e^{-k(I_t - x_0)}} \right)$$

**Variable Definitions:**
* **$I(t) = c - r(t)$**: The **Refinance Sentiment**. 
    * $c$: Original mortgage coupon rate.
    * $r(t)$: Current market rate (projected via the Hull-White Model).
* **$CPR_{min} / CPR_{max}$**: The floor and ceiling of prepayment speeds, determined via Bootstrap sampling.
* **$k$**: Sensitivity factor (how fast the market reacts to rate drops).
* **$x_0$**: Threshold (the spread required before refinancing becomes economically attractive).

---

### 3. Methodology: Bootstrap Monte Carlo
To avoid the limitations of deterministic models or assuming a perfect Normal distribution, we apply a **Bootstrap sampling** method within our Monte Carlo framework.

#### Stochastic $CPR_{min}$ and $CPR_{max}$
Instead of fixed values, we draw from the actual 2019 data distribution:
1.  **Lower Bound ($CPR_{min}$):** We isolate the bottom 20% of the observed CPR distribution and resample uniformly. This captures the "baseline" turnover (moves, deaths, divorces) that occurs regardless of rates.
2.  **Upper Bound ($CPR_{max}$):** We isolate the top 20% of the observed CPR distribution and resample uniformly. This captures the maximum "refinance surge" capacity of the market.

#### The Simulation Process
1.  **Interest Rate Path:** Generate $r(t)$ using the **Hull-White short-rate model**.
2.  **Sentiment Calculation:** Compute $I(t)$ for each time step.
3.  **Bootstrap Draw:** For each simulation path, draw a $CPR_{min}$ and $CPR_{max}$ from the empirical 2019 dataset.
4.  **CPR Projection:** Apply the Logistic function to find the future projected prepayment rate.

---

### 4. Summary of Results
By resampling uniformly from observed data points, the model captures **realistically skewed distributions**. This accounts for the fact that refinancing behavior is often suppressed by friction costs and "burnout," providing a more robust risk assessment for mortgage-backed securities than traditional Gaussian simulations.
