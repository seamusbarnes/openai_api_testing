# utils_response.py

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