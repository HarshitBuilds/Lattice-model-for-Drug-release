#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
import os
from matplotlib.patches import Patch
# Function to read the size distribution data
def read_size_distribution(filename="Sizedistribution.txt"):
    sizedist = []
    
    with open(filename, 'r') as file:
        for line in file:
            try:
                value = float(line.strip())
                sizedist.append(value)
            except ValueError:
                print(f"Warning: Could not parse line: '{line.strip()}'")
    
    return np.array(sizedist)

# Function to create and save the histogram
def plot_size_distribution(sizedist, filename):
    # Create cluster sizes (i+1 for each sizedist[i])
    cluster_sizes = np.arange(1, len(sizedist) + 1)
    
    sizedist_new = []
    cluster_sizes_new = []
    for i in range(len(sizedist)): #Remove all cluster sizes with zero frequency
        if sizedist[i] > 0.0:
            sizedist_new.append(sizedist[i])
            cluster_sizes_new.append(cluster_sizes[i])
    
    sizedist = np.array(sizedist_new)
    cluster_sizes = np.array(cluster_sizes_new)
    # Create the figure and axis
    # after you’ve trimmed out zeros and made `cluster_sizes` & `sizedist` 1D arrays:
    # Number-average:
    number_avg = np.sum(cluster_sizes * sizedist) / np.sum(sizedist)

    # Weight-average:
    weight_avg = np.sum(cluster_sizes**2 * sizedist) \
           / np.sum(cluster_sizes * sizedist)
    sizedist = sizedist *100/ np.sum(sizedist)  #converting frequency to percentage
    
    # Extract parameter label from filename
    if "Sizedistribution" in filename:
        param_label = filename.replace("Sizedistribution", "").replace(".txt", "")
    else:
        param_label = ""
    
    # Set font style and sizes to match plot_comparison.py
    plt.rcParams.update({
        'font.family': 'Arial',
        'font.size': 12,  # Increased from 10
        'axes.titlesize': 16,  # Increased from 12
        'axes.labelsize': 14,  # Increased from 11        '
        'xtick.labelsize': 11,  # Increased from 10
        'ytick.labelsize': 11,  # Increased from 10
        'legend.fontsize': 11,  # Increased from 9
        'figure.dpi': 300
    })
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Plot as histogram
    ax.bar(cluster_sizes, sizedist, width=0.8, alpha=0.7, color='blue', edgecolor='black')
    
    # Add labels and title
    ax.set_xlabel('Aggregate size')
    ax.set_ylabel('Percentage of all ant aggregates')
    ax.set_title('Ant aggregate size Distribution')
    ax.set_ylim(0, 25)  # Set y-axis limit to 100% for better readability
    #ax.set_xlim(1,100)  # Set x-axis limit to cover all cluster sizes
    #ax.set_yscale('log')
    #ax.set_xscale('log')
    # Add grid for better readability (commented out to match plot_comparison.py style)
    # ax.grid(axis='y', alpha=0.3)
    
    # Adjust x-axis to show integer values
    ax.set_xticks(cluster_sizes)
    
    # Only show a subset of x ticks if there are many cluster sizes
    #if len(cluster_sizes) > 20:
        #ax.set_xticks(np.arange(1, len(sizedist) + 1, 2))
    
    ax.legend(handles=[
    Patch(color='none', label=f'{param_label}'),
    Patch(color='none', label=f'Number avg: {number_avg:.3f}'),
    Patch(color='none', label=f'Weight avg: {weight_avg:.3f}')
    ], loc='upper right', frameon=True, handlelength=0)
    # Improve layout
    plt.tight_layout()
    
    # Save the figure
    plt.savefig(f'cluster_size_distribution_{param_label}.png', dpi=300)
    print("Plot saved as 'cluster_size_distribution.png'")
    
    # Show the plot
    plt.show()

def main():
    # Specify the filename here - change this to the desired Sizedistribution file
    filename = "Sizedistribution(x=150).txt"
    
    if not os.path.exists(filename):
        print(f"Error: {filename} not found!")
        return
    
    # Read the data
    sizedist = read_size_distribution(filename)
    
    if len(sizedist) == 0:
        print(f"Error: No valid data found in {filename}")
        return
    
    print(f"Read {len(sizedist)} size distribution values")
    
    # Plot the data
    plot_size_distribution(sizedist, filename)

if __name__ == "__main__":
    main()