from __future__ import division

%load_ext autoreload
%autoreload 2

import helper_functions as hf

raw_path = '../../data/raw/'
fnames = ['debate_091016.txt','debate_191016.txt']

with open(raw_path + fnames[0]) as f:

    data = [line for line in f.readlines()[1:] if line != '\n']

    data = (eval(d) for d in data)

    fields = ['text','timestamp_ms','geo','place','lang']
    data = ([hf.try_extract(d,f) for f in fields] for d in data)
    data = (d for d in data if (d[-1] == 'en') and (d[0] is not None) and (d[0][:2] != 'RT'))

    for chunk in hf.chunker(data,10000):
        print(chunk[0][0])


g = (i for i in range(1003))

for grp in grouper(g,100):
    print(sum(grp))

s = 'RT blah'

s[:2]
