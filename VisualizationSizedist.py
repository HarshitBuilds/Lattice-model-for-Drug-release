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
def plot_size_distribution(sizedist):
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
    plt.figure(figsize=(10, 6))
    
    # Plot as bars
    plt.bar(cluster_sizes, sizedist, width=0.8, alpha=0.7, color='blue', edgecolor='black')
    
    # Add labels and title
    plt.xlabel('Aggregate size', fontsize=14)
    plt.ylabel('Percentage of all ant aggregates', fontsize=14)
    plt.title('Ant aggregate size Distribution', fontsize=16)
    
    # Add grid for better readability
    plt.grid(axis='y', alpha=0.3)
    
    # Adjust x-axis to show integer values
    plt.xticks(cluster_sizes)
    
    # Only show a subset of x ticks if there are many cluster sizes
    if len(cluster_sizes) > 20:
        plt.xticks(np.arange(1, len(sizedist) + 1, 2))
    
    
    plt.legend(handles=[
    Patch(color='none', label=f'Number average Aggregate size: {number_avg:.3f}'),
    Patch(color='none', label=f'Weight average Aggregate size: {weight_avg:.3f}')
    ], loc='upper right', frameon=True, handlelength=0)
    # Improve layout
    plt.tight_layout()
    
    # Save the figure
    plt.savefig('cluster_size_distribution.png', dpi=300)
    print("Plot saved as 'cluster_size_distribution.png'")
    
    # Show the plot
    plt.show()

def main():
    if not os.path.exists("Sizedistribution.txt"):
        print("Error: Sizedistribution.txt not found!")
        return
    
    # Read the data
    sizedist = read_size_distribution()
    
    if len(sizedist) == 0:
        print("Error: No valid data found in Sizedistribution.txt")
        return
    
    print(f"Read {len(sizedist)} size distribution values")
    
    # Plot the data
    plot_size_distribution(sizedist)

if __name__ == "__main__":
    main()