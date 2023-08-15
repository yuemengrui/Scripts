# *_*coding:utf-8 *_*
# @Author : YueMengRui
import os
import json
from typing import List


def load_jsonl(json_path: str):
    data = []
    with open(json_path, 'r', encoding='utf-8') as f:
        for json_str in f:
            try:
                result = json.loads(json_str.strip('\n'))
                data.append(result)
            except:
                print('error', json_str)
    return data


def save_jsonl(data_list: List, json_path: str, mode='w', encoding='utf-8'):
    dir = os.path.dirname(os.path.abspath(json_path))
    if not os.path.exists(dir):
        print(dir)
        os.makedirs(dir)
    with open(json_path, mode=mode, encoding=encoding) as f:
        for entry in data_list:
            json.dump(entry, f, ensure_ascii=False)
            f.write('\n')
    print(f'save to {json_path}, size: {len(data_list)}')


def load_json(json_path: str, encoding='utf-8'):
    with open(json_path, mode='r', encoding=encoding) as f:
        data = json.load(f)
    return data


def save_json(data, json_path, mode='w', encoding='utf-8'):
    dir = os.path.dirname(os.path.abspath(json_path))
    if not os.path.exists(dir):
        print(dir)
        os.makedirs(dir)
    with open(json_path, mode=mode, encoding=encoding) as f:
        f.write(json.dumps(data, ensure_ascii=False))
