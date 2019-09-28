from zmq_socket import ZMQsocket

remote_ip = '192.168.0.113'
port = '8008'
socket = ZMQsocket(port=port)
socket.connect()
socket.start_calibration()

socket.start_recording()
# socket.notify({'subject': '1'})
