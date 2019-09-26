import zmq
import msgpack as serializer
import logging, time

class ZMQsocket:
    """
    Create a zeromq socket object. 
    Note: Localhost is ``127.0.0.1`` 
    and Pupil-Recorder default port is ``50020``.
    """

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.ctx = zmq.Context()
        self.socket = zmq.Socket(self.ctx, zmq.REQ)
        self.logger = logging.getLogger(__name__)
        self.logger.info('Creating zeromq socket object')

    # Probably better to have a separate connect method than init
    def zmq_connect(self):
        self.socket.connect('tcp://{}:{}'.format(self.ip, self.port))
        self.logger.info("ZMQ socket bound to {} on port {}".format(self.ip, self.port))

    def notify(self, notification):
        """
        Primary communication method with Pupil-Recorder
        Use ``send_trigger()`` instead if appropriate.
        """

        topic = 'notify.' + notification['subject']
        payload = serializer.dumps(notification, use_bin_type=True)
        self.socket.send_string(topic, flags=zmq.SNDMORE)
        self.socket.send(payload)
        self.logger.info('Payload sent: {}'.format(payload))
        return self.socket.recv_string()

    def send_trigger(self, label, timestamp, duration=0.):
        """
        Sends a notification that delivers a trigger to Pupil-Recorder.
        """
        return self.notify({'subject': 'annotation', 'label': label,
                            'timestamp': timestamp, 'duration': duration,
                            'source':'homelabs framework', 'record': True}) 
    
    def set_time(self, time='0.0'):
        """
        Placeholder time-setting. Pupil-Sync is probably superior.
        Default is ``0.0``.
        """
        self.socket.send_string('T {}'.format(time))
        self.logger.info(self.socket.recv_string())

    def start_calibration(self):
        self.socket.send_string('C')
        self.logger.info(self.socket.recv_string())

    def stop_calibration(self):
        self.socket.send_string('c')
        self.logger.info(self.socket.recv_string())

    def start_recording(self, recTitle):  # TOM EDITED TO ADD CUSTOM TITLE
        self.socket.send_string('R %s'%recTitle)
        self.logger.info(self.socket.recv_string())

    def stop_recording(self):
        self.socket.send_string('r')
        self.logger.info(self.socket.recv_string())
