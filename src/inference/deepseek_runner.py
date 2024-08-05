import backoff
import openai

api_key = ""
@backoff.on_exception(backoff.expo, openai.RateLimitError)
def deepseek_runner(args,messages):

    from openai import OpenAI

    client = OpenAI(
        api_key=api_key,
        base_url="https://api.deepseek.com/v1"
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
