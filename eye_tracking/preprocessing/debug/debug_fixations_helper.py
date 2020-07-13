import pandas as pd
import cv2
import os
from glob import glob
from eye_tracking.preprocessing.functions.manual_detection import print_progress_bar


def exports_data(exports_fixations_df, outputfile_name):
    exports_time = exports_fixations_df.start_timestamp
    exports_duration = exports_fixations_df.duration
    if outputfile_name == '/compare_fixations.csv':
        exports_x = exports_fixations_df.norm_pos_x
        exports_y = exports_fixations_df.norm_pos_y
    else:
        # this is for blinks
        exports_x = exports_fixations_df.start_timestamp
        exports_y = exports_fixations_df.start_timestamp
    return exports_x, exports_y, exports_time, exports_duration

def fixations_preprocessing_data(preprocessing_fixations_df):
    time = preprocessing_fixations_df.timestamp
    duration = preprocessing_fixations_df.duration

    import ast
    a = preprocessing_fixations_df.norm_pos
    b = [ast.literal_eval(st) for st in a]
    norm_x = [ib[0] for ib in b]
    norm_y = [ib[1] for ib in b]
    # norm_x = preprocessing_fixations_df.norm_pos
    # norm_y = preprocessing_fixations_df.norm_pos
    return norm_x, norm_y, time, duration

def compare_fixations(export_path, preprocessing_path, outputfile_name = '/compare_fixations.csv'):

    # create fixations dataframe from existing csv file & extract relevant info
    exports_fixations_df = pd.read_csv(export_path)
    exports_fixations_df = exports_fixations_df.apply(pd.to_numeric, errors='coerce')
    preprocessing_fixations_df = pd.read_csv(preprocessing_path)

    exports_x, exports_y, exports_time, exports_duration = exports_data(exports_fixations_df, outputfile_name)
    if outputfile_name == '/compare_fixations.csv':
        fixations_x, fixations_y, fixations_time, fixations_duration = fixations_preprocessing_data(preprocessing_fixations_df)
    else:
        # this is for blinks
        fixations_x, fixations_y, fixations_time, fixations_duration = exports_data(preprocessing_fixations_df, outputfile_name)

    preprocessed_x = []
    preprocessed_y = []
    preprocessed_time = []
    preprocessed_duration = []
    export_x = []
    export_y = []
    export_time = []
    export_duration = []
    multiple = []
    print_progress_bar(0, len(exports_time), prefix='Progress:', suffix='Complete', length=50)
    index = 0

    for beg_t in exports_time:
        end_t = beg_t + (exports_duration[index] / 1000)
        # ir = 0

        no_entry = True
        multiples_val = False
        for t in fixations_time:

            if (t >= beg_t) and (t <= end_t):

                i = fixations_time[fixations_time == t].index[0]
                preprocessed_x.append(fixations_x[i])
                preprocessed_y.append(fixations_y[i])
                preprocessed_time.append(fixations_time[i])
                preprocessed_duration.append(fixations_duration[i])

                export_x.append(exports_x[index])
                export_y.append(exports_y[index])
                export_time.append(beg_t)
                export_duration.append(exports_duration[index])

                multiple.append(multiples_val)
                multiples_val = True

                no_entry = False
        if no_entry:
            preprocessed_x.append("no entry")
            preprocessed_y.append("no entry")
            preprocessed_time.append("no entry")
            preprocessed_duration.append("no entry")

            export_x.append(exports_x[index])
            export_y.append(exports_y[index])
            export_time.append(beg_t)
            export_duration.append(exports_duration[index])

            multiple.append(False)

        index = index + 1
        print_progress_bar(index + 1, len(exports_time), prefix='Progress:', suffix='Complete', length=50)

    coords = {'exports_x': export_x, 'exports_y': export_y, 'preprocessed_x': preprocessed_x,
              'preprocessed_y': preprocessed_y, 'preprocessed_time': preprocessed_time, 'exports_time': export_time,
              'exports_duration': export_duration, 'preprocessed_duration': preprocessed_duration, 'multiples': multiple}
    compare_fixations_df = pd.DataFrame(coords)

    head, tail = os.path.split(preprocessing_path)
    compare_fixations_df.to_csv(os.path.join(head + outputfile_name), index=False)

    return compare_fixations_df

def revert_norm(coord, width, height):
    x = coord[0]*width
    y = coord[1]*height
    # return (x.astype(int), y.astype(int))
    return (int(x), int(y))

