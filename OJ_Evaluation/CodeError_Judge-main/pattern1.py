import os
import yaml
import argparse
import numpy as np
import judger
import time

def load_config(filename):
    with open(filename, 'r') as config_file:
        config = yaml.safe_load(config_file)
    return config

def pass_at_k(n,c,k):
    """
    :param n: total number of samples
    :param c: number of correct samples
    :param k: k in pass@k
    """
    if n<k: # k can't be bigger than n
        return float('nan')
    elif n-c<k:
        return 1.0
    else:
        return 1.0-np.prod(1.0-k/np.arange(n-c+1,n+1))

def Main():
    config = load_config('config.yml')
    use_config = config['use_config']
    if use_config == True:
        problem_name = config['problem_name']
        multi_code_dir =  config['multi_code_dir']
        input_dir = config['input_dir']
        answer_dir = config['answer_dir']
        timeLimit = config['timeLimit']
        memoryLimit = config['memoryLimit']
        showDetails = config['showDetails']
    else: # An example of command: python pattern1.py --problem_name "A+B problem" --multi_code_dir D:/LocalJudgeData/MultiCode/ --input_dir D:/LocalJudgeData/Input/ --answer_dir D:/LocalJudgeData/Output/ --timeLimit 1 --memoryLimit 512 --showDetails False
        parser = argparse.ArgumentParser(description='Your program description here')
        parser.add_argument('--problem_name', type=str, help='The problem you want to test')
        parser.add_argument('--multi_code_dir', type=str, help='Path to code directory')
        parser.add_argument('--input_dir', type=str, help='Path to input directory')
        parser.add_argument('--answer_dir', type=str, help='Path to answer directory')
        parser.add_argument('--timeLimit', type=int, help='Time limit in seconds')
        parser.add_argument('--memoryLimit', type=int, help='Memory limit in megabytes')
        parser.add_argument('--showDetails', type=str, help='Show details (True or False)', choices=['True', 'False'])
        args = parser.parse_args()
        problem_name = args.problem_name
        multi_code_dir = args.multi_code_dir
        input_dir = args.input_dir
        answer_dir = args.answer_dir
        timeLimit = args.timeLimit
        memoryLimit = args.memoryLimit
        showDetails = args.showDetails
        if showDetails=="True": showDetails = True
        else: showDetails = False

    problems = os.listdir(input_dir) # All the problems in dataset
    codes = os.listdir(multi_code_dir)
    c_value, n_value = 0, len(codes)
    if problem_name not in problems: # Check if this problem exists
        print("This problem does not exist!")
    
    for i, code in enumerate(codes):
        print("code",i,' ',code)
        code_path = os.path.join(multi_code_dir, code)
        input_path = os.path.join(input_dir, problem_name)
        answer_path = os.path.join(answer_dir, problem_name)
        result = judger.judge(code_path, input_path, answer_path, timeLimit, memoryLimit, showDetails)
        # print(showDetails)
        if result=='AC':
            c_value = c_value+1
    
    for k_value in range(1,8):
        # print(n_value, c_value, k_value)
        print("k=",k_value," pass@k=",pass_at_k(n_value,c_value,k_value))

if __name__ == '__main__':
    start_time = time.time()
    Main()
    end_time = time.time()
    print(f"time cost: {end_time - start_time} s")