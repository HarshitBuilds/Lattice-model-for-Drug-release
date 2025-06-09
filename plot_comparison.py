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

def plot_comparison(file1, file2, file3):
    """Plot data from two AverageOverSimulations files."""
    # Read data from both files
    t1, n1_total, n1_lower, n1_upper = read_average_over_simulations(file1)
    t2, n2_total, n2_lower, n2_upper = read_average_over_simulations(file2)
    t3, n3_total, n3_lower, n3_upper = read_average_over_simulations(file3)
    # Plotting for the entire lattice.
    plt.figure(figsize=(12, 8))
    
    # Plot data from file 1, file 2 and file 3
    plt.plot(t1, n1_total, 'b-', linewidth=2, label=f'({file1})')
    plt.plot(t2, n2_total, 'b--', linewidth=2, label=f'({file2})')
    plt.plot(t3, n3_total, 'b:', linewidth=2, label=f'({file3})')

    # Add labels and title
    plt.xlabel('$t_{MC}$', fontsize=14)
    plt.ylabel('Number of ants', fontsize=14)
    plt.title('For entire lattice', fontsize=16)
    
    # Set logarithmic scale for x-axis
    plt.xscale('log')

    # Add grid and legend
    plt.grid(True, alpha=0.3)
    plt.legend(loc='best')
    
    # Save the plot
    plt.tight_layout()
    plt.savefig('ReleaseProfile EntireLattice (w1=0.0,0.1,0.2&w2=0.1).png', dpi=300)
    plt.close()    

    # Ploting for hydrophobic layer (lower lattice) data
    plt.figure(figsize=(12, 8))
    plt.plot(t1, n1_lower, 'g-', linewidth=2, label=f'({file1})')
    plt.plot(t2, n2_lower, 'g--', linewidth=2, label=f'({file2})')
    plt.plot(t3, n3_lower, 'g:', linewidth=2, label=f'({file3})')
    plt.xlabel('$t_{MC}$', fontsize=14)
    plt.ylabel('Number of ants', fontsize=14)
    plt.title('For hydrophobic layer', fontsize=16)
    
    # Set logarithmic scale for x-axis
    plt.xscale('log')

    # Add grid and legend
    plt.grid(True, alpha=0.3)
    plt.legend(loc='best')
    
    # Save the plot
    plt.tight_layout()
    plt.savefig('ReleaseProfile HydrophobicLayer (w1=0.0,0.1,0.2&w2=0.1).png', dpi=300)
    plt.close()

    # Ploting for hydrophilic layer (upper lattice) data
    plt.figure(figsize=(12, 8))

    plt.plot(t1, n1_upper, 'r-', linewidth=2, label=f'({file1})')
    plt.plot(t2, n2_upper, 'r--', linewidth=2, label=f'({file2})')
    plt.plot(t3, n3_upper, 'r:', linewidth=2, label=f'({file3})')
    plt.xlabel('$t_{MC}$', fontsize=14)
    plt.ylabel('Number of ants', fontsize=14)
    plt.title('For hydrophilic layer', fontsize=16)
    
    # Set logarithmic scale for x-axis
    plt.xscale('log')

    # Add grid and legend
    plt.grid(True, alpha=0.3)
    plt.legend(loc='best')
    
    # Save the plot
    plt.tight_layout()
    plt.savefig('ReleaseProfile HydrophilicLayer (w1=0.0,0.1,0.2&w2=0.1).png', dpi=300)
    plt.close()

    plt.figure(figsize=(12, 8))
    per1_total = 100 - ((n1_total / n1_total[0])* 100) #percentage of ants released 
    per2_total = 100 - ((n2_total / n2_total[0])* 100) #percentage of ants released
    per3_total = 100 - ((n3_total / n3_total[0])* 100) #percentage of ants released
    # Plot percentage of ants released from entire lattice
    #code for skipping first entry of the array to avoid log(0)
    t1 , per1_total = t1[1:],per1_total[1:]
    t2 , per2_total = t2[1:],per2_total[1:]
    t3 , per3_total = t3[1:],per3_total[1:]

    plt.plot(t1, per1_total, 'r-', linewidth=2, label=f'({file1})')
    plt.plot(t2, per2_total, 'r--', linewidth=2, label=f'({file2})')
    plt.plot(t3, per3_total, 'r:', linewidth=2, label=f'({file3})')
    plt.xlabel('$t_{MC}$', fontsize=14)
    plt.ylabel('Percentage of ants released', fontsize=14)
    plt.title('From entire lattice', fontsize=16)
    
    # Set logarithmic scale for x-axis and y-axis
    plt.xscale('log')
    plt.yscale('log')
    # Add grid and legend
    plt.grid(True, alpha=0.3)
    plt.legend(loc='best')
    
    # Save the plot
    plt.tight_layout()
    plt.savefig('Percentage Released (w1=0.0,0.1,0.2&w2=0.1).png', dpi=300)
    plt.close()
def main():
    # Define file names (adjust as needed)
    file1 = "AverageOverSimulations(w1=0.0).txt"
    file2 = "AverageOverSimulations(w1=0.1).txt"
    file3 = "AverageOverSimulations(w1=0.2).txt"
    
    # Check if files exist
    if not os.path.exists(file1):
        print(f"Error: {file1} not found!")
        return
    if not os.path.exists(file2):
        print(f"Error: {file2} not found!")
        return
    if not os.path.exists(file3):
        print(f"Error: {file3} not found!")
        return
    
    # Plot the comparison
    plot_comparison(file1, file2, file3)

if __name__ == "__main__":
    main()