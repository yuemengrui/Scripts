# *_*coding:utf-8 *_*
# @Author : YueMengRui
import os


def chunk_file(input_file_path: str, output_dir: str, size: int = 1024 * 1024 * 1024):
    input_file = open(input_file_path, 'rb')

    part = 1
    while True:
        print(part)
        chunk = input_file.read(size)
        if not chunk:
            break

        chunk_path = os.path.join(output_dir, 'chunk_' + str(part))

        with open(chunk_path, 'wb') as f:
            f.write(chunk)

        part += 1


def merge_file(chunk_dir: str, chunk_num: int, target_file_path: str):
    with open(target_file_path, 'wb') as f:
        for i in range(1, chunk_num):
            print(i)
            chunk_path = os.path.join(chunk_dir, 'chunk_' + str(i))
            with open(chunk_path, 'rb') as chunk_f:
                data = chunk_f.read()

            f.write(data)
