import argparse
import json
import os


def parse_iofile():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_path", required=True, help="Input file path")
    parser.add_argument("-o", "--output_path", required=True, help="Output file path")
    args = parser.parse_args()
    return args

def load_data(file):
    with open(file) as f:
        return [json.loads(line) for line in f.readlines()]

def dump_data(data, file):
    if os.path.exists(file):
        print(f"{file} exists")
        exit()
    with open(file, "a") as f:
        for d in data:
            f.write(json.dumps(d) + "\n")
            f.flush()