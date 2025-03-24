for n in 10; #size of the lattice
do
for w1 in 0.1; #wall fraction
do
for w2 in 0.1; #wall fraction
do
for p in 0.0; #probability of crossing wall
do
for a in 0.1; #ant fraction
do
for x in 5; #partition between top and bottom layer (ensure < n)
do 
for pj in 0.0; #probability of moving from top to bottom
do
for tau_val in 5; #tau value for calculating mean square displacement
do
s="run_w1_${w1}_w2_${w2}_p_${p}_a_${a}_n_${n}_x_${x}_pj_${pj}"
mkdir "$s" -p 
cd "$s"
sweeps=100 #number of MC sweeps in simulation
mcruns=10 #number of MC runs to average over
for ((r=1;r<=mcruns;r++)); 
do
    ../ANT --WALLF1 "$w1" --WALLF2 "$w2" -p "$p" -a "$a" -r "$r" -s "$sweeps" -S 1000000 -n "$n" -x "$x" --PJUMP "$pj" --tau_val "$tau_val"
done
python3 ../process.py "$mcruns" "$a" "$w1" "$w2" "$x" "$sweeps" "$tau_val" #processing part of the code 
#find . -maxdepth 1 -name "*.dat" -print0 | xargs -0 rm #to remove the .dat files produced 
cd ..
done
done
done
done
done
done
done
done