import json

def clean(data):
    try:
        return json.loads(data)
    except:
        return data