import json

refs_path = 'refs_zero_shot.txt'
pres_path = 'pres_zero_shot.txt'
path = 'debugevalsuite_task124.jsonl'

refs = [i.strip() for i in open(refs_path,'r',encoding='utf8').readlines()]
pres = [i.strip() for i in open(pres_path,'r',encoding='utf8').readlines()]

def read_data_file(path):
    data = []
    with open(path,'r',encoding='utf8') as file:
        for line in file:
            item = json.loads(line)
            if item['task2_choice'] != '':
                data.append(item)
    return data

data = read_data_file(path)

langs = [i['language'] for i in data]
errors = [j['major_error_type'] for j in data]


import numpy as np

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
def calc_accuracy(refs, pres):
    if refs in pres and is_single_answer(pres):
        return 1
    else:
        return 0


dict = {}
all_score = []
for k in range(len(refs)):
    acc = calc_accuracy(refs[k],pres[k])

    if langs[k] not in dict.keys():
        dict[langs[k]] = {}
    if errors[k] not in dict[langs[k]].keys():
        dict[langs[k]][errors[k]] = []
    dict[langs[k]][errors[k]].append(acc)
    all_score.append(acc)

print(dict)

print(f'all:{np.mean(all_score)}')

print(f'python_syntax:{np.mean(dict["python"]["syntax error"])}')
print(f'python_reference:{np.mean(dict["python"]["reference error"])}')
print(f'python_logic:{np.mean(dict["python"]["logic error"])}')
print(f'python_multiple:{np.mean(dict["python"]["multiple error"])}')
print(f'python_all:{np.mean(dict["python"]["syntax error"]+dict["python"]["reference error"]+dict["python"]["logic error"]+dict["python"]["multiple error"])}')

print(f'cpp_syntax:{np.mean(dict["cpp"]["syntax error"])}')
print(f'cpp_reference:{np.mean(dict["cpp"]["reference error"])}')
print(f'cpp_logic:{np.mean(dict["cpp"]["logic error"])}')
print(f'cpp_multiple:{np.mean(dict["cpp"]["multiple error"])}')
print(f'cpp_all:{np.mean(dict["cpp"]["syntax error"]+dict["cpp"]["reference error"]+dict["cpp"]["logic error"]+dict["cpp"]["multiple error"])}')

print(f'java_syntax:{np.mean(dict["java"]["syntax error"])}')
print(f'java_reference:{np.mean(dict["java"]["reference error"])}')
print(f'java_logic:{np.mean(dict["java"]["logic error"])}')
print(f'java_multiple:{np.mean(dict["java"]["multiple error"])}')
print(f'java_all:{np.mean(dict["java"]["syntax error"]+dict["java"]["reference error"]+dict["java"]["logic error"]+dict["java"]["multiple error"])}')



