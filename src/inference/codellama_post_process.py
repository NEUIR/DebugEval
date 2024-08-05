def post_process_error_type_identification_zero_shot(response):
    response = response.split('\n')[0]
    response = response.replace("\n", " ")
    return response


def post_process_error_code_localization_zero_shot(response):
    response = response.split('\n')[0]
    response = response.replace("\n", " ")
    return response


def post_process_code_repair_zero_shot(response):
    if '```code' in response:
        response = response.split('```code')[-1].split('```')[0]
    elif '```cpp' in response:
        response = response.split('```cpp')[-1].split('```')[0]
    elif '```java' in response:
        response = response.split('```java')[-1].split('```')[0]
    elif '```python' in response:
        response = response.split('```python')[-1].split('```')[0]
    elif '```Python' in response:
        response = response.split('```Python')[-1].split('```')[0]
    elif '```code' not in response and '```cpp' not in response and '```python' not in response and '```java' not in response and '```' in response:
        response = response.split('```')[1]
    else:
        response = response
    if 'Correct_Solution:' in response:
        response = response.replace('Correct_Solution:', '')
    return response.strip()


def post_process_code_review_zero_shot(response):
    response = response.split('\n')[0]
    if 'the correct' in response.lower() and 'B' in response:
        return 'Code-A'
    if 'the correct' in response.lower() and 'A' in response:
        return 'Code-B'
    if '.' in response:
        response = response.split('.')[0]
    if 'Code-A' in response and 'Code-B' in response:
        return "don't know"
    return response



