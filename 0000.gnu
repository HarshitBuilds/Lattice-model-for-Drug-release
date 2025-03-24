set terminal jpeg
unset border
set size square 1,1
set xrange[0:11]
set yrange[0:11]
set output "0000.jpeg"
unset tics
unset key
p "0000.dat" w p ps 3 pt 3 lc rgb 'black'
