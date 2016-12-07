from html.parser import HTMLParser
import re
import json
import datetime as dt

class Entry():
    def __init__(self, time):
        self.time = ''
        self.time_base = time
        self.speaker = ''
        self.text = ''

    @property
    def value(self):
        return {
            'time': self.time,
            'time_utc': self.get_utc_time(self.time_base, self.time),
            'speaker': self.speaker,
            'text': re.sub('(\.){2,}$','.',self.text)
            }

    @staticmethod
    def get_utc_time(base, delta):
        hr, min, sec = map(float, delta.split(':'))
        td = dt.timedelta(hours=hr, minutes=min, seconds=sec)
        return (base + td).isoformat() + 'Z'
        
        

class HTMLParseTable(HTMLParser):
    __outer_class = 'table-wrap load-transcript'
    __outer_tag = 'div'
    __inner_tags = {
            'th': 0,
            'strong': 0,
            'p': 0
        }
    
    __outer_capture = False
    __outer_instances = 0

    __entry = None
    __output = []
    __time = ''

    @property
    def output(self):
        return self.__output

    @property
    def time_start(self):
        return self.__time
    
    @time_start.setter
    def time_start(self, value):
        self.__time = dt.datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ" )

    
    def handle_starttag(self, tag, attrs):
        if not self.__outer_capture:        
            if tag == self.__outer_tag:
                if self.has_attribute(attrs, 'class', self.__outer_class):
                    self.__outer_capture = True
                    print('Found outer tag!')
                    
                if self.__outer_capture:
                    self.__outer_instances += 1
        if self.__outer_capture:
            if tag in self.__inner_tags.keys():
                self.__inner_tags[tag] += 1
            
    def handle_endtag(self, tag):
        if self.__outer_capture:
            if tag == self.__outer_tag:
                self.__outer_instances -= 1
            elif tag in self.__inner_tags.keys():
                self.__inner_tags[tag] -= 1
                if tag == 'p':
                    self.__output.append(self.__entry.value)

            if self.__outer_instances == 0:
                self.__outer_capture = False
                print('Found end tag!')

    def handle_data(self, data):
        if self.__outer_capture:
            if self.__inner_tags.get('th') > 0:
                m = re.search('(\d{2}\:\d{2}\:\d{2})', data)
                if m:
                    self.__entry = Entry(self.time_start)
                    self.__entry.time = m.group(1)
            elif self.__inner_tags.get('strong') > 0:
                self.__entry.speaker = data
            elif self.__inner_tags.get('p') > 0:
                self.__entry.text += data


    @staticmethod
    def has_attribute(attrs, key, value):
        found = False
        for k,v in attrs:
            if k == key and v == value:
                found = True
        return found
            
# Set the start time of the event as YYYY-MM-DDTHH:MM:SSZ
parser = HTMLParseTable()
ts = input('Event UTC Start Time (YYYY-MM-DDTHH:MM:SSZ):')
parser.time_start = ts

with open('index.html','r') as f:
    s = f.read()
    parser.feed(s)

with open('output.json', 'w') as f:
    json.dump(parser.output, f, sort_keys=True,indent=4, separators=(',', ': '))
