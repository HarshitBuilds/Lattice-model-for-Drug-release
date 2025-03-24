set terminal jpeg
unset border
set size square 1,1
set xrange[0:11]
set yrange[0:11]
set output "0000.jpeg"
unset tics
unset key
set arrow from 2,1 to 3,1 nohead lc rgb 'black'
set arrow from 3,4 to 4,4 nohead lc rgb 'black'
set arrow from 6,3 to 7,3 nohead lc rgb 'black'
set arrow from 7,4 to 8,4 nohead lc rgb 'black'
set arrow from 0,2 to 0,3 nohead lc rgb 'black'
set arrow from 4,2 to 5,2 nohead lc rgb 'black'
set arrow from 7,2 to 7,3 nohead lc rgb 'black'
set arrow from 1,1 to 1,2 nohead lc rgb 'black'
set arrow from 6,5 to 7,5 nohead lc rgb 'black'
set arrow from 4,2 to 4,3 nohead lc rgb 'black'
set arrow from 7,1 to 8,1 nohead lc rgb 'black'
set arrow from 4,9 to 4,10 nohead lc rgb 'black'
set arrow from 2,10 to 3,10 nohead lc rgb 'black'
set arrow from 6,5 to 6,6 nohead lc rgb 'black'
set arrow from 2,9 to 3,9 nohead lc rgb 'black'
set arrow from 9,9 to 10,9 nohead lc rgb 'black'
set arrow from 6,6 to 7,6 nohead lc rgb 'black'
set arrow from 5,6 to 5,7 nohead lc rgb 'black'
set arrow from 5,6 to 6,6 nohead lc rgb 'black'
set arrow from 0,6 to 1,6 nohead lc rgb 'black'
set arrow from 9,5 to 9,6 nohead lc rgb 'black'
p "0000.dat" w p ps 3 pt 3 lc rgb 'black'
