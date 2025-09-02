//ANTCODE: system.cpp System Class Function Definitions (Revision Date: February 12, 2017)
//Defines the classes used in system.h  
#include <thread>
#include "system.h" 
using namespace std;
void System::CreateAnts()
{
	W.resize(MAXSWEEPS+1, vector<int> (NANT,0));
	alonglayer.resize(11,vector<int> (NG,0)); //stores distribution from t=0 to t=2*10^5
    const gsl_rng_type * gsl_T;
    gsl_rng * gsl_r;
    gsl_T = gsl_rng_default;
    gsl_r = gsl_rng_alloc (gsl_T);
	
    gsl_rng_set(gsl_r,RANDOMSEED /*time(NULL)*/ /*seed*/);
	int* cellindex = nullptr;
	int* filledcells=new int[NANT]; //index of all possible cells occupied by ants
	if(is_top==0) { //bottom lattice
	cellindex = new int[NG_new];//index of all possible positions in bottom lattice
	for (int i = 0; i < NG_new; i++)
      cellindex[i]=i;
    gsl_ran_shuffle(gsl_r, cellindex, NG_new, sizeof(int)); //for shuffling the order of elements inside the array
    gsl_ran_choose(gsl_r, filledcells, NANT, cellindex, NG_new, sizeof(int)); //randomly choosing NANT entries from cellindex and passing it to filledcells.
	}
	else{  //top lattice
	cellindex = new int[(NG2 - NG_new)];//index of all possible positions in top lattice
	for (int i = 0; i < (NG2-NG_new); i++)
      cellindex[i]=i+NG_new;
    gsl_ran_shuffle(gsl_r, cellindex, NG2 - NG_new, sizeof(int)); //for shuffling the order of elements inside the array
    gsl_ran_choose(gsl_r, filledcells, NANT, cellindex, NG2-NG_new, sizeof(int)); //randomly choosing NANT entries from cellindex and passing it to filledcells.
	}
    vector<int> initialtime;
	for(int i=0; i<NANT; i++)
    {
      	AntCluster ac; 
      	Coordinate coord;

      	coord.x = filledcells[i]/NG; //row number
		coord.y = filledcells[i]%NG; //column number
		coord.realX = coord.x;
		coord.realY = coord.y;
      	ac.cells.push_back(filledcells[i]); //stores index
      	ac.initialCoordinates.push_back(coord); //stores intial coordinates
      	ac.newCoordinates.push_back(coord); //stores new coordinates
      	initialtime.push_back(filledcells[i]); //stores the location of ants at t = 0

      	AC.push_back(ac); 
		//ac stores info for individual ants and AC is a list storing info for all the ants.

    }
	W[0]=initialtime; //indices of ants at t = 0
    //cout<<"Ants created\n";
	delete[] filledcells;
	delete[] cellindex;
    gsl_rng_free (gsl_r); //to free up memory allocated to the random number generator.
}

void System::CreateWalls()
{
    const gsl_rng_type * gsl_T;
    gsl_rng * gsl_r;
    gsl_T = gsl_rng_default;
    gsl_r = gsl_rng_alloc (gsl_T);
	
	gsl_rng_set(gsl_r,RANDOMSEED /*seed*/); //gsl_r is a pointer to a random number generator object usedfor generating random numbers.
    int ntot=NG2+NG*(NG+1);  //leftmost same as rightmost wall
    int* wallindex1= new int[NG*x + (x+1)*NG]; //all cell boundaries in first lattice.
	int* wallindex2 = new int[(NG-x)*NG + (NG-x)*NG]; //all cell boundaries in second lattice.
    walls1=new int[NWALL1]; //to store the index for all the walls among all the cell boundaries in first lattice.
	walls2 = new int[NWALL2];
	int index1 = 0;
	int index2 = 0;
	for (int i = 0; i < ntot; i++)
	{
		if (i < x * NG) //vertical walls in first lattice
		{
			wallindex1[index1] = i;
			index1++;
		}
		else if (i >= x * NG && i < NG * NG) //vertical walls in second lattice
		{
			wallindex2[index2] = i;
			index2++;
		}
		else if (i >= NG * NG && i < (NG) * (NG + x + 1)) //horizontal walls in first lattice
		{
			wallindex1[index1] = i;
			index1++;
		}
		else if (i >= (NG) * (NG + x + 1) && i < ntot) //horizontal walls in second lattice
		{
			wallindex2[index2] = i;
			index2++;
		}
	}
    gsl_ran_shuffle(gsl_r, wallindex1, NG * x + (x + 1) * NG, sizeof(int)); //shuffling walls in the first lattice
    gsl_ran_choose(gsl_r, walls1, NWALL1, wallindex1, NG * x + (x + 1) * NG, sizeof(int));
	if(x!=NG) //for x=NG(only hydrophobic layer), walls2 and wallindex2 are empty arrays.
	{
		gsl_ran_shuffle(gsl_r, wallindex2, (NG - x) * NG + (NG - x) * NG, sizeof(int)); //comment out for x=1
		gsl_ran_choose(gsl_r, walls2, NWALL2, wallindex2, (NG - x) * NG + (NG - x) * NG, sizeof(int)); //comment out for x=1
	}
    gsl_rng_free (gsl_r);
	delete[] wallindex1;
	delete[] wallindex2;
}

