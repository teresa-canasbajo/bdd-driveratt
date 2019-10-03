from zmq_socket import ZMQsocket
from time import sleep, time

remote_ip = '10.142.20.154'
print('Make sure the ports match with Pupil Capture Remote Plugin and the one in zmq_pocket.py')
port = '50020'
socket = ZMQsocket()
socket.connect()
# socket.start_calibration()

# Grab the time module for timesync
time_fn = time

# Sync time
print(socket.set_time(time_fn))

# # Start the notifications puglin
socket.notify({'subject': 'start_plugin', 'name': 'Annotation_Capture', 'args': {}})
#
socket.start_recording() # commenting this out to test something, needs to be uncommented later.

sleep(1.)

# Send some annotations
socket.annotation('start_trial', 0)
sleep(5.)  # sleep a bit

socket.annotation('end_trial', 0)
sleep(1.)

# Finish up
socket.stop_recording()
print('Script completed.')
