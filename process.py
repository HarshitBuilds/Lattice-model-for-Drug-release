import os
from numpy import sqrt
import sys
totalframes=int(sys.argv[1]) #number of MC simulations to average over.
a=float(sys.argv[2])
w1 = float(sys.argv[3])
w2=float(sys.argv[4])
interface=int(sys.argv[5])
maxsweeps=int(sys.argv[6])
tau = int(sys.argv[7]) #tau for calculating msd
is_top = int(sys.argv[8]) #0 for bottom lattice and 1 for upper lattice
thalfav=0.0 #average thalf
nav=[] #average n 
nav_lower=[] #average n lower lattice
nav_upper=[] #average n upper lattice
nav2=[] #stddev n
sar=[] #number of values for each t
sizedist = [] #to store size distribution
msd = [] #to store mean square displacement for all the MC simulations
for i in range(totalframes):
  index=0 #to keep track of the line in that file
  fname="rand_"+str(i+1)+".dat"
  #print fname
  #f=open(fname,'r')
  with open(fname) as f:
    line = f.readline()  # Read the first line
    while line: #iterating over lines in the file
      next_line = f.readline()  # Check if there's a next line
      if not next_line:  # Last line check, for size distribution data printed in the last line of the .dat file
        line = line.strip()  # strip the current line
        tokens = [token for token in line.split("\t") if token]  # Split on tabs and filter out empty tokens
        temp = [int(token) for token in tokens]  # Convert tokens to integers (or float(token) if needed)
      
      else: #if not the last line
        if(index<=maxsweeps):
          l=line.split()
          t=int(l[1])
          n=int(l[3])
          n1=int(l[5]) #for lower lattice
          n2=int(l[7]) #for upper lattice
          if t>=index:
            nav.append(n)
            nav_lower.append(n1)
            nav_upper.append(n2)
            nav2.append(n*n)
            sar.append(1)
            index=index+1
          # else:
          #   nav[t]+=n
          #   nav_lower[t]+=n1
          #   nav_upper[t]+=n2  
          #   nav2[t]+=n*n
          #   sar[t]+=1   
        else: #for retrieving mean square displacement data from the .dat file
           l = line.split()
           msd.append(float(l[0]))

      line = next_line  # Move to the next line (or exit loop)
        
  if(i==0):
    sizedist = temp
          #with open("temp.txt", 'w') as f:
            #for i in range(len(temp)):
             # print(temp[i], file=f)
  else:
    sizedist = [a + b for a, b in zip(sizedist, temp)] #processing size distribution across different files 
    

f = open("AverageOverSimulations.txt", 'w')
# print("t\tn\tfreq\tSD", file=f)
print("t\tn\tn1\tn2", file=f)
for i in range(index):
  if i==0:
    initial_n = nav[i]
  if i== index-1 :
    final_n = nav[i]
    final_n1 = nav_lower[i]
    final_n2 = nav_upper[i]
  nav[i]=float(nav[i])/float(totalframes)
  nav_lower[i]=float(nav_lower[i])/float(totalframes)
  nav_upper[i]=float(nav_upper[i])/float(totalframes)
  #nav2[i]=sqrt(float(nav2[i])/float(totalframes)-float(nav[i]*nav[i]))
  # print(i, "\t", nav[i], "\t", sar[i], "\t", nav2[i], file=f)
  print(i,"\t",nav[i],"\t",nav_lower[i],"\t", nav_upper[i],file =f)
x  = (final_n/initial_n)*100 #percentage of ants trapped in entire lattice
x1  = (final_n1/initial_n)*100 #percentage of ants trapped in lower lattice
x2 = (final_n2/initial_n)*100 #percentage of ants trapped in upper lattice
#print(x,file=f)
f.close()
f = open("Sizedistribution.txt", "w")
for i in range(len(sizedist)):
  sizedist[i] = float(sizedist[i])/float(totalframes)
  print(sizedist[i], file=f)
f.close()
os.chdir("/home/root1/Desktop/LatticeCodes/Trials")
percent_file = "Percentagetrapped.txt"
if not os.path.exists(percent_file): #if PercentageTrapped.txt not present then create 
    with open(percent_file, 'a') as f:
        print("Ant Fraction", "\t", "w1", "\t", "w2","\t","x","\t", "PercentTrapped","\t", "Inlower","\t","Inupper", file=f)
        
with open(percent_file, 'a') as f: #if PercentageTrapped.txt already present
    print(a, "\t",w1, "\t",w2,"\t",interface,"\t", x, "\t", x1, "\t", x2, file=f)

mean_r_square = 0.0 #average mean square displacement across all the MC simulations
for i in range(len(msd)):
   mean_r_square += msd[i]
mean_r_square = mean_r_square/len(msd)

#add code for msd txt file similar to percentagetrapped.txt 
os.chdir("/home/root1/Desktop/LatticeCodes/Trials")
percent_file = "MSD.txt"
if not os.path.exists(percent_file): #if MSD.txt not present then create 
    with open(percent_file, 'a') as f:
        print("Tau", "\t", "MSD","\t", is_top, file=f)
        
with open(percent_file, 'a') as f: #if MSD.txt already present
    print(tau, "\t",mean_r_square, file=f)     
          

        