import cohere, json, markdown2
import sys

api_key = "uH6F1TxZgwc8RKA4d9DQhoZyYy54RX61hNbxI4ky"
co = cohere.ClientV2(api_key)

def main():
    if not api_key:
        print("Error: Please Configure The API Key.")
        sys.exit(1)

    model_name = "command-a-03-2025"
    conversation = [{"role": "system", "content": "You are a helpful assistant."}]

    print("==== cohere chatbot ====")

    while True:
        try:
            user_input = input("You: ").strip()
            if not user_input:
                continue
            if user_input.lower() in {"exit", "quit"}:
                print("bye!")
                break

            conversation.append({"role": "user", "content": user_input})
            
            response_stream = co.chat_stream(
                model=model_name,
                messages=conversation)
            
            assistant_response = ""

            print("Bot:", end=" ", flush=True)
            # for chunk in response_stream:
            #     if chunk.type == "content-delta":
            #         token_text = chunk.delta.message.content.text
            #         assistant_response += token_text
            #         print(token_text, end="", flush=True)

            buffer = ""
            token_text = ""
            for chunk in response_stream:
                if chunk.type == "content-delta":
                    token_text = chunk.delta.message.content.text
                    buffer += token_text
                    converted = markdown2.markdown(buffer)  # Convert Markdown to HTML
            print(converted, end="", flush=True)

            print("\n")
            # conversation.append({"role": "assistant", "content": assistant_response})

        except KeyboardInterrupt:
            print("\nbye!")
            break
        except Exception as e:
            print(f"\nerror : {e}\n")
            conversation.pop()
            continue

if __name__ == "__main__":
    main()