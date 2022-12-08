#!/usr/bin/env python3
import rospy
from std_msgs.msg import String
from turtle1.srv import printer

history = [] 


def callback(data):
    #rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
    history.append(data.data)
    #print("data. data : %s" %data.data)


def printer_callback(request):
    ans = "      ".join(history)
    return ans


def listener():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("received_requests", String, callback)
    s = rospy.Service('/printer', printer, printer_callback)
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()


if __name__ == '__main__':
    listener()
 
