#!/bin/bash

# Parameters for the simulation
for n in 200; # size of the lattice
do
for w1 in 0.1; # wall fraction in bottom layer
do
for w2 in 0.1;  # wall fraction in upper layer
do
for p in 0.0; # probability of crossing wall
do
for a in 0.0025; # ant fraction
do
for x in 100; # partition layer (e.g., 50 for a 200x200 lattice)
do
for pj in 0.0; # probability of jumping from top to bottom
do
# Directory name for movie. 
s="movie_w1_${w1}_w2_${w2}_p_${p}_a_${a}_n_${n}_x_${x}_pj_${pj}"

mkdir -p "movie/$s"
cd "movie/$s"

#Running the simulation for generating the movie
../../ANT --WALLF1 "$w1" --WALLF2 "$w2" --PWALL "$p" -a "$a" -n "$n" -x "$x" --PJUMP "$pj" --is_top 0 -s 200000 -S 1000

echo "Generating movie..."
gnuplot *.gnu
ffmpeg -r 10 -f image2 -i %d.jpeg -crf 15 "${s}.avi" #Jpeg to video conversion (with fps settings)

echo "Cleaning up..." #Deleting the jpeg files
rm -f *.jpeg
rm -f *.gnu
rm -f *.dat

cd ../..
echo "Finished processing for $s"

done
done
done
done
done
done
done

echo "All movies created."