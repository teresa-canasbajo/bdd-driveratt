from functions.pl_surface_forTesting import *

# goal path
workingpath = '/media/whitney/New Volume/Teresa/bdd-driveratt/VP1/raw'
# test path
newtestpath = "/home/whitney/Teresa/demos/surfacetest2/SurfaceTest2"

pupil_video = '/home/whitney/recordings/2019_10_03/006'

# test path from 10/17 recording at lab with calibration
path3 = '/home/whitney/Teresa/demos/old/surfaceANDcalibration_3screens'
# test path from 10/25 recording
path = '/home/whitney/Teresa/demos/3screens_1025'
# test path from 10/31 recording with reflective markers
path2 = '/home/whitney/Teresa/demos/001 - 1.6 pupil capture'
# test path from 11/4 recording
path4 = '/home/whitney/Teresa/demos/2019_11_04/000'

tracker = map_surface(path4, loadSurface=False)

print('done')

