#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
import os
import matplotlib.ticker as mticker

def read_average_over_simulations(filename):
    """Read data from AverageOverSimulations.txt file."""
    t_values, n_values, n1_values, n2_values = [], [], [], []
    with open(filename, 'r') as f:
        next(f) # Skip header
        for line in f:
            try:
                values = line.strip().split()
                t, n, n1, n2 = int(values[0]), float(values[1]), float(values[2]), float(values[3])
                t_values.append(t)
                n_values.append(n)
                n1_values.append(n1)
                n2_values.append(n2)
            except (ValueError, IndexError) as e:
                print(f"Error parsing line: {line.strip()}, {e}")
    return np.array(t_values), np.array(n_values), np.array(n1_values), np.array(n2_values)

def plot_comparison(file1, file2, file3, panel_labels=('a', 'b', 'c', 'd')):
    """Plot data with final, polished formatting for font readability."""

    # font sizes for plots
    plt.rcParams.update({
        'font.family': 'Arial',       # Explicitly set a clean, standard font
        'font.size': 10,              # Default font size
        'axes.titlesize': 12,         # Title font size
        'axes.labelsize': 11,         # UPPED: X and Y labels font size for clarity
        'xtick.labelsize': 10,         # UPPED: X-tick labels
        'ytick.labelsize': 10,         # UPPED: Y-tick labels
        'legend.fontsize': 9,         # UPPED: Legend font size
        'figure.dpi': 300
    })

    t1, n1_total, n1_lower, n1_upper = read_average_over_simulations(file1)
    t2, n2_total, n2_lower, n2_upper = read_average_over_simulations(file2)
    t3, n3_total, n3_lower, n3_upper = read_average_over_simulations(file3)

    label1, label2, label3 = f'x={file1[25:-5]}', f'x={file2[25:-5]}', f'x={file3[25:-5]}'

    # --- Plotting for the entire lattice ---
    fig, ax = plt.subplots(figsize=(4, 3))
    ax.plot(t1, n1_total, 'b-', linewidth=2, label=label1)
    ax.plot(t2, n2_total, 'b--', linewidth=2, label=label2)
    ax.plot(t3, n3_total, 'b:', linewidth=2, label=label3)
    ax.set(xlabel='$t_{MC}$', ylabel='Number of ants', title='For entire lattice', xscale='log', ylim=(0, 100))
    ax.yaxis.set_major_locator(mticker.MultipleLocator(20))
    ax.yaxis.set_minor_locator(mticker.MultipleLocator(10))
    # ax.grid(True, which='major', linestyle='-', linewidth='0.5', color='gray', alpha=0.5)
    # ax.grid(True, which='minor', linestyle=':', linewidth='0.5', color='gray', alpha=0.2)
    # ax.spines['top'].set_visible(False)
    # ax.spines['right'].set_visible(False)
    #ax.text(-0.15, 1.05, f'({panel_labels[0]})', transform=ax.transAxes, size=12, weight='bold')
    ax.legend(loc='best')
    plt.tight_layout()
    plt.savefig(f'ReleaseProfile EntireLattice ({label1},{label2},{label3}).png')
    plt.close()

    # --- Plotting for hydrophobic layer ---
    fig, ax = plt.subplots(figsize=(4, 3))
    ax.plot(t1, n1_lower, 'g-', linewidth=2, label=label1)
    ax.plot(t2, n2_lower, 'g--', linewidth=2, label=label2)
    ax.plot(t3, n3_lower, 'g:', linewidth=2, label=label3)
    ax.set(xlabel='$t_{MC}$', ylabel='Number of ants', title='For hydrophobic layer', xscale='log', ylim=(0, 100))
    ax.yaxis.set_major_locator(mticker.MultipleLocator(20))
    ax.yaxis.set_minor_locator(mticker.MultipleLocator(10))
    # ax.grid(True, which='major', linestyle='-', linewidth='0.5', color='gray', alpha=0.5)
    # ax.grid(True, which='minor', linestyle=':', linewidth='0.5', color='gray', alpha=0.2)
    # ax.spines['top'].set_visible(False)
    # ax.spines['right'].set_visible(False)
    #ax.text(-0.15, 1.05, f'({panel_labels[1]})', transform=ax.transAxes, size=12, weight='bold')
    ax.legend(loc='best')
    plt.tight_layout()
    plt.savefig(f'ReleaseProfile HydrophobicLayer ({label1},{label2},{label3}).png')
    plt.close()

    # --- Plotting for hydrophilic layer ---
    fig, ax = plt.subplots(figsize=(4, 3))
    ax.plot(t1, n1_upper, 'r-', linewidth=2, label=label1)
    ax.plot(t2, n2_upper, 'r--', linewidth=2, label=label2)
    ax.plot(t3, n3_upper, 'r:', linewidth=2, label=label3)
    ax.set(xlabel='$t_{MC}$', ylabel='Number of ants', title='For hydrophilic layer', xscale='log', ylim=(0, 100))
    ax.yaxis.set_major_locator(mticker.MultipleLocator(20))
    ax.yaxis.set_minor_locator(mticker.MultipleLocator(10))
    # ax.grid(True, which='major', linestyle='-', linewidth='0.5', color='gray', alpha=0.5)
    # ax.grid(True, which='minor', linestyle=':', linewidth='0.5', color='gray', alpha=0.2)
    # ax.spines['top'].set_visible(False)
    # ax.spines['right'].set_visible(False)
    #ax.text(-0.15, 1.05, f'({panel_labels[2]})', transform=ax.transAxes, size=12, weight='bold')
    ax.legend(loc='best')
    plt.tight_layout()
    plt.savefig(f'ReleaseProfile HydrophilicLayer ({label1},{label2},{label3}).png')
    plt.close()

    #---plotting for percentage of ants released from the entire lattice---
    fig, ax = plt.subplots(figsize=(4, 3))
    per1_total = 100 - ((n1_total / n1_total[0]) * 100)
    per2_total = 100 - ((n2_total / n2_total[0]) * 100)
    per3_total = 100 - ((n3_total / n3_total[0]) * 100)
    t1_s, per1_total_s = t1[1:], per1_total[1:]
    t2_s, per2_total_s = t2[1:], per2_total[1:]
    t3_s, per3_total_s = t3[1:], per3_total[1:]

    ax.plot(t1_s, per1_total_s, 'r-', linewidth=1.5, label=label1)
    ax.plot(t2_s, per2_total_s, 'r--', linewidth=1.5, label=label2)
    ax.plot(t3_s, per3_total_s, 'r:', linewidth=1.5, label=label3)
    ax.set(xlabel='$t_{MC}$', ylabel='% of ants released', xscale='log', yscale='log', ylim=(0.75, 100))
    ax.legend(loc='best')
    plt.tight_layout()
    plt.savefig(f'Percentage Released ({label1},{label2},{label3}).png')
    plt.close()

def main():
    """Main function to run the plotting script."""
    file1 = "AverageOverSimulations(x=50).txt"
    file2 = "AverageOverSimulations(x=100).txt"
    file3 = "AverageOverSimulations(x=150).txt"
    
    for f in [file1, file2, file3]:
        if not os.path.exists(f):
            print(f"Error: {f} not found!")
            return
            
    plot_comparison(file1, file2, file3, panel_labels=('a', 'b', 'c'))
    print("Plots generated successfully with final font enhancements.")

if __name__ == "__main__":
    main()