import argparse
import json
import os

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