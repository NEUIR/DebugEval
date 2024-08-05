import backoff
import openai
from openai import OpenAI
import os
api_key = ""
@backoff.on_exception(backoff.expo, openai.RateLimitError)
def gpt_runner(args,messages):
    import openai

    openai.api_key = api_key  # 令牌处创建，获得
    openai.api_base = 'https://www.jcapikey.com/v1'

    openai.default_headers = {"x-foo": "true"}

    from openai import OpenAI

    client = OpenAI(
        api_key=api_key,
        base_url='https://www.jcapikey.com/v1'
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

