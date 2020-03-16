import sys
import json
import random
import pandas as pd

from bisect import bisect_left

def main(json_filepath, output_filepath):
    with open(json_filepath, 'r') as f:
        items = ['Tree', 'Vehicle','Person', 'Building', 'Skyscraper']
        frames = json.load(f) #frame results listed chronologically
        fixations = generate_fixations_frame()
        fixations = [(random.uniform(0, 1), random.uniform(0, 1)) for _ in frames]
        # print('Frame  \tFixation     \tObjects')
        data = []
        for i, frame in enumerate(frames):
            # print(f'{i}   \t({"%.3f" % x}, {"%.3f" % y})\t{identify(x, y, frames[i])}')
            x, y = fixations[i]
            objects = identify(x, y, frame)
            boxes = [objects.get(item, None) for item in items]
            data.append([i, "(%.3f,  %.3f)" % (x, y)] + boxes)
        columns = ['Frame', 'Fixation'] + items
        df = pd.DataFrame(data, columns=columns)
        df.to_csv(output_filepath)

def generate_fixations_frame():
    df = pd.read_csv('fixations.csv')
    fixations_by_frame = []
    for i in range(len(df)):
        row = df.iloc[i]
        frame_span = row['end_frame_index'] - row['start_frame_index']
        if row['confidence'] > 0.8:
            fixations_by_frame += [(row['norm_pos_x'] , row['norm_pos_y']) * frame_span]
        else:
            fixations_by_frame += [(0, 0) * frame_span]
    return fixations_by_frame

def identify(x, y, frame):
    """Identifies all potential entities that the user was fixated on during a
    keyframe of the simulation based on highest confidence bounding boxes.

    Keyword arguments:
    x -- relative path to config file (float)
    y -- number of test iterations (float)
    frame -- tensorflow_hub detector output; comes sorted in descending order by scores (dict)
    """
    min_confidence = 0.2 #TODO: should this be specified more empiraclly? or maybe set it super low only for billboard class?
    scores = [float(s) for s in frame['detection_scores'][::-1]]
    cutoff = len(scores) - bisect_left(scores, min_confidence) 
    print('Cut: ', cutoff)
    boxes = frame['detection_boxes'][:cutoff]
    entities = frame['detection_class_entities'][:cutoff]

    def inside_box(box):
        ymin, xmin, ymax, xmax = map(lambda s: float(s), box)
        return xmin <= x <= xmax and ymin <= y <= ymax

    return {entities[j]: boxes[j] for j, box in enumerate(boxes[::-1]) if inside_box(box)}

if __name__ == '__main__':
    args = sys.argv[1:]
    assert(len(args) >= 2)
    main(*args)
