import boto3
import requests
import json
import gradio as gr
import ollama

# Choose the model usage 'bedrock' or 'local' or 'lib'
# ensure to have valid AWS credentials to use bedrock
MODEL_USAGE = 'lib'

# bedrock model details
BEDROCK_MODEL_NAME = "anthropic.claude-3-haiku-20240307-v1:0"

# local model details
LOCAL_MODEL_URL = "http://localhost:11434/api/generate"
LOCAL_MODEL_NAME = "llama3"

headers = {
    'Content-Type': 'application/json',
}

conversation_history = []

def generate_response_using_lib(prompt):    
    response = ollama.chat(model='llama3', messages=[
      {
        'role': 'user',
        'content': prompt,
      },
    ])
    response_text = response['message']['content']
    print(response_text)
    return response_text

def generate_response_using_local_model(prompt):
    conversation_history.append(prompt)

    full_prompt = "\n".join(conversation_history)

    data = {
        "model": LOCAL_MODEL_NAME,
        "stream": False,
        "prompt": full_prompt,
    }

    response = requests.post(LOCAL_MODEL_URL, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        response_text = response.text
        data = json.loads(response_text)
        actual_response = data["response"]
        conversation_history.append(actual_response)
        return actual_response
    else:
        print("Error:", response.status_code, response.text)
        return None

def generate_message_using_bedrock(prompt):
    """
    Generates a message using the Anthropic Claude model.
    """
    bedrock_runtime = boto3.client(service_name='bedrock-runtime')
    model_id = BEDROCK_MODEL_NAME
    max_tokens = 1000
    user_message = [{
        "role": "user",
        "content": prompt
    }]
    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": max_tokens,
        "messages": user_message
    })
    response = bedrock_runtime.invoke_model(body=body, modelId=model_id)
    response_body = json.loads(response.get('body').read())
    response_text = response_body['content'][0]['text']
    return response_text

def generate_response(prompt):    
    if prompt is None or prompt == "":
        return None

    if MODEL_USAGE == 'bedrock':
        response = generate_message_using_bedrock(prompt)
    elif MODEL_USAGE == 'lib':
        response = generate_response_using_lib(prompt)
    else:    
        response = generate_response_using_local_model(prompt)
    return response

iface = gr.Interface(
    fn=generate_response,
    inputs=gr.Textbox(lines=2, placeholder="Enter your prompt here..."),
    outputs="text"
)

iface.launch()
