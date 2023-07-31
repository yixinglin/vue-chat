import tiktoken

def count_tokens(content, model_name = "gpt-3.5-turbo"):
    encoding = tiktoken.encoding_for_model(model_name)
    tokens = encoding.encode(content)
    num_tokens = len(tokens)
    return num_tokens

def count_tokens_from_list(messages: list):
    n = 0
    for m in messages:
        n += count_tokens(m["content"])
    return n

