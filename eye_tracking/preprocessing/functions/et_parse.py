# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import logging


def parse_message(msg):
    # Input: message to be parsed
    #        (e.g. annotations from pldata['annotations'])
    # Output: pandas Series of the parsedmsg
    #         see "overview dataframe pdf"

    # get a logger
    logger = logging.getLogger(__name__)

    try:
        timestamp = msg['timestamp']
        exp_event = msg['label']
    except:
        return np.nan

    # splits msg into list of str and removes punctuation
    split = exp_event.split(' ')
    split = [remove_punctuation(elem) for elem in split]

    block = None
    trial = None
    task = ''

    # assign block and trial number
    if 'trial' in split:
        i = split.index('trial')
        trial = split[i + 1]
    if 'block' in split:
        i = split.index('block')
        block = split[i + 1]

    # assign different trial events
    if split[0] == 'Block':
        if split[2] == 'Begins':
            task = 'Block begins'
        block = split[1]
    elif split[0] == 'Begin':
        task = 'Trial begins'
    elif split[0] == 'Fixation':
        task = 'Fixation dot'
    elif split[0] == 'Image':
        task = 'Image onset'
    elif split[0] == 'Adjust':
        if split[2] == 'begins':
            task = 'Adjust task'
    elif split[0] == 'Ending':
        task = 'End trial'

    parsedmsg = {'block': block, 'trial': trial, 'exp_event': exp_event, 'timestamp': timestamp, 'task': task}

    return pd.Series(parsedmsg)


def remove_punctuation(s):
    string_punctuation = ".,;"
    no_punct = ""
    for letter in s:
        if letter not in string_punctuation:
            no_punct += letter
    return no_punct
