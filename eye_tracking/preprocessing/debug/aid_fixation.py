import os

def get_frames(folder):
    from functions.manual_detection import extract_frames, detect_tags, print_progress_bar
    from glob import glob

    if True:
        video_path = folder + "/world.mp4"
        # Create frame path using OS package
        # Define the name of the directory to be created
        frames_path = folder + "/frames"
        try:
            if not os.path.exists(frames_path):
                os.mkdir(frames_path)
                print("Successfully created the directory %s " % frames_path)
                extract_frames(video_path, frames_path)
            else:
                print("Directory %s already exists." % frames_path)
        except OSError:
            print("Creation of the directory %s failed" % frames_path)
    # Sort by index in.../frame<index>.png
    all_images = sorted(glob(f'{frames_path}/*.png'), key=lambda f: int(os.path.basename(f)[5:-4]))
    all_images = all_images[:-1]

    num_images = len(all_images)
    return  all_images

def define_event(idx, all_images, fake_gpool):
    from video_capture import fake_backend
    import cv2

    img_path = all_images[idx]
    # read image:
    img = cv2.imread(img_path)

    # timestamp is stored in fake_gpool
    timestamp = fake_gpool.timestamps[idx]
    index = idx
    events = {'frame': fake_backend.Frame(timestamp, img, index)}
    return events