void System::CreateCells()
{
	//create without wall and ant entries
	for (int i = 0; i < NG2; i++) //total number of cells in the lattice
	{
		Cell c; //object of the cell class defined in cell.h
		c.row = int(i / NG);
		c.col = i % NG;
		//cout<<"i= "<<i<<" row= "<<c.row<<" col= "<<c.col<<endl;
		//Left Neighbor
		if (c.col != 0)
			c.nbrs.push_back(i - 1);
		else
			c.nbrs.push_back(i - 1 + NG); //bcz of PBC
		//Right Neighbor
		if (c.col != NG - 1)
			c.nbrs.push_back(i + 1);
		else
			c.nbrs.push_back(i + 1 - NG); //bcz of PBC
		//Top Neighbor
		if (c.row != NG - 1)
			c.nbrs.push_back(i + NG);
		else
			c.nbrs.push_back(-1); //no PBC in top and bottom
		//Bottom Neighbor
		if (c.row != 0)
			c.nbrs.push_back(i - NG);
		else
			c.nbrs.push_back(-1); 
		C.push_back(c); //c is for individual cell, C is for entire lattice storing info for all the cells
	}

	/*for(int i=0; i<NG2; i++)
	{
		cout<<C[i].row<<','<<C[i].col<<'\t'<<C[i].nbrs[0]<<','<<C[i].nbrs[1]<<','<<C[i].nbrs[2]<<','<<C[i].nbrs[3]<<endl;
	}*/

	//fill ants
	list<AntCluster>::iterator it;
	for (it = AC.begin(); it != AC.end(); it++) //runs NANT number of times 
	{
		list<int>::iterator it2;
		for (it2 = (*it).cells.begin(); it2 != (*it).cells.end(); it2++) //iterates over the cells list in Ant cluster object
		{
			C[(*it2)].isAnt = true; //marks those cells(given by index it2) as true where ants are located.
			if (C[(*it2)].row < x)
				NANT1++;
			else
				NANT2++;
		}
	}
	//put wall in the cell boundaries//
	for (int i = 0; i < NWALL1; i++) //for first lattice
	{
		int itemp, irow, icol;
		int w = walls1[i];
		if (w < NG2) //vertical walls
		{
			itemp = w;
			irow = int(itemp / NG);
			icol = itemp % NG;
			// cout<<"irow="<<irow<<"icol="<<icol<<endl;
			if (icol != NG)
				C[irow * NG + icol].isWall[0] = true; //left wall
			if (icol != 0)
				C[irow * NG + icol - 1].isWall[1] = true; //right wall
			else   //for PBC
				C[irow * NG + icol + NG - 1].isWall[1] = true; //marks right wall for icol=0
		}
		else //horizontal wall
		{
			itemp = w - NG2;
			irow = int(itemp / NG);
			icol = itemp % NG;
			//cout<<"irow="<<irow<<" icol="<<icol<<endl;
			if (irow != NG)
				C[irow * NG + icol].isWall[3] = true;//bottom wall
			if (irow != 0)
				C[(irow - 1) * NG + icol].isWall[2] = true;//top wall
		}
	}
	for (int i = 0; i < NWALL2; i++) //for second lattice
	{
		int itemp, irow, icol;
		int w = walls2[i]; //w is index of the i'th wall 
		if (w < NG2) //vertical wall (either left or right)
		{
			itemp = w;
			irow = int(itemp / NG); //In any given row there are NG walls.
			icol = itemp % NG; //Goes from 0 to NG-1
			// cout<<"irow="<<irow<<" icol="<<icol<<endl;
			if (icol != NG)
				C[irow * NG + icol].isWall[0] = true; //left wall 
			if (icol != 0)
				C[irow * NG + icol - 1].isWall[1] = true; //right wall
			else
				C[irow * NG + icol + NG - 1].isWall[1] = true; //marks right wall for icol=0
		}
		else //horizontal wall
		{
			itemp = w - NG2;
			irow = int(itemp / NG);
			icol = itemp % NG;
			//cout<<"irow="<<irow<<" icol="<<icol<<endl;
			if (irow != NG)
				C[irow * NG + icol].isWall[3] = true; //bottom wall
			if (irow != 0)
				C[(irow - 1) * NG + icol].isWall[2] = true; //top wall
		}
	}

	//check for all blocks
	for (int i = 0; i < NG2; i++)
		C[i].findperm();
	// cout<<endl;
	if (PWALL == 0.0 && (WALLF1 > 0.0 || WALLF2 > 0.0))
	{
		for (int i = 0; i < NG2; i++)
		{
			double tot_perm = C[i].perm;
			//check one cell
			if (tot_perm == 1.0)
			{
				C[i].isBlock = true;
				continue;
			}
			else
			{
				//check up to two cells
				for (int j = 0; j < 4; j++)
				{
					if (C[i].nbrs[j] != -1 && C[i].isWall[j] == false)//neighboring cell present and no common wall
					{
						tot_perm = C[i].perm + C[C[i].nbrs[j]].perm;
						if (tot_perm == 6.0 / 4.0)
						{
							C[i].isBlock = true;
							break;
						}
					}
				}
			}

		}
	}


}

