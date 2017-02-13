'''
Audio Processing Lab - Assignment 2, Task 4
Nestor Napoles, Feb. 2017

This scripts takes the duplicate files in the "dataset" folder
and generates a json with a reduced set of features from each of 
the duplications for that mbid.
'''

import os
import json
from natsort import natsorted

smalldataset = 'ab-duplicates100-2016-03-02'
largedataset = 'ab-duplicates1000-2016-03-02'

dataset = largedataset

outdir = '{}_reduced'.format(dataset)
features = {}

if not os.path.exists(outdir):
    os.makedirs(outdir)

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

curr_mbid = ''
skip = False

for folder in os.listdir(dataset):
    print '{}...'.format(os.path.join(dataset,folder))
    folderpath = os.path.join(dataset, folder)
    files = os.listdir(folderpath)
    files = [x for x in files if x.endswith('.json')]
    files = natsorted(files, key=lambda y: y.lower())
    for duplicate in files:
        mbid, dupnumber = parseduplication(duplicate)
        if mbid != curr_mbid:
            # Write the previous mbid file
            if not skip and curr_mbid != '':
                with open(outpath,'w') as o:
                    json.dump(features, o)
            # Now compute the path for the upcoming file
            outpath = os.path.join(outdir, '{}.json'.format(mbid))
            if not os.path.exists(outpath):
                skip = False
                print '\tWriting {}...'.format(outpath)
                features = {
                'length':[],
                'replay_gain':[],
                'average_loudness':[],
                'bpm':[],
                'onset_rate':[],
                'beats_count':[],
                'chords_histogram':[[],[],[],[],[],[],
                                    [],[],[],[],[],[],
                                    [],[],[],[],[],[],
                                    [],[],[],[],[],[]],
                'hpcp_mean':[[],[],[],[],[],[],
                            [],[],[],[],[],[],
                            [],[],[],[],[],[],
                            [],[],[],[],[],[],
                            [],[],[],[],[],[],
                            [],[],[],[],[],[]],
                'key_key':[],
                'key_scale':[],
                'key_strength':[],
                'tuning_frequency':[]
                }
            else:
                skip = True
                print '\tSkipping {}...'.format(outpath)
        curr_mbid = mbid
        if skip:
            continue
        else:
            duplicatepath = os.path.join(folderpath, duplicate)
            with open(duplicatepath) as f:
                data = json.load(f)
                dupdict = comparisonfeatures(data)
                for key in dupdict:
                    if key == 'hpcp_mean' or key == 'chords_histogram':
                        for i,value in enumerate(dupdict[key]):
                            features[key][i].append(value)
                    else:
                        features[key].append(dupdict[key])
# Write the last element
if not skip:
    with open(outpath,'w') as o:
        json.dump(features, o)
