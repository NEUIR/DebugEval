refs_path = 'code_review/zero_shot/refs_zero_shot.txt'
pres_path = 'code_review/zero_shot/pres_zero_shot.txt'

reverse_refs_path = 'code_review_reverse/zero_shot/refs_zero_shot.txt'
reverse_pres_path = 'code_review_reverse/zero_shot/pres_zero_shot.txt'

path = 'debugevalsuite_task124.jsonl'

refs = ['Code-'+i.strip() for i in open(refs_path,'r',encoding='utf8').readlines()]
pres = [i.strip() for i in open(pres_path,'r',encoding='utf8').readlines()]

reverse_refs = ['Code-'+i.strip() for i in open(reverse_refs_path,'r',encoding='utf8').readlines()]
reverse_pres = [i.strip() for i in open(reverse_pres_path,'r',encoding='utf8').readlines()]


def read_data_file(path):
    data = []
    with open(path,'r',encoding='utf8') as file:
        for line in file:
            item = json.loads(line)
            if item['task4'] == 'True':
                data.append(item)
    return data


import json
import numpy as np

def judge(ref,pre):
    if ref in pre:
        return 1
    else:
        return 0

count = 0
dict = {}
all_1 = []
all_2 = []
all = []

data = read_data_file(path)

for item in data:
    language = item['language']
    major = item['major_error_type']
    if language not in dict.keys():
        dict[language] = {}
    if major not in dict[language].keys():
        dict[language][major] = []
    dict[language][major].append(judge(refs[count],pres[count]) and judge(reverse_refs[count],reverse_pres[count]))
    all_1.append(judge(refs[count],pres[count]))
    all_2.append(judge(reverse_refs[count],reverse_pres[count]))
    all.append(judge(refs[count],pres[count]) and judge(reverse_refs[count],reverse_pres[count]))
    count += 1

print(f"all:{np.mean(all)}")
print(len(all))

print(f"all_1:{np.mean(all_1)}")
print(len(all_1))

print(f"all_2:{np.mean(all_2)}")
print(len(all_2))


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
