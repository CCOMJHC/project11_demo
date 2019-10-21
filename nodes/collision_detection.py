#!/usr/bin/env python
import rospy

from marine_msgs.msg import Contact
from geographic_visualization_msgs.msg import GeoVizItem
from geographic_visualization_msgs.msg import GeoVizPointList
from geographic_msgs.msg import GeoPoint
from geographic_msgs.msg import GeoPointStamped
from std_msgs.msg import ColorRGBA
import project11
import math

angles = []

for angle in range(0,360,45):
    angles.append(math.radians(angle))

joy_leds = (angles[6:8]+angles[0:1],angles[0:3],angles[4:7],angles[2:5])

def contactCallback(data):
    if data.callsign.startswith('/joy'):
        joy_id = int(data.callsign[-1])
        point_list = GeoVizPointList()
        lat_rad = math.radians(data.position.latitude)
        lon_rad = math.radians(data.position.longitude)
        for a in angles:
            p = project11.geodesic.direct(lon_rad,lat_rad,a,10)
            point_list.points.append(GeoPoint(math.degrees(p[1]),math.degrees(p[0]),0.0))
        point_list.points.append(point_list.points[0])
        point_list.size = 2
        point_list.color = ColorRGBA(.5,.5,.5,.75)
        viz_item = GeoVizItem()
        viz_item.id = data.callsign
        viz_item.lines.append(point_list)
        
        led_point_list = GeoVizPointList()
        for a in joy_leds[joy_id]:
            p = project11.geodesic.direct(lon_rad,lat_rad,a,11)
            led_point_list.points.append(GeoPoint(math.degrees(p[1]),math.degrees(p[0]),0.0))
        led_point_list.size = 3
        led_point_list.color = ColorRGBA(0,1,0,1)
        viz_item.lines.append(led_point_list)
        
        display_pub.publish(viz_item)
            
def positionCallback(data):
    #print 'asv:',data
    pass
        



rospy.init_node('collision_detection')
display_pub = rospy.Publisher('/udp/project11/display',GeoVizItem,queue_size = 10)
rospy.Subscriber('/contact', Contact, contactCallback)
rospy.Subscriber('/position', GeoPointStamped, positionCallback)
rospy.spin()
