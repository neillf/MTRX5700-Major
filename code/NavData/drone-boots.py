## MTRX5700
# Xue Yin Zhang
#
# Get some navigation while starting up and calibrating and doing a move

## clean startup sequence
import time, sys
import ps_drone         # Import PS-Drone-API
import pickle           # python library to save and restore variables
import boots

## clean start up
drone = ps_drone.Drone()                                                      # Start using drone
drone.startup()                                                               # Connects to drone and starts subprocesses
drone.reset()                                                                 # Sets drone's status to good (LEDs turn green when red)
while (drone.getBattery()[0] == -1):  time.sleep(0.1)                         # Wait until the drone has done its reset

## make sure drone has enough battery
if drone.getBattery()[0] < 30:
    print "battery too low"
    drone.land()        # land for safety (even though it's not in the air atm)
    quit()              # end program

## print out battery status
print "Battery: "+str(drone.getBattery()[0])+"%  "+str(drone.getBattery()[1]) # Gives a battery-status

## set mode of data packages
drone.useDemoMode(False)
drone.getNDpackage(["demo", "time", "altitude", "magneto", "vision_detect"])         # Packets, which shall be decoded
time.sleep(1.5)

## set maximum altitude
CDC = drone.ConfigDataCount
drone.setConfig("control:altitude_max","3500")                      # Request change of an option
drone.setConfig("control:control_yaw","6.11")
while CDC == drone.ConfigDataCount:     time.sleep(0.001)           # Wait until configuration has been set (after resync is done)
for i in drone.ConfigData:
    if i[0] == "control:altitude_max":	print "   "+str(i)+"   Count: "+str(drone.ConfigDataCount)+"   Timestamp: "+str(drone.ConfigDataTimeStamp)
for i in drone.ConfigData:
    if i[0] == "control:control_yaw":	print "   "+str(i)+"   Count: "+str(drone.ConfigDataCount)+"   Timestamp: "+str(drone.ConfigDataTimeStamp)

## set up vision detection
# Shell-Tag=1, Roundel=2, Black Roundel=4, Stripe=8, Cap=16, Shell-Tag V2=32, Tower Side=64, Oriented Roundel=128
drone.setConfig("detect:detect_type","5")
drone.setConfig("detect:detections_select_v", "128")   # oriented roundel with ground camera
CDC = drone.ConfigDataCount
while CDC == drone.ConfigDataCount:    time.sleep(0.01)        # Wait until configuration has been set

time.sleep(1.0)         # Give it some time to awake fully

drone.trim()                # Recalibrate sensors
drone.getSelfRotation(5)    # Auto-alteration-value of gyroscope-sensor
print "Auto-alternation: " + str(drone.selfRotation) + "deg/sec"

## main program

# check what data packages are being sent/received
if drone.State[10] == 0:
    print "Navdata: all"
else:
    print "Navdata: demo. dumb drone"
    drone.useDemoMode(False)
    time.sleep(2.0)

drone.takeoff()
print "Takeoff"
boots.wait_nav(drone, 7.0)

while drone.NavData["demo"][0][2]: time.sleep(0.1)  # still in landed mode?
drone.mtrim()
print "mtrim"
boots.wait_nav(drone, 3.0)

drone.moveUp(0.5)
print "move up"
boots.wait_nav(drone, 1.0)

drone.moveForward(0.10)
print "move forward"
boots.wait_nav(drone, 30.0)
#
#drone.anim(0,1000)
#print "anim 0"
#boots.wait_nav(drone, 0.5)
#
#drone.anim(1,1000)
#print "anim 1"
#boots.wait_nav(drone, 0.5)
#
#drone.anim(2,1000)
#print "anim 2"
#boots.wait_nav(drone, 0.5)
#
#drone.anim(3,1000)
#print "anim 3"
#boots.wait_nav(drone, 0.5)
#
#drone.moveDown(1)
#print "move down"
#boots.wait_nav(drone, 3)

drone.stop()
print "stop"
boots.wait_nav(drone, 0.45)

drone.land()
print "land"
boots.wait_nav(drone, 2.0)

boots.save_nav()
