#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
import os

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
    
    # Create the figure and axis
    plt.figure(figsize=(10, 6))
    
    # Plot as bars
    plt.bar(cluster_sizes, sizedist, width=0.8, alpha=0.7, color='blue', edgecolor='black')
    
    # Add labels and title
    plt.xlabel('Cluster Size', fontsize=14)
    plt.ylabel('Frequency', fontsize=14)
    plt.title('Ant Cluster Size Distribution', fontsize=16)
    
    # Add grid for better readability
    plt.grid(axis='y', alpha=0.3)
    
    # Adjust x-axis to show integer values
    plt.xticks(cluster_sizes)
    
    # Only show a subset of x ticks if there are many cluster sizes
    if len(cluster_sizes) > 20:
        plt.xticks(np.arange(1, len(sizedist) + 1, 2))
    
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