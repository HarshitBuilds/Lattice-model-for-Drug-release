import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import os

def read_msd_data(filename="MSD.txt"):
    tau_values = []
    msd_values = []
    
    with open(filename, 'r') as file:
        # Skip the header line
        header = file.readline()
        
        # Read the data lines
        for line in file:
            parts = line.strip().split()
            if len(parts) >= 2:
                try:
                    tau = float(parts[0])
                    msd = float(parts[1])
                    
                    # Skip NaN values
                    if not np.isnan(msd):
                        tau_values.append(tau)
                        msd_values.append(msd)
                except (ValueError, IndexError) as e:
                    print(f"Warning: Could not parse line: {line.strip()}")
                    print(f"Error: {e}")
    
    return np.array(tau_values), np.array(msd_values)

# Function to fit a line and calculate the slope (diffusion coefficient)
def fit_line_and_get_slope(tau_values, msd_values):
    if len(tau_values) < 2:
        print("Error: Not enough data points for fitting")
        return None, None, None
    
    # Fit a linear model: MSD = 2*D*tau + b
    slope, intercept, r_value, p_value, std_err = stats.linregress(tau_values, msd_values)
    
    # In 1D, the diffusion coefficient D = slope/2
    D = slope/2
    
    return slope, intercept, D, r_value**2, std_err

# Function to plot the data and the fitted line
def plot_fit(tau_values, msd_values, slope, intercept, r_squared):
    plt.figure(figsize=(10, 6))
    plt.scatter(tau_values, msd_values, color='blue', label='Data')
    
    # Generate fitted line
    line_x = np.linspace(min(tau_values), max(tau_values), 100) #100 data points on x-axis 
    line_y = slope * line_x + intercept
    
    plt.plot(line_x, line_y, color='red', 
             label=f'Fit: MSD = {slope:.4f}τ + {intercept:.4f}\nR² = {r_squared:.4f}')
    
    plt.xlabel('τ')
    plt.ylabel('MSD')
    plt.title('Mean Square Displacement vs Tau')
    plt.grid(True)
    plt.legend()
    
    # Save the plot
    plot_filename = "msd_fit.png"
    plt.savefig(plot_filename)
    plt.close()
    print(f"Plot saved as {plot_filename}")

def main():
    # Path to the MSD.txt file
    msd_file = "MSD.txt"
    
    maxsweeps  = 100000 #total number of MC sweeps in a simulation 
    # Read the data
    tau_values, msd_values = read_msd_data(msd_file)

    # Only keeping tau and msd values till tau <= maxsweeps/2
    mask = tau_values <= maxsweeps/2
    tau_values = tau_values[mask]
    msd_values = msd_values[mask]
    
    if len(tau_values) == 0:
        print("No valid data found in the file.")
        return
    
    # Fit line and get slope
    slope, intercept, D, r_squared, std_err = fit_line_and_get_slope(tau_values, msd_values)
    
    if slope is not None:
        print(f"\nResults:")
        print(f"Number of data points: {len(tau_values)}")
        print(f"Number of MC sweeps: {maxsweeps}")
        print(f"last value of tau: {tau_values[-1]}") #close to maxsweeps/2
        print(f"Slope: {slope:.6f}")
        print(f"Intercept: {intercept:.6f}")
        print(f"Diffusion coefficient (D = slope/2): {D:.6f}")
        print(f"R-squared: {r_squared:.6f}")
        print(f"Standard error: {std_err:.6f}")
        
        # Plot the fit
        plot_fit(tau_values, msd_values, slope, intercept, r_squared)

if __name__ == "__main__":
    main()