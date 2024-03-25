from openai import OpenAI

client = OpenAI(
    api_key="XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
)

messages = [{
    "role": "system",
    "content": "You are a helpful assistant, that can assist in answering questions and providing information about "
               "upcoming and past festivals. If any other question is asked then some sort of information about "
               "festivals, respond with 'I do not have any knowledge about that! Ask me about festivals!'"
}]

while True:
    user_input = input("You: ")
    messages.append({
        "role": "user",
        "content": user_input,
    })

    chat_completion = client.chat.completions.create(
        messages=messages,
        model="gpt-4-0125-preview",
    )

    messages.append({
        "role": "assistant",
        "content": chat_completion.choices[0].message.content,
    })
    print("AI:", chat_completion.choices[0].message.content)
