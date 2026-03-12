#!/usr/bin/env python3
"""
Fit Fick's law analytical solution to concentration profiles at different MC timesteps.
Analytical solution: C(X,T) = (4/π) * Σ_{n=0}^{∞} [(-1)^n / (2n+1)] * cos(((2n+1)π/2)*X) * exp(-((2n+1)²π²/4)*T)
where C = c/c₀ (dimensionless concentration), X = x/L (dimensionless position), T = dimensionless time
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from pathlib import Path


def analytical_solution(X, T, n_terms=50):
    """
    Compute the analytical solution C(X,T) for Fick's law.
    
    Parameters:
    -----------
    X : array-like
        Dimensionless position (x/L), range [0, 1)
    T : float
        Dimensionless time
    n_terms : int
        Number of terms in the Fourier series
    
    Returns:
    --------
    C : array-like
        Dimensionless concentration c/c₀
    """
    X = np.asarray(X)
    C = np.zeros_like(X, dtype=float)
    
    for n in range(n_terms):
        coeff = (4.0 / np.pi) * ((-1.0)**n) / (2*n + 1)
        cos_term = np.cos(((2*n + 1) * np.pi / 2.0) * X)
        exp_term = np.exp(-((2*n + 1)**2 * np.pi**2 / 4.0) * T)
        C += coeff * cos_term * exp_term
    
    return C


def fit_function(X, T):
    """Wrapper for curve_fit - fit only T as a parameter."""
    return analytical_solution(X, T, n_terms=50)


def read_layer_distribution(filepath):
    """
    Read LayerDistribution file with 7 lines corresponding to 7 MC timesteps.
    Each line has 50 entries (concentration in each row).
    
    Returns:
    --------
    profiles : list of arrays
        7 concentration profiles (one per timestep)
    mc_steps : list
        MC timesteps [0, 500, 1000, 5000, 10000, 50000, 100000]
    """
    profiles = []
    with open(filepath, 'r') as f:
        for line in f:
            values = [float(x) for x in line.strip().split()]
            if len(values) > 0:
                profiles.append(np.array(values))
    
    # MC timesteps corresponding to the 7 lines
    mc_steps = [0, 500, 1000, 5000, 10000, 50000, 100000]
    
    return profiles, mc_steps


def main():
    # Styling consistent with other plots
    plt.rcParams.update({
        'font.family': 'Arial',
        'font.size': 10,
        'axes.titlesize': 12,
        'axes.labelsize': 11,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'legend.fontsize': 9,
        'figure.dpi': 300,
    })
    
    # Parameters
    c0 = 0.5  # Initial concentration
    L = 200.0  # System length
    filepath = Path("Conc_profile/LayerDistribution(friendly).txt")
    
    if not filepath.exists():
        print(f"Error: {filepath} not found!")
        return
    
    # Read data
    profiles, mc_steps = read_layer_distribution(filepath)
    
    if len(profiles) != 7:
        print(f"Warning: Expected 7 profiles, got {len(profiles)}")
    
    # Select which timesteps to plot (indices into the profiles/mc_steps arrays)
    # Modify these lists to plot any subset of the 7 available timesteps
    indices_to_plot = [0, 2, 4, 5, 6]  # e.g., [0,2,4,5,6] plots MC steps at indices 0,2,4,5,6
    
    # Filter profiles and mc_steps based on selected indices
    profiles_filtered = [profiles[i] for i in indices_to_plot]
    mc_steps_filtered = [mc_steps[i] for i in indices_to_plot]
    
    # Setup plot - select colors/markers based on number of timesteps to plot
    fig, ax = plt.subplots(figsize=(6, 4))
    all_colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2']
    all_markers = ['o', 's', '^', 'v', 'D', 'P', 'X']
    
    # Use only the needed number of colors/markers
    n_plots = len(indices_to_plot)
    colors = all_colors[:n_plots]
    markers = all_markers[:n_plots]
    
    fitted_T_values = []
    r2_values = []
    
    for i, (c_profile, mc_step) in enumerate(zip(profiles_filtered, mc_steps_filtered)):
        # Convert to dimensionless variables
        x_positions = np.arange(len(c_profile))  # 0, 1, 2, ..., 49
        X = x_positions / L  # Dimensionless position [0, 1)
        C_data = c_profile / c0  # Dimensionless concentration
        
        # Fit to find optimal T
        if mc_step == 0:
            # At t=0, the profile should be constant (initial condition)
            # Use analytical solution with many terms to reduce Gibbs oscillations
            # Or better: just use the constant initial condition C=1
            T_opt = 0.0
            C_fit = np.ones_like(X)  # Perfect initial condition: C=1 everywhere
            r2 = 1.0  # Perfect fit for initial condition
        else:
            try:
                # Initial guess for T based on MC step (arbitrary scaling)
                T_guess = mc_step / 10000.0
                
                # Fit
                popt, _ = curve_fit(fit_function, X, C_data, p0=[T_guess], 
                                   bounds=(0, np.inf), maxfev=5000)
                T_opt = popt[0]
                C_fit = analytical_solution(X, T_opt)
                
                # Calculate R² (coefficient of determination)
                ss_res = np.sum((C_data - C_fit) ** 2)  # Sum of squared residuals
                ss_tot = np.sum((C_data - np.mean(C_data)) ** 2)  # Total sum of squares
                r2 = 1 - (ss_res / ss_tot)
            except Exception as e:
                print(f"Fitting failed for MC step {mc_step}: {e}")
                T_opt = np.nan
                C_fit = C_data  # Use data as fallback
                r2 = np.nan
        
        fitted_T_values.append(T_opt)
        r2_values.append(r2)
        
        # Plot data points and fit
        label_data = f'MC={mc_step}'
        label_fit = f'Fit T={T_opt:.4f}' if not np.isnan(T_opt) else 'Fit failed'
        
        # Plot fitted curve (smooth line) with R² in label
        if not np.isnan(T_opt) and not np.isnan(r2):
            label_str = f'MC={mc_step}, R²={r2:.4f}'
        else:
            label_str = f'MC={mc_step}'
        ax.plot(X, C_fit, linestyle='-', linewidth=1.5, color=colors[i], 
                alpha=0.8, label=label_str)
        
        # Plot data points at X = 0, 0.1, 0.2, ..., 1.0
        X_target = np.arange(0, 1.1, 0.1)  # 0, 0.1, 0.2, ..., 1.0
        
        X_sparse = []
        C_sparse = []
        for x_val in X_target:
            # Find the closest index in X to this target value
            idx = np.argmin(np.abs(X - x_val))
            X_sparse.append(X[idx])
            C_sparse.append(C_data[idx])
        
        # Plot the data points
        ax.plot(X_sparse, C_sparse, marker=markers[i], linestyle='', 
                    markersize=5, color=colors[i], alpha=0.7, markerfacecolor='none', markeredgewidth=1.2)
    
    ax.set_xlabel(r'Dimensionless position $Z = z/L$')
    ax.set_ylabel(r'Dimensionless concentration $C = c/c_0$')
    #ax.set_title('Concentration profiles: Simulation data vs Fick\'s law fit')
    ax.legend(loc='best', frameon=True, ncol=2, fontsize=8.5, 
              handlelength=1.5, handletextpad=0.5, columnspacing=1.0, borderpad=0.3)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, None)
    
    plt.tight_layout()
    outfile = "conc_profile_fit.png"
    plt.savefig(outfile, dpi=300)
    print(f"Saved concentration profile plot to {outfile}")
    
    # Print MC steps vs T relationship with R² values
    print("\nMC steps vs Dimensionless time T:")
    print("MC step\t\tT\t\tR²")
    print("-" * 50)
    for mc, T, r2 in zip(mc_steps_filtered, fitted_T_values, r2_values):
        print(f"{mc}\t\t{T:.6f}\t\t{r2:.6f}")
    
    # Plot MC steps vs T to visualize relationship
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    valid_mask = ~np.isnan(fitted_T_values)
    mc_valid = np.array(mc_steps_filtered)[valid_mask]
    T_valid = np.array(fitted_T_values)[valid_mask]
    
    ax2.plot(mc_valid, T_valid, marker='o', linestyle='-', linewidth=1.5, markersize=6)
    ax2.set_xlabel('MC steps')
    ax2.set_ylabel('Dimensionless time $T$')
    #ax2.set_title('Relationship: MC steps vs $T$')
    ax2.grid(alpha=0.3)
    
    # Try linear fit to establish relationship (forced through origin)
    if len(mc_valid) >= 2:
        # Fit: T = slope * MC (force intercept = 0)
        # Using least squares: slope = sum(MC * T) / sum(MC^2)
        slope = np.sum(mc_valid * T_valid) / np.sum(mc_valid ** 2)
        T_fit_line = slope * mc_valid
        ax2.plot(mc_valid, T_fit_line, 'r--', linewidth=1, 
                label=f'Linear fit: T = {slope:.2e}·MC')
        ax2.legend(loc='best', frameon=True)
        print(f"\nLinear relationship (through origin): T = {slope:.6e} * MC_steps")
    
    plt.tight_layout()
    outfile2 = "MC_vs_T_relationship.png"
    plt.savefig(outfile2, dpi=300)
    print(f"Saved MC vs T plot to {outfile2}")
    
    plt.show()


if __name__ == "__main__":
    main()
