from itertools import islice
from numpy import array, nan

import pandas as pd
from tempfile import NamedTemporaryFile
import preprocessor as p
import re
import subprocess

def try_extract(d,field):
    try:
        return d[field]
    except Exception:
        return None


def chunker(iterable, n):
    iterable = iter(iterable)
    count = 0
    group = []
    while True:
        try:
            group.append(iterable.next())
            count += 1
            if count % n == 0:
                yield group
                group = []
        except StopIteration:
            yield group
            break

def extract_name(d):
    if d[3] != None:
        return d[3]['full_name']
    else:
        return None

def extract_centroid(d):
    if d[3] != None:
        return array(d[3]['bounding_box']['coordinates']).mean(axis=1)[0]
    else:
        return None

def make_df(data_chunk,i,base_fname):
    fname = '../../data/processed/{}_{}.csv'.format(base_fname,i)

    coords = [extract_centroid(d) for d in data_chunk]
    place_names = [extract_name(d) for d in data_chunk]
    tweets = [d[0] for d in data_chunk]
    dates = [pd.to_datetime(int(d[1])*1000000) for d in data_chunk]
    data_chunk = {'coord':coords,'place_name':place_names,'tweet':tweets,'date':dates}

    df = pd.DataFrame(data_chunk)
    df = df.drop_duplicates(subset=['tweet'])
    df = df.fillna(value=nan)

    df['long'] = df.iloc[:,0].map(lambda x : x[0],na_action='ignore')
    df['lat'] = df.iloc[:,0].map(lambda x : x[1],na_action='ignore')
    df = df.drop('coord',axis=1)

    regex = re.compile('[\.\t\,\:;\(\)\.\?\*\%\'\!\+\"]')
    df.tweets = df.tweet.map(lambda x : x.encode('utf-8').strip())
    df['cleaned_tweet'] = df.tweets.map(p.clean)
    df['cleaned_tweet'] = df.cleaned_tweet.map(lambda x : regex.sub('',x).lower())

    df = df.reset_index()
    df = df.drop('index',axis=1)

    t1 = NamedTemporaryFile()
    t2 = NamedTemporaryFile()
    t3 = NamedTemporaryFile()

    df.tweet.to_csv(t1.name,encoding='utf-8',index=False)
    df.cleaned_tweet.to_csv(t2.name,encoding='utf-8',index=False)

    subprocess.call('curl --data-binary @{} "http://www.sentiment140.com/api/bulkClassify" > {}'.format(t1.name,t3.name),shell=True)
    pols = pd.read_csv(t3.name,header=None)
    df['polarity'] = pols[0]

    subprocess.call('curl --data-binary @{} "http://www.sentiment140.com/api/bulkClassify" > {}'.format(t2.name,t3.name),shell=True)
    pols = pd.read_csv(t3.name,header=None)
    df['polarity_cl'] = pols[0]

    t1.close()
    t2.close()
    t3.close()

    df.to_csv(fname,encoding='utf-8')
