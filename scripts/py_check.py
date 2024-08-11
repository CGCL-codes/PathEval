import os
import json
import tempfile
import subprocess
import tqdm

def compile_and_run(code):
    temp_dir = tempfile.TemporaryDirectory()
    file_path = os.path.join(temp_dir.name, "temp.py")
    with open(file_path, "w") as f:
        f.write(code)
    try:
        result = subprocess.run(["python3", file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10)
        output = result.stdout.decode("utf-8")
        stderr = result.stderr.decode("utf-8")
    except subprocess.TimeoutExpired:
        temp_dir.cleanup()
        return -1 , "runtime error", "Timeout"

    temp_dir.cleanup()
    return result.returncode, output, stderr

def check_one(d, filling):
    target = d['target']
    focal_method = d['focal_method']
    target = target.replace("<FILL_ME>", filling)
    return compile_and_run(focal_method + "\n" + target)
