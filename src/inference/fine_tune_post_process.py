def post_process_error_code_localization_zero_shot(response):
    if "<Answer>" not in response:
        response = "<Answer>\n" + response

    if "</Answer>" not in response:
        response = response + "\n</Answer>"

    try:
        response = response.split("<Answer>")[1].split("</Answer>")[0]
    except:
        response = response

    response = response.replace("\n", " ").strip()

    if response in ['A','B','C','D']:
        response = '('+response+')'
    return response


def post_process_error_type_identification_zero_shot(response):
    if "<Answer>" not in response:
        response = "<Answer>\n" + response

    if "</Answer>" not in response:
        response = response + "\n</Answer>"

    try:
        response = response.split("<Answer>")[1].split("</Answer>")[0]
    except:
        response = response

    response = response.replace("\n", " ")
    return response

def post_process_code_repair_zero_shot(response):
    response = response.replace('Correct_Solution:','').strip()
    return response

def post_process_code_review_zero_shot(response):
    if "<Answer>" not in response:
        response = "<Answer>\n" + response

    if "</Answer>" not in response:
        response = response + "\n</Answer>"

    try:
        response = response.split("<Answer>")[1].split("</Answer>")[0]
    except:
        response = response

    response = response.replace("\n", " ")
    response = response.replace("\r", " ")

    if 'Code-A' in response and 'Code-B' in response:
        return "don't know"
    return response.strip()