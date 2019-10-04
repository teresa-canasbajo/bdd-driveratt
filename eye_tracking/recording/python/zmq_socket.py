import zmq
import msgpack as serializer

print('Opening ports')
class ZMQsocket:

    # the ip address of the eyetracker is always 127.0.0.1.

    def __init__(self, ip='127.0.0.1', port='50020'):
        """
        Setup zmq socket, context, and remote helper.

        Parameters:
        port (float): Specified port to connect to. Defaults to 50020.
        """
        self.ip = ip 
        self.port = port
        self.ctx = zmq.Context()
        self.socket = zmq.Socket(self.ctx, zmq.REQ) # this is pub socket

    def connect(self):
        """
        Connects to defined zmq socket.
        """
        self.socket.connect(f'tcp://{self.ip}:{self.port}')
        self.socket.send_string('PUB_PORT')
        self.pub_port = self.socket.recv_string()
        self.pub_socket = zmq.Socket(self.ctx, zmq.PUB)
        self.pub_socket.connect(f"tcp://{self.ip}:{self.pub_port}")

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

    def set_time(self, time_fn):
        """
        Sets the time in pupil.

        Parameters:
        time (float): Time to set to. 
        """
        self.time_fn = time_fn
        self.socket.send_string(f'T {time_fn()}')
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

    # TODO fix sending annotations
    def send_trigger(self, trigger):
        """
        Sends a trigger object pub_socket
        """
        payload = serializer.dumps(trigger, use_bin_type=True)
        self.pub_socket.send_string(trigger['topic'], flags=zmq.SNDMORE)
        self.pub_socket.send(payload)

    def new_trigger(self, topic, label, duration):
        """
        Creates a trigger dictionary object (make sure set_time() has been invoked)
        """
        return {
            "topic": topic,
            "label": label,
            "timestamp": self.time_fn(),
            "duration": duration,
        }

    def annotation(self, label, duration):
        """
        Shortcut to sending an annotation to pupil remote (make sure set_time() has been invoked)
        """
        self.send_trigger(self.new_trigger('annotation', label, duration))


    print('Done!')