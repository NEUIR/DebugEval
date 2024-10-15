import json
import argparse
import os
from tqdm import tqdm
from gpt_runner import gpt_runner
from deepseek_runner import deepseek_runner
from Qwen_runner import Qwen_runner
# from vllm_runner import vllm_runner,get_llm_sampling_params,vllm_generate
from vllm_runner import vllm_runner
import response_post_process
import codellama_post_process
import fine_tune_post_process
import codeQwen_post_process
# from eval.error_type_identification import calc_accuracy
def read_jsonl_file(file_path):
    results = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            results.append(json.loads(line.strip()))
    return results


def write_jsonl_file(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as f:
        for line in data:
            f.write(json.dumps(line, ensure_ascii=False) + '\n')

def write_to_txt_file(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as f:
        for line in data:
            f.write(line + '\n')

def is_single_answer(answer):
    count = 0
    if '(A)' in answer:
        count += 1
    if '(B)' in answer:
        count += 1
    if '(C)' in answer:
        count += 1
    if '(D)' in answer:
        count += 1

    if count <= 1:
        return 1
    else:
        return 0
def calc_accuracy(refs_file, pres_file):
    refs = [x.strip() for x in open(refs_file, 'r', encoding='utf-8').readlines()]
    pres = [x.strip() for x in open(pres_file, 'r', encoding='utf-8').readlines()]
    assert len(refs) == len(pres)

    length = len(refs)
    count = 0
    for i in range(length):
        r = refs[i]
        p = pres[i]
        if r in p and is_single_answer(p):
            count += 1
    acc = round(count/length*100, 2)
    return acc

def calc_review_ACC(refs_file, pres_file):
    refs = ['Code-'+x.strip() for x in open(refs_file, 'r', encoding='utf-8').readlines()]
    pres = [x.strip() for x in open(pres_file, 'r', encoding='utf-8').readlines()]
    assert len(refs) == len(pres)

    length = len(refs)
    count = 0
    for i in range(length):
        r = refs[i]
        p = pres[i]
        if r in p:
            count += 1
    acc = round(count / length * 100, 2)
    return acc

def main():
    parser = argparse.ArgumentParser()
    # gpt-3.5-turbo-0125  gpt-4o-mini  gpt-3.5-turbo(gpt-3.5-turbo-0125)  deepseek-coder  deepseek-chat  qwen2-72b-instruct
    parser.add_argument("--model", type=str, default='', help="name to model")
    parser.add_argument("--data_path", type=str, default='', help="Path to data")
    parser.add_argument("--prompt_dir", type=str, default='', help="Path to prompt dir")
    parser.add_argument("--output_dir", type=str, default='', help="Path to output dir")
    parser.add_argument("--task", type=str, default="", help="Task name",choices=["error_code_localization","error_type_identification","code_repair","code_review","code_review_reverse","issue_generation"])
    parser.add_argument("--prompt_type", type=str, default="", help="Prompt type",choices=["zero_shot"])
    parser.add_argument("--platform", type=str, default="", help="Platform name",choices=["atcoder","leetcode","all"])
    parser.add_argument("--n", type=int, default=1, help="Number of samples to generate")
    parser.add_argument("--temperature", type=float, default=0.2, help="Temperature for sampling")
    parser.add_argument("--top_p", type=float, default=0.95, help="Top p for sampling")
    parser.add_argument("--max_tokens", type=int, default=1024, help="Max tokens for sampling")
    args = parser.parse_args()

    # read data
    print("Reading data from {}".format(args.data_path))
    data = read_jsonl_file(args.data_path)
    print("Data read successfully, total {} samples".format(len(data)))

    # select platform
    if args.platform != "all":
        data = [d for d in data if d['platform'] == args.platform]
        print("Selected platform: {}, total {} samples".format(args.platform, len(data)))

    # for error_code_localization we should filter the data that has error_code_snippet,error_code_snippet key is not ""
    if args.task == "error_code_localization":
        data = [d for d in data if d['task1_options'] != '']
        print("Selected task: {}, total {} samples".format(args.task, len(data)))

    if args.task == "error_type_identification":
        data = [d for d in data if d['task2_choice'] != '']
        print("Selected task: {}, total {} samples".format(args.task, len(data)))

    if args.task == "code_repair":
        print("Selected task: {}, total {} samples".format(args.task, len(data)))

    if args.task == "code_review":
        data = [d for d in data if d['task4'] == 'True']
        print("Selected task: {}, total {} samples".format(args.task, len(data)))

    if args.task == "code_review_reverse":
        data = [d for d in data if d['task4'] == 'True']
        print("Selected task: {}, total {} samples".format(args.task, len(data)))

    # read prompt
    if args.task == 'code_repair':
        if 'FT' in args.model and 'llama' in args.model and 'no_cot' in args.model:
            prompt_path = os.path.join(args.prompt_dir, args.task,'NO_COT','llama_fine_tune',
                                       "prompt_{}.txt".format(args.prompt_type))
            print("Reading prompt from {}".format(prompt_path))
            prompt_template = None
            with open(prompt_path, 'r', encoding='utf-8') as f:
                prompt_template = f.read()
            assert prompt_template is not None, "Prompt template is None"
            print("Prompt read successfully")
        elif 'FT' in args.model and 'deepseek' in args.model and 'no_cot' in args.model:
            prompt_path = os.path.join(args.prompt_dir, args.task,'NO_COT','deepseek_fine_tune',
                                       "prompt_{}.txt".format(args.prompt_type))
            print("Reading prompt from {}".format(prompt_path))
            prompt_template = None
            with open(prompt_path, 'r', encoding='utf-8') as f:
                prompt_template = f.read()
            assert prompt_template is not None, "Prompt template is None"
            print("Prompt read successfully")
        elif 'FT' in args.model and 'llama' in args.model and 'cot' in args.model:
            prompt_path = os.path.join(args.prompt_dir, args.task,'COT','llama_fine_tune',
                                       "prompt_{}.txt".format(args.prompt_type))
            print("Reading prompt from {}".format(prompt_path))
            prompt_template = None
            with open(prompt_path, 'r', encoding='utf-8') as f:
                prompt_template = f.read()
            assert prompt_template is not None, "Prompt template is None"
            print("Prompt read successfully")
        elif 'FT' in args.model and 'deepseek' in args.model and 'cot' in args.model:
            prompt_path = os.path.join(args.prompt_dir, args.task,'COT','deepseek_fine_tune',
                                       "prompt_{}.txt".format(args.prompt_type))
            print("Reading prompt from {}".format(prompt_path))
            prompt_template = None
            with open(prompt_path, 'r', encoding='utf-8') as f:
                prompt_template = f.read()
            assert prompt_template is not None, "Prompt template is None"
            print("Prompt read successfully")
        else:
            prompt_path = os.path.join(args.prompt_dir, args.task, "prompt_{}.txt".format(args.prompt_type))
            print("Reading prompt from {}".format(prompt_path))
            prompt_template = None
            with open(prompt_path, 'r', encoding='utf-8') as f:
                prompt_template = f.read()
            assert prompt_template is not None, "Prompt template is None"
            print("Prompt read successfully")
    else:
        if 'FT' in args.model and 'llama' in args.model:
            prompt_path = os.path.join(args.prompt_dir, args.task, 'llama_fine_tune',
                                       "prompt_{}.txt".format(args.prompt_type))
            print("Reading prompt from {}".format(prompt_path))
            prompt_template = None
            with open(prompt_path, 'r', encoding='utf-8') as f:
                prompt_template = f.read()
            assert prompt_template is not None, "Prompt template is None"
            print("Prompt read successfully")
        elif 'FT' in args.model and 'deepseek' in args.model:
            prompt_path = os.path.join(args.prompt_dir, args.task, 'deepseek_fine_tune',
                                       "prompt_{}.txt".format(args.prompt_type))
            print("Reading prompt from {}".format(prompt_path))
            prompt_template = None
            with open(prompt_path, 'r', encoding='utf-8') as f:
                prompt_template = f.read()
            assert prompt_template is not None, "Prompt template is None"
            print("Prompt read successfully")
        else:
            prompt_path = os.path.join(args.prompt_dir, args.task,"prompt_{}.txt".format(args.prompt_type))
            print("Reading prompt from {}".format(prompt_path))
            prompt_template = None
            with open(prompt_path, 'r', encoding='utf-8') as f:
                prompt_template = f.read()
            assert prompt_template is not None, "Prompt template is None"
            print("Prompt read successfully")
    # check output dir
    output_dir = os.path.join(args.output_dir, args.task, args.prompt_type)
    # if the output dir does not exist, create it
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    output_path = os.path.join(output_dir, "results_{}.jsonl".format(args.prompt_type))
    if not os.path.exists(output_path):
        remaining_data = data
    else:
        print("Reading existing results from {}".format(output_path))
        done_results = read_jsonl_file(output_path)
        done_ids = set([r['question_id'] for r in done_results])
        print("Existing results read successfully,total {} samples".format(len(done_results)))
        remaining_data = [d for d in data if d['question_id'] not in done_ids]
    print("Remaining {} samples to generate".format(len(remaining_data)))

    runner = None
    if "gpt" in args.model:
        runner = gpt_runner
    elif args.model == 'deepseek-chat' or args.model == 'deepseek-coder':
        runner = deepseek_runner
    elif args.model == 'qwen2-72b-instruct':
        runner = Qwen_runner
    else:
        runner = vllm_runner
        # llm, sampling_params = get_llm_sampling_params(args)

    # remaining_data = remaining_data[:10]
    # Inference
    if args.task == "error_code_localization":
        with open(output_path, "a") as f:
            for line in tqdm(remaining_data, desc="Generating samples", total=len(remaining_data)):
                try:
                    question_content = line['question_content']
                    buggy_code = line['buggy_code']
                    options = line['task1_options']
                    prompt = prompt_template.replace("%%%Task%%%",question_content).replace("%%%Incorrect_Solution%%%",buggy_code).replace("%%%Options%%%",options)
                    print("=====================================")
                    print("Prompt: ", prompt)
                    print("=====================================")
                    messages = [{"role": "user", "content": prompt}]
                    responses = runner(args, messages)
                    print("=====================================")
                    print("Responses: ", responses)
                    print("=====================================")
                    line['responses'] = responses
                    line['private_test_cases'] = ''
                    f.write(
                        json.dumps(line) + "\n"
                    )
                    f.flush()  # make sure the output is written to file
                except Exception as e:
                    line['responses'] = [repr(e)]
                    line['private_test_cases'] = ''
                    f.write(
                        json.dumps(line) + "\n"
                    )
                    f.flush()  # make sure the output is written to file
                    print(repr(e))

    elif args.task == "error_type_identification":
        with open(output_path, "a") as f:
            for line in tqdm(remaining_data,desc="Generating samples",total=len(remaining_data)):
                try:
                    question_content = line['question_content']
                    buggy_code = line['buggy_code']
                    prompt = prompt_template.replace("%%%Task%%%",question_content).replace("%%%Incorrect_Solution%%%",buggy_code)
                    print("=====================================")
                    print("Prompt: ", prompt)
                    print("=====================================")
                    messages = [{"role": "user", "content": prompt}]
                    responses = runner(args, messages)
                    print("=====================================")
                    print("Responses: ", responses)
                    print("=====================================")
                    line['responses'] = responses
                    line['private_test_cases'] = ''
                    f.write(
                        json.dumps(line) + "\n"
                    )
                    f.flush()  # make sure the output is written to file
                except Exception as e:
                    line['responses'] = [repr(e)]
                    line['private_test_cases'] = ''
                    f.write(
                        json.dumps(line) + "\n"
                    )
                    f.flush()  # make sure the output is written to file
                    print(repr(e))
    elif args.task == "code_repair":
        with open(output_path, "a") as f:
            for line in tqdm(remaining_data, desc="Generating samples", total=len(remaining_data)):
                try:
                    question_content = line['question_content']
                    buggy_code = line['buggy_code']
                    lang = line['language']
                    prompt = prompt_template.replace("%%%Task%%%", question_content).replace(
                        "%%%Incorrect_Solution%%%", buggy_code).replace("%%%lang%%%",lang)
                    print("=====================================")
                    print("Prompt: ", prompt)
                    print("=====================================")
                    messages = [{"role": "user", "content": prompt}]
                    responses = runner(args, messages)
                    print("=====================================")
                    print("Responses: ", responses)
                    print("=====================================")
                    line['responses'] = responses
                    line['private_test_cases'] = ''
                    f.write(
                        json.dumps(line) + "\n"
                    )
                    f.flush()  # make sure the output is written to file
                except Exception as e:
                    line['responses'] = [repr(e)]
                    line['private_test_cases'] = ''
                    f.write(
                        json.dumps(line) + "\n"
                    )
                    f.flush()  # make sure the output is written to file
                    print(repr(e))
    elif args.task == "code_review" or args.task == "code_review_reverse":
        with open(output_path, "a") as f:
            for line in tqdm(remaining_data, desc="Generating samples", total=len(remaining_data)):
                try:
                    question_content = line['question_content']
                    buggy_code = line['buggy_code']
                    correct_code = line['correct_code']
                    prompt = prompt_template.replace("%%%Task%%%",question_content).replace("%%%buggy_code%%%",buggy_code).replace("%%%correct_code%%%",correct_code)
                    print("=====================================")
                    print("Prompt: ", prompt)
                    print("=====================================")
                    messages = [{"role": "user", "content": prompt}]
                    responses = runner(args, messages)
                    print("=====================================")
                    print("Responses: ", responses)
                    print("=====================================")
                    line['responses'] = responses
                    line['private_test_cases'] = ''
                    f.write(
                        json.dumps(line) + "\n"
                    )
                    f.flush()  # make sure the output is written to file
                except Exception as e:
                    line['responses'] = [repr(e)]
                    line['private_test_cases'] = ''
                    f.write(
                        json.dumps(line) + "\n"
                    )
                    f.flush()  # make sure the output is written to file
                    print(repr(e))
    # Evaluation


    if args.task == "error_code_localization":
        if 'codellama' in args.model:
            if args.prompt_type == "zero_shot":
                post_process_func = codellama_post_process.post_process_error_code_localization_zero_shot
        elif 'codeQwen' in args.model:
            if args.prompt_type == "zero_shot":
                post_process_func = codeQwen_post_process.post_process_error_code_localization_zero_shot
        elif 'FT' in args.model:
            if args.prompt_type == "zero_shot":
                post_process_func = fine_tune_post_process.post_process_error_code_localization_zero_shot
        else:
            if args.prompt_type == "zero_shot":
                post_process_func = response_post_process.post_process_error_code_localization_zero_shot
        references = []
        predictions = []
        results_file = open(output_path, 'r', encoding='utf8')
        for elem in results_file:
            line = json.loads(elem)
            references.append(line['task1_answer'])
            predictions.append(post_process_func(line['responses'][0]))
        refs_file = os.path.join(output_dir, "refs_{}.txt".format(args.prompt_type))
        pres_file = os.path.join(output_dir, "pres_{}.txt".format(args.prompt_type))
        write_to_txt_file(refs_file, references)
        write_to_txt_file(pres_file, predictions)
        acc = calc_accuracy(refs_file, pres_file)
        print("Overall Accuracy: ", acc, "%")
    elif args.task == "error_type_identification":
        references = []
        predictions = []
        # 使用prompt_type来区分不同的评估函数
        if 'codellama' in args.model:
            if args.prompt_type == "zero_shot":
                post_process_func = codellama_post_process.post_process_error_type_identification_zero_shot
        elif 'codeQwen' in args.model:
            if args.prompt_type == "zero_shot":
                post_process_func = codeQwen_post_process.post_process_error_type_identification_zero_shot
        elif 'FT' in args.model:
            if args.prompt_type == "zero_shot":
                post_process_func = fine_tune_post_process.post_process_error_type_identification_zero_shot
        else:
            if args.prompt_type == "zero_shot":
                post_process_func = response_post_process.post_process_error_type_identification_zero_shot
        results_file = open(output_path,'r',encoding='utf8')
        for elem in results_file:
            line = json.loads(elem)
            choice = line['task2_choice']
            references.append(choice)
            predictions.append(post_process_func(line['responses'][0]))
        refs_file = os.path.join(output_dir, "refs_{}.txt".format(args.prompt_type))
        pres_file = os.path.join(output_dir, "pres_{}.txt".format(args.prompt_type))
        write_to_txt_file(refs_file, references)
        write_to_txt_file(pres_file, predictions)
        acc = calc_accuracy(refs_file, pres_file)
        print("Overall Accuracy: ", acc, "%")

    elif args.task == "code_repair":
        if 'codellama' in args.model:
            if args.prompt_type == "zero_shot":
                post_process_func = codellama_post_process.post_process_code_repair_zero_shot
        elif 'codeQwen' in args.model:
            if args.prompt_type == "zero_shot":
                post_process_func = codeQwen_post_process.post_process_code_repair_zero_shot
        elif 'FT' in args.model and 'no_cot' in args.model:
            if args.prompt_type == "zero_shot":
                post_process_func = fine_tune_post_process.post_process_code_repair_zero_shot
        else:
            if args.prompt_type == "zero_shot":
                post_process_func = response_post_process.post_process_code_repair_zero_shot

        python_path = os.path.join(output_dir, "python_{}.jsonl".format(args.prompt_type))
        java_path = os.path.join(output_dir, "java_{}.jsonl".format(args.prompt_type))
        cpp_path = os.path.join(output_dir, "cpp_{}.jsonl".format(args.prompt_type))

        python_file = open(python_path,'w',encoding='utf8')
        java_file = open(java_path,'w',encoding='utf8')
        cpp_file = open(cpp_path, 'w', encoding='utf8')

        results_file = open(output_path, 'r', encoding='utf8')
        for elem in results_file:
            line = json.loads(elem)
            language = line['language']
            groupy = {
                'question_id': line['question_id'],
                'responses': post_process_func(line['responses'][0])
            }
            if language == 'python':
                python_file.write(json.dumps(groupy)+'\n')
            elif language == 'java':
                java_file.write(json.dumps(groupy)+'\n')
            elif language == 'cpp':
                cpp_file.write(json.dumps(groupy)+'\n')
    elif args.task == "code_review":
        references = []
        predictions = []
        if 'codellama' in args.model:
            if args.prompt_type == "zero_shot":
                post_process_func = codellama_post_process.post_process_code_review_zero_shot
        elif 'codeQwen' in args.model:
            if args.prompt_type == "zero_shot":
                post_process_func = codeQwen_post_process.post_process_code_review_zero_shot
        elif 'FT' in args.model:
            if args.prompt_type == "zero_shot":
                post_process_func = fine_tune_post_process.post_process_code_review_zero_shot
        else:
            if args.prompt_type == "zero_shot":
                post_process_func = response_post_process.post_process_code_review_zero_shot
        results_file = open(output_path,'r',encoding='utf8')
        for elem in results_file:
            line = json.loads(elem)
            choice = 'A'
            references.append(choice)
            predictions.append(post_process_func(line['responses'][0]))
        refs_file = os.path.join(output_dir, "refs_{}.txt".format(args.prompt_type))
        pres_file = os.path.join(output_dir, "pres_{}.txt".format(args.prompt_type))
        write_to_txt_file(refs_file, references)
        write_to_txt_file(pres_file, predictions)
        acc = calc_review_ACC(refs_file, pres_file)
        print("Overall Accuracy: ", acc, "%")
    elif args.task == "code_review_reverse":
        references = []
        predictions = []
        if 'codellama' in args.model:
            if args.prompt_type == "zero_shot":
                post_process_func = codellama_post_process.post_process_code_review_zero_shot
        elif 'codeQwen' in args.model:
            if args.prompt_type == "zero_shot":
                post_process_func = codeQwen_post_process.post_process_code_review_zero_shot
        elif 'FT' in args.model:
            if args.prompt_type == "zero_shot":
                post_process_func = fine_tune_post_process.post_process_code_review_zero_shot
        else:
            if args.prompt_type == "zero_shot":
                post_process_func = response_post_process.post_process_code_review_zero_shot
        results_file = open(output_path,'r',encoding='utf8')
        for elem in results_file:
            line = json.loads(elem)
            choice = 'B'
            references.append(choice)
            predictions.append(post_process_func(line['responses'][0]))
        refs_file = os.path.join(output_dir, "refs_{}.txt".format(args.prompt_type))
        pres_file = os.path.join(output_dir, "pres_{}.txt".format(args.prompt_type))
        write_to_txt_file(refs_file, references)
        write_to_txt_file(pres_file, predictions)
        acc = calc_review_ACC(refs_file, pres_file)
        print("Overall Accuracy: ", acc, "%")



















if __name__ == '__main__':
    main()
