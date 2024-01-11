import streamlit as st
import pandas as pd
import time
from io import StringIO
import os
import json
import subprocess

def parallel_request(messages, model, temperature, api_key, max_requests_per_minute = 200, max_tokens_per_minute = 4000, max_attempts = 5, logging_level = 10):
    """
    Make requests in system_message, user_message pairs. 
    format messages as a list of tuples, [(system_message_1, user_message_1), (system_message_2, user_message_2), ...]
    if system message is None, then it is a user message only
    """
    # remove 00temp.jsonl if it exists
    if os.path.exists('00temp.jsonl'):
        os.remove('00temp.jsonl')
    if os.path.exists('00temp_responses.jsonl'):
        os.remove('00temp_responses.jsonl')

    # create jsonl file 
    with open('00temp.jsonl', 'w') as outfile:
        for entry in messages:
            if entry[0] is None:
                data = {"model": model, "messages": [{"role": "user", "content": entry[1]}],"temperature": temperature}
            else:
                data = {"model": model, "messages": [{"role": "system", "content": entry[0]}, {"role": "user", "content": entry[1]}],"temperature": temperature}
            json.dump(data, outfile)
            outfile.write('\n')

    # Define the command to call the script
    command = [
        "python", "api_request_parallel_processor.py",
        "--requests_filepath", "00temp.jsonl",
        "--save_filepath", "00temp_responses.jsonl",
        "--request_url", "https://api.openai.com/v1/chat/completions",
        "--api_key", api_key,
        "--max_requests_per_minute", str(max_requests_per_minute),
        "--max_tokens_per_minute", str(max_tokens_per_minute),
        "--token_encoding_name", "cl100k_base",
        "--max_attempts", str(max_attempts),
        "--logging_level", str(logging_level)
    ]

    # Launch the Windows shell command and get the output
    output = subprocess.check_output(command, shell=True)

    # Decode the bytes to string and print the output
    print(output.decode("utf-8"))

    # read in responses
    with open('00temp_responses.jsonl', 'r') as f:
        responses = [json.loads(line) for line in f]
    request_messages_dict  = [response[0]['messages'] for response in responses]
    response_messages = [response[1]['choices'][0]['message']['content'] for response in responses]

    request_messages = []
    for rm in request_messages_dict:
        if len(rm) == 1: #contains only user message
            request_messages.append((None, rm[0]['content']))
        elif len(rm) == 2: #contains system and user message
            request_messages.append((rm[0]['content'], rm[1]['content']))
        else:
            raise Exception('Request message has no body')
    

    # remove 00temp.jsonl if it exists
    if os.path.exists('00temp.jsonl'):
        os.remove('00temp.jsonl')
    if os.path.exists('00temp_responses.jsonl'):
        os.remove('00temp_responses.jsonl')
    
    return request_messages, response_messages


# Function to simulate loading and analyzing the data
def analyze_data(data):
    # Placeholder for data analysis logic
    # Return dummy values for tokens count and estimated cost
    tokens_count = 1000  # Dummy value
    estimated_cost = 5.0  # Dummy value
    return tokens_count, estimated_cost

# Function to simulate execution of prompts
def execute_prompts(data):
    # Placeholder for execution logic
    # Simulate some processing time
    time.sleep(2)
    response_tokens = 500  # Dummy value
    return response_tokens

# Streamlit UI layout
st.title('Parallel Prompts - Execute OpenAI API Requests simultanously')

# api key input box
api_key = st.text_input("OpenAI API Key")

# Choose input method
input_method = st.radio("Choose input method:", ('Upload CSV File', 'Textbox Input'))

# File upload or Textbox for input
if input_method == 'Upload CSV File':
    uploaded_file = st.file_uploader("Upload CSV", type='csv')
    if uploaded_file is not None:
        # Read the file into a dataframe
        df = pd.read_csv(uploaded_file)
        data = df.to_csv(index=False)
else:
    user_input = st.text_area("Enter prompts", height=300)
    # if user_input:
    #     # # Convert textbox input to dataframe
    #     # data = StringIO(user_input)
    #     # df = pd.read_csv(data, header=None)
    #     # data = df.to_csv(index=False)
        
    #     # user input expects a list of tuples, [(system_message_1, user_message_1), (system_message_2, user_message_2), ...]

# # Load button
# Execute button (only visible after loading data)

if st.button('Execute Prompts'):
    t_start = time.time()
    with st.spinner('Executing...'):
      
        request = eval(user_input)
        request_messages, response_messages = parallel_request(request, "gpt-4-0613", 0, api_key=api_key, max_requests_per_minute = 200, max_tokens_per_minute = 4000, max_attempts = 5, logging_level = 10)
        
        t_completion = time.time() - t_start
        st.success(f"Execution Completed in {t_completion:.2f} seconds.")
        # # print response
        st.write("Responses:")
        for response in response_messages:
            st.write(response)
        

# Download results button (only visible after execution)
if 'download_button' in locals():
    if download_button.button('Download Results'):
        # Placeholder for download logic
        st.success("Results downloaded successfully.")

