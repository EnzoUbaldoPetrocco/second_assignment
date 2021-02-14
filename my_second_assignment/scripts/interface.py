#!/usr/bin/env python

import rospy
import time
from std_srvs.srv import *
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Point
from move_base_msgs.msg import MoveBaseActionGoal
from geometry_msgs.msg import Twist
from my_second_assignment.srv import randomService, randomServiceResponse


## The aim of this script is to get user commands.

## 1)move randomly in the environment, by choosing 1 out of 6 possible
## target positions:
## [(-4,-3);(-4,2);(-4,7);(5,-7);(5,-3);(5,1)]

## 2) directly ask the user for the next target position (checking that
## the position is one of the possible six) and reach it

## 3) start following the external walls

## 4) stop in the last position

## 5) (optional) change the planning algorithm to dijkstra (move_base) to the bug0

##Global variables, like the positions
possible_positions = [(-4,-3),(-4,2),(-4,7),(5,-7),(5,-3),(5,1)]
srv_wall_follow = None
pub_move_base = None
pub_twist = None
client= None
actual_x = None
actual_y = None


##This function publish the desired position
##to 'move_base/goal' topic
def go_to(x, y):
	global pub_move_base
	move_goal = MoveBaseActionGoal()
	move_goal.goal.target_pose.header.frame_id= "map"
	move_goal.goal.target_pose.pose.orientation.w=1
	move_goal.goal.target_pose.pose.position.x=x
	move_goal.goal.target_pose.pose.position.y=y
	pub_move_base.publish(move_goal)

	
##A random destination is chosen among the possible
def random_destination():
	global client
	global srv_wall_follow
	srv_wall_follow(False)
	response = client()
        x=response.x
        y=response.y
	print("\nLet's reach the position: (" + str(x) + "," + str(y) + ")")
	go_to(x, y)
	


##This function ask to the user the destination among
##a list of possible targets
def ask_user_destination():
	global possible_positions, srv_wall_follow
	srv_wall_follow(False)
	try:
		user_command= int(raw_input("\n\nPress the respectively number for the destination: \n1) (-4,-3) \n2) (-4,2) \n3) (-4,7) \n3) (5,-7)  \n4) (5,-3) \n5) (5,1)\n"))
		print(str(user_command))
		target=possible_positions[user_command -1]
		print(str(target) + " This is the target you asked for: ")
		go_to(target[0], target[1])
	except Exception as e:
		print("\nInvalid command!\n")
		
	

##This function command the robot to follow the walls
def follow_walls():
	global srv_wall_follow
	srv_wall_follow(True)
	print("\nfollow walls")


	
##This function command the robot to stop
##First it publish a 2D Twist equal to zero
##Then it sets the actual position as the next target
def stop():
	global pub_twist, actual_x, actual_y
	
	twist= Twist()
	twist.linear.x=0
	twist.linear.y=0
	twist.angular.z=0
	pub_twist.publish(twist)
	
	srv_wall_follow(False)
	print("\nLet's stay in the position: (" + str(actual_x) + "," + str(actual_y) + ")")
	go_to(actual_x, actual_y)
	print("\nstop")



##Every time the '/odom' publish the position this function
## put them in global variables
def positionCallback(msg):
	global actual_x, actual_y
	actual_x = msg.pose.pose.position.x
	actual_y = msg.pose.pose.position.y
	



##Let's define the main function: initialization and infinite loop
def main():
	
	rospy.init_node("interface")
	global srv_wall_follow, pub_move_base, pub_twist, client, srv_pos
	client = rospy.ServiceProxy('/server', randomService)
	pub_twist= rospy.Publisher('/cmd_vel', Twist, queue_size=1)
	srv_wall_follow= rospy.ServiceProxy( 'wall_follower_switch', SetBool)
	pub_move_base= rospy.Publisher('move_base/goal', MoveBaseActionGoal, queue_size=1)
	srv_pos= rospy.Subscriber('/odom',Odometry,positionCallback)
	rospy.sleep(5)
	while not rospy.is_shutdown():
		print("\n\nHello, this is the user interface. Here you can choose some actions to send to the robot.\nThe functions are the following: " +
		"\n1) move randomly in the environment, by choosing 1 out of 6 possible target positions: \n[(-4,-3);(-4,2);(-4,7);(5,-7);(5,-3);(5,1)];" +
		"\n2) directly ask the user for the next target position (checking that the position is one of the possible six) and reach it;" +
		"\n3) start following the external walls" +
		"\n4) stop in the last position")
		try:
			command= int(raw_input("choose a number to choose the command: "))
		except Exception as e:
			print("\nInvalid command!\n")
			continue
		if command == 1:
			random_destination()
		elif command == 2:
			ask_user_destination()
		elif command == 3:
			follow_walls()
		elif command == 4:
			stop()
		
		else:
			print("wrong button, would you like to exit?")
		

if __name__ == "__main__":
	main()






