//ANT: ant.h Ant Class (Revision Date: Jan 15, 2017)
#ifndef _ANTCLUSTER_H
#define _ANTCLUSTER_H
#include "header.h"
#include "coordinate.h"
class AntCluster
{
public:
    list<int> cells; //cell indices of ants in the cluster
    list<Coordinate> initialCoordinates, newCoordinates;
};
#endif
