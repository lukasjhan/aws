import json

def load_config(stage: str):
    with open('config.json') as config:
        return json.load(config)[stage]