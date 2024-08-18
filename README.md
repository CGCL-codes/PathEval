# PathEval: Evaluation Set for Directed Test Input Generation

This is an evaluation set for the problem of **directed/targeted test input generation**, especially targeting Large Language Models (LLMs).
The goal of directed test input (a.k.a. targeted test input) generation is to automatically generate test inputs to reach a certain code location or produce a particular result. 

Targeted input generation plays a crucial role in various software engineering and security tasks, including fuzzing, bug reproduction (where the target is the bug location), and test suite augmentation (where the target is the specific code to be covered). It has also been extensively integrated with conventional testing tools to enhance coverage and overall performance.

Constraint-based techniques, such as symbolic execution
and concolic testing, have been well-explored in this problem while Large Language Models (LLMs) have demonstrated exceptionally good performance in code understanding and reasoning. We use PathEval to benchmark the ability of LLMs to solve the problem of directed test input generation. 

## Installation

### Linux (Debian)
Install gcc, g++, python3 and openjdk by the following commands.
```shell
apt update
apt install -y -q build-essential gcc g++ python3 python3-pip openjdk-11-jdk-headless libssl-dev
python3 -m pip install tqdm

git clone https://github.com/CGCL-codes/PathEval.git
cd PathEval
```

### Docker
```shell
git clone https://github.com/CGCL-codes/PathEval.git
cd PathEval

docker build -t patheval .
docker run -it --rm patheval /bin/bash

# cd /work in container
```

## Usage
**The evaluation will compile and execute untrusted model-generated data and code (see scripts/*_check.py). It is strongly encouraged to run this project in a sandbox (e.g., docker container).**

Users can simply use this dataset through a couple of APIs.

**Example**
```python
from patheval import set_dataset, read_problems, evaluate_one
# select the dataset that corresponds to the language
set_dataset("patheval_cpp") # or "patheval_java" or "patheval_py" or "logic_bombs_c"
# load the problems
problems = read_problems()
# give the completion from your LLMs and the evaluate result will return.

# completion = query(...)
evaluate_one(problems[0], completion)['pass'] # True / False
```

Or you can validate offline with the script `patheval.py`:
```shell
python3 patheval.py --dataset patheval_java --input sample.jsonl
```
For the optional dataset see the documentation for `set_dataset` below.
The format of `sample.jsonl` is as follows, the order doesn't matter.
```text
{"index": 486, "completion": "\"Mary had a little lamb\", 4"}
{"index": 532, "completion": "\"Hello,Hello,world !\" "}
{"index": 572, "completion": "Arrays.asList(1.0, 2., 3.)"}
...
```
We expect that each question can have **one or more rows of answers (multiple rows of data with the same index)**. If a question does not have a corresponding answer, then it fails by default.

**APIs**

**`set_dataset(dataset_name)`**
- Purpose: Selects the dataset for evaluation.
- Parameters:
  - `dataset_name` (str): The name of the dataset to use. Valid values are:
    - `"patheval_cpp"`: C++ dataset
    - `"patheval_java"`: Java dataset
    - `"patheval_py"`: Python dataset
    - `"logic_bombs_c"`: logic bombs dataset (in C language)
- Returns: None

**`read_problems()`**
- Purpose: Loads the problems from the selected dataset.
- Parameters: None
- Returns: `problems` (list): A list of problems.

**`evaluate_one(problem, completion)`**
- Purpose: Evaluate the given completion for a single problem.
- Parameters:
  - `problem` (object): One problem from the `read_problems()` returned list.
  - `completion` (str): The completion generated by LLMs.
- Returns: the input `problem` dictionary, with an additional key:
  - `"pass"` (bool): Indicates whether the completion passes the problem

### Sample
For each sample, the following information is provided:
| Key | Description |
| ---- | -----------| 
| index | index in **this dataset** |
| humaneval_task_id | task id in **HumanEval** | 
| focal_method_name | function name of focal method |
| focal_method_para | parameters of focal method |
| focal_method_return_type | return value type of focal method |
| focal_method | code of focal method |
| target | code of target | 

*In logic_bombs samples, humaneval_task_id is replaced by logic_bombs_task_id.*

The samples are placed under the `data` folder in `.jsonl` files, the samples in the three different files are semantically the same, but belong to different programming languages. 

An example C++ sample is shown as follow.
```json
{
  "index": 180,
  "humaneval_task_id": "CPP/53",
  "focal_method_name": "add",
  "focal_method_para": "(int x,int y)",
  "focal_method_return_type": "int",
  "focal_method": "#include<stdio.h>\n#include<stdlib.h>\nusing namespace std;\n#include<algorithm>\n#include<math.h>\nint add(int x,int y){\n    return x+y;\n}",
  "target": "#undef NDEBUG\n#include<assert.h>\n\nint main(){\n\tauto result = add(<FILL_ME>);\n\tassert(result==5);\n}"
}
```
We use `<FILL_ME>` to mark the position for LLMs to fill in.

## DataSet Extension
We are trying to extend the dataset from real-world open-source projects, a sample is shown under `data/rw`. These samples will be added to this repo once finished.

## Known Issues
There is a very small difference in the number of samples in the dataset for the three programming languages due to the fact that this dataset was converted from [HumanEval-X](https://huggingface.co/datasets/THUDM/humaneval-x) using our automated methodology, where a very small number of samples failed in this process and were discarded.

## Citation
This is originally created for our paper "Towards Understanding the Effectiveness of Large Language Models on Directed Test Input Generation" (ASE 2024, to appear). The preview version will be uploaded soon.

```text
@inproceedings{jiang2024towards,
  title={Towards Understanding the Effectiveness of Large Language Models on Directed Test Input Generation},
  author={Zongze, Jiang and Ming, Wen and Jialun, Cao and Xuanhua, Shi and Hai, Jin },
  booktitle={39th {IEEE/ACM} International Conference on Automated Software Engineering,
                  {ASE} 2024, California, United States, October 27 - November 1, 2024},
  year={2024}
}
```