//friendly ant in lower lattice and blind in top
void System::CreateAntClusters() //for merging clusters 
{
    list<AntCluster>::iterator itc1,itc2; 
	list<int>::iterator it1, it2, it3, x1, x2;
    bool merge=false;
    int ncluster=AC.size(); //number of clusters in AC
    
    for(itc1=AC.begin(); itc1!=AC.end(); itc1++) //first cluster
    {
		itc2 = AC.begin();
		x1 = (*itc1).cells.begin();
		if (C[*x1].row >= x)
			continue;
	//cout<<"outer"<<endl;
	
	while(itc2!=AC.end())//second cluster
	{
		
	   // cout<<"inner"<<endl;
	    merge=false; 
		x2 = (*itc2).cells.begin();
		if (C[*x2].row >= x)
		{
			itc2++;
			continue;
		}
	    if(itc2==itc1) //dont merge if both are same cluster
	    {
	      itc2++;
	      continue;
	    }
	    for(it1=(*itc1).cells.begin(); it1!=(*itc1).cells.end(); it1++)//iterates over cells in first cluster
	    {
			
		for(it2=(*itc2).cells.begin(); it2!=(*itc2).cells.end(); it2++)//iterates over cells in second cluster
		{
			if (C[*it2].row >= x) //if in top lattice move to the next cluster
				continue;
		    //proceed only if both cells have ants 
		    if(C[*it1].isAnt && C[*it2].isAnt) 
		    {
			//check whether they are neighbors and without common walls
			for(int r=0; r<4; r++) //checking for all the 4 directions 
			{
			    if(C[*it1].nbrs[r]==(*it2) && C[*it1].isWall[r]==false)
			    {
				//merge clusters
				//move all cells of itc2 in itc1 
				(*itc1).cells.insert((*itc1).cells.end(),(*itc2).cells.begin(),(*itc2).cells.end());
				//remove itc2
				itc2=AC.erase(itc2); 
				//after this itc2 points to the next cluster.
				//cout<<"merged"<<endl;
				merge=true; 
				ncluster--;
				break;
			    }
			}
		    }
		    if(merge)//check next cluster
		      break;
		}
		if(merge)//check next cluster
		      break;
		} // if merge happens break out of all loops for the second cluster.
	if(!merge)
	itc2++; //if not merged move to the next "second" cluster (the "first" cluster is same).
	}

    }
   /* cout<<AC.size()<<" clusters remaining\n";*/
	/*cout << "ants in cluster ";*/
	/*cout << " Number of clusters are " << AC.size() << endl;*/
	//cout << "Ant indices are : ";
	
	// int count = 0; commented 
	// for (itc1 = AC.begin(); itc1 != AC.end(); itc1++)
	// {
	// 	/*cout << (*itc1).cells.size()<<" ";*/
	// 	for (it1 = (*itc1).cells.begin(); it1 != (*itc1).cells.end(); it1++)
	// 	{
	// 		cout << (*it1) << " ";
	// 	}
	// 	cout << ",";
	// 	for (it1 = (*itc1).cells.begin(); it1 != (*itc1).cells.end(); it1++)
	// 		count++;
	// }
	/*cout << "number of ants are "<<count<<endl;*/
	//iterate over every cell in the lattice
	// cout << "number of clusters : " << AC.size()<<" "; commented out
	/*cout << "Ant at index : ";
	for (int i = 0; i < NG2; i++)
	{
		if (C[i].isAnt)
			cout << i << " ";
	}
	cout << endl;*/
	
}


