for n in 200; #size of the lattice
do
for w1 in 0.1; #wall fraction in bottom layer
do
for w2 in 0.1;  #wall fraction in upper layer
do
for p in 0.0; #probability of crossing wall
do
for a in 0.0025; #ant fraction
do
for x in 100; #partition between top and bottom layer (ensure < n) 
do 
for pj in 0.0; #probability of moving from top to bottom
do
s="run_w1_${w1}_w2_${w2}_p_${p}_a_${a}_n_${n}_x_${x}_pj_${pj}"
mkdir "$s" -p 
cd "$s"
sweeps=1000000 #number of MC sweeps in simulation 
mcruns=300 #number of MC runs to average over
is_top=0 #initialising ants 0 for bottom layer (default), 1 for top layer
tau_inc=1000 #add parameter for tau interval spacing.  
for ((r=1;r<=mcruns;r++)); 
do
    ../ANT --WALLF1 "$w1" --WALLF2 "$w2" -p "$p" -a "$a" -r "$r" -s "$sweeps" -S 1000000 -n "$n" -x "$x" --PJUMP "$pj" --is_top "$is_top" --tau_inc "$tau_inc"
done
python3 ../process.py "$mcruns" "$a" "$w1" "$w2" "$x" "$sweeps" "$is_top" "$tau_inc" "$n" #processing part of the code 
#find . -maxdepth 1 -name "*.dat" -print0 | xargs -0 rm #to remove the .dat files produced 
cd ..
done
done
done
done
done
done
done