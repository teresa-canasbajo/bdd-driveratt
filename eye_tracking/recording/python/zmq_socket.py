import zmq
import msgpack as serializer

class ZMQsocket:

    def __init__(self, ip='127.0.0.1', port='50020'):
        """
        Setup zmq socket, context, and remote helper.

        Parameters:
        port (float): Specified port to connect to. Defaults to 50020.
        """
        self.ip = ip 
        self.port = port
        self.ctx = zmq.Context()
        self.socket = zmq.Socket(self.ctx, zmq.REQ)

    def connect(self):
        """
        Connects to defined zmq socket.
        """
        self.socket.connect(f'tcp://{self.ip}:{self.port}')

    def start_calibration(self):
        """
        Starts pupil calibration procedure.
        """
        self.socket.send_string('C')
        return self.socket.recv_string()

    def stop_calibration(self):
        """
        Stops pupil calibration procedure.
        """
        self.socket.send_string('c')
        return self.socket.recv_string()

    def start_recording(self, dir_name=None):
        """
        Starts pupil recording.
        Parameters:
        dir_name (str): Optional name for directory
        """
        if dir_name:
            self.socket.send_string(f'R {dir_name}')
        else:
            self.socket.send_string('R')       
        return self.socket.recv_string()

    def stop_recording(self):
        """
        Stops pupil recording.
        """
        self.socket.send_string('r')
        return self.socket.recv_string()

    def set_time(self, time):
        """
        Sets the time in pupil.

        Parameters:
        time (float): Time to set to. 
        """
        self.socket.send_string(f'T {time}')
        return self.socket.recv_string()
    
    # send notification:
    def notify(self, notification):
        """Sends ``notification`` to Pupil Remote"""
        topic = 'notify.' + notification['subject']
        payload = serializer.dumps(notification, use_bin_type=True)
        self.socket.send_string(topic, flags=zmq.SNDMORE)
        self.socket.send(payload)
        return self.socket.recv_string()

    #test notification, note that you need to listen on the IPC to receive notifications!
    #notify({'subject':"calibration.should_start"})
    #notify({'subject':"calibration.should_stop"})