void System::Move()
{
  const gsl_rng_type * gsl_T;
  gsl_rng * gsl_r;
  gsl_T = gsl_rng_default;
  gsl_r = gsl_rng_alloc (gsl_T);
  
  gsl_rng_set(gsl_r, RANDOMSEED/*seed*/); 
  int nantc=NANT;//number of remaining clusters
  int nant=NANT; //number of remaining ants
  list<AntCluster>::iterator it;
  list<int>::iterator it2;
  list<Coordinate>::iterator it3, it4, it5; //to iterate over coordinate type list 
  int sample_count=1;
  double MeanR, RootMeanR; 
  int dist[100]; //Related to radial distribution function.

  	char FileName[100], FileName1[100];
    // sprintf(FileName,"msd_%d.txt", RANDOMSEED); //commented out as no need for displacement right now
    // //find tesc_av  
    // ofstream out;
    // out.open(FileName);

    // sprintf(FileName1,"dist_%d.txt", RANDOMSEED);
    // //find tesc_av  
    // ofstream out1;
    // out1.open(FileName1);
	int movetracker = 0;
	int p = 1; //index for W vector 
	sizedist.resize(NANT);
	std::fill(sizedist.begin(), sizedist.end(), 0);
  	for(int k=0; k<MAXSWEEPS; k++) //maximum number of MC sweeps. All ants are displaced in one MC sweep.
  	{
		// cout << "Number of movements: " << movetracker << endl;
		movetracker = 0;//define a new variable to track movement in each time step.
    	CreateAntClusters();
   		//  cout<<k<<".jpeg: "<<nant<<" ants in "<<AC.size()<<" clusters\n";
		if(k==MAXSWEEPS-1) //last MC sweep 
		{		
			for(it = AC.begin(); it!=AC.end();it++) //iterating over every ant cluster
			{
				int num = 0; //number of elements in this cluster
				for(it2=(*it).cells.begin(); it2!=(*it).cells.end(); it2++)
				{
					if (C[*it2].row >= x) //if in upperlayer move to the next cluster
						break;
					num++;
				}
				if(num>0)
					sizedist[num-1]++;
			}
		}
      	if((k)%NSAMPLE==0) //NSAMPLE is the sampling frequency
      	{
			//cout<<k<<endl;
			//cout<<AC.size()<<' ';
			writeGNU(k);
		}

     	
		// double msd_step = 0.0; //mean square displacement of the overall system in a single sweep

		// for(int j =0; j<100 ; j++) //
		// {
		// 	dist[j] = 0;
		// }
		//commenting coordinate code
		//for(it = AC.begin(); it!=AC.end(); it++) //iterates over all the ant clusters
  // 		{
  // 			it3 = (*it).initialCoordinates.begin(); //initialising the iterator 
  // 			it4 = (*it).newCoordinates.begin(); 
  // 			
  // 			//cout<<(*it3).x<<","<<(*it3).y<<"---->"<<(*it4).x<<","<<(*it4).y<<" real "<<(*it3).realX<<","<<(*it3).realY<<"---->"<<(*it4).realX<<","<<(*it4).realY<<endl;
  // 			msd_step += double(pow(((*it4).realX - (*it3).realX), 2) + pow(((*it4).realY - (*it3).realY), 2))/double(NANT); 

  // 			//claculating the distribution of ants (mean distance from the centre)
  // 			MeanR = double(pow(((*it4).realX - double(NG+1)/2.0), 2) + pow(((*it4).realY - double(NG+1)/2.0), 2));
  // 			RootMeanR = sqrt(MeanR);
  // 			for(int j =0; j<100; j++) //purpose of this loop?
  // 			{
  // 				if(RootMeanR>=j && RootMeanR<j+1)
  // 				{
  // 					dist[j]++;
  // 				}
  // 			}
		//}

		//if((k)%NSAMPLE==0)
  //    	{
		//	out<<k<<'\t'<<msd_step<<'\t'<<sqrt(msd_step)<<endl;

		//	out1<<" "<<endl;
		//	out1<<" "<<endl;
		//	out1<<" "<<endl;


		//	for(int j =0; j<100; j++)
  // 			{
  // 				out1<<j+1<<'\t'<<dist[j]<<'\t'<<double(dist[j])/(4.0*PI*((j+1)*(j+1)-j*j))<<endl;
  // 			}
  // 			
		//	//cout<<k<<'\t'<<msd_step<<endl;
		//}
		vector<int> latertime;
		if(k==0)
			latertime = W[0]; //take the indices for the initial time
		else if(k>0) 
			latertime = W[p-1]; //intialising present timestep indices with previous timestep indices
             
		int Numcluster = AC.size(); //to store number of cluster in that timestep
		nantc = AC.size(); //number of unsplitted cluster.
		int track = 0; //iterates over every cluster
     	for(int j=0; j<Numcluster; j++) //in every time step AC.size() number of clusters are moved.
      	{
			//cout<<AC.size()<<endl;
	      	/*nantc=AC.size();*/
			/*int antcindex= gsl_rng_uniform_int(gsl_r, nantc);*/ //commented to ensure movement over every cluster
			int antcindex = track; //points to the cluster to move 
	      	//choose any antcluster randomly
			if (nantc <= 0) 
			{
				cout << "All splitted";
				break;
			}

	      	it=AC.begin();
	      	for(int l=0; l<antcindex; l++) {
		    	it++; //it is the iterator to the chosen cluster.
			}	      

			if (it == AC.end()) 
			{
				// Handle the error or break out of the loop
				cout << "End reached ";
				cout << antcindex<<" "<<AC.size();

			}
			track++;
	      	//move all cells in that cluster if possible, store all new cells in an vector 
	      	vector<int> newcells; //new indices for the chosen cluster
	      	vector<int> oldcells; //old indices for the chosen cluster
	      	vector<Coordinate> oldCoord, newCoord;
	      
	      	//choose random number between 0 to 3
	      	int r=gsl_rng_uniform_int(gsl_r,4);
			
	      	for(it2=(*it).cells.begin(); it2!=(*it).cells.end(); it2++) //for checking the wall condition for that cluster
	      	{
		  		int cellindex=(*it2);
		  		/*Coordinate acoord;

		  		acoord.x = (*it5).x;
		  		acoord.y = (*it5).y;
		  		acoord.realX = (*it5).realX;
		  		acoord.realY = (*it5).realY;*/
				//  cout<<"cellindex="<<cellindex<<endl;
				//cout<<acoord.x<<","<<acoord.y<<","<<acoord.realX<<","<<acoord.realY<<endl;
				oldcells.push_back(cellindex); 
				/*oldCoord.push_back(acoord);*/
		  		double move_r;


		  		if(C[cellindex].isWall[r]) //if wall is present in that direction of movement.
		    		move_r=gsl_rng_uniform_pos(gsl_r);
		  		else
		    		move_r=0.0; 

		  		//check whether movement is possible with walls
		  		if(move_r>PWALL)//leave this cluster
		    		break;
		  		else
		  		{
		    		newcells.push_back(C[cellindex].nbrs[r]); //wall condition passed for that ant
		    		//cout<<cellindex<<","<<C[cellindex].nbrs[r]<<" r ="<<r<<endl;
					
					//commenting coordinate code
		    		/*Coordinate acoordnew;
		    		acoordnew.x = C[cellindex].nbrs[r]/NG;
		    		acoordnew.y = C[cellindex].nbrs[r]%NG;*/

		    		/*if(r==0)
		    		{
		    			acoordnew.realX = (*it5).realX;
		    			acoordnew.realY = (*it5).realY - 1;
		    		}else if(r==1)
		    		{
						acoordnew.realX = (*it5).realX;
		    			acoordnew.realY = (*it5).realY + 1;
		    		}else if(r==2)
		    		{
						acoordnew.realX = (*it5).realX + 1;
		    			acoordnew.realY = (*it5).realY;		    			
		    		}else
		    		{

						acoordnew.realX = (*it5).realX - 1;
		    			acoordnew.realY = (*it5).realY;		    			
		    		}*/

		    		//cout<<acoordnew.x<<","<<acoordnew.y<<","<<acoordnew.realX<<","<<acoordnew.realY<<endl;
		    		/*newCoord.push_back(acoordnew);*/
		  		}

		  		/*it5++;*/ //causing some list error.
	      	}

	   		//   cout<<"out of loop"<<endl;
	      	if(newcells.size()!=(*it).cells.size())
	      	{
		  		continue; // go to next cluster
	      	}
			//cout<<newcells.size()<<endl;
			//for(int m=0; m<newcells.size(); m++)
				//cout<<newcells[m]<<" ";	

	      	bool newwall=false;
	      	/*check whether there are wall between new cells*/
	      	for(int m=0; m<newcells.size(); m++)
	      	{
				if(newcells[m]==-1 || C[newcells[m]].row >= x) //if ant has escaped the lattice or moved from hydrophobic to hydrophilic
		    		continue;                                  //both cases in which friendship condition does not apply

				//all neigbors of newcells[m]
				for(int l=0; l<4; l++)
				{
		  			if(C[newcells[m]].nbrs[l]==-1)
		    			continue;

		  			for(int n=0; n<newcells.size(); n++)
		  			{
		      			if(C[newcells[m]].nbrs[l]==newcells[n] && C[newcells[m]].isWall[l]==true)
		      			{
							double move_r=gsl_rng_uniform_pos(gsl_r);
							//cout<<"wall found"<<endl;
							if(move_r>PWALL) 
							{
			  					newwall=true;
			  					break;
							}
		      			}
		  			}

		  			if(newwall)
		    			break;
				}

				if(newwall)
		  			break;
	      	}

	      	if(newwall) //frienship condition non satisfied. Move to the next cluster.
				continue;
	      
	      	/*now check if the new cells are not occupied by other clusters*/
	      	int i;
	      	//temporary set all the isAnt of oldcells to false
	      	for(int m=0; m<oldcells.size(); m++)
		  		C[oldcells[m]].isAnt=false;

	      	for(i=0; i<newcells.size(); i++)
	      	{
		  		if(newcells[i]==-1)
		    	 	continue;
		  		else if(C[newcells[i]].isAnt) //to check if cells are occupied by ants of other cluster.
		  			break;
	      	}

	      	//cout<<"newcellsize "<<newcells.size()<<" value of i "<<i<<endl;
			bool check =false; //for ant cluster case trying to leave from bottom
			bool split = false; //for splitting cluster
			bool last = false;
	      	if(i<newcells.size())
	      	{
		  		for(int m=0; m<oldcells.size(); m++)
		      		C[oldcells[m]].isAnt=true; //rejecting the move.
		  		continue; //go to next cluster
	      	}
	      	else //movement is possible for that cluster
	      	{
		  		i=0; //to iterate over the newcells and oldcells
		  		it2=(*it).cells.begin(); 
		  		/*it5=(*it).newCoordinates.begin();*/
		  		while(it2!=(*it).cells.end()) //iterating over the different ants in that cluster
		  		{
		      		int cellindex=(*it2);
					//updating the indices vector in latertime for this cluster
					for(int idx=0;idx<NANT;idx++)
							{
								if(oldcells[i]==latertime[idx])
									latertime[idx] = newcells[i]; //new index of the corresponding ant
							}
		      		if(newcells[i]==-1)
		      		{  
						if (r == 3) //ant trying to escape from the bottom boundary. 
						{
							C[oldcells[i]].isAnt = true; //reject the move 
							check = true;
							it2++;
							//break; commenting so that entire cluster indices get updated with new values
						}
						else //from top
						{
							tesc.push_back(k);
							tesc2.push_back(k);
							nant--;
							movetracker++;
							if ((*it).cells.size() == 1)
							{
								//cout<<"cluster escape\n";
								it = AC.erase(it);
								nantc--;
								track--;
								break;
							}
							else //delete only element
								it2 = ((*it).cells).erase(it2);
						}
		      		}
		      		else  //ant is not escaping
		      		{
						bool deref = false;
						
						movetracker++; 
						//cout<<"cell index "<<newcells[i]<<" ";
						//cout<<"i="<<i<<"\tnewcell="<<newcells[i]<<endl;
			  			C[newcells[i]].isAnt=true;
						

						//  cout<<"i="<<i<<"\tcellindex="<<cellindex<<"\tnewcells="<<newcells[i]<<endl;
						if (C[newcells[i]].row == x && C[oldcells[i]].row == x-1) //from bottom to top
						{
							//demerging operation
							if ((*it).cells.size() == 1) //deleting the entire cluster.
							{
								//cout<<"cluster escape\n";
								it = AC.erase(it);
								nantc--;
								track--;
								last = true;
								split = false;
							}
							else //delete only one ant element
							{
								it2 = ((*it).cells).erase(it2);
								deref = true;
								split = true;
							}
							
							AntCluster ac;
							//coord.x = filledcells[i] / NG; //row number
							//coord.y = filledcells[i] % NG; //column number
							//coord.realX = coord.x;
							//coord.realY = coord.y;
							ac.cells.push_back(newcells[i]); //stores index
							//ac.initialCoordinates.push_back(coord); //stores intial coordinates
							//ac.newCoordinates.push_back(coord); //stores new coordinates
							
							AC.push_back(ac);
						
							tent2.push_back(k);
							tesc1.push_back(k);
						}
						else if (C[newcells[i]].row == x-1 && C[oldcells[i]].row == x) //from top to bottom
						{
							double jump;
							jump=gsl_rng_uniform_pos(gsl_r);
							if(jump>PJUMP) //PJUMP is the probability of jump from top to bottom.
							{
								//code to reject the move
								C[oldcells[i]].isAnt = true; 
								C[newcells[i]].isAnt = false;
								for(int idx=0;idx<NANT;idx++) //updating the latertime vector with oldcells list
								{
									if(newcells[i]==latertime[idx])
										latertime[idx] = oldcells[i]; 
								}
								break;
							}
							else
							{
								tent1.push_back(k);
								tesc2.push_back(k);
								
							}
							
						}
			  			//(*it2)=newcells[i]; //passes the new cellindex to the cells list.
						if (last == true)
							break;

						if (deref==false) {
							(*it2) = newcells[i]; // Passes the new cell index to the cells list.
							it2++;
						}
						//commmenting coord codes
			  			/*(*it5).x=newCoord[i].x;
			  			(*it5).y=newCoord[i].y;
			  			(*it5).realX=newCoord[i].realX;
			  			(*it5).realY=newCoord[i].realY;*/
			  			 //move to the next cell.
			  			/*it5++;*/
		      		}
		      		i++;
		  		}
				if (split) //splitting the cluster if any ant crosses the border.
				{
					nantc--;
					track--;
					it2 = (*it).cells.begin();
					while (it2 != (*it).cells.end())
					{
						int cellindex = (*it2);
						it2 = ((*it).cells).erase(it2); //delete the ant from the cluster
						AntCluster ac; //create new cluster
						ac.cells.push_back(cellindex); 
						AC.push_back(ac);
					}
					it = AC.erase(it); //deletes the old cluster
				}
				if (check) //when bottom move is rejected. The entire ant cluster move is rejected.
				{
					for (int m = 0; m < newcells.size(); m++) //removing the newlocations.
					{
						if (newcells[m] == -1) //out of the lattice cell
							continue;
						else
							C[newcells[m]].isAnt = false;
					}
					for (int m = 0; m < oldcells.size(); m++)
					{
						C[oldcells[m]].isAnt = true; //rejecting the move.
						
					}
					//code storing the change in cells list of the cluster
					int i = 0;
					it2 = (*it).cells.begin();
					while (it2 != (*it).cells.end())
					{
						(*it2) = oldcells[i];
						i++;
						it2++;
					}
					for(int m=0;m<newcells.size();m++) //replacing the new indices with old ones due to rejection
					{
						for(int idx=0;idx<NANT;idx++)
							{
								if(newcells[m]==latertime[idx])
									latertime[idx] = oldcells[m]; //replacing with the old indexes due to rejection of the move
							}
					}
				}
	      	}
			
      	}
		W[p]=latertime; 
	
		//code for evaluating msd for all the windows for all the taus
		if(k==MAXSWEEPS-1)
		{
		if(is_top==0) //for bottom lattice
			{
			for(int tau_val=1;tau_val<=MAXSWEEPS;tau_val+=tau_inc) 
				{
					//double total_r_square  = 0; //for all the intervals at a given tau
					//int count =  MAXSWEEPS-tau_val;
				//for(int i=0;i<MAXSWEEPS-tau_val;i++) //all the intervals  
					//{
						double r_square = 0; //r square for a given tau
						int n1 = NANT; //number of ants in the bottom lattice at time t = tau_val
						for(int j=0;j<NANT;j++)
						{
							if(W[tau_val][j]==-1||W[tau_val][j]>=(NG_new)) //condition for ant to be outside bottom lattice
							{
								n1--; 
							}
							else //if inside then compute msd for that ant
							{
								int x0 = int(W[0][j]/NG);
								int y0 = W[0][j]%NG;
								
								int xm = int(W[tau_val][j]/NG);
								int ym = W[tau_val][j]%NG; 
								int delx = xm-x0;
								if(abs(delx)>NG/2) //PBC correction
									delx = NG-delx;	
								r_square += (ym - y0)*(ym - y0) + (delx)*(delx); //summed over each ant
							}
						}
						if(n1==0) //all ants have escaped the bottom layer
						{
							//count = i; //number of intervals to average over
							valid_tau.push_back(0); //For a tau, indicates not to consider this interval(tau)
							//break;
						}
						else
						{
							valid_tau.push_back(1); ////For a tau, indicates to consider this interval(tau)
							r_square = r_square/(n1);
							//total_r_square += r_square;
						}
					//}
					//total_r_square = total_r_square/(count);
					//msd.push_back(total_r_square); //for a particular tau
					nants_inlayer.push_back(n1);
					msd.push_back(r_square); //for that particular tau
				}
				
			}	
		else //for top lattice
		{
			for(int tau_val=1;tau_val<=MAXSWEEPS;tau_val+=tau_inc) 
				{
					//double total_r_square = 0; //for all the intervals at a given tau
					//int count=MAXSWEEPS-tau_val;
					//for(int i=0;i<MAXSWEEPS-tau_val;i++) //all the intervals  
					//{
							double r_square = 0; //r_square for a given tau
							int n2 = NANT; //number of ants in the top lattice at time t = tau_val
							for(int j=0;j<NANT;j++)
							{
								if(W[tau_val][j]==-1||W[tau_val][j]<(NG_new)) //condition for ant to be outside bottom lattice
								{
									n2--; 
								}
								else //if inside then compute msd for that ant
								{	
									int x0 = int(W[0][j]/NG);
									int y0 = W[0][j]%NG;
									
									int xm = int(W[tau_val][j]/NG);
									int ym = W[tau_val][j]%NG; 
									int delx = xm-x0;
									if(abs(delx)>NG/2) //PBC correction
										delx = NG-delx;	

									r_square += (ym - y0)*(ym - y0) + (delx)*(delx); //summed over each ant
								}
							}
						if(n2==0) //all ants have escaped the top layer
						{
							//count = i;
							//break;
							valid_tau.push_back(0); //For a tau, indicates not to consider this interval(tau) for averaging later
						}
						
						else
						{
							valid_tau.push_back(1); //For a tau, indicates not to consider this interval(tau) for averaging later
							r_square = r_square/(n2);
							//total_r_square += r_square;
						}
					
					//total_r_square = total_r_square/(count);
					//msd.push_back(total_r_square); //for a particular tau
					nants_inlayer.push_back(n2);
					msd.push_back(r_square); //for that particular tau
				}
				
			}
			//add code for storing location at different z
			int count = 0;
			for(int i = 0;i<=200000;i+=20000) //timesteps
			{
				for(int j=0;j<NANT;j++)
				{
					if(W[i][j]!=-1) //ensure only ants inside the lattice are used for computing the layerwise distribution
					{
					int row = int(W[i][j]/NG);
					alonglayer[count][row]++;
					}
				}
				count++;
			}
			if(count!=11)
			cout<<"error in alonglayer";
		}
		else
		p++; //incrementing index of the W vector


      	//check if all remaining cells are blocked
      	int block=0;//number of blocked ants
      	for(int j=0; j<NG2; j++)
      	{
	  		if(C[j].isBlock && C[j].isAnt)
	      		block++;
      	}
		
      	if(block==nant && nant!=0)
      	{
	  		cout<<"ants blocked in remaining cells"<<endl;
	  		break;
      	}
  	}

  	// out.close();
  	cout<<nant<<" ants remaining"<<endl;
  	gsl_rng_free (gsl_r);
}

