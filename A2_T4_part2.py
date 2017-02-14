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
import numpy as np

smalldataset = 'ab-duplicates100-2016-03-02'
largedataset = 'ab-duplicates1000-2016-03-02'
dataset = smalldataset

reduceddataset = '{}_reduced'.format(dataset)
averagesfile = '{}_averages.json'.format(dataset)

files = os.listdir(reduceddataset)
files = [x for x in files if x.endswith('.json')]
files = natsorted(files, key=lambda y: y.lower())

averages = {}

def compute_averages(d):
    averages = {}
    # Getting length
    averages['length'] = {'mean':np.mean(d['length']), 'std':np.std(d['length'])}
    # Getting replay_gain
    averages['replay_gain'] = {'mean':np.mean(d['replay_gain']), 'std':np.std(d['replay_gain'])}
    # Getting average_loudness
    averages['average_loudness'] = {'mean':np.mean(d['average_loudness']), 'std':np.std(d['average_loudness'])}
    # Getting bpm
    averages['bpm'] = {'mean':np.mean(d['bpm']), 'std':np.std(d['bpm'])}
    # Getting onset_rate
    averages['onset_rate'] = {'mean':np.mean(d['onset_rate']), 'std':np.std(d['onset_rate'])}
    # Getting beats_count
    averages['beats_count'] = {'mean':np.mean(d['beats_count']), 'std':np.std(d['beats_count'])}
    # Getting chords_histogram
    averages['chords_histogram'] = [{'mean':np.mean(x), 'std':np.std(x)} for x in d['chords_histogram']]
    # Getting hpcp_mean
    averages['hpcp_mean'] = [{'mean':np.mean(x), 'std':np.std(x)} for x in d['hpcp_mean']]
    # Getting key_key
    averages['key_key'] = max(set(d['key_key']), key=d['key_key'].count)
    # Getting key_scale
    averages['key_scale'] = max(set(d['key_scale']), key=d['key_scale'].count)
    # Getting key_strength
    averages['key_strength'] = {'mean':np.mean(d['key_strength']), 'std':np.std(d['key_strength'])}
    # Getting tuning_frequency
    averages['tuning_frequency'] = {'mean':np.mean(d['tuning_frequency']), 'std':np.std(d['tuning_frequency'])}
    return averages

for f in files:
    mbid = f[:-5]
    filepath = os.path.join(reduceddataset, f)
    with open(filepath) as fd:
        data = json.load(fd)
        averages[mbid] = compute_averages(data)

with open(averagesfile, 'w') as fd:
    json.dump(averages, fd)
