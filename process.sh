for n in 100;
do
for w1 in 0.1; #wall fraction
do
for w2 in 0.1; #wall fraction
do
for p in 0.0; #probability of crossing wall
do
for a in 0.01; #ant fraction
do
for x in 50; 
do 
for pj in 0.0; #probability of moving from top to bottom
do
for tau in 10; #tau value for calculating mean square displacement
s="run_w1_${w1}_w2_${w2}_p_${p}_a_${a}_n_${n}_x_${x}_pj_${pj}"
mkdir "$s"
cd "$s"
sweeps=1000000 #number of MC sweeps in simulation
mcruns=100 #number of MC runs to average over
for ((r=1;r<=mcruns;r++)); 
do
  ../ANT --WALLF1 "$w1" --WALLF2 "$w2" -p "$p" -a "$a" -r "$r" -s "$sweeps" -S 1000000 -n "$n" -x "$x" --PJUMP "$pj"
done
python3 ../process.py "$mcruns" "$a" "$w1" "$w2" "$x" "$sweeps" "$tau" #processing part of the code 
find . -maxdepth 1 -name "*.dat" -print0 | xargs -0 rm
cd ..
done
done
done
done
done
done
done
done