import cohere
api_key = "uH6F1TxZgwc8RKA4d9DQhoZyYy54RX61hNbxI4ky"
co = cohere.ClientV2(api_key)

response = co.chat_stream(
    model="command-a-03-2025",
    messages=[{"role": "user", "content": "write a tweet about cohere"}]
)

for event in response:
    if event.type == "content-delta":
        print(event.delta.message.content.text, end="")
