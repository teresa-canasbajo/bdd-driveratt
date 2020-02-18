import json
import random
import pandas as pd

from bisect import bisect_left

def main():
    with open('./frames.json', 'r') as f:
        items = ['Tree', 'Vehicle', 'Billboard', 'Person', 'Building', 'Skyscraper'] #TODO: how should the items of interest be specified? 600 potential classes from base detector, but the ones we're interested in maybe we want to specify manually
        frames = json.load(f) #TODO: this json should be modified so that frame dictionarys have a key corresponding to the same image frame the fixations.csv will later specify
        fixations = [(random.uniform(0, 1), random.uniform(0, 1)) for _ in frames] #TODO: modify code to pull fixations from actual csv
        # print('Frame  \tFixation     \tObjects')
        data = []
        cumulative_sum = 0
        frames_with_billboards = 0
        for i, frame in enumerate(frames):
            # print(f'{i}   \t({"%.3f" % x}, {"%.3f" % y})\t{identify(x, y, frames[i])}')
            x, y = fixations[i]
            objects = identify(x, y, frame)
            boxes = [objects.get(item, None) for item in items]
            data.append([i, "(%.3f,  %.3f)" % (x, y)] + boxes)
            if bc = billboard_confidence(frame):
                cumulative_sum += bc
                frames_with_billboards += 1
        print("Average billboard confidence: %f" % (cumulative_sum/frames_with_billboards))
        columns = ['Frame', 'Fixation'] + items
        df = pd.DataFrame(data, columns=columns)
        df.to_csv(r'./object_fixations.csv')

def billboard_confidence(frame):
    billboard_scores = [float(frame['detection_scores'][i]) for i in range(len(frame['detection_scores'])) if frame['detection_class_entities'][i] == 'Billboard']
    if len(billboard_scores) > 0:
        return billboard_scores[0]
    return 0

def identify(x, y, frame):
    """Identifies all potential entities that the user was fixated on during a
    keyframe of the simulation based on highest confidence bounding boxes.

    Keyword arguments:
    x -- relative path to config file (float)
    y -- number of test iterations (float)
    frame -- tensorflow_hub detector output; comes sorted in descending order by scores (dict)
    """
    min_confidence = 0.2 #TODO: should this be specified more empiraclly? 
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
    main()
