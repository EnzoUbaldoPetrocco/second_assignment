#!/usr/bin/env python

import rospy
import random
import time
from my_second_assignment.srv import randomService, randomServiceResponse

possible_positions = [(-4,-3),(-4,2),(-4,7),(5,-7),(5,-3),(5,1)]

##function random simply generates a number between 0 and 5 values
def rndm():
	return (random.randrange(0, 100)%6)

##Let's define an handler which will generate the two random coordinates
def handleRandom(msg): 
	global possible_positions
	index = rndm()
	target=possible_positions[index]
	print("\n\nI'm handling the random target")
	print("\nthe index is: "+ str(index))
	print("\nthe target is: " + str(target))
	return randomServiceResponse(target[0], target[1])
	
##Let's define the main function
def randomMain():
	print("\nLet's serve! I'm executing the main server.py")
	rospy.init_node("server")
	s = rospy.Service("server" , randomService, handleRandom)
	rospy.spin()

if __name__ == "__main__":
	randomMain()

