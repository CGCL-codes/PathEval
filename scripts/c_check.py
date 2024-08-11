import subprocess
import tempfile
import os
import shutil

includes = """
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <sys/time.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <errno.h>
#include <unistd.h>
#include <err.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netdb.h>
#include <arpa/inet.h>
#include <stdarg.h>
"""

def compile_and_run(code):
    original_dir = os.getcwd()
    temp_dir = tempfile.TemporaryDirectory()
    shutil.copytree("scripts/include", os.path.join(temp_dir.name, "include"))
    shutil.copytree("scripts/lib", os.path.join(temp_dir.name, "lib"))
    os.chdir(temp_dir.name)
    with open("./a.c", "w") as f:
        f.write(code)
    compile_command = ['gcc', "./a.c","lib/sha1.c", "lib/aes.c", "lib/crypto_utils.c", '-lm','-lcrypto', '-lpthread', '-o', './a.out', "-Iinclude"]
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
    rv, output, error = compile_and_run(includes + "\n" + code + "\n" + target)
    return rv, output, error


def test():
    import json
    with open("data/logic_bombs_c.jsonl") as f:
        data = [json.loads(s) for s in f.readlines()]
    for d in data:
        rv, output, error = check_one(d, "\"7\"")
        if "compile error" in output:
            print(d['focal_method'])
            print(error)
            raise Exception("Test fail, compilation error.")

if __name__ == "__main__":
    test()
