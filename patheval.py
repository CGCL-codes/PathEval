from utils import load_data, dump_data
from pprint import pprint
import tqdm
import argparse

dataset = None

datasets = {
     "patheval_cpp":"data/patheval_cpp.jsonl",
     "patheval_py":"data/patheval_py.jsonl",
     "patheval_java":"data/patheval_java.jsonl",
     "logic_bombs_c":"data/logic_bombs_c.jsonl",
}

def set_dataset(ds):
    global dataset
    global datasets
    if ds not in datasets.keys():
        raise Exception("no dataset.")
    dataset = ds

def read_problems() -> list:
    if dataset != None:
        return load_data(datasets[dataset])
    raise Exception("set_dataset should be called first.")

def debug_one(d:dict, completion:str):
        if dataset == "patheval_cpp":
            import scripts.cpp_check as c
            pprint(c.check_one(d, completion))
        elif dataset ==  "patheval_java":
            import scripts.java_check as c
            pprint(c.check_one(d, completion))
        elif dataset ==  "patheval_py":
            import scripts.py_check as c
            pprint(c.check_one(d, completion))
        elif dataset == "logic_bombs_c":
             import scripts.c_check as c
             pprint(c.check_one(d, completion))

def evaluate_one(d:dict, completion:str) -> True:
        if dataset == "patheval_cpp":
            import scripts.cpp_check as c
            rv, _, _ = c.check_one(d, completion)
        elif dataset ==  "patheval_java":
            import scripts.java_check as c
            rv, _, _ = c.check_one(d, completion)
        elif dataset ==  "patheval_py":
            import scripts.py_check as c
            rv, _, _ = c.check_one(d, completion)
        elif dataset == "logic_bombs_c":
             import scripts.c_check as c
             rv, _, _ = c.check_one(d, completion)
        d['pass'] = (rv == 0)
        d['completion'] = completion
        return d

def evaluate_all(problems, completions):
    for idx, problem in enumerate(problems):
        problems[idx]['pass'] = False
    for completion in tqdm.tqdm(completions):
        idx = completion['index']
        comp = completion['completion']
        d = evaluate_one(problems[idx], comp)
        if d['pass']:
             problems[idx]['pass'] = True
    pass_samples = list(filter(lambda x : x['pass'], problems))
    pass_rate = len(pass_samples) / len(problems)
    print(f"Pass Rate : {pass_rate} ({len(pass_samples)} / {len(problems)})")


def test():
    set_dataset("patheval_py")
    data = read_problems()
    d = data[0]
    assert evaluate_one(d, "[1.1, 2.2, 3.3], 2")['pass']

    set_dataset("patheval_java")
    data = read_problems()
    d = data[0]
    assert evaluate_one(d, "Arrays.asList(1.1, 2.2, 3.3), 2.0")['pass']

    set_dataset("patheval_cpp")
    data = read_problems()
    d = data[0]
    assert not evaluate_one(d, "vector<float>({1.1,2.2,3.3}), 2.0")['pass']
    assert evaluate_one(d, "vector<float>{1.5, 2.5, 3.5, 4.5, 5.5}, 0.5")['pass']

    catch = False
    try:
         set_dataset("123")
    except:
         catch = True
    assert catch


def main():
    parser = argparse.ArgumentParser(description='Process some command line arguments.')
    # Add arguments
    parser.add_argument('--dataset', type=str, required=True,
                        help='the selected dataset')
    parser.add_argument('-i', '--input', type=str, required=True,
                        help='the json file of index and completion from LLMs for each problem.')
    # Parse arguments
    args = parser.parse_args()

    set_dataset(args.dataset)
    problems = read_problems()
    try:
        completions = load_data(args.input)
    except Exception as e:
         print(e)
         exit(-1)
    evaluate_all(problems, completions)

if __name__ == "__main__":
    # test()
    main()