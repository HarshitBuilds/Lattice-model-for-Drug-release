import os
import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt


def read_size_distribution_counts(filename: Path) -> np.ndarray:
	"""Read size distribution as in VisualizationSizedist.py.
	Each line represents the frequency for aggregate size i (1-indexed).
	Returns a 1D numpy array of counts (float).
	"""
	sizedist = []
	try:
		with open(filename, 'r') as file:
			for line in file:
				s = line.strip()
				if not s:
					continue
				try:
					sizedist.append(float(s))
				except ValueError:
					# Mirror VisualizationSizedist.py behavior: warn and continue
					print(f"Warning: Could not parse line in {filename}: '{s}'")
	except FileNotFoundError:
		return np.array([], dtype=float)
	return np.array(sizedist, dtype=float)


def compute_number_and_weight_average(counts: np.ndarray) -> tuple[float, float]:
	"""Compute number-average and weight-average aggregate sizes from counts.
	counts[i] corresponds to frequency of aggregate size (i+1).

	number_avg = sum(size * count) / sum(count)
	weight_avg  = sum(size^2 * count) / sum(size * count)

	Returns (number_avg, weight_avg). If invalid, returns (nan, nan) or (num_avg, nan).
	"""
	if counts.size == 0:
		return float('nan'), float('nan')

	sizes = np.arange(1, counts.size + 1, dtype=float)
	# Optionally filter zeros (not required for correctness, but avoids 0/0 edge cases)
	mask = counts > 0
	if not np.any(mask):
		return float('nan'), float('nan')
	c = counts[mask]
	s = sizes[mask]

	total = np.sum(c)
	if total == 0:
		return float('nan'), float('nan')
	number_avg = float(np.sum(s * c) / total)

	denom = np.sum(s * c)
	if denom == 0:
		return number_avg, float('nan')
	weight_avg = float(np.sum((s ** 2) * c) / denom)
	return number_avg, weight_avg


def main():
	# Optional base directory argument; defaults to current directory
	base_dir = sys.argv[1] if len(sys.argv) > 1 else "."
	base_path = Path(base_dir).resolve()

	# Styling consistent with other plots in this workspace
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

	# Target files (w1 values)
	target_w1 = [0.0, 0.001, 0.01, 0.05, 0.1, 0.2]
	found_w1: list[float] = []
	number_avgs: list[float] = []
	weight_avgs: list[float] = []	

	for w1 in target_w1:
		fname = f"Sizedistribution(w1)/Sizedistribution(w1={w1}).txt"
		fpath = base_path / fname
		if not fpath.exists():
			print(f"[warn] Missing file: {fname}, skipping")
			continue

		counts = read_size_distribution_counts(fpath)
		if counts.size == 0:
			print(f"[warn] {fname} is empty or invalid, skipping")
			continue

		n_avg, w_avg = compute_number_and_weight_average(counts)
		print(f"{fname}: number_avg={n_avg:.3f} | weight_avg={w_avg:.3f}")

		found_w1.append(w1)
		number_avgs.append(n_avg)
		weight_avgs.append(w_avg)

	if not found_w1:
		print("No valid size distribution files found among targets.")
		return

	# Sort by w1 for plotting
	order = np.argsort(found_w1)
	w1_vals = np.array(found_w1, dtype=float)[order]
	n_av = np.array(number_avgs, dtype=float)[order]
	w_av = np.array(weight_avgs, dtype=float)[order]

	# Plot both averages vs w1
	fig, ax = plt.subplots(figsize=(4, 3))
	ax.plot(w1_vals, n_av, marker='o', linestyle='-', linewidth=1, markersize=3, label='Number average')
	ax.plot(w1_vals, w_av, marker='s', linestyle='--', linewidth=1, markersize=3, label='Weight average')

	ax.set_xlabel(r'$w_1$')
	ax.set_ylabel('Average aggregate size')
	#ax.set_title('Average aggregate size vs $w_1$')
	ax.set_xticks(w1_vals)
	ax.set_xticklabels([str(w) for w in w1_vals])
	ax.set_ylim(bottom=0)
	ax.legend(loc='best', frameon=True)

	plt.tight_layout()
	outfile = base_path / "average_aggregate_size_vs_w1.png"
	plt.savefig(outfile, dpi=300)
	print(f"Saved plot to {outfile}")
	plt.show()


if __name__ == "__main__":
	main()

