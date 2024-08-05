from utils import check_correctness as apps_check_correctness
import json
import re
from tqdm import tqdm
import os

def read_jsonl_file(file_path):
    """
    Read data from file_path, and return a list of data
    :param file_path: The file path to read
    :return: The data read from file_path
    """
    results = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            results.append(json.loads(line.strip()))
    return results


def write_jsonl_file(file_path, data):
    """
    Write data to file_path
    :param file_path: The file path to write
    :param data: The data to write
    :return:
    """
    with open(file_path, 'w', encoding='utf-8') as f:
        for line in data:
            f.write(json.dumps(line, ensure_ascii=False) + '\n')


def check_comp_code_success(solution, reference):
    try:
        res,metadata= apps_check_correctness(
            in_outs=reference,
            generation=solution,
            timeout=90,
            # debug=False
            debug=True
        )
        print("res:", res)
        print("metadata:", metadata)
        success = all(map(lambda x: x == True, res))
    except Exception as e:
        print(e)
        success = False
        metadata = None
    return success, metadata

def convert_testcases_format(private_test_cases):
    reference = {}
    inputs = []
    outputs = []
    # if private_test_cases is not a list, convert it to a list
    if not isinstance(private_test_cases, list):
        private_test_cases = json.loads(private_test_cases)
    for testcase in private_test_cases:
        inputs.append(testcase['input'])
        outputs.append(testcase['output'])
    reference['inputs'] = inputs
    reference['outputs'] = outputs
    return reference

def main(file_path,output_path,private_test_cases_path):
    path = file_path
    print("loading data from", path)
    data = read_jsonl_file(path)
    print("data loaded, total", len(data), "items")

    private_test_cases = []

    with open(private_test_cases_path) as file:
        for line in file:
            private_test_cases.append(json.loads(line))

    # new_data根据question_id排序

    new_data = sorted(data, key=lambda x: x['question_id'])
    new_test_cases = sorted(private_test_cases, key=lambda x:x['question_id'])

    check_data = []
    for i,line in enumerate(tqdm(new_data)):
        check_dict = {}
        responses = line['responses']
        assert line['question_id'] == new_test_cases[i]['question_id'],"the question isn't same"
        reference = convert_testcases_format(new_test_cases[i]['private_test_cases'])
        responses_success,responses_metadata = check_comp_code_success(responses, reference)

        print("question_id:", line['question_id'])
        print("responses_success:", responses_success)
        print("responses_metadata:", responses_metadata)
        check_dict['question_id'] = str(line['question_id'])
        check_dict['responses'] = str(line['responses'])
        check_dict['responses_success'] = str(responses_success)
        check_dict['responses_metadata'] = str(responses_metadata)
        check_data.append(check_dict)
        print("===")
    write_jsonl_file(output_path, check_data)


    print("Done!")
if __name__ == '__main__':
    path = '/data3/yangweiqing/result/gpt-4o-mini/code_repair/zero_shot/python_zero_shot.jsonl'
    out = '/data3/yangweiqing/result/gpt-4o-mini/code_repair/zero_shot/python_result.jsonl'
    private_test_cases_path = '/data2/yangweiqing/repairbench/atcoder_private_test_cases.jsonl'
    main(path,out,private_test_cases_path)