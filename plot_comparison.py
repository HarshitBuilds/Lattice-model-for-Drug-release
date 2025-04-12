#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
import os

def read_average_over_simulations(filename):
    """Read data from AverageOverSimulations.txt file."""
    t_values = []
    n_values = []
    n1_values = []
    n2_values = []
    
    with open(filename, 'r') as f:
        # Skip header
        header = f.readline()
        
        # Read data
        for line in f:
            values = line.strip().split()
            if len(values) >= 4:
                try:
                    t = int(values[0])
                    n = float(values[1])
                    n1 = float(values[2])
                    n2 = float(values[3])
                    
                    t_values.append(t)
                    n_values.append(n)
                    n1_values.append(n1)
                    n2_values.append(n2)
                except (ValueError, IndexError) as e:
                    print(f"Error parsing line: {line.strip()}, {e}")
    
    return np.array(t_values), np.array(n_values), np.array(n1_values), np.array(n2_values)

def plot_comparison(file1, file2):
    """Plot data from two AverageOverSimulations files."""
    # Read data from both files
    t1, n1_total, n1_lower, n1_upper = read_average_over_simulations(file1)
    t2, n2_total, n2_lower, n2_upper = read_average_over_simulations(file2)
    
    # Create the plot
    plt.figure(figsize=(12, 8))
    
    # Plot data from file 1
    plt.plot(t1, n1_total, 'b-', linewidth=2, label=f'Total ants ({file1})')
    plt.plot(t1, n1_lower, 'g-', linewidth=2, label=f'Lower lattice ({file1})')
    plt.plot(t1, n1_upper, 'r-', linewidth=2, label=f'Upper lattice ({file1})')
    
    # Plot data from file 2
    plt.plot(t2, n2_total, 'b--', linewidth=2, label=f'Total ants ({file2})')
    plt.plot(t2, n2_lower, 'g--', linewidth=2, label=f'Lower lattice ({file2})')
    plt.plot(t2, n2_upper, 'r--', linewidth=2, label=f'Upper lattice ({file2})')
    
    # Add labels and title
    plt.xlabel('Number of MC sweeps', fontsize=14)
    plt.ylabel('Number of ants', fontsize=14)
    plt.title('Comparison of Ant Distribution', fontsize=16)
    
    # Add grid and legend
    plt.grid(True, alpha=0.3)
    plt.legend(loc='best')
    
    # Save the plot
    plt.tight_layout()
    plt.savefig('ReleaseProfile(w1=0.0&w1=0.1).png', dpi=300)
    
    # Show the plot
    plt.show()

def main():
    # Define file names (adjust as needed)
    file1 = "AverageOverSimulations(w1=0.0).txt"
    file2 = "AverageOverSimulations(w1=0.1).txt"
    
    # Check if files exist
    if not os.path.exists(file1):
        print(f"Error: {file1} not found!")
        return
    if not os.path.exists(file2):
        print(f"Error: {file2} not found!")
        return
    
    # Plot the comparison
    plot_comparison(file1, file2)

if __name__ == "__main__":
    main()