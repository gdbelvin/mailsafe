import json
from google.appengine.ext import ndb

def default(obj):
    from datetime import date
    from datetime import datetime
    if isinstance(obj, datetime):
        return obj.isoformat()
    elif isinstance(obj, date):
        return oisoformat()
    elif isinstance(obj, ndb.Key):
        return obj.id()
    else:
        #return 
        raise TypeError(repr(obj) + " is not JSON serializable")

def dumps(obj):
    if type(obj) == list:
        return  "[" + ", ".join([dumps(x) for x in obj]) + "]"
    if type(obj) == dict:
        return json.dumps(obj, default=default)
    else:
        d = obj.to_dict()
        d['key'] = obj.key.id()
        return json.dumps(d, default=default)
