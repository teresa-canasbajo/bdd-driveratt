# Overview

The main goal of this module is to categorize each detected fixation by the object that the subject was looking at (if any) and calculate the proportion of time the subject was fixated on each object class. As such, the task is broken into parts: object detection, identification, and visualization. 


# Object Detection 
See ```object_detection.py``` for details.

For object detection, we utilize pre-trained models from TensorflowHub that are specialized for multiple object localization on single images. The most important function in this file is detect_objects, which given a path to the frames of the subject video runs the object detector to get a list of potential objects for each frame (you can look through frames.json for an example of the output). You don’t need to worry about the other helper functions, but feel free to modify them if you want to change how the detection works. You can also optionally pass in a path to a video file to be extracted into single frames to be used for the object detection. The output is saved to a json file, which will used for the identification stage.

Usage:
```
python object_detection.py PATH_TO_FRAMES_FOLDER OUTPUT_PATH [PATH_TO_VIDEO_FILE]
```

# Identification
See ```identification.py``` and ```billboard_identification.py``` for details.

The purpose of this stage is to identify the object that the subject is fixating on for each frame of the video. This is done by seeing if the fixation point is contained within any of the detected bounding boxes for that frame. If there are multiple, we categorize the fixation using the object with the highest confidence detection. 

Most object class detections are handled within ```identification.py```, and only objects detected with at least 0.2 confidence are considered. Billboards are handled separately, however, due to TensorflowHub models generally having lower confidence and less frequent Billboard detections, and because we care about Billboards in particular for saliency models. To deal with this, we lower our threshold for acceptable detections and applying a simple smoothing procedure to fill in gaps in between two billboard detections that are likely to be the same billboard. This procedure should be run before the all purpose identification script, which aggregates the output of billboard detection and all other object detections into on file.

Usage:
```
python billboard_identification.py PATH_TO_JSON OUTPUT_PATH DETECTION_THRESHOLD SMOOTHING_THRESHOLD FPS
python identification.py PATH_TO_JSON BILLBOARD_CSV_PATH OUTPUT_PATH
```

# Visualization
See ```visualization.py``` for details.
 
This stage simply turns all the information we have compiled into a final summarizing figure of object fixations as a percentage of total video frames. 
The current code produces simple seaborn bar plots, but can be easily improved to generate nicer or more complicated figures (be sure to maintain compatability with Pandas).

Usage:
```
python visualization.py PATH_TO_CSV
```

# Other
These files contain provide additional functionality that may be helpful for debugging the performance of object detection and identification. 

## Animation
```animate.py``` helps annotate the original subject video with the identified bounding boxes. It can also generate side-by-side annotations to help evaluate the
billboard smoothing method.

For animating original TFHub detections:
```
python animate.py tf PATH_TO_FRAMES PATH_TO_JSON FINAL_OUTPUT_PATH DETECTION_THRESHOLD
```

For animating smoothed TFHub detections:
```
python animate.py tf_smoothed PATH_TO_FRAMES PATH_TO_CSV FINAL_OUTPUT_PATH
``` 

For comparison:
```
python animate.py tf_compare PATH_TO_FRAMES FINAL_OUTPUT_PATH
```
