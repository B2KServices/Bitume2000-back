import json


def read_file_as_json(fname):
    with open(fname) as f:
        content = f.read()
        if content == '':
            raise Exception('File is empty in read_file_ad_json')
        return json.loads(content)
