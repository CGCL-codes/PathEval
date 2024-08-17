import os
import subprocess
import json
import tempfile
import tqdm
import sys
import shutil

def compile_and_run(focal_method, main):
    original_dir = os.getcwd()
    temp_dir = tempfile.TemporaryDirectory()
    os.chdir(temp_dir.name)
    with open("./Main.java", "w") as f:
        f.write(main)
    with open("./FocalMethod.java", "w") as f:
        f.write(focal_method)

    class_name = "Main"
    compile_command = ['javac', './Main.java', './FocalMethod.java']
    compile_process = subprocess.run(compile_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if compile_process.returncode == 0:
        run_command = ['java', class_name]
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

def check_one(d, filling):
    focal_method = d['focal_method']
    main = d['target']
    new_main = main.replace("<FILL_ME>", filling)
    prefix = "import java.util.*;\nimport java.lang.*;\n"
    new_main = prefix + new_main
    return compile_and_run(focal_method, new_main)