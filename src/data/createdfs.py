from __future__ import division

import helper_functions as hf

raw_path = '../../data/raw/'
processed_path = '../../processed/'
fnames = ['debate_091016.txt','debate_191016.txt']

with open(raw_path + fnames[0]) as f:

    data = [line for line in f.readlines()[1:] if line != '\n']

    data = (eval(d) for d in data)

    fields = ['text','timestamp_ms','geo','place','lang']
    data = ([hf.try_extract(d,f) for f in fields] for d in data)
    data = (d for d in data if (d[-1] == 'en') and (d[0] is not None) and (d[0][:2] != 'RT'))

    for ind,chunk in enumerate(hf.chunker(data,10000)):
        hf.make_df(chunk,ind,fnames[0])


with open(raw_path + fnames[1]) as f:

    data = [line for line in f.readlines()[1:] if line != '\n']

    data = (eval(d) for d in data)

    fields = ['text','timestamp_ms','geo','place','lang']
    data = ([hf.try_extract(d,f) for f in fields] for d in data)
    data = (d for d in data if (d[-1] == 'en') and (d[0] is not None) and (d[0][:2] != 'RT'))

    for ind,chunk in enumerate(hf.chunker(data,10000)):
        hf.make_df(chunk,ind,fnames[1])
