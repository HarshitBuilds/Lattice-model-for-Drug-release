//AntCode: system.h System Class (Revision Date: February 12, 2017)
//From the splitlattice folder
#ifndef _SYSTEM_H
#define _SYSTEM_H
#include "header.h"
#include "cell.h"
#include "antcluster.h"
#include "coordinate.h"
#include <boost/filesystem.hpp>
using namespace std;

class System
{
  public:
    int RANDOMSEED, MAXSWEEPS,NG,NG2,NANT,NWALL,NWALL1,NWALL2, NSAMPLE, NG_new,x, tau_val; //split into 2 lattices.
    double WALLF1, WALLF2, PWALL, ANTF, PJUMP; //ANTF for the lower lattice.
    // 1 for lower lattice
    int NANT1 = 0;
    int NANT2 = 0;
/* NUMERICAL SETTINGS (INPUT)
 * int RANDOMSEED=seed for random number generator
 * int MAXSWEEPS=maximum number of MC sweeps (every sweep meaning trial movement of all ants
 * int NSAMPLE=sampling frequency in number of MC sweeps
 * 
 * MODEL PARAMETERS (INPUT)
 * double WALLF=fraction of walls (#wall/total possible walls)
 * double PWALL=probability of crossing wall (0 for completely block, 1 if completely free)
 * dount ANTF=fraction of ants in the first lattice (#ants/#cells)
 * int NG=number of cells in each direction
 * 
 * MODEL PARAMETERS (DERIVED)
 * int NG2=total #cells=round off NG*NG
 * int NWALL=total #wall=round off WALLF*(NG+1)*(NG+1)
 * int NANT=total #ant=round off ANTF*NG2
 */
     
    void ReadInput(int argc, char *argv[])
    {
        options_description desc("Usage:\nANT <options>");
        desc.add_options()
        ("help,h", "print usage message")
        ("MAXSWEEPS,s", value<int>(&MAXSWEEPS)->default_value(10), "max. no. of MC sweeps (default 100)")
	    ("RANDOMSEED,r", value<int>(&RANDOMSEED)->default_value(1), "seed for random number generator (default 1)")
	    ("NSAMPLE,S", value<int>(&NSAMPLE)->default_value(100), "sampling frequency in #MC sweeps (default 100)")
        ("WALLF1, 1", value<double>(&WALLF1)->default_value(0.0), "fraction of walls (default 0.5)")
        ("WALLF2, 2", value<double>(&WALLF2)->default_value(0.0), "fraction of walls (default 0.5)")
        // ("x,x", value<int>(&x)->default_value(5))
	    ("PWALL,p", value<double>(&PWALL)->default_value(0.0), "probability of crossing wall (0 for completely block, 1 if completely free) (default 0.0)")
        ("ANTF,a", value<double>(&ANTF)->default_value(0.01), "fraction of ants (default 0.5)")
        /*("ANTF2,a", value<double>(&ANTF2)->default_value(0.0), "fraction of ants (default 0.0)")*/
        ("NG,n", value<int>(&NG)->default_value(10), "#cells in each direction (default 10) ")
        ("x,x", value<int>(&x)->default_value(5), "lattice split factor (default 0.2*NG)")
        ("PJUMP,pj", value<double>(&PJUMP)->default_value(0.5), "probability of movement from top to bottom (default 0.5)")
        ("tau_val,tau_val", value<int>(&tau_val)->default_value(5), "tau value for calculating mean square displacement");
        variables_map vm;
        store(parse_command_line(argc, argv, desc), vm);
        notify(vm);

        if (vm.count("help"))
        {
          cout << desc << "\n";
          exit(1);
        }
        
        //Calculate other parameters
        NG2=NG*NG;
        // x = NG*(0.2); //directly from command line
        NG_new = NG * x; //Number of cells in the first lattice 
        
	  //NANT =int(round(ANTF*double(NG_new))); //for all ants in first half of the matrix
    NANT = int(round(ANTF*double(NG2))); //total number of ants in the matrix
    // NANT = 10;
    NWALL1 = int(round(WALLF1 * double(NG * x + (x + 1) * NG))); //number of walls in first lattice.
    NWALL2 = int(round(WALLF2 * double((NG - x) * NG + (NG - x) * NG))); //number of walls in second lattice.
    NWALL = NWALL1 + NWALL2;
	  cout<<"Input Read\n"<<NG2<<" cells, "<<NWALL1<<" walls in (lower lattice), "<<NWALL2<<" walls in (upper lattice), " << NANT << " ants \n"<< endl;
    
    }
    
    
    list<AntCluster> AC;   //list of ant clusters, in the beginning all ants are an independent cluster
    void CreateAnts(); 
    void CreateAntClusters(); //for blind ant case
    
    vector<int> tesc;  //escape time vector.
    vector<int> tesc1;
    vector<int> tesc2;
    vector<int> tent1;
    vector<int> tent2;
    vector<int> sizedist; //to store # of cluster of each size
    vector<double> msd; //for storing msd for every steps followed by averaging
    int *walls1; //for first lattice 
    int *walls2; //for second lattice
    void CreateWalls();
    double mean_r_square; //overall mean square displacement for particular tau value
    vector<Cell> C; //vector of cells
    void CreateCells();
    
    vector<vector<int>> W; // the sliding window to store indices of 2*tau timesteps at a given time
    void Move();
    void writeGNU(int);

    void writeOutput();
};
#endif
