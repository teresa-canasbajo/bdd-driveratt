from functions.pl_surface_forTesting import *

# goal path
workingpath = '/media/whitney/New Volume/Teresa/bdd-driveratt/VP1/raw'
# test path
newtestpath = "/home/whitney/Teresa/demos/surfacetest2/SurfaceTest2"

pupil_video = '/home/whitney/recordings/2019_10_03/006'

# test path 4 from 10/8 recording at lab with good lighting
path1 = '/home/whitney/Teresa/demos/surfaceTestUpdatedTagsLab/014'
# test path from 10/15 recording at lab with eye & good lighting
path2 = '/home/whitney/Teresa/demos/surfaceTestLabEye/000'
# test path from 10/17 recording at lab with calibration
path3 = '/home/whitney/Teresa/demos/surfaceANDcalibration_3screens'


# tracker = map_surface(path2, loadCache=False, loadSurface=False)
tracker = map_surface(path3, loadSurface=False)

