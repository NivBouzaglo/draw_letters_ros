import rospy 
import math 
from turtle1.srv import drawer, drawerResponse
from turtlesim.srv import SetPen
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
import time 
from std_msgs.msg import String
from std_srvs.srv import Empty

# default positions 
x = 0 
y = 0 
theta = 0 
letter = ''
color = ''
publisher = ''
#theta = 0.0

#def callback(request):
#    return drawerResponse(request.x * request.y)

def callback(request):
    letter = request.letter
    color = request.color
    msg = " lacation " + str(request.x) +" " + str(request.y)+ " letter : "+ request.letter+ " color: "+request.color
    rate = rospy.Rate(10) # 10hz
    rospy.loginfo(msg)
    pub.publish(msg)

    set_pen = rospy.ServiceProxy('turtle1/set_pen', SetPen)
    change_pen_color(color)
    #color = get_RGB(request.color)
    #set_pen_func = set_pen(color[0], color[1], color[2], 2, 0 )
    #rospy.init_node("turtle_pose", anonymous=True)
    cmd_vel_topic = '/turtle1/cmd_vel'
    publisher = rospy.Publisher(cmd_vel_topic, Twist, queue_size=10)

    if letter == "I":
        return write_i(publisher)
    elif letter == "T":
        return write_t(publisher)
    else: 
        return write_l(publisher)


def write_l(publisher):
    msg = Twist()
    move_in_line(3, msg,  publisher)
    rotate("right", 180, msg, publisher)
    move_in_line(3, msg,  publisher)
    rotate("left", 90 ,msg,  publisher)
    move_in_line(3, msg,  publisher)
    return drawerResponse(" done ")

def write_t( publisher): 
    msg = Twist()
    rotate("right", 96 ,msg,  publisher)
    move_in_line(3, msg, publisher)
    rotate("right", 90 ,msg,  publisher)
    move_in_line(1.5, msg, publisher)
    rotate("right", 180, msg, publisher)
    move_in_line(3, msg,  publisher)
    return drawerResponse(" done ")

def write_i(publisher):
    msg = Twist()
    move_in_line(2, msg, publisher)
    rotate("right", 180, msg, publisher)
    move_in_line(3, msg,  publisher)
    rotate("right", 180, msg, publisher)
    move_in_line(1.5, msg, publisher)
    rotate("right", 90 ,msg,  publisher)
    move_in_line(3, msg, publisher)
    rotate("right", 90 ,msg,  publisher)
    move_in_line(1.5, msg, publisher)
    rotate("right", 180, msg, publisher)
    move_in_line(3, msg,  publisher)
    return drawerResponse('done ')

def rotate(direction, angle, msg , publisher ): 

    speed = 40 
    #angle = 90 
    PI = PI = 3.1415926535897
    angular_speed = speed*2*PI/360
    relative_angle = angle*2*PI/360

    #msg.angular.x = 0
    #msg.angular.y = 0 
    #msg.linear.x = 0 
    #msg.linear.y = 0
    #msg.linear.z = 0 

    msg.angular.z = abs(angular_speed) if direction == "right" else -abs(angular_speed)
    t0= rospy.Time.now().to_sec()
    current_angle = 0 

    while current_angle< relative_angle:
        publisher.publish(msg)
        t1 = rospy.Time().now().to_sec()
        current_angle = angular_speed * (t1 - t0)
    
    msg.angular.z = 0 
    publisher.publish(msg)
    #rospy.spin()
    return drawerResponse("done " )





def set_position(pose_request):
    global x, y, theta 
    x = pose_request.x
    y = pose_request.y
    theta = pose_request.theta
    #return  write_letter(1)
    return ''

def write_line(distance):
    msg = Twist()
    global x, y 
    current_x, current_y = x, y
    #msg.linear.x = abs(0.5)
    msg.linear.y = abs(0.5)
    dis = 0.0
    rate = rospy.Rate(10)
    cmd_vel_topic = '/turtle1/cmd_vel'
    publish_position = rospy.Publisher(cmd_vel_topic, Twist, queue_size=10)
    while True :
        rospy.loginfo("moving...")
        publish_position.publish(msg)
        rate.sleep()
        dis = dis + abs(0.5 * math.sqrt(((x - current_x) ** 2 ) + ((y- current_y) ** 2)))
        print (dis)
        if not( dis < distance ): 
            rospy.loginfo('reach ')
            break 
    #msg.linear.x = 0
    msg.linear.y = 0 
    publish_position.publish(msg)
    return drawerResponse("done " )


def move_in_line(len,msg, publisher ):
    speed = 8
    msg.linear.x = speed
    msg.linear.y = 0
    msg.linear.z = 0
    msg.angular.x = 0  
    msg.angular.y = 0  
    msg.angular.z = 0

    t0 = rospy.Time.now().to_sec()
    distance = 0
    while distance < len :
        #rospy.loginfo("moving...")
        publisher.publish(msg)
        t1 = rospy.Time.now().to_sec()
        distance = speed * (t1 - t0 )
    
    msg.linear.x= 0 
    publisher.publish(msg)



def change_pen_color(color):
    rospy.wait_for_service('/turtle1/set_pen')
    try: 
        set_pen = rospy.ServiceProxy('turtle1/set_pen', SetPen)
        if color == 'black': 
            set_pen(0, 0, 0 , 3, 0)
        else: 
            set_pen(255, 255, 0, 3, 0)
    except rospy.ServiceException: 
        pass 


def get_RGB(color): 
    if color == "black":
        return [0, 0, 0]
    elif color == "yellow": 
        return [255, 255, 0]

if __name__ == "__main__":
    
    rospy.init_node('draw_letters')
    pub = rospy.Publisher('received_requests', String, queue_size=18)

    service = rospy.Service("drawer",drawer, callback)
    rospy.spin()

