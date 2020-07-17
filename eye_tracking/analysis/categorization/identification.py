import sys
import json
import random
import pandas as pd
import ast
from bisect import bisect_left

def main(json_filepath, smoothed_billboards_path, output_filepath):
    """Categorizes each fixation by the object the subject was fixated on (if any). 
    Handles billboards separately due to the need for smoothing.

    Keyword arguments: 
    json_filepath -- path to output of object_detection.py
    smoothed_billboards_path -- path to output of billboard_identification.py
    output_filepath -- savepath for generated csv
    """
    with open(json_filepath, 'r') as f:
        items = ['Tree', 'Vehicle','Person', 'Building', 'Skyscraper']
        frames = json.load(f) #frame results listed chronologically
        smoothed_billboard_detections = pd.read_csv(smoothed_billboards_path, index_col=0)

        # fixations = generate_fixations_frame()
        fixations = [(random.uniform(0, 1), random.uniform(0, 1)) for _ in frames]

        data = []
        for i, frame in enumerate(frames):
            # x, y = fixations.iloc[i] #use with actual frame
            x, y = fixations[i] # use with randomly generated data

            # standard object fixation process
            objects = identify(x, y, frame)
            boxes = [objects.get(item, None) for item in items]

            # custom process for billboards
            smoothed_billboard_boxes = ast.literal_eval(smoothed_billboard_detections.iloc[i]['Smoothed'])
            to_append = None
            for box in smoothed_billboard_boxes:
                if inside_box(x, y, box):
                    to_append = box
                    break
            boxes.append(to_append)

            data.append([i, "(%.3f,  %.3f)" % (x, y)] + boxes)
        columns = ['Frame', 'Fixation'] + items + ['Billboard']
        df = pd.DataFrame(data, columns=columns)
        df.to_csv(output_filepath)

def generate_fixations_frame():
    """Converts detected fixation data into a working Pandas dataframe. 
    Expects data to be located in fixations.csv
    """
    df = pd.read_csv('fixations.csv')
    fixations = []
    frame = []
    prev_start = 0
    for i in range(len(df)):
        row = df.iloc[i]

        # fill in gaps
        if row['start_frame_index'] - prev_start > 0:
            for j in range(prev_start, row['start_frame_index']):
                frame.append(j)
                fixations.append((0,0))
        
        # fill in fixations if high enough confidence
        if row['confidence'] > 0.8:
            for j in range(row['start_frame_index'], row['end_frame_index']):
                frame.append(j)
                fixations.append((row['norm_pos_x'] , row['norm_pos_y']))
        else:
            for j in range(row['start_frame_index'], row['end_frame_index']):
                frame.append(j)
                fixations.append((0, 0))

        prev_start = row['end_frame_index']
    return pd.DataFrame({"Fixations": fixations}, index=frame)

def inside_box(x, y, box):
    """Determines if the point (x, y) is contained within the 
    specified bounding box.

    Keyword arguments:
    x -- x coord 
    y -- y coord 
    box -- bounding box ordered ymin, xmin, ymax, xmax 
    """
    ymin, xmin, ymax, xmax = map(lambda s: float(s), box)
    return xmin <= x <= xmax and ymin <= y <= ymax

def identify(x, y, frame):
    """Identifies all potential entities that the user was fixated on during a
    keyframe of the simulation based on highest confidence bounding boxes.

    Keyword arguments:
    x -- relative path to config file
    y -- number of test iterations
    frame -- tensorflow_hub detector output sorted in descending order of scores
    """
    min_confidence = 0.2 #TODO: should this be specified more empiraclly? or maybe set it super low only for billboard class?
    scores = [float(s) for s in frame['detection_scores'][::-1]]
    cutoff = len(scores) - bisect_left(scores, min_confidence) 
    # print('Cut: ', cutoff)
    boxes = frame['detection_boxes'][:cutoff]
    entities = frame['detection_class_entities'][:cutoff]
    return {entities[j]: boxes[j] for j, box in enumerate(boxes[::-1]) if inside_box(x, y, box)}

if __name__ == '__main__':
    args = sys.argv[1:]
    assert(len(args) >= 3)
    main(*args)
