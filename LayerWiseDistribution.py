import matplotlib.pyplot as plt
import numpy as np
import os

# Input filename
input_filename = "LayerDistribution.txt"
steps = 200000 #time step interval to for plotting layerwise distribution of ants
try:
    with open(input_filename, 'r') as f:
        for line_index, line in enumerate(f):
            # Strip whitespace and split by tab
            parts = line.strip().split('\t')

            # Convert parts to floats, skip if empty line or conversion fails
            try:
                y_values = [float(p) for p in parts if p] # Filter out empty strings just in case
                if not y_values: # Skip empty lines
                    continue
            except ValueError:
                print(f"Warning: Could not convert data to numbers on line {line_index + 1}. Skipping.")
                continue

            # Create x-axis values (index + 1)
            x_values = np.arange(1, len(y_values) + 1)

            # Create the plot
            plt.figure(figsize=(10, 6)) # Optional: Adjust figure size
            plt.plot(x_values, y_values, marker='o', linestyle='-') # Added markers for clarity

            # Set labels and title
            plt.xlabel("z")
            plt.ylabel("Number of ants")
            plt.title(f"Layer wise Distribution - Line {line_index*steps}")
            plt.grid(True) # Optional: Add grid

            # Define output filename
            output_filename = f"layer_{line_index*steps}_distribution.png"

            # Save the plot
            plt.savefig(output_filename)
            print(f"Plot saved to {output_filename}")

            # Close the plot figure to free memory
            plt.close()

except FileNotFoundError:
    print(f"Error: Input file '{input_filename}' not found.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

print("Finished processing all lines.")