################################################################################
          VISUALIZATION SCRIPTS FOR MONTE CARLO SIMULATION DATA              
################################################################################

RELEASE PROFILE COMPARISON SCRIPTS
----------------------------------
plot_comparison(w1).py  - Compares release profiles for w1 ∈ {0.0, 0.001, 0.01, 0.05, 0.1, 0.2}
plot_comparison(w2).py  - Compares release profiles for w2 ∈ {0.0, 0.1, 0.2, 0.4, 0.6, 0.8}
plot_comparison(N).py   - Compares release profiles for N ∈ {50, 100, 150, 200, 250, 300}
plot_comparison(x).py   - Compares release profiles for x ∈ {10, 25, 50, 100, 150}

Input:  ReleaseProfile({param})/AverageOverSimulations({param}={value}).txt
Output: PNG release profile plots for entire lattice, friendly layer, blind layer and % released from entire lattice
Usage:  python plot_comparison(w1).py  (no arguments; run from Visualizations directory)


AGGREGATE SIZE ANALYSIS
-----------------------
AggregateSize.py
  - Computes number-average and weight-average aggregate sizes vs w1
  - Input:  Sizedistribution(w1)/Sizedistribution(w1={value}).txt
  - Output: average_aggregate_size_vs_w1.png
  - Usage:  python AggregateSize.py [base_directory]

VisualizationSizedist.py
  - Creates histogram of aggregate size distribution from a single file
  - Input:  Sizedistribution(w1={value}).txt
  - Output: cluster_size_distribution_{param}.png
  - Usage:  python VisualizationSizedist.py  (edit filename in main() to change input)


CONCENTRATION PROFILE FITTING
-----------------------------
conc_profile.py
  - Fits Fick's law analytical solution to concentration profiles
  - Input:  Conc_profile/LayerDistribution(friendly).txt
  - Output: conc_profile_fit.png, MC_vs_T_relationship.png
  - Usage:  python conc_profile.py  (no arguments needed)


LATTICE VISUALIZATION
---------------------
visualize_lattice_positions.py
  - Generates spatial snapshots of ant positions on 200x200 lattice
  - Input:  LatticePositions file
  - Output: AntPosition/t={value}.png
  - Usage:  python visualize_lattice_positions.py [input] [step] [outdir]


DATA FORMATS
------------
AverageOverSimulations.txt:  t | n (total) | n1 (friendly) | n2 (blind)
Sizedistribution.txt:        Each line i = frequency of aggregates of size i


REQUIREMENTS
------------
Python 3.8+, NumPy, Matplotlib, SciPy (for conc_profile.py)
