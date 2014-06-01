import json

def default(obj):
    from datetime import date
    from datetime import datetime
    if isinstance(obj, datetime):
        return obj.isoformat()
    elif isinstance(obj, date):
        return oisoformat()
    else:
        return 
        #raise TypeError(repr(obj) + " is not JSON serializable")

def dumps(obj):
    if type(obj) == list:
        return  "[" + ", ".join([dumps(x) for x in obj]) + "]"
    else:
        return json.dumps(obj.to_dict(), default=default)
