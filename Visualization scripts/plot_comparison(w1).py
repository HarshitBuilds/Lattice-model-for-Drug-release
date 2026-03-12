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

def plot_comparison(file1, file2, file3, file4, file5, file6, panel_labels=('a', 'b', 'c', 'd')):
    """Plot data with final, polished formatting for font readability."""

    # --- KEY CHANGE: Final tweaks to fonts ---
    plt.rcParams.update({
        'font.family': 'Arial',       # Explicitly set a clean, standard font
        'font.size': 10,              # Default font size
        'axes.titlesize': 12,         # Title font size
        'axes.labelsize': 11,         # UPPED: X and Y labels font size for clarity
        'xtick.labelsize': 9,         # UPPED: X-tick labels
        'ytick.labelsize': 9,         # UPPED: Y-tick labels
        'legend.fontsize': 9,         # UPPED: Legend font size
        'figure.dpi': 300
    })

    # Read all files
    t = []
    n_total = []
    n_lower = []
    n_upper = []
    labels = []
    files = [file1, file2, file3, file4, file5, file6]
    for f in files:
        t_f, n_f, n1_f, n2_f = read_average_over_simulations(f)
        t.append(t_f)
        n_total.append(n_f)
        n_lower.append(n1_f)
        n_upper.append(n2_f)
        # Build label from filename by removing the prefix and .txt
        label = f.replace("ReleaseProfile(w1)/AverageOverSimulations", "").replace(".txt", "")
        labels.append(label)
        

    # --- Plotting for the entire lattice (all) ---
    fig, ax = plt.subplots(figsize=(4, 3))
    styles = ['b-', 'b--', 'b:', 'g-', 'g--', 'g:']
    for i in range(len(files)):
        ax.plot(t[i], n_total[i], styles[i % len(styles)], linewidth=2, label=labels[i])
    ax.set(xlabel='$t_{MC}$', ylabel='Percentage of ants',  title='For entire lattice',  xscale = 'log' , ylim=(0, 100))
    ax.yaxis.set_major_locator(mticker.MultipleLocator(20))
    ax.yaxis.set_minor_locator(mticker.MultipleLocator(10))
    ax.legend(loc='best')
    plt.tight_layout()
    plt.savefig(f'ReleaseProfile EntireLattice (all_w1).png')
    plt.close()

    # --- Plotting for friendly layer (all) ---
    fig, ax = plt.subplots(figsize=(4, 3))
    for i in range(len(files)):
        ax.plot(t[i], n_lower[i], styles[i % len(styles)], linewidth=2, label=labels[i])
    ax.set(xlabel='$t_{MC}$', ylabel='Percentage of ants', title='For friendly layer', xscale = 'log', ylim=(0, 100))
    ax.yaxis.set_major_locator(mticker.MultipleLocator(20))
    ax.yaxis.set_minor_locator(mticker.MultipleLocator(10))
    ax.legend(loc='best')
    plt.tight_layout()
    plt.savefig(f'ReleaseProfile FriendlyLayer (all_w1).png')
    plt.close()

    # --- Plotting for blind layer (all) ---
    fig, ax = plt.subplots(figsize=(4, 3))
    for i in range(len(files)):
        ax.plot(t[i], n_upper[i], styles[i % len(styles)], linewidth=2, label=labels[i])
    ax.set(xlabel='$t_{MC}$', ylabel='Percentage of ants', title='For blind layer', xscale = 'log', ylim=(0, 100))
    ax.yaxis.set_major_locator(mticker.MultipleLocator(20))
    ax.yaxis.set_minor_locator(mticker.MultipleLocator(10))
    ax.legend(loc='best')
    plt.tight_layout()
    plt.savefig(f'ReleaseProfile BlindLayer (all_w1).png')
    plt.close()

    #---plotting for percentage of ants released from the entire lattice---
    fig, ax = plt.subplots(figsize=(4, 3))
    for i in range(len(files)):
        per_total = 100 - ((n_total[i] / n_total[i][0]) * 100)
        t_s, per_total_s = t[i][1:], per_total[1:]
        ax.plot(t_s, per_total_s, styles[i % len(styles)], linewidth=1.5, label=labels[i])
    ax.set(xlabel='$t_{MC}$', ylabel='% of ants released', xscale = 'log' ,yscale='log', ylim=(0.75, 100))
    ax.legend(loc='best')
    plt.tight_layout()
    plt.savefig(f'Percentage Released (all_w1).png')
    plt.close()

    print("Plots generated successfully with final font enhancements.")

def main():
    """Main function to run the plotting script."""
    # Define six w1 values and build filenames accordingly
    w1_values = [0.0, 0.001, 0.01, 0.05, 0.1, 0.2]
    file1, file2, file3, file4, file5, file6 = [f"ReleaseProfile(w1)/AverageOverSimulations(w1={v}).txt" for v in w1_values]

    # Validate files exist
    for f in [file1, file2, file3, file4, file5, file6]:
        if not os.path.exists(f):
            print(f"Error: {f} not found!")
            return

    # Plot all six together
    plot_comparison(file1, file2, file3, file4, file5, file6, panel_labels=('a', 'b', 'c', 'd'))
    print("Plots generated successfully with final font enhancements.")

if __name__ == "__main__":
    main()