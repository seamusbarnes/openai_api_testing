import os
from openai import OpenAI
from datetime import datetime
from utils_response import *
import os
import json

def api_conversation(
        message,
        messages=None,
        client=None,
        model='gpt-4o',
        system_prompt='You are a helpful assistant.',
        max_tokens=None,
        temperature=None):

    if not client:
        client = OpenAI()

    if not messages:
        messages = [{
            'role': 'system',
            'content': system_prompt
            }]
        
    messages.append({
        'role': 'user',
        'content': message
        })

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

    messages.append({
        'role': 'assistant',
        'content': get_response_content(response)
        })
    
    return response, messages, t0, t1      

def log_interaction(
        response,
        messages,
        t0,
        t1,
        new_chat,
        data_path='data/',
        log_file='log.txt'):
    
    model, tokens, cost = get_response_metadata(response)
    response_message = get_response_content(response)
    response_time = (t1 - t0).total_seconds()

    timestamp_call_str = t0.strftime('%Y-%m-%d %H:%M:%S')
    timestamp_response_str = t1.strftime('%Y-%m-%d %H:%M:%S')

    metadata = {"new_chat": new_chat,
                "timestamp_call": timestamp_call_str,
                "timestamp_response": timestamp_response_str,
                "input_tokens": tokens[0],
                "output_tokens": tokens[1],
                "total_tokens": sum(tokens),
                "message": messages,
                "most_recent_response": response_message,
                "model": model,
                "cost ($)": f'{cost:.4f}',
                "response_time (s)": response_time,  # Example response time in seconds
            }
    
    with open(os.path.join(data_path, log_file), 'a') as file:
        json.dump(metadata, file, indent=4)
        file.write('\n')
    return



def main():
    print("Welcome to the in-line chatgpt conversation environment")
    print("To exit environment, type 'exit()'")
    print("To see list of commands, type 'help()")
    
    client = OpenAI()
    message_count = 0
    cost = 0

    initial = True

    while True:
        print('--------------------')
        user_input = input(f"Enter message {message_count}: ")
        if user_input.lower() == 'exit()':
            print("End of session")
            break
        if user_input.lower() == 'help()':
            print("Available commands:")
            print("exit(): exits conversation")
            print("help(): displays this help message")
            print("print_conv_logs(): prints conversation history")
            print("print_conv_cost(): prints conversation total cost")
            continue

        if user_input.lower() == 'print_conv_logs()':
            try:
                for msg in messages:
                    print(msg)
            except UnboundLocalError as e:
                print(f'UnboundLocalError: cannot print conv logs before conversation has started')
            continue

        if user_input.lower() == 'print_conv_cost()':
            print(f'conversation cost: {cost:.4f} $')
            continue

        
        
        print(f'{datetime.now()}: User input sent')
        print(f'User message {message_count}: {user_input}')
        
        if initial:
            response, messages, t0, t1 = api_conversation(
                message=user_input,
                messages=None
                )
        else:
            response, messages, t0, t1 = api_conversation(
                message=user_input,
                messages=messages
                )

        log_interaction(
            response,
            messages,
            t0,
            t1,
            initial
        )

        initial = False
        
        response_message = get_response_content(response)
        cost += get_response_cost(response)
        print(' ')
        print(f'{datetime.now()}: Response received')
        print(f'Response message: {response_message}')
        print(' ')

        message_count += 1

if __name__ == "__main__":
    main()