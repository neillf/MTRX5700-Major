## MTRX5700
# Xue Yin Zhang
#
# Get some navigation while starting up and calibrating and doing a move

## clean startup sequence
import time, sys
import ps_drone         # Import PS-Drone-API
import pickle

## create empty lists where we store the navdata
pitch = []
roll = []
yaw = []
demo_alt = []
vx = []
vy = []
vz = []
nav_time = []
mx = []
my = []
mz = []
altitude_ref = []
detect_n = []
detect_type = []
detect_dist = []
detect_rot = []

## store all the navdata
def append_nav(drone):
    pitch.append(drone.NavData["demo"][2][0])   # theta
    roll.append(drone.NavData["demo"][2][1])    # phi
    yaw.append(drone.NavData["demo"][2][2])     # psi
    demo_alt.append(drone.NavData["demo"][3])   # altitude in
    vx.append(drone.NavData["demo"][4][0])      # velocity in x-direction
    vy.append(drone.NavData["demo"][4][1])      # velocity in y-direction
    vz.append(drone.NavData["demo"][4][2])
    nav_time.append(drone.NavData["time"][0])
    mx.append(drone.NavData["magneto"][0][0])
    my.append(drone.NavData["magneto"][0][1])
    mz.append(drone.NavData["magneto"][0][2])
    altitude_ref.append(drone.NavData["altitude"][3])   # altitude in mm
    detect_n.append(drone.NavData["vision_detect"][0])      # number of markers detected
    if detect_n[-1] > 0:
        print "detected tag"
    detect_type.append(drone.NavData["vision_detect"][1])   # types of detected markers
    detect_x.append(drone.NavData["vision_detect"][2])
    detect_y.append(drone.NavData["vision_detect"][3])
    detect_width.append(drone.NavData["vision_detect"][4])
    detect_depth.append(drone.NavData["vision_detect"][5])
    detect_dist.append(drone.NavData["vision_detect"][6])
    detect_ang.append(drone.NavData["vision_detect"][7])
    detect_rot.append(drone.NavData["vision_detect"][9])
    return

## receive navdata packet
def wait_nav(drone, time_s):
    NDC = drone.NavDataCount
    start = time.time()
    while (time.time() - start) < time_s:
        while drone.NavDataCount == NDC:  time.sleep(0.001)                       # Wait until next time-unit
        NDC = drone.NavDataCount
        append_nav(drone)
    return

def save_nav():
    with open('navdata-vars.pickle', 'w') as f:  # Python 3: open(..., 'wb')
        pickle.dump([pitch, roll, yaw, demo_alt, vx, vy, vz, nav_time, mx, my, mz, pwm_fl, pwm_fr, pwm_br, pwm_bl, detect_n, detect_type, detect_x, detect_y, detect_width, detect_depth, detect_dist, detect_ang, detect_rot, checksum], f)
