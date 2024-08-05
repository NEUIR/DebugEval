import os
import yaml
import judger
import argparse
import time
import json
import numpy as np

def load_config(filename):
    with open(filename, 'r') as config_file:
        config = yaml.safe_load(config_file)
    return config

def Main(path):
    f = open(path,'w',encoding='utf8')
    config = load_config('config.yml')
    use_config = config['use_config']
    all_result = []
    if use_config == True:
        code_dir =  config['code_dir']
        input_dir = config['input_dir']
        answer_dir = config['answer_dir']
        timeLimit = config['timeLimit']
        memoryLimit = config['memoryLimit']
        showDetails = config['showDetails']
        print('============================')
        print(code_dir)
        print('============================')
    else: # An example of command: python pattern2.py --code_dir D:/LocalJudgeData/Code/ --input_dir D:/LocalJudgeData/Input/ --answer_dir D:/LocalJudgeData/Output/ --timeLimit 1 --memoryLimit 512 --showDetails True
        parser = argparse.ArgumentParser(description='Your program description here')
        parser.add_argument('--code_dir', type=str, help='Path to code directory')
        parser.add_argument('--input_dir', type=str, help='Path to input directory')
        parser.add_argument('--answer_dir', type=str, help='Path to answer directory')
        parser.add_argument('--timeLimit', type=int, help='Time limit in seconds')
        parser.add_argument('--memoryLimit', type=int, help='Memory limit in megabytes')
        parser.add_argument('--showDetails', type=str, help='Show details (True or False)', choices=['True', 'False'])
        args = parser.parse_args()
        code_dir = args.code_dir
        input_dir = args.input_dir
        answer_dir = args.answer_dir
        timeLimit = args.timeLimit
        memoryLimit = args.memoryLimit
        showDetails = args.showDetails
        if showDetails=="True": showDetails = True
        else: showDetails = False


    problems = os.listdir(code_dir) # name of all problems
    for i,problem in enumerate(problems):
        try:
            print('\nproblem',(i+1),':',problem)
            code_path = os.path.join(code_dir, problem)
            input_path = os.path.join(input_dir, problem)
            answer_path = os.path.join(answer_dir, problem)

            code_files = os.listdir(code_path)
            allowed_code_extensions = {".c", ".cpp", ".java", ".py"}
            filtered_files = [f for f in code_files if os.path.isfile(os.path.join(code_path, f)) and os.path.splitext(f)[-1] in allowed_code_extensions]
            input_cnt = len(os.listdir(input_path))
            answer_cnt = len(os.listdir(answer_path))
            if len(filtered_files)==0:
                print('Error: No code file!\n')
            elif input_cnt != answer_cnt:
                print('Error: Different number of input and answer!\n')
            else:
                for j, code in enumerate(filtered_files):
                    print("code",j,' ',code)
                    code_file_path = os.path.join(code_path, code)
                    result = judger.judge(code_file_path, input_path, answer_path, timeLimit, memoryLimit, showDetails)
                    groupy = {
                        'question_id':problem,
                        'result':result
                    }
                    f.write(json.dumps(groupy)+'\n')
                    f.flush()
                    if result == 'AC':
                        all_result.append(1)
                    else:
                        all_result.append(0)
        except:
            print('error')
    print(f'pass@1:{np.mean(all_result)}')
                
if __name__ == '__main__':
    out_path = ''
    print(out_path)
    start_time = time.time()
    Main(out_path)
    end_time = time.time()
    print(f"time cost: {end_time - start_time} s")