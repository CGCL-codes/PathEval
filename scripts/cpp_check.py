import subprocess
import tempfile
from utils import load_data, dump_data
import os
import shutil

def compile_and_run(code):
    original_dir = os.getcwd()
    temp_dir = tempfile.TemporaryDirectory()
    os.chdir(temp_dir.name)
    with open("./a.cpp", "w") as f:
        f.write(code)

    compile_command = ['g++', "./a.cpp", '-o', './a.out', "-std=c++11", "-lcrypto", "-lssl"]
    compile_process = subprocess.run(compile_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if compile_process.returncode == 0:
        run_command = ['./a.out']
        try:
            run_process = subprocess.run(run_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10)
            output = run_process.stdout.decode('utf-8')
            error = run_process.stderr.decode('utf-8')
            rv = run_process.returncode
        except subprocess.TimeoutExpired:
            os.chdir(original_dir)
            shutil.rmtree(temp_dir.name) 
            return -1 , "runtime error", "Timeout"
    else:
        error = compile_process.stderr.decode('utf-8')
        rv = -1
        output = "compile error"
    os.chdir(original_dir)
    shutil.rmtree(temp_dir.name) 
    return rv, output, error

def check_one(d, completion):
    code = d['focal_method']
    target = d['target']
    target = target.replace("<FILL_ME>", completion)
    rv, output, error = compile_and_run(code + "\n" + target)
    return rv, output, error
