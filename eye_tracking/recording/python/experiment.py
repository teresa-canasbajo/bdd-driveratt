from zmq_socket import ZMQsocket

remote_ip = '192.168.0.113'
print('Make sure the ports match with Pupil Capture Remote Plugin and the one in zmq_pocket.py')
port = '50020'
socket = ZMQsocket(port=port)
socket.connect()
socket.start_calibration()

socket.start_recording()
# socket.notify({'subject': '1'})
