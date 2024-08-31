import json

refs = "refs_zero_shot.txt"
pres = "pres_zero_shot.txt"
path = "debugevalsuite_task124.jsonl"

refs = [i.strip() for i in open(refs,'r',encoding='utf8').readlines()]
pres = [i.strip() for i in open(pres,'r',encoding='utf8').readlines()]

def read_data_file(path):
    data = []
    with open(path,'r',encoding='utf8') as file:
        for line in file:
            item = json.loads(line)
            if item['task1_options'] != '':
                data.append(item)
    return data

data = read_data_file(path)
language = [i['language'] for i in data]



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
    if language[k] not in dict.keys():
        dict[language[k]] = []
    dict[language[k]].append(acc)
    all_score.append(acc)

print(dict)
print(len(dict['cpp']))
print(len(dict['java']))
print(len(dict['python']))
print(f'cpp:{np.mean(dict["cpp"])}')
print(f'java:{np.mean(dict["java"])}')
print(f'python:{np.mean(dict["python"])}')
print(f'all:{np.mean(all_score)}')
