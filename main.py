# main.py

import os
from openai import OpenAI
from datetime import datetime
from utils import *

def log_interaction(input_text, output_text, message_sent, message_received, log_file='log.txt'):
    with open(log_file, 'a') as file:

        # timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        timestamp = message_sent.strftime('%Y-%m-%d %H:%M:%S')
        file.write(f'{timestamp}: User input: {input_text}\n')
        
        # timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        timestamp = message_received.strftime('%Y-%m-%d %H:%M:%S')
        file.write(f'{timestamp}: Output: {output_text}\n\n')
    return

def timestamp_pretty():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def main():
    print("Welcome to in-line gpt chat (type 'exit()' to exit)")
    
    client = OpenAI()

    while True:
        user_input = input("Enter something: ")
        if user_input.lower() == 'exit()':
            print("Goodbye!")
            break
        
        print('waiting for response)')
        print(timestamp_pretty())
        response, message_sent, message_received = call_api_single(user_input, client=client)
        output = get_response_content(response)
        print(output)
        
        log_interaction(user_input, output, message_sent, message_received)

if __name__ == "__main__":
    main()