// commenting out gnu function to reduce the files produced on running code
void System::writeGNU(int index)
{
	// Get current working directory
    char cwd[1024];
    if (getcwd(cwd, sizeof(cwd)) == NULL) {
        cerr << "Error getting current working directory" << endl;
        return;
    }

   ofstream out;
   char FileName[1024];
   //sprintf(FileName,"%d.dat",index);
   sprintf(FileName, "%s/%04d.dat", cwd, index); //Insert the contents of cwd (current working directory) where %s is and insert the value of index where %d is
   out.open(FileName);
   //write ant data
   for(int i=0; i<NG2; i++)
	if(C[i].isAnt)
	    out<<C[i].col+0.5<<" "<<C[i].row+0.5<<endl;
   out.close();
   
   sprintf(FileName, "%s/%04d.gnu", cwd, index);
   //sprintf(FileName,"%d.gnu",index);
   out.open(FileName);
   out<<"set terminal jpeg"<<endl;
   out<<"unset border"<<endl;
   out<<"set size square 1,1"<<endl;
   out<<"set xrange["<<0<<":"<<NG+1<<"]"<<endl;
   out<<"set yrange["<<0<<":"<<NG+1<<"]"<<endl;
//    out<<"set output \""<<index<<".jpeg\""<<endl;
	char jpegName[64];
    sprintf(jpegName, "%04d.jpeg", index);
    out << "set output \"" << jpegName << "\"" << endl;
   out<<"unset tics"<<endl;
   out<<"unset key"<<endl;
   //write walls
   int w,irow, icol;
   for(int i=0; i<NWALL1; i++)
   {
		if(walls1[i]<NG2)//vertical wall
		{
			w=walls1[i];
			irow=int(w/NG);
			icol=w%NG;
			out<<"set arrow from "<<icol<<","<<irow<<" to "<<icol<<","<<irow+1<<" nohead lc rgb \'black\'"<<endl;
		}
		else //horizontal wall
		{
			w=walls1[i]-NG2;
			irow=int(w/NG);
			icol=w%NG;
			out<<"set arrow from "<<icol<<","<<irow<<" to "<<icol+1<<","<<irow<<" nohead lc rgb \'black\'"<<endl;
		}
   }
	for (int i = 0; i < NWALL2; i++) //for second lattice.
	{
		if (walls2[i] < NG * NG)//vertical wall
		{
			w = walls2[i];
			irow = int(w / NG);
			icol = w % (NG);
			out << "set arrow from " << icol << "," << irow << " to " << icol << "," << irow + 1 << " nohead lc rgb \'black\'" << endl;
		}
		else//horizontal wall
		{
			w = walls2[i] - NG * NG;
			irow = int(w / NG);
			icol = w % NG;
			out << "set arrow from " << icol << "," << irow << " to " << icol + 1 << "," << irow << " nohead lc rgb \'black\'" << endl;
		}
	}
	char datName[64];
	sprintf(datName, "%04d.dat", index);
   out<<"p \""<</*index*/datName<<"\" w p ps 3 pt 3 lc rgb \'black\'"<<endl;
   out.close(); 
   
}

