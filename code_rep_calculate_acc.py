import json
import numpy as np
result_path = '/python_result.jsonl'
data_path = 'debugevalsuite_task3_python.jsonl'

if 'python' in data_path:
    panduan = 'responses_success'
else:
    panduan = 'result'

question_error = {}

dict = {}

def read_jsonl_file(path):
    data = []
    with open(path,'r',encoding='utf8') as f:
        for line in f:
            item = json.loads(line)
            data.append(item)
    return data

results = read_jsonl_file(result_path)
datas = read_jsonl_file(data_path)

for elem in datas:
    question_error[elem['question_id']] = elem['major_error_type']

acc = []

for i,line in enumerate(results):
    error = question_error[line['question_id']]
    if line[panduan] == 'True':
        acc.append(1)
        if error not in dict.keys():
            dict[error] = []
        dict[error].append(1)
    else:
        acc.append(0)
        if error not in dict.keys():
            dict[error] = []
        dict[error].append(0)


print(dict)
print(f'average:{np.mean(acc)}')
print(dict.keys())
print(f'syntax:{np.mean(dict["syntax error"])}')
print(f'reference:{np.mean(dict["reference error"])}')
print(f'logic:{np.mean(dict["logic error"])}')
print(f'multiple:{np.mean(dict["multiple error"])}')

