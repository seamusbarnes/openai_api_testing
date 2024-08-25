from openai import OpenAI
from datetime import datetime
import os
import json

def call_api_single(message_content,
                    client=None,
                    model=None,
                    system_prompt=None,
                    max_tokens=None,
                    temperature=None):
    model = 'gpt-4o' if not model else model
    system_prompt = 'You are a helpful assistant' if not system_prompt else system_prompt
    temperature = 1.0 if not temperature else temperature

    if not client:
        client = OpenAI()

    messages = [
        {
            'role': 'system',
            'content': system_prompt
        },
        {
            'role': 'user',
            'content': message_content
        }
    ]

    t0 = datetime.now()

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        n=1,
        max_tokens=max_tokens,
        response_format={'type': 'text'},
        temperature=temperature
    )

    t1 = datetime.now()
    return response, t0, t1

def get_response_cost(response):
    pricing_units = 1e6
    pricing = {'gpt-4o': (5.0, 15.0),
               'gpt-4o-2024-08-06': (2.5, 10.0),
               'gpt-4o-2024-05-13': (5.0, 15.0),
               'gpt-4o-mini': (0.150, 0.600),
               'gpt-4o-mini-2024-07-18': (0.150, 0.600),
               'chatgpt-4o-latest': (5.00, 15.00),
               'gpt-4-turbo': (10.00, 30.00),
               'gpt-4-turbo-2024-04-09': (10.00, 30.00),
               'gpt-4': (30.00, 60.00),
               'gpt-4-32k': (60.00, 120.00),
               'gpt-4-0125-preview': (10.00, 30.00),
               'gpt-4-1106-preview': (10.00, 30.00),
               'gpt-4-vision-preview': (10.00, 30.00),
               'gpt-3.5-turbo-0125': (0.50, 1.50),
               'gpt-3.5-turbo-instruct': (1.50, 2.00),
               'gpt-3.5-turbo-1106': (1.00, 2.00),
               'gpt-3.5-turbo-0613': (1.50, 2.00),
               'gpt-3.5-turbo-16k-0613': (3.00, 4.00),
               'gpt-3.5-turbo-0301': (1.50, 2.00),
               'davinci-002': (2.00, 2.00),
               'babbage-002': (0.40, 0.40)
               }
    
    model = get_response_model(response)
    input_tokens, output_tokens = get_response_tokens(response)

    input_rate, output_rate = pricing[model]
    input_cost = (input_tokens/pricing_units) * input_rate
    output_cost = (output_tokens/pricing_units) * output_rate

    return input_cost + output_cost

def get_response_model(response):
    return response.model

def get_response_tokens(response):
    return response.usage.prompt_tokens, response.usage.completion_tokens

def get_response_content(response):
    return response.choices[0].message.content

def get_response_metadata(response, verbose=True):

    model = get_response_model(response)
    input_tokens, output_tokens = get_response_tokens(response)
    cost = get_response_cost(response)

    return model, (input_tokens, output_tokens), cost

def log_interaction(
        response,
        user_input,
        timestamp_call,
        timestamp_response,
        data_path='data/',
        log_file='log.txt'):
    
    model, tokens, cost = get_response_metadata(response)
    response_message = get_response_content(response)
    response_time = (timestamp_response - timestamp_call).total_seconds()

    timestamp_call_str = timestamp_call.strftime('%Y-%m-%d %H:%M:%S')
    timestamp_response_str = timestamp_response.strftime('%Y-%m-%d %H:%M:%S')

    metadata = {"timestamp_call": timestamp_call_str,
                "timestamp_response": timestamp_response_str,
                "input_tokens": tokens[0],
                "output_tokens": tokens[1],
                "total_tokens": sum(tokens),
                "input_message": user_input,
                "response_message": response_message,
                "model": model,
                "cost ($)": f'{cost:.4f}',
                "response_time (s)": response_time,  # Example response time in seconds
            }
    
    with open(os.path.join(data_path, log_file), 'a') as file:
        json.dump(metadata, file, indent=4)
        file.write('\n')
    return