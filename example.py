from patheval import set_dataset, read_problems, evaluate_one
from pprint import pprint

def ask(prompt):
    # hook, this completion is from gpt-3.5-turbo
    return "vector<float>{1.5, 2.5, 3.5, 4.5, 5.5}, 1.0"

def your_model_or_approach_here(d):
    # query with custom prompt
    prompt = f"""Please fill the arguments tagged with <FILL_ME> to make the targeted assertion success.\n```{d['focal_method'] + d['target']}```"""
    completion = ask(prompt)
    # any post-processing if needed, for example:
    completion = completion.strip()
    return completion


set_dataset("patheval_cpp") # or "patheval_java" or "patheval_py" or "logic_bombs_c"
problems = read_problems()
problem = problems[0]
print(evaluate_one(problem, your_model_or_approach_here(problem))['pass'])

