#!/usr/bin/env python3
"""Test json on python"""

import json

def readjson():
    with open('config.json', 'r') as json_file:
        info_dict = json.load(json_file)
        print(info_dict)
readjson()
