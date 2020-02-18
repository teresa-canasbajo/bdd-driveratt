# -*- coding: utf-8 -*-

import numpy as np

# Pretty serious workaround. Ignores errors in imports :S
import builtins
from types import ModuleType
import logging

logger = logging.getLogger(__name__)


class DummyModule(ModuleType):
    def __getattr__(self, key):
        return None

    __all__ = []  # support wildcard imports


def tryimport(name, *args, **kwargs):
    try:
        imp = realimport(name, *args, **kwargs)
        # print('success: '+name)
        return imp
    except Exception as e:
        print('reached exception:' + name)
        if name == 'cPickle':  # because how they import cPickle/Pickle
            return realimport('pickle', *args, **kwargs)

            # print(e)
        return DummyModule(name)


realimport, builtins.__import__ = builtins.__import__, tryimport
try:

    from eye_tracking.analysis.lib.pupil_new.pupil_src.shared_modules.calibration_routines.finish_calibration import \
        finish_calibration, select_calibration_method

    from eye_tracking.analysis.lib.pupil_new.pupil_src.shared_modules.calibration_routines.gaze_mappers import *

    from eye_tracking.analysis.lib.pupil_new.pupil_src.shared_modules.gaze_producer.controller import *
    from eye_tracking.analysis.lib.pupil_new.pupil_src.shared_modules.gaze_producer.controller.calculate_all_controller import calculate_all

    from eye_tracking.analysis.lib.pupil_new.pupil_src.shared_modules.gaze_producer.gaze_from_offline_calibration import *


    #wrong, old version
    #from eye_tracking.analysis.lib.pupil.pupil_src.shared_modules.gaze_producers import calibrate_and_map

    import lib.pupil_new.pupil_src.shared_modules.player_methods


except Exception as e:
    print('-------------------')
    print(e)
    pass
tryimport, builtins.__import__ = builtins.__import__, realimport


# raise

class global_container():
    pass


def list_to_stream(gaze_list):
    import msgpack
    gaze_serialized = [msgpack.packb(gaze, use_bin_type=True) for gaze in gaze_list]
    return (gaze_serialized)


def notify_all(self, notification=''):
    logger.info(notification)


def gen_fakepool(folder, inp_gaze=[], calibration_mode='2d'):

    # defines default parameters for calibration data

    from eye_tracking.analysis.lib.pupil_new.pupil_src.shared_modules.plugin import Plugin_List

    fake_gpool = global_container()
    fake_gpool.capture = global_container()
    fake_gpool.capture.frame_size = (1280, 960)
    fake_gpool.window_size = (1280, 960)
    fake_gpool.min_calibration_confidence = 0.6
    fake_gpool.gaze_positions_by_frame = inp_gaze
    fake_gpool.app = 'not-capture'
    fake_gpool.user_dir = '/home/whitney/pupil_player_settings'
    fake_gpool.rec_dir = folder

    fake_gpool.detection_mapping_mode = calibration_mode
    fake_gpool.plugin_by_name = ''
    fake_gpool.plugins = Plugin_List(fake_gpool, [])

    fake_gpool.plugins.clean = lambda: None
    fake_gpool.active_calibration_plugin = global_container()

    fake_gpool.active_calibration_plugin.notify_all = notify_all
    fake_gpool.get_timestamp = lambda: None
    return fake_gpool


def pl_recalibV2(pupil_list, ref_list, inp_gaze, version='new', calibration_mode='2d', eyeID=None):  # eye could be 0 or 1
    #if calibration_mode == '3d':
        #from eye_tracking.analysis.lib.pupil.pupil_src.shared_modules.calibration_routines.optimization_calibration import \
         #   bundle_adjust_calibration  # we magically need this for libceres to work

    # from calibration_routines.gaze_mappers import Binocular_Vector_Gaze_Mapper
    # from calibration_routines.gaze_mappers import Monocular_Gaze_Mapper
    # from calibration_routines.gaze_mappers import Vector_Gaze_Mapper
    import copy
    import sys

    pupil = copy.copy(pupil_list)
    ref = copy.copy(ref_list)
    gaze = copy.copy(inp_gaze)


    #from pupil_new.pupil_src.shared_modules.gaze_producer import gaze_from_offline_calibration

    #offline_calib = gaze_from_offline_calibration.GazeFromOfflineCalibration(gaze)

    # to check pupil labs version
    # there seems to be some problem here
    #if hasattr(lib.pupil.pupil_src.shared_modules.player_methods, 'Bisector'):
        # pupillab v1.8 or newer needs the data serialized
    #if version == 'new':
      #  pupil = list_to_stream(pupil)
       # gaze = list_to_stream(gaze)

    if eyeID is not None:  # remove everthing nonspecified
        pupil = [p for p in pupil if p['id'] == eyeID]

    fake_gpool = gen_fakepool(gaze, calibration_mode) # gets default parameters for calibration data

    #logger.info(finish_calibration)
    #calib_generator = finish_calibration(fake_gpool, pupil, ref)
    #is there a reason why gpool_user directory is in home/whitney/pupil_player_settings/user_calibration_data?
    #in finish_calibration, it's stopping after the save function - nothing seems to be getting saved, but why?
    #maybe this is all that's needed once it gets past saving?

    #GazeFromOfflineCalibration(fake_gpool)._setup_controllers()

    #CalibrationController().calculate(finish_calibration(fake_gpool, pupil, ref))

    #calib_generator = Binocular_Gaze_Mapper_Base(g_pool=fake_gpool).map_batch(pupil)
    #results.extend for loop - results not updating, breaking in datum?
    #perhaps, this is the wrong function - too deep, instead look 1 above in gaze producers

    #the following is from gaze_producers
    logger.info(calculate_all)
    calib_generator = calculate_all()

    #calib_generator = Binocular_Gaze_Mapper(g_pool=fake_gpool, params=gaze)._map_binocular()
    #doesn't even go into calibrate.make_map_function

    # maybe gaze_mappers class for second half of calibrate_and_map?
    # method, result = select_calibration_method(fake_gpool, pupil_list, ref_list)
    #logger.info(calibrate_and_map)
    ###calib_generator = calibrate_and_map(fake_gpool, ref, pupil, gaze, 0, 0)  # here the actual calibration is done
    # calibrate_and_map should work correctly, but check in future if errors.
    tmp = next(calib_generator)  # start once
    output = []
    try:
        i = 0
        while True:
            i += 1
            newsamp = next(calib_generator)
            if newsamp[0] == 'Mapping complete.':
                logger.info('Mapping complete')
                break
            if i % 100000 == 1:
                logger.info(newsamp[0])
            try:
                output.append(newsamp[1][0])
            except Exception as e:
                print(newsamp)
    except StopIteration:
        logger.error('error')
        pass
    calib_generator.close()
    return output

