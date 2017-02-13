'''
Audio Processing Lab - Assignment 2, Task 4
Nestor Napoles, Feb. 2017

This scripts takes the reduced json files generated in the
previous step and merges them into a single, small, json file
that contains an average of the features from all the duplications
taken from the dataset. This is later used to compare to a new duplication.
'''

import os
import json
from natsort import natsorted

smalldataset = 'ab-duplicates100-2016-03-02'
largedataset = 'ab-duplicates1000-2016-03-02'
dataset = largedataset

reduceddataset = '{}_reduced'.format(dataset)
averagesfile = '{}_averages.json'.format(dataset)

files = os.listdir(reduceddataset)
files = [x for x in files if x.endswith('.json')]
files = natsorted(files, key=lambda y: y.lower())

averages = {}

def compute_averages(d):
    averages = {}
    # Getting length
    averages['length'] = sum(d['length'])/float(len(d['length']))
    # Getting replay_gain
    averages['replay_gain'] = sum(d['replay_gain'])/float(len(d['replay_gain']))
    # Getting average_loudness
    averages['average_loudness'] = sum(d['average_loudness'])/float(len(d['average_loudness']))
    # Getting bpm
    averages['bpm'] = sum(d['bpm'])/float(len(d['bpm']))
    # Getting onset_rate
    averages['onset_rate'] = sum(d['onset_rate'])/float(len(d['onset_rate']))
    # Getting beats_count
    averages['beats_count'] = sum(d['beats_count'])/len(d['beats_count'])
    # Getting chords_histogram
    averages['chords_histogram'] = [sum(x)/float(len(x)) for x in d['chords_histogram']]
    # Getting hpcp_mean
    averages['hpcp_mean'] = [sum(x)/float(len(x)) for x in d['hpcp_mean']]
    # Getting key_key
    averages['key_key'] = max(set(d['key_key']), key=d['key_key'].count)
    # Getting key_scale
    averages['key_scale'] = max(set(d['key_scale']), key=d['key_scale'].count)
    # Getting key_strength
    averages['key_strength'] = sum(d['key_strength'])/float(len(d['key_strength']))
    # Getting tuning_frequency
    averages['tuning_frequency'] = sum(d['tuning_frequency'])/float(len(d['tuning_frequency']))
    return averages

for f in files:
    mbid = f[:-5]
    filepath = os.path.join(reduceddataset, f)
    with open(filepath) as fd:
        data = json.load(fd)
        averages[mbid] = compute_averages(data)

with open(averagesfile, 'w') as fd:
    json.dump(averages, fd)
