#!/usr/bin/env python3
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
import math
# cd jackal_ws; source devel/setup.bash ; python3 src/nav-competition-icra2022/run.py --gui --world_idx 11

flag = 0

def remapCallback(msg):
    pub2 = rospy.Publisher('/cmd_vel', Twist, queue_size = 10)
    pub2.publish(msg)

def callback(msg):
    #print(msg.ranges[0],msg.ranges[360],msg.ranges[719] ) #len is 2019 from 0-360
    vel = Twist()
    global flag
    if math.isinf(msg.ranges[0]) and math.isinf(msg.ranges[360]) and math.isinf(msg.ranges[719]):
        flag = 1 
    
    if flag ==1:
        remapSub = rospy.Subscriber('/alternate_cmd_vel', Twist, remapCallback)
    
    
    else:
        if sum(msg.ranges[150:250])/100 < 1:
            vel.linear.x = 0.5
            vel.angular.z = 0.3
            pub.publish(vel)
        elif sum(msg.ranges[250:320])/70 < 1.5:
            vel.linear.x = 0.2
            vel.angular.z = 0.4
            pub.publish(vel)
        elif sum(msg.ranges[320:340])/60 < 1.5:
            vel.angular.z = 0.5
            pub.publish(vel)
        elif sum(msg.ranges[340:380])/40 < 1.5:
            vel.angular.z = 0.6
            pub.publish(vel)
        elif sum(msg.ranges[380:440])/60 < 1.5:
            vel.angular.z = -0.5
            pub.publish(vel)
        elif sum(msg.ranges[440:510])/70 < 1.5:
            vel.linear.x = 0.2
            vel.angular.z = -0.4
            pub.publish(vel)
        elif sum(msg.ranges[510:610])/100 < 1:
            vel.linear.x = 0.5
            vel.angular.z = -0.3
            pub.publish(vel)
        else:
            vel.linear.x = 0.5
            pub.publish(vel)
    
    


if __name__ == "__main__":
    rospy.init_node('test', anonymous=False)
    
    msg = Twist()
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    
    rate = rospy.Rate(10) 

    while not rospy.is_shutdown():
        sub = rospy.Subscriber('/front/scan', LaserScan, callback)
        rate.sleep()

    #rospy.spin()