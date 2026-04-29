# ============================================================
# Effective Duration & Convexity Analysis
# ============================================================
# This section computes the effective duration and convexity
# of the MBS price with respect to parallel shifts in the
# yield curve using finite differences.
#
# Methodology:
#   1. Shift the entire yield curve up/down by 25bp
#   2. Re-run the full MC MBS valuation for each shifted curve
#   3. Compute:
#      Eff. Duration  = (P_down - P_up) / (2 * shift * P_base)
#      Eff. Convexity = (P_up + P_down - 2*P_base) / (shift^2 * P_base)
# ============================================================

def run_mbs_valuation_shifted(shift_bps, method='apqs', B0=1.0, 
                               coupon_rate=0.04, N=361, seed=42, n_paths=50):
    """
    Run MBS valuation with a parallel shift applied to the yield curve.
    Uses the same pipeline as run_mbs_valuation but with shifted yields.
    """
    shift_decimal = shift_bps / 10000.0
    shifted_yields = np.array(yields) + shift_decimal
    
    T_sim = N / 12
    n_steps = N
    
    curve_shifted = YieldCurve(maturities, shifted_yields)
    hw_shifted = HullWhiteModel(curve_shifted, a=a, b=b, sigma=sigma, 
                                 eta=eta, rho=rho, method=method)
    rates, _, _, t_grid = hw_shifted.simulate(
        T=T_sim, n_steps=n_steps, n_paths=n_paths, seed=seed
    )
    
    n_paths_sim, n_times = rates.shape
    short_rate_df_shifted = pd.DataFrame({
        "path_id": np.repeat(np.arange(n_paths_sim), n_times),
        "time_years": np.tile(t_grid, n_paths_sim),
        "month": np.tile(np.round(t_grid * 12).astype(int), n_paths_sim),
        "short_rate": rates.reshape(-1)
    })
    
    refi_df_shifted = coupon_df.merge(short_rate_df_shifted, how='cross')
    refi_df_shifted['refi_incentive'] = refi_df_shifted['coupon_rate'] - refi_df_shifted['short_rate']
    refi_df_shifted['CPR_proj'] = cpr_min + (cpr_max - cpr_min) / (
        1 + np.exp(-k_hat * (refi_df_shifted['refi_incentive'] - theta_hat))
    )
    
    price, all_pvs = calculate_mbs_price(
        B0=B0, coupon_rate=coupon_rate, N=N,
        hw_rates=rates, refi_df=refi_df_shifted, method=method
    )
    return price, all_pvs


# --- Compute Duration and Convexity across coupon rates ---

shift_bps = 25
shift = shift_bps / 10000.0
n_paths_dur = 50

duration_results = []
for c in coupon_list:
    print(f"Computing duration for coupon={c:.1%}...")
    
    p_base, _ = run_mbs_valuation(method='apqs', coupon_rate=c, 
                                   n_paths=n_paths_dur, seed=42)
    p_up, _ = run_mbs_valuation_shifted(shift_bps=shift_bps, coupon_rate=c,
                                         n_paths=n_paths_dur, seed=42)
    p_down, _ = run_mbs_valuation_shifted(shift_bps=-shift_bps, coupon_rate=c,
                                           n_paths=n_paths_dur, seed=42)
    
    eff_dur = (p_down - p_up) / (2 * shift * p_base)
    eff_conv = (p_up + p_down - 2 * p_base) / (shift**2 * p_base)
    
    duration_results.append({
        'coupon_rate': c,
        'price_base': p_base,
        'price_up': p_up,
        'price_down': p_down,
        'eff_duration': eff_dur,
        'eff_convexity': eff_conv
    })

duration_df = pd.DataFrame(duration_results)
print("\n")
print(duration_df[['coupon_rate', 'price_base', 'eff_duration', 'eff_convexity']].to_string(index=False))


# --- Visualization ---

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

ax1.plot(duration_df['coupon_rate'], duration_df['eff_duration'], 
         marker='o', color='steelblue', linewidth=2)
ax1.set_xlabel('Coupon Rate')
ax1.set_ylabel('Effective Duration')
ax1.set_title('Effective Duration by Coupon Rate')
ax1.grid(True, alpha=0.3)

ax2.plot(duration_df['coupon_rate'], duration_df['eff_convexity'], 
         marker='s', color='coral', linewidth=2)
ax2.set_xlabel('Coupon Rate')
ax2.set_ylabel('Effective Convexity')
ax2.set_title('Effective Convexity by Coupon Rate')
ax2.grid(True, alpha=0.3)

plt.suptitle('MBS Interest Rate Sensitivity (±25bp parallel shift)', fontsize=13)
plt.tight_layout()
plt.show()
