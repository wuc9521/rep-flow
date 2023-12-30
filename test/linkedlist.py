import json

linked_list = [
    {"screenshot": "screenshot_bash_arg:_100.png", "type": "Touch", "action": "ACTION_DOWN"},
    {"screenshot": "screenshot_bash_arg:_100.png", "type": "Touch", "action": "ACTION_UP"},
    {"screenshot": "screenshot_bash_arg:_-p.png", "type": "Touch", "action": "ACTION_DOWN"},
    {"screenshot": "screenshot_bash_arg:_-p.png", "type": "Touch", "action": "ACTION_UP"},
    {"screenshot": "screenshot_args:_[-p,_com.liuyaoli.myapplication,_-v,_500,_-throttle,_100].png", "type": "Touch", "action": "ACTION_DOWN"},
    {"screenshot": "screenshot_args:_[-p,_com.liuyaoli.myapplication,_-v,_500,_-throttle,_100].png", "type": "Touch", "action": "ACTION_UP"},
    {"screenshot": "screenshot_bash_arg:_-throttle.png", "type": "Touch", "action": "ACTION_DOWN"},
    {"screenshot": "screenshot_bash_arg:_-throttle.png", "type": "Touch", "action": "ACTION_UP"},
]

# Specify the file path
json_file_path = "linked_list_data.json"

# Dump the data to JSON file
with open(json_file_path, "w") as json_file:
    json.dump(linked_list, json_file, indent=2)

print(f"Data dumped to {json_file_path}")
