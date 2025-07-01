import cohere, json
import sys

api_key = "uH6F1TxZgwc8RKA4d9DQhoZyYy54RX61hNbxI4ky"
co = cohere.ClientV2(api_key)

def main(user_input=None):
    if not api_key:
        return("Error: Please Configure The API Key.")

    model_name = "command-a-03-2025"
    conversation = [{"role": "system", "content": "You are a helpful assistant."}]

    if not user_input:
        return "Input cannot be empty."

    conversation.append({"role": "user", "content": user_input})
    
    response_stream = co.chat_stream(
        model=model_name,
        messages=conversation)
    
    assistant_response = ""

    for chunk in response_stream:
        if chunk.type == "content-delta":
            token_text = chunk.delta.message.content.text
            assistant_response += token_text
            
            print(token_text, end="", flush=True)
            
    conversation.append({"role": "assistant", "content": assistant_response})    

if __name__ == "__main__":
    (main("hello my name is mohammad"))