void System::writeOutput()
{
	delete[] walls1;
	delete[] walls2;
    char FileName[100];
   	sprintf(FileName,"rand_%d.dat",RANDOMSEED); //simulation time vs number of ants data
	cout<<FileName<<endl;
	// sprintf(FileName, "rand_1.dat");
    //find tesc_av 
    ofstream out;
    out.open(FileName);
    int n=NANT;
	int n1 = NANT1; //initial number of ants in first lattice
	int n2 = NANT2; //initial number of ants in second lattice
	int m = tesc.size();
    int index=0;
	int esc1 = 0;
	int esc1_size = tesc1.size();
	int esc2 = 0;
	int esc2_size = tesc2.size();
	int ent1 = 0;
	int ent1_size = tent1.size();
	int ent2 = 0;
	int ent2_size = tent2.size();

		
		for (int i = 0; i <= MAXSWEEPS; i++) //to ensure movements in the last timestep are also tracked
		{
			out << setw(6) << "t" << "\t" << setw(12) << i << "\t" << setw(6) << "NANT" << "\t" << setw(12) << n << "\t" << setw(6) << "NANT1" << "\t" << setw(12) << n1 << "\t" << setw(6) << "NANT2" << "\t" << setw(12) << n2 << "\t" << setw(6) << endl;

			if (index < m)
			{
				while (tesc[index] + 1 == i + 1) //to iterate over tesc vector.
				{
					n--;
					index++;
					if (index == m)
						break;
				}
			}
			if (esc1 < esc1_size) //first lattice escape
			{
				while (tesc1[esc1] + 1 == i + 1) //to iterate over tesc vector.
				{
					n1--;
					esc1++;
					if (esc1 == esc1_size)
						break;
				}
			}
			if (ent1 < ent1_size) //first lattice enter
			{
				while (tent1[ent1] + 1 == i + 1) //to iterate over tesc vector.
				{
					n1++;
					ent1++;
					if (ent1 == ent1_size)
						break;
				}
			}
			if (esc2 < esc2_size) //second lattice escape
			{
				while (tesc2[esc2] + 1 == i + 1) //to iterate over tesc vector.
				{
					n2--;
					esc2++;
					if (esc2 == esc2_size)
						break;
				}
			}
			if (ent2 < ent2_size) //second lattice enter
			{
				while (tent2[ent2] + 1 == i + 1) //to iterate over tesc vector.
				{
					n2++;
					ent2++;
					if (ent2 == ent2_size)
						break;
				}
			}

		}
		if(msd.size()!=valid_tau.size()||msd.size()!=nants_inlayer.size())
		cout<<"Error sizes not equal";
		//adding msd for the simulation to the output file
		for(int i=0;i<msd.size();i++)
		out<<msd[i]<<"\t"<<valid_tau[i]<<"\t"<<nants_inlayer[i]<<endl;

		//adding size distribution data to the last file
		for(int i =0;i<sizedist.size();i++)
		{
			out<<sizedist[i]<<"\t";
		}
		
	
	
	/*for (int i = finalt+2; i< MAXSWEEPS/10; i++)
	{
		out<<setw(6)<<"t"<<"\t"<<setw(12)<<i<<"\t"<<setw(6)<<"NANT"<<"\t"<<setw(12)<<n<<"\t"<<endl;
	}*/
    out.close();
	sprintf(FileName,"layer_%d.dat",RANDOMSEED); //Number of ants vs z data
	cout<<FileName<<endl;
	// sprintf(FileName, "rand_1.dat");
    //find tesc_av 
    
    out.open(FileName);
	for(int i=0;i<alonglayer.size();i++)
	{
		for(int j=0;j<NG;j++)
		out<<alonglayer[i][j]<<"\t";
		
		out<<endl;
	}
	out.close();
}
