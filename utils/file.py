import os

def get_i(directory_path, i):
    i = int(i)
    try:
        items = os.listdir(directory_path)
        if 0 <= i < len(items):
            # return os.path.join(directory_path, items[i])
            return items[i]
        else:
            return f"Index {i} is out of range."
    except Exception as e:
        return str(e)
