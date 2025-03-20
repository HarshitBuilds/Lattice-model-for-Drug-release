//ANT: cell.h Cell Class (Revision Date: Jan 15, 2017)
#ifndef _CELL_H
#define _CELL_H
#include "header.h"
class Cell
{
public:
    int row; //row index
    int col; //col. index
    vector<bool> isWall; //whether there is wall on left, right, up, down
    vector<int> nbrs; //cell indices of neighboring cells (left, right, up, down, -1 if none)
    bool isAnt; //if ant is present
    bool isBlock; //if all walls are blocked
    double perm; //fraction of walls
    void findperm()
    {
	perm=double(int(isWall[0])+int(isWall[1])+int(isWall[2])+int(isWall[3]))/4.0;
	//cout<<perm<<"\t";
    }
    Cell(){row=0; col=0; 
      //default is no wall
      isWall.push_back(false);
      isWall.push_back(false);
      isWall.push_back(false);
      isWall.push_back(false);
      isAnt=false;
      isBlock=false;
      perm=0.0;
    }
};
#endif
