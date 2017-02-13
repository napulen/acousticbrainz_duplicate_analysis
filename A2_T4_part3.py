'''
Audio Processing Lab - Assignment 2, Task 4
Nestor Napoles, Feb. 2017

This script takes the computed average features from
the duplications dataset, and compares that to any
unknown duplication to calculate similarity between
them, attempting to say if the duplication corresponds
to the same audio file that was already analyzed.
'''

import os
import json
from natsort import natsorted
import numpy as np

smalldataset = 'ab-duplicates100-2016-03-02'
largedataset = 'ab-duplicates1000-2016-03-02'
dataset = smalldataset

averagesfile = '{}_averages.json'.format(dataset)

averages = {}

# Loading the averages json computed in previous code
with open(averagesfile) as f:
    averages = json.load(f)

# Parse the name of the file to get mbid and number of duplication
def parseduplication(dup):
    parsed = dup[:-5].rsplit('-', 1)
    return (parsed[0], parsed[1])

def comparisonfeatures(dupjson):
    features = {}
    # Getting length
    features['length'] = dupjson['metadata']['audio_properties']['length']
    # Getting replay_gain
    features['replay_gain'] = dupjson['metadata']['audio_properties']['replay_gain']
    # Getting average_loudness
    features['average_loudness'] = dupjson['lowlevel']['average_loudness']
    # Getting bpm
    features['bpm'] = dupjson['rhythm']['bpm']
    # Getting onset_rate
    features['onset_rate'] = dupjson['rhythm']['onset_rate']
    # Getting beats_count
    features['beats_count'] = dupjson['rhythm']['beats_count']
    # Getting chords_histogram
    features['chords_histogram'] = dupjson['tonal']['chords_histogram']
    # Getting hpcp_mean
    features['hpcp_mean'] = dupjson['tonal']['hpcp']['mean']
    # Getting key_key
    features['key_key'] = dupjson['tonal']['key_key']
    # Getting key_scale
    features['key_scale'] = dupjson['tonal']['key_scale']
    # Getting key_strength
    features['key_strength'] = dupjson['tonal']['key_strength']
    # Getting tuning_frequency
    features['tuning_frequency'] = dupjson['tonal']['tuning_frequency']
    return features

def generatesimilarityvector(d):
    v = np.array([])
    for key in sorted(d):
        if key == 'hpcp_mean' or key == 'chords_histogram':
            for i in d[key]:
                v = np.append(v, i)
        elif key == 'key_key':
            '''asd'''
        elif key == 'key_scale':
            '''asd'''
        else:
            v = np.append(v, d[key])
    return v


def computesimilarity(mbid, d):
    dupvector = generatesimilarityvector(d)
    avgvector = generatesimilarityvector(averages[mbid])
    print '{} {}'.format(mbid, np.linalg.norm(dupvector-avgvector))
    ### Compute similarity

# Load every file from the provided dataset
for folder in os.listdir(dataset):
    print '{}...'.format(os.path.join(dataset,folder))
    folderpath = os.path.join(dataset, folder)
    files = os.listdir(folderpath)
    files = [x for x in files if x.endswith('.json')]
    files = natsorted(files, key=lambda y: y.lower())
    for duplicate in files:
        mbid, dupnumber = parseduplication(duplicate)
        duplicatepath = os.path.join(folderpath, duplicate)
        with open(duplicatepath) as f:
            data = json.load(f)
            dupdict = comparisonfeatures(data)
            similarity = computesimilarity(mbid, dupdict)
