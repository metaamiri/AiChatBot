import cohere, json
import sys

api_key = "uH6F1TxZgwc8RKA4d9DQhoZyYy54RX61hNbxI4ky"
co = cohere.ClientV2(api_key)

def main(user_input):
    if not api_key:
        print("Error: Please Configure The API Key.")
        sys.exit(1)

    model_name = "command-a-03-2025"
    conversation = [{"role": "system", "content": "You are a helpful assistant."}]

    print("==== cohere chatbot ====")

    while True:
        try:
            conversation.append({"role": "user", "content": user_input})
            
            response_stream = co.chat_stream(
                model=model_name,
                messages=conversation)
            
            assistant_response = ""

            for chunk in response_stream:
                if chunk.type == "content-delta":
                    token_text = chunk.delta.message.content.text
                    assistant_response += token_text
                    # print(token_text, end="", flush=True)

            conversation.append({"role": "assistant", "content": assistant_response})

        
        except Exception as e:
            print(f"\nerror : {e}\n")
            conversation.pop()
            continue
        
        return token_text

if __name__ == "__main__":
    main()