import rospy
from sensor_msgs.msg import MultiEchoLaserScan
from std_msgs.msg import String
import numpy as np

class station(object):
        def __init__(self, name):
	    rospy.init_node('UTM30LXEW', anonymous=True)
            self.tic = 0
	    self.toc = 0
	    self.acum = 0
	    self.acum2 = 0
	    self.new = 0
	    self.last = 1
	    self.total = 20
	    self.d = np.zeros(self.total+1)
	    self.ang = np.zeros(self.total+1)
	    self.main_station()

        def main_station(self):
            rospy.Subscriber('/echoes', MultiEchoLaserScan, self.callback)
            rospy.spin()

        def callback(self,data):
	    self.tic = rospy.get_time()
	    delta_hor_angle = data.angle_increment
	    max_hor_angle =   data.angle_max
	    min_hor_angle =   data.angle_min
	    ranges =          data.ranges
	    N = len(ranges)
	    theta = np.linspace(min_hor_angle,max_hor_angle,N)
	    D0 = N//2 + 1
	    # # Lacer Split
	    ranges_0 = np.zeros(9)
	    angles_0 = np.zeros(9)
	    N0 = D0-4
	    for k in range(0,9):
		aux = str(ranges[N0+k]).split("[")
		aux = aux[1].split(",")
		aux = aux[0].strip("]")
#		print ranges[N0+k]
		ranges_0[k] = float(aux)
	    n = len(ranges_0)
	    # # Distance mesurement
	    self.d[self.new] = (ranges_0[n//2]+ranges_0[n//2+1]+ranges_0[n//2+2])/3.0
	    # # # Moving average filter
	    self.acum += self.d[self.new]
	    self.acum -= self.d[self.last]
	    avg = self.acum/self.total
	    # # Relation angle mesurement
	    self.ang[self.new] = (ranges_0[8]*ranges_0[2])/(ranges_0[0]*ranges_0[6])
	    # # # Moving average filter
	    self.acum2 += self.ang[self.new]
	    self.acum2 -= self.ang[self.last]
	    angle = self.acum2/self.total
	    # # Increment
	    self.new += 1
	    self.last += 1
	    if  self.new == self.total+1:
		self.new = 0
	    if self.last == self.total+1:
		self.last = 0
	    self.toc=rospy.get_time()
	    # rospy.loginfo("Time: "+str(self.toc-self.tic))
	    pub=rospy.Publisher('Distance_Angle',String,queue_size=1)
	    pub.publish("Distance: "+str(avg)+"\nAngle relationship: "+str(angle)+"\nTime Delay: "+str(self.toc-self.tic))
	    print "d: "+str(avg)+",\tAng: "+str(angle)

if __name__ == '__main__':
    hokuyo   = station('Station')
