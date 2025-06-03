import os
from numpy import sqrt
import sys
totalframes=int(sys.argv[1]) #number of MC simulations to average over.
a=float(sys.argv[2])
w1 = float(sys.argv[3])
w2=float(sys.argv[4])
interface=int(sys.argv[5])
maxsweeps=int(sys.argv[6])
is_top = int(sys.argv[7]) #0 for bottom lattice and 1 for upper lattice
tau_inc = int(sys.argv[8]) #value by which tau gets incremented
ng = int(sys.argv[9]) #size of the lattice
thalfav=0.0 #average thalf
nav=[] #average n 
nav_lower=[] #average n lower lattice
nav_upper=[] #average n upper lattice
nav2=[] #stddev n
sar=[] #number of values for each t
sizedist = [] #to store size distribution
msd = [] #to store mean square displacement for all the MC simulations
valid_tau = []
nants_inlayer = []
for i in range(totalframes):
  index=0 #to keep track of the line in that file
  fname="rand_"+str(i+1)+".dat"
  #print fname
  #f=open(fname,'r')
  count = 0 #iterates over the tau values in msd for that .dat file
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
          
          if(i==0): #For the first .dat file
            nav.append(n)
            nav_lower.append(n1)
            nav_upper.append(n2)
            nav2.append(n*n)
            sar.append(1)
          else:
            nav[t]+=n
            nav_lower[t]+=n1
            nav_upper[t]+=n2  
            nav2[t]+=n*n
            sar[t]+=1   
          index += 1
        else: #for retrieving mean square displacement data from the .dat file
           l = line.split()
           if(i==0): #for the first .dat file
            msd.append(float(l[0]))
            valid_tau.append(float(l[1]))
            nants_inlayer.append(float(l[2]))
           else:
            msd[count]+=float(l[0])
            valid_tau[count]+=float(l[1])
            nants_inlayer[count]+=float(l[2])
            count += 1

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
  nav[i]=float(nav[i])/float(totalframes)
  nav_lower[i]=float(nav_lower[i])/float(totalframes)
  nav_upper[i]=float(nav_upper[i])/float(totalframes)
  if i==0:
    initial_n = nav[i]
  if i== index-1 :
    final_n = nav[i]
    final_n1 = nav_lower[i]
    final_n2 = nav_upper[i]
  #nav2[i]=sqrt(float(nav2[i])/float(totalframes)-float(nav[i]*nav[i]))
  # print(i, "\t", nav[i], "\t", sar[i], "\t", nav2[i], file=f)
  print(i,"\t",nav[i],"\t",nav_lower[i],"\t", nav_upper[i],file =f)

x  = round((final_n/initial_n)*100,2) #percentage of ants trapped in entire lattice
x1  = round((final_n1/initial_n)*100,2) #percentage of ants trapped in lower lattice
x2 = round((final_n2/initial_n)*100,2) #percentage of ants trapped in upper lattice
diff  = (initial_n-final_n)*(90/100) #90% of ant release
t_90 = 0
for i in range(index):
  if((initial_n-nav[i])>=diff):
    t_90 = i
    break

#print(x,file=f)
f.close()
f = open("Sizedistribution.txt", "w")
for i in range(len(sizedist)):
  sizedist[i] = float(sizedist[i])/float(totalframes)
  print(sizedist[i], file=f)
f.close()
for i in range(len(msd)):
    if valid_tau[i]!=0:
      msd[i] = msd[i]/(valid_tau[i]) #Final msd values averaged over different mc runs
      nants_inlayer[i]=nants_inlayer[i]/(valid_tau[i])

with open("MSD.txt", "w") as f:
  print("Tau", "\t", "MSD","\t", "#ants_at_tau","\t",is_top, file=f)
  for i in range(len(msd)):        
    print(tau_inc*i+1, "\t",msd[i], "\t", nants_inlayer[i], file=f)  
         
num_points_per_line =  ng
num_lines_per_layer_file = 11
layer_data_sums = [[0.0] * num_points_per_line for _ in range(num_lines_per_layer_file)]
for i in range(totalframes):
  fname="layer_"+str(i+1)+".dat"
  with open(fname) as f:
    for line_index in range(num_lines_per_layer_file):
      line = f.readline()  # Read the first line
      parts = line.strip().split('\t')
      for point_index in range(num_points_per_line):
        layer_data_sums[line_index][point_index] += float(parts[point_index])/totalframes

with open("LayerDistribution.txt", "w") as f:
  for i in range(num_lines_per_layer_file):
    for j in range(num_points_per_line):
      print(layer_data_sums[i][j], end="\t",file=f)
    print(file=f)

os.chdir("/home/harshit/LatticeModel")
percent_file = "Percentagetrapped.txt"
if not os.path.exists(percent_file): #if PercentageTrapped.txt not present then create 
    with open(percent_file, 'a') as f:
        print("a", "\t", "w1", "\t", "w2","\t","x","\t", "%Trapped","\t", "Inlower","\t","Inupper","\t","t_90%" ,file=f)
        
with open(percent_file, 'a') as f: #if PercentageTrapped.txt already present
    print(a, "\t",w1, "\t",w2,"\t",interface,"\t", x, "\t", x1, "\t", x2,"\t",t_90 ,file=f)





     