 #!/usr/bin/env python3
import rospy
import sys

import numpy as np
import random
import math
from enum import Enum
from turtlesim.srv import Spawn, Kill
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose 
from turtle1.srv import drawer, drawerResponse
from std_msgs.msg import String

import turtlesim.srv 
import std_srvs.srv
import sys


def talker(x, y, letter, color ):
    pub = rospy.Publisher('chatter', String, queue_size=10)
    req_str = " request: {} {} {} {}".format(x, y, letter, color)
    rospy.loginfo(req_str)
    pub.publish(req_str)



if __name__ == "__main__":
    try:
        if len(sys.argv)== 5 : 
            x = float(sys.argv[1])
            y = float(sys.argv[2])
            letter = sys.argv[3]
            color = sys.argv[4]
        else: 
            print("Please enter posiotion[x, y, angle], letter and color...") 
            exit(1)

        rospy.init_node('talker', anonymous=True)


        rospy.wait_for_service('/kill')
        kill = rospy.ServiceProxy('kill', Kill)
        kill('turtle1')

        rospy.wait_for_service('/spawn')
        spawn = rospy.ServiceProxy('spawn', Spawn)
        spawn(x, y, 0,'turtle1')

        rospy.wait_for_service('/drawer')
        draw_func = rospy.ServiceProxy('drawer', drawer)
        ans = draw_func(x, y, letter, color)

        talker(x, y, letter, color)
        
    except rospy.ROSInterruptException:
        rospy.loginfo("node terminated...")

