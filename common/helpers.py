from pathlib import Path
import json
import re
import os


def get_userdata_dict(file='userdata.json', base_url=None):
    test_data_file = Path(__file__).parent.parent.absolute() / 'data' / file
    env = get_test_env()
    if base_url:
        test_env = get_reg_exp_match('://(.*?)\.', base_url)
    elif env:
        test_env = env
    else:
        test_env = 'test'
    with open(test_data_file) as json_file:
        user_data = json.load(json_file)
    return user_data[test_env]

def get_reg_exp_match(pattern, string):
    match = re.search(pattern, string, re.IGNORECASE)
    title = match.group(1) if match else None
    return title

def get_test_env():
    return os.getenv('TEST_ENV', None)
