for n in 50;
do
for w1 in 0.0 0.6 0.7 0.8 0.9; #wall fraction
do
for w2 in 0.0 0.6 0.7 0.8 0.9; #wall fraction
do
for p in 0.0; #probability of crossing wall
do
for a in 0.04; #ant fraction
do
for x in 5 10 15 30 40;
do
s="run_w1_${w1}_w2_${w2}_p_${p}_a_${a}_n_${n}_x_${x}"
cd movie
mkdir -p "$s"
cd "$s"
../../ANT --WALLF1 "$w1" --WALLF2 "$w2" -p "$p" -a "$a" -r "$RANDOM" -s 10000 -S 10000 -n "$n" -x "$x"

# Debug: List all files
echo "Generated files:"
ls

# Count .gnu files
gnu_count=$(ls *.gnu 2>/dev/null | wc -l)
echo "Number of .gnu files: $gnu_count"

# Explicitly run gnuplot for each .gnu file with error checking
for gnufile in *.gnu; do
    echo "Processing $gnufile"
    gnuplot "$gnufile" || echo "Gnuplot failed for $gnufile"
done

# Check jpeg files
jpeg_count=$(ls *.jpeg 2>/dev/null | wc -l)
echo "Number of .jpeg files: $jpeg_count"

# If no jpeg files, try to diagnose
if [ $jpeg_count -eq 0 ]; then
    echo "Checking gnuplot installation"
    gnuplot --version
    
    echo "Checking first .gnu file contents:"
    cat $(ls *.gnu | head -n 1)
fi

# Video creation remains the same
if ls *.jpeg 1> /dev/null 2>&1; then
    ffmpeg -r 5 -f image2 -pattern_type glob -i '*.jpeg' -crf 15 "$s.avi"
    
    rm -f *.jpeg
    rm -f *.gnu
    rm -f *.dat
else
    echo "No image files found for $s"
fi

cd ../..
done
done
done
done
done
done