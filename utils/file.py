import os
import json

def get_i(id, i):
    LIST_DIR = os.path.join(os.path.dirname(__file__), '../data/list')
    i = int(i)
    try:
        with open(os.path.join(LIST_DIR, str(id)+'.json'),'r') as f:
            data = json.load(f)
        if 0 <= i < len(data):
            return data[i]['guidance']+'.png', i==len(data)-1
        else:
            return f"Index {i} is out of range."
    except Exception as e:
        return str(e)
