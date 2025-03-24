for n in 100;
do
for w1 in 0.2; #wall fraction
do
for w2 in 0.2; #wall fraction
do
for p in 0.0 ; #probability of crossing wall (permeability)
do
for a in 0.0001; #ant fraction
do
for x in 50;
do
for pj in 0.0; #probability of movement from top to bottom 
do
s="run_w1_${w1}_w2_${w2}_p_${p}_a_${a}_n_${n}_x_${x}_pj_${pj}"
cd movie
mkdir "$s"
cd "$s"
  ../../ANT --WALLF1 "$w1" --WALLF2 "$w2" -p "$p" -a "$a" -r "$RANDOM" -s 10000 -S 50 -n "$n" -x "$x" --PJUMP "$pj"
gnuplot *.gnu
#for gnufile in $(ls -v *.gnu); do
#    gnuplot "$gnufile" #produces the jpeg images
#done

#ffmpeg -r 5 -f image2 -i %d.jpeg -crf 15 "$s.avi"
if ls *.jpeg 1> /dev/null 2>&1; then
    # Use ls to sort the jpeg files numerically
    ffmpeg -r 5 -f image2 -i "%04d.jpeg" -crf 15 "$s.avi"
    
    rm -f *.jpeg
    rm -f *.gnu
    rm -f *.dat
else
    echo "No image files found for $s"
fi
rm -f *.jpeg
rm -f *.gnu
rm -f *.dat
cd ../..
done
done
done
done
done
done
done
