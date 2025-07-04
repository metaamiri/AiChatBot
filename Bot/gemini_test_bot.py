from google import genai
import time

client = genai.Client(api_key="API_KEY")

response = client.models.generate_content_stream(
    model="gemini-2.0-flash",
    contents=["hello"]
)

for chunk in response:
    print(chunk.text, end="", flush=True)
    time.sleep(0.1)  # Simulate processing delay


chat = client.chats.create(model="gemini-2.5-flash")

response = chat.send_message("my name is mohammad")
print(response.text)

response = chat.send_message("what is my name?")
print(response.text)

for message in chat.get_history():
    print(f'role - {message.role}',end=": ")
    print(message.parts[0].text)