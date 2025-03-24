set terminal jpeg
unset border
set size square 1,1
set xrange[0:11]
set yrange[0:11]
set output "0000.jpeg"
unset tics
unset key
set arrow from 1,2 to 1,3 nohead lc rgb 'black'
set arrow from 4,3 to 5,3 nohead lc rgb 'black'
set arrow from 8,3 to 8,4 nohead lc rgb 'black'
set arrow from 6,2 to 7,2 nohead lc rgb 'black'
set arrow from 9,2 to 10,2 nohead lc rgb 'black'
set arrow from 5,0 to 6,0 nohead lc rgb 'black'
set arrow from 1,5 to 2,5 nohead lc rgb 'black'
set arrow from 0,4 to 1,4 nohead lc rgb 'black'
set arrow from 0,1 to 1,1 nohead lc rgb 'black'
set arrow from 3,1 to 4,1 nohead lc rgb 'black'
set arrow from 1,3 to 1,4 nohead lc rgb 'black'
set arrow from 8,9 to 9,9 nohead lc rgb 'black'
set arrow from 4,9 to 4,10 nohead lc rgb 'black'
set arrow from 5,8 to 5,9 nohead lc rgb 'black'
set arrow from 7,9 to 7,10 nohead lc rgb 'black'
set arrow from 6,8 to 6,9 nohead lc rgb 'black'
set arrow from 0,7 to 0,8 nohead lc rgb 'black'
set arrow from 5,6 to 5,7 nohead lc rgb 'black'
set arrow from 8,8 to 9,8 nohead lc rgb 'black'
set arrow from 1,7 to 2,7 nohead lc rgb 'black'
set arrow from 6,5 to 6,6 nohead lc rgb 'black'
p "0000.dat" w p ps 3 pt 3 lc rgb 'black'