def fixation_video(frames_path, fixations_path, type = 'preprocessed'):
    # surfaces_df = pd.read_csv(frames_path + '/surface_coordinates.csv')
    # surfaces_df = surfaces_df.apply(pd.to_numeric, errors='coerce')

    img_n_total = []
    all_images = sorted(glob(f'{frames_path}/*.png'), key=lambda f: int(os.path.basename(f)[5:-4]))
    all_images = all_images[:-1]

    for i, img_path in enumerate(all_images):
        # all frame numbers
        head, tail = os.path.split(img_path)
        img_n_total.append(int(''.join(list(filter(str.isdigit, tail)))))

    # match world timestamps to appropriate frame
    head, tail = os.path.split(frames_path)
    timestamps_path = os.path.join(head, 'world_timestamps.npy')
    import numpy as np
    time = np.load(timestamps_path)
    frame = {'image': img_n_total, 'timestamp': time}

    if type == 'preprocessed':
        preprocessing_fixations_df = pd.read_csv(fixations_path)
        fixations_x, fixations_y, fixations_time, fixations_duration = fixations_preprocessing_data(preprocessing_fixations_df)
        fixation_frames_path = frames_path + '/preprocessed_fixations'
    else:
        exports_fixations_df = pd.read_csv(fixations_path)
        exports_fixations_df = exports_fixations_df.apply(pd.to_numeric, errors='coerce')
        fixations_x, fixations_y, fixations_time, fixations_duration = exports_data(exports_fixations_df)
        fixation_frames_path = frames_path + '/export_fixations'

    if not os.path.exists(fixation_frames_path):
        os.mkdir(fixation_frames_path)

    i = 0
    n = 0

    print_progress_bar(0, len(fixations_time), prefix='Progress:', suffix='Complete', length=50)

    for f in fixations_time:

        # match fixation timestamp to surface timestamp
        while (i < (len(frame['timestamp']) - 1)) and (f >= frame['timestamp'][i + 1]):
            i = i + 1
            # if (fixations_time[n-1] + (fixations_duration[n-1]/1000)) >= frame['timestamp'][i]:
            #     if fixations_time[n-1] <= frame['timestamp'][i]:
            #         create_frame(frames_path, frame, i, fixations_x, n-1, fixations_y, fixation_frames_path)

        if f >= frame['timestamp'][i]:

            create_frame(frames_path, frame, i, fixations_x, n, fixations_y, fixation_frames_path)

            # test_i = i + 1
            # while (f + (fixations_duration[n]/1000)) >= frame['timestamp'][test_i]:
            #     create_frame(frames_path, frame, i, fixations_x, n, fixations_y, fixation_frames_path)
            #     test_i = test_i + 1
        n = n + 1

        print_progress_bar(n + 1, len(fixations_time), prefix='Progress:', suffix='Complete', length=50)

    # remaining_img(frames_path, fixation_frames_path)

    create_video(fixation_frames_path, type)

def create_frame(frames_path, frame, i, fixations_x, n, fixations_y, fixation_frames_path):
    img_path = frames_path + '/frame' + str(frame['image'][i]) + '.png'
    img = cv2.imread(img_path, cv2.IMREAD_COLOR)
    c = (fixations_x[n], 1-fixations_y[n])
    height = img.shape[0]
    width = img.shape[1]
    coords = revert_norm(c, width, height)

    cv2.circle(img, coords, 2, (0, 0, 255), 8)  # point in the center of the screen

    head, tail = os.path.split(img_path)
    num = ''.join(list(filter(str.isdigit, tail)))
    cv2.imwrite(fixation_frames_path + '/' + num + '.png', img)


def remaining_img(src, dst):
    import glob
    import shutil
    import os
    from pathlib import Path

    list_of_files = glob.glob(src + '/*.png')
    latest_file = len(list_of_files)-1
    n = 0
    print_progress_bar(n, latest_file, prefix='Progress:', suffix='Complete', length=50)
    for pngfile in glob.iglob(os.path.join(src, "*.png")):
        head, tail = os.path.split(pngfile)
        fileExist = dst + "/" + tail
        if not Path(fileExist).exists():
            shutil.copy(pngfile, dst)
        n = n + 1
        print_progress_bar(n, latest_file, prefix='Progress:', suffix='Complete', length=50)

def create_video(image_folder, type):
    os.chdir(image_folder)
    video_name = type + '_video.avi'

    images = [int(''.join(list(filter(str.isdigit, img)))) for img in os.listdir(image_folder) if img.endswith(".png")]
    images.sort()
    images = images[:-1]
    frame = cv2.imread(os.path.join(image_folder, str(images[0])+'.png'))
    height, width, layers = frame.shape

    video = cv2.VideoWriter(video_name, 0, 19, (width, height))

    print_progress_bar(0, len(images), prefix='Progress:', suffix='Complete', length=50)
    index = 0
    for image in images:
        video.write(cv2.imread(os.path.join(image_folder, str(image) + '.png')))
        index = index + 1
        print_progress_bar(index + 1, len(images), prefix='Progress:', suffix='Complete', length=50)

    cv2.destroyAllWindows()
    video.release()



