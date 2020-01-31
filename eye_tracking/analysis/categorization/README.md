# Overview

The categorization folder runs the object detection and data processing functions on the video after it has been separated into its individual frames. It consists of two files, object_detection.py and identification.py.


# Object Detection

The most important function in this file is detect_objects, which takes in the path to the frames and a detector object and returns a list of objects for each frame (you can look through frames.json for an example of the output). You don’t need to worry about the other helper functions, but feel free to modify them if you want to change how the detection works.

For an example usage of detect_objects, refer to the main function. A detector object is initialized, a frames directory is either created or loaded (depending on whether it already existed), and detect_objects is called. The output is saved to the frames.json file, which will be important for the next stage, identification.


# Identification

The purpose of this file is to record the object that the driver is fixating on for each frame of the video. We’ll be using the JSON file from object detection, along with the fixation data from the eye tracker, to produce a CSV output with all relevant information.

Refer to main function to see the task in progress. We declare the items to look out for, load the JSON and fixation data (right now this is just a list of randomly generated coordinates since the fixation data wasn’t available when I wrote it), call identify for each frame, and finally save the output to a Pandas dataframe. When the fixation data is available, it should be processed into a list of lists, separated by frame and coordinates. Then, the function should properly identify what  the driver is looking at in a sample video.

