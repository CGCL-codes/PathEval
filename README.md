# PathEval: LLM Directed Input Generation Evaluation Set

This is an evaluation set for the directed/targeted input solving problem. We use it to benchmark the ability of large language models for generation input to reach a certain code location or particular result.

## Installation

### Linux (Debain)

Install gcc, g++ python3 and openjdk by the following commands.
```shell
apt update
apt install -y -q build-essential gcc g++ python3 python3-pip openjdk-11-jdk-headlessl
python3 -m pip install tqdm
```

### Docker
```shell
docker build -t patheval .
```

## Usage
**The evaluation will compile and execute untrusted model-generated data and code (see scripts/*_check.py). It is strongly encouraged not to run this project in a sandbox (e.g., docker container).**

### APIs
Users can simply use this dataset through a couple of apis.
```python
from patheval import set_language, read_problems, evaluate_one
# select the dataset that corresponds to the language
set_dataset("patheval_cpp") # or "patheval_java" or "patheval_py" or "logic_bombs_c"
# load the problems
problems = read_problems()
# give the completion from your LLMs and the evaluate result will return.
evaluate_one(problems[0], "your_completion_here")['pass'] # True / False
```

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

The samples are placed under `data` folder in `.jsonl` files, the samples in the three different files are semantically the same, but belong to different programming languages. 

An example c++ sample is shown as follw.
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

## Known Issues
There is a very small difference in the number of samples in the dataset for the three programming languages due to the fact that this dataset was converted from [HumanEval-X](https://huggingface.co/datasets/THUDM/humaneval-x) using our automated methodology, where a very small number of samples failed in this process and were discarded.

## Citation
This is originally created for our paper "Towards Understanding the Effectiveness of Large Language Models on Directed Test Input Generation" (ASE 2024, to appear). The preview version will be uploaded soon.