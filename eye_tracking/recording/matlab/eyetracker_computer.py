from mm_modules import pupilsocket, pytcp, pyudp
import logging
from time import time

time_fn = time

# Begin runtime with entry of ppID
# This is used later for setting dir/file names
participantID = input('Participant ID: ')

## Establish Logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')

fileHandler = logging.FileHandler('{}_{}.log'.format(participantID, time_fn()))
fileHandler.setLevel(logging.DEBUG)
fileHandler.setFormatter(formatter)

streamHandler = logging.StreamHandler()
streamHandler.setFormatter(formatter)

logger.addHandler(streamHandler)
logger.addHandler(fileHandler)
logger.info('Logging initialised at {}.'.format(fileHandler))

## Connect sockets
# udp sock
udpListeningSock = pyudp.UDPsocket('192.168.0.113', 8008)
udpListeningSock.sock_bind()

pupilLink = pupilsocket.ZMQsocket('192.168.0.113', 8008)
pupilLink.zmq_connect()
logger.info('Pupil socket connected.')

pupilLink.notify({'subject': 'start_plugin',
                    'name': 'Log_History',
                    'args': {}})
pupilLink.notify({'subject': 'start_plugin',
                    'name': 'Annotation_Capture',
                    'args': {}})
logger.info('Pupil-Recorder Annotations plugin prompted.')

## The Pupil developers recommend using their Sync system
## Time() here will work but won't be millisecond accurate.
pupilLink.set_time(time_fn())
logger.info('Pupil-Recorder time set.')
pupilLink.send_trigger('Dummy Trigger', timestamp=time_fn())

## Define Triggers using a dict for pseudo switch cases
## Note that this solution will not handle mixed cases
# Commands
def startrec():
    # This is currently set to receive input from stimuli code 
    # you may want to just change recTitle input to ParticipantID
    pupilLink.start_recording(recTitle=data[10:len(data)])
def stoprec():
    pupilLink.stop_recording()
def startcal():
    pupilLink.start_calibration()
def stopcal():
    pupilLink.stop_calibration()
# Triggers
def trig0():
    pupilLink.send_trigger('Event0', timestamp=time_fn())
def trig1():
    pupilLink.send_trigger('Event1', timestamp=time_fn())
def trig2():
    pupilLink.send_trigger('Event2', timestamp=time_fn())
def trig3():
    pupilLink.send_trigger('Event3', timestamp=time_fn())
def trig4():
    pupilLink.send_trigger('Event4', timestamp=time_fn())

triggerDict = {
    # Commands
    b'START_REC' : startrec,
    b'STOP_REC' : stoprec,
    b'START_CAL' : startcal,
    b'STOP_CAL' : stopcal,
    # Triggers
    b'0': trig0,
    b'1': trig1,
    b'2': trig2,
    b'3': trig3,
    b'4': trig4
    }

## start listening to udpListeningSock
while True:
    data, time = udpListeningSock.sock_listen()
    print(data, time)
    if data:
        triggerDict[data]()