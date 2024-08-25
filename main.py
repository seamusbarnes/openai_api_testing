# main.py

import os
from openai import OpenAI
from datetime import datetime
from utils import *
import json

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

def timestamp_pretty():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def main():
    print("Welcome to in-line gpt chat (type 'exit()' to exit)")
    
    client = OpenAI()

    while True:
        print('--------------------')
        user_input = input("Enter message: ")
        if user_input.lower() == 'exit()':
            print("End of session")
            break
        
        print(f'{timestamp_pretty()}: User input sent')
        print(f'User message: {user_input}')
        
        response, timestamp_call, timestamp_response = call_api_single(
            user_input,
            client=client
            )
        
        log_interaction(
            response,
            user_input,
            timestamp_call,
            timestamp_response
        )
        
        response_message = get_response_content(response)
        print(' ')
        print(f'{timestamp_pretty()}: Response received')
        print(f'Response message: {response_message}')
        print(' ')

if __name__ == "__main__":
    main()