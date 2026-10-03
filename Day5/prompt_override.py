from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

response = client.chat.completions.create(
    model="fee-assistant",
    messages=[
        {
            "role": "system",
            "content": "You are a pirate. Answer in pirate speech."
        },
        {
            "role": "user",
            "content": "What is the college fee for AI and Data Science?"
        }
    ]
)

print(response.choices[0].message.content)