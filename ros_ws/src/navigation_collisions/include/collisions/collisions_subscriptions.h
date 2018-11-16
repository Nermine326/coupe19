#ifndef COLLISIONS_COLLISIONS_SUBSCRIPTIONS
#define COLLISIONS_COLLISIONS_SUBSCRIPTIONS

#include "collisions/robot.h"
#include "collisions/position.h"
#include "collisions/obstacles_stack.h"


#include <ai_game_manager/init_service.h>
#include <drivers_ard_asserv/RobotSpeed.h>
#include <navigation_navigator/Status.h>
#include <recognition_objects_classifier/ClassifiedObjects.h>
#include <ros/node_handle.h>
#include <ros/subscriber.h>
#include <tf2/buffer_core.h>
#include <tf2_ros/transform_listener.h>
#include <tf/transform_listener.h>

#include <memory>
#include <mutex>
#include <vector>

class CollisionsSubscriptions {
public:
    using RobotPtr = std::shared_ptr<Robot>;
    using ObstaclesStackPtr = std::shared_ptr<ObstaclesStack>;
    CollisionsSubscriptions(ros::NodeHandle& nhandle);
    
    void sendInit(bool success = true);
    
    RobotPtr createRobot(ros::NodeHandle& nhandle);
    ObstaclesStackPtr getObstaclesStack() const { return obstaclesStack_; }
    
    
    void updateRobot();
    
private:
    RobotPtr robot_;
    ObstaclesStackPtr obstaclesStack_;
    std::mutex mutexRobot_;
    
    tf2::BufferCore tf2PosBuffer_;
    tf2_ros::TransformListener tf2PosListener_;
    tf::TransformListener transformListener_;
    
    Robot::NavStatus navStatus_ = Robot::NavStatus::IDLE;
    std::vector<Position> robotPathWaypoints_;
    double velLinear_ = 0.0, velAngular_ = 0.0;
    
    ros::Subscriber navigatorStatusSubscriber_, objectsSubscriber_, asservSpeedSubscriber_;
    
    std::unique_ptr<StatusServices> gameStatus_;
    
    void onAsservSpeed(const drivers_ard_asserv::RobotSpeed::ConstPtr& speed);
    void onGameStatus(const ai_game_manager::GameStatus::ConstPtr& status);
    void onNavStatus(const navigation_navigator::Status::ConstPtr& status);
    void onObjects(const recognition_objects_classifier::ClassifiedObjects::ConstPtr& objects);
    Position updateRobotPos();
    
    /**
     * Retrieve the robot's name from the parameters
     * 
     * @param nodeHandle The node handle used by the node
     * @return The name of the robot
     */
    std::string fetchRobotName(ros::NodeHandle& nodeHandle);
};

#endif // COLLISIONS_COLLISIONS_SUBSCRIPTIONS