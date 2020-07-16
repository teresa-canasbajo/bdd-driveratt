import os
import numpy as np
import logging
from eye_tracking.lib.pupil.pupil_src.shared_modules.camera_models import load_intrinsics

class global_container():
    pass

def notify_all(self, notification=''):
    # get a logger
    logger = logging.getLogger(__name__)
    logger.info(notification)

def gen_fakepool(inp_gaze=[], surface_dir = '', calibration_mode='2d'):
    from eye_tracking.lib.pupil.pupil_src.shared_modules.plugin import Plugin_List

    fake_gpool = global_container()
    fake_gpool.capture = global_container()
    fake_gpool.capture.frame_size = (1280, 960)
    fake_gpool.window_size = (1280, 960)
    fake_gpool.min_calibration_confidence = 0.6
    fake_gpool.gaze_positions_by_frame = inp_gaze
    fake_gpool.app = 'not-capture'
    #user_dir seems problematic aka not found later on
    # fake_gpool.user_dir = '/work'
    # fake_gpool.rec_dir = '/work'
    surface_dir = os.path.join(surface_dir, 'work')
    if not os.path.exists(surface_dir):
        os.mkdir(surface_dir)
    fake_gpool.user_dir = surface_dir
    fake_gpool.rec_dir = surface_dir

    # fake_gpool.detection_mapping_mode = calibration_mode
    fake_gpool.plugin_by_name = ''
    fake_gpool.plugins = Plugin_List(fake_gpool, [])

    fake_gpool.plugins.clean = lambda: None
    fake_gpool.active_calibration_plugin = global_container()

    fake_gpool.active_calibration_plugin.notify_all = notify_all
    fake_gpool.get_timestamp = lambda: None
    return (fake_gpool)

def fake_gpool_surface(folder=None):
    if not folder:
        raise ('we need the folder else we cannot load timestamps and surfaces etc.')
    surface_dir = os.path.join(folder, 'surface')
    if not os.path.exists(surface_dir):
        os.makedirs(surface_dir)

    fake_gpool = gen_fakepool(folder)
    fake_gpool.surfaces = []
    fake_gpool.rec_dir = surface_dir
    fake_gpool.timestamps = np.load(os.path.join(folder, 'world_timestamps.npy'))
    fake_gpool.capture.timestamps = np.load(os.path.join(folder, 'world_timestamps.npy'))
    fake_gpool.capture.source_path = os.path.join(folder, 'world.mp4')
    fake_gpool.capture.intrinsics = load_intrinsics('', 'Pupil Cam1 ID2', (1280, 720))
    fake_gpool.seek_control = global_container()
    fake_gpool.seek_control.trim_left = 0
    fake_gpool.seek_control.trim_right = 0
    fake_gpool.timeline = global_container()
    return fake_gpool
