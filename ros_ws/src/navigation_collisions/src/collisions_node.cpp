#include "collisions/collisions_node_class.h"

#include <ros/ros.h>

#include <iostream>

// A commenter
#define DEBUG = 1

using namespace std;

int main(int argc, char *argv[]){
    ros::init(argc, argv, "collisions");
    CollisionsNode mainNode;
    
    ros::spin();
    
    return 0;
}
