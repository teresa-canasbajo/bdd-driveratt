from zmq_socket import ZMQsocket
from time import sleep, time

remote_ip = '192.168.0.113'
print('Make sure the ports match with Pupil Capture Remote Plugin and the one in zmq_pocket.py')
port = '50020'
socket = ZMQsocket(port=port)
socket.connect()
socket.start_calibration()

socket.start_recording() # commenting this out to test something, needs to be uncommented later.
# socket.notify({'subject': '1'})

# # TODO fixing sending annotations
# time_fn = time
#
# socket.send_string('T {}'.format(time_fn()))
# print(socket)
#
# # Start the notifications puglin
# socket.notify({'subject': 'start_plugin', 'name': ' Annotation_Capture', 'args': {}})
#
# # let's try sending something
# # socket.send_string('R')
# # socket.recv_string()
#
# sleep(1.)  # sleep for a few seconds, can be less
#
# # Send a trigger with the current time
# # The annotation will be saved to annotation.pldata if a recording is runnin. The Annotation_Player plugin will
# # automatically retrieve, display and export all recorded annotations.
#
# label = 'custom_annotation_label'
# duration = 0.
# minimal_trigger = socket.new_trigger(label, duration, time_fn)  # this defines the trigger
# socket.send_trigger(minimal_trigger)  # this actually sends it
# sleep(1.)  # sleep a bit
#
# minimal_trigger = socket.new_trigger(label, duration, time_fn)
# socket.send_trigger(minimal_trigger)
#
# # add custom keys to your annotation
# minimal_trigger['W'] = 'W'  # testing if it receives everything, not sure why now we don't need to define label
# # duration and all
# send_trigger(minimal_trigger)
# sleep(1.)
#
# # stop recording
# socket.stop_recording()
