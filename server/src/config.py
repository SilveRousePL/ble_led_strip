import json

def get_config():
    f = open('config.json',)
    config = json.load(f)
    return config
