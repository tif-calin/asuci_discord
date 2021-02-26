import json
import datetime as dt

def save_json(data, path):
    '''
    saves a list or dict in json format with indent = 2
    '''
    with open(path, 'w') as f:
        f.write(json.dumps(data, indent = 2))

def load_json(path, default = None):
    '''
    tries to load a json file at a path
    if no such file exist returns default
    '''
    try:
        with open(path) as f:
            return json.load(f)
    except FileNotFoundError:
        return default

def get_by_kv(lst, key, val):
    '''
    for a list of dicts
    returns the first instance of the dict who's .key == val
    '''
    for d in lst:
        if d.get(key) == val: return d

def str_date(s, return_str = False):
    '''
    takes a string like "November 3, 2020", returns a datetime.datetime by default or str like "2020-11-03"
    '''
    s = s.strip().split()

    m = int(dt.datetime.strptime(s[0], '%B').month)
    d = int(s[1][:-1])
    y = int(s[3])

    dt = dt.datetime(y, m, d)

    if return_str: return str(dt.date())
    else: return dt 