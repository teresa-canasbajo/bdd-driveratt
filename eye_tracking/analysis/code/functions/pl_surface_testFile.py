from functions.pl_surface_forTesting import *
from functions.et_preprocess import *


def test():
    # datapath = '/media/whitney/New Volume/Teresa/bdd-driveratt'
    # data = preprocess_et(subject='VP1', datapath=datapath, save=True,
    #                      eventfunctions=(make_blinks, make_saccades, make_fixations))
    # print(data)
    t1 = map_surface("/home/whitney/Teresa/SurfaceTest/worldFolder")
    return t1
