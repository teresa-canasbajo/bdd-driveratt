

How to set up python packages to connect to Pupil Labs eyetracker:

- Clone repo: https://github.com/mtaung/eye_socket
- Follow instructions to install: pip install -r requirements.txt (remember to activate your virtual environment if you have one)
- Install pupil capture to your computer. Find it here: https://github.com/pupil-labs/pupil/releases. Note that you may need an older version to work with annotations. 
- Important that everytime that you set it up change the files with the correct port! The IP address of the eyetracker is in the Pupil Capture, remote pluging. 
If using it within Psychopy:
- Import function zmq_socket.py. This will import all functions that you need to interact with Pupil Labs.
- The class handles the initialisation of the ZMQ socket. The address for this will default to localhost:50020, as these are the defaults for pupil-labs systems.
-  script has a bunch of functions you can use to send triggers to the eyetracker. Here are a list of the ones that are predefined:
- You need to have Pupil Capture running on the background at all times during the experiment. 

The idea is that, if in your Psychopy code you import the zmq_socket function and then you call the function socket.start_calibration() then it will open Pupil Capture, run the calibration, then close the screen. Next, you call the socket.start_recording() and then just put the rest of your code that normally would run your experiment just below. At the end add socket.stop_recording(). 

Notes: If more than one device using the eyetracker's ip address (127.0.0.1), consider using different ports to distinguish them.

### FUNCTIONS ###
	connect(): Connect to the defined ZMQ socket. Run this after initialising the socket object in your experiment.

	start_calibration() If you want to calibrate, it may be better to calibrate within a recording, depending on your desired workflow. This way, you can recalibrate offline if required.

	stop_calibration(): Stops the pupil calibration procedure. This shouldn't be necessary if the calibration is completed properly.

	start_recording(): Starts a pupil recording. You can optionally input a directory name into the parameter dir_name, which will rename the master directory of any recordings under this title.

	stop_recording(): Stops a recording when specified. You will want to run this to ensure that your recorded data have complete headers.

	set_time(): Sets the time on the pupil trackers. By default, pupil clock is not fixed. We presently synchronise our clocks manually at the start of a recording session and align data post-hoc; I personally find this more informative in my work. For those that need consistent realtime sync, I am looking to implement Pupil-Labs' own time sync functionality in the future.

	notify(): This functionality is currently incomplete and requires some further work to get going. If you're interested in this or have done so before, feel free to submit a PR.

	new_trigger(): Creates a trigger with a given topic, label, and duration. Make sure to sync timestamps first through set_time().

	send_trigger(): Sends a trigger (like an annotation) to Pupil Remote.

	annotatation(): Shortcut to sending an annotation to Pupil Remote. Make sure to sync timestamps first through set_time().

### FUNCTIONS
