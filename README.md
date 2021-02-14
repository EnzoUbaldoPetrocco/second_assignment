
# The first assignment

## Introduction
	
This project is a ROS package for controlling a robot in a simulation where the robot doesn't know a priori the map.
This project involves only the coding regarding to the user interface.
The planning algorithm is dijkstra (move_base) and gmapping for localizing.

## Computational graph







## Installation

Before running this ros package some installation are needed.
Before all install ROS and python.

Then it must be installed  with the command:

```bash
sudo apt-get install ros-<your_ros_distro>-navigation
```

Then, move the terminal to your working space and then to src folder and proceed with the next steps:

```bash
git clone https://github.com/CarmineD8/robot_description
```

```bash
git clone https://github.com/CarmineD8/slam_gmapping
```

```bash
git clone https://github.com/CarmineD8/final_assignment
```

IMPORTANT: check your ROS version. With melodic ros versione you'll need to switch branch to 'noetic'; this can ben done through the next bash command, in EVERY folders generated from the three previous clone commands:

```bash
git checkout noetic
```

## How to run it

Now, let's follow these simple step which will let the user to launch the program:

Open the first terminal

```bash
roscore &
```

```bash
catkin_make
```

```bash
roslaunch final_assignment simulation_gmapping.launch
```

Don't close this terminal and open the second one

```bash
roslaunch my_second_assignment server.launch
```

## Behavior implemented

The robot spawn in a specific point of the map in Rviz and Gazebo simulations.
Both have the same map, but in Gazebo we can see the entire map, because this is the simulation from the point of view of an external agent; while in Rviz we can see part of the map, since the scan reveals the map exploring the map.

The robot moves around following the instruction given by the user, it can:
-Go to a target selected randomly among a list of targets
-Go to a target selected from the user among a list of targets 
-Follow the walls
-Stop

The list of possible target is: (-4,-3);(-4,2);(-4,7);(5,-7);(5,-3);(5,1)

The behavior can be observed in Rviz or Gazebo environment.

## Architectural structure

This project involves the creation of two nodes within a package.
The nodes are written in python and comunicate each other through 'randomService.srv' message described in srv folder.
'randomService.srv' response contains the two coordinates, selected 

Both nodes are contained inside scripts folder.
- '/interface' controls the robot behavior through a list of command given that the user has to select. 
It subscribes to '/odom' to get the actual position of the robot, ha a publisher to '/cmd_vel' to publish stop the robot, subscribes to the service '/Server' to get the random target, a publisher to 'move_base/goal' to reach the position and  it subscribes to 'wall_follower_switch' service if it has to follow the walls.
This node enters in an infinite loop (the node can go out only if the program is shutdown) when the user ask for a command, the program goes to a specific function.

- '/Server' receive the request for a new target and sends the random target among a list of given target.
(More information in docs folder)


## Considerations

First of all, the optional task of the assignment: 'switch from bug0 to dijkstra and vice versa' is not implemented. 
Another limitation is that the algorithms are optimal for a 'finite' map, in an open environment the target could have difficulties.
The algorithm could detect that it is convenient to turn right, instead of turning left when on left there is a wall; in fact up to now the robot, even it has a wall on left i turn on left until it reaches a wall, then it goes back and then trying again to turn left.
Another improvement should be creating a node for every command, such that every node can communicate through topic. It is preferrable, in case of improvements of a specific task or many of them, to divide into files rather then having a unique giant and complex file.
















