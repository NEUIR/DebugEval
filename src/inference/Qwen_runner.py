from openai import OpenAI
import os

def Qwen_runner(args,messages):

    client = OpenAI(
        api_key='',
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",  # 填写DashScope服务的base_url
    )
    response = client.chat.completions.create(
        model=args.model,
        messages=messages,
        max_tokens=args.max_tokens,
        temperature=args.temperature,
        top_p=args.top_p,
        stop=[],
        n=args.n
    )
    responses = [response.choices[i].message.content for i in range(args.n)]
    return responses

