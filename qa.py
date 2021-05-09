import openai

openai.api_key = "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"

def answer_question(text):
    response = openai.Completion.create(
        engine="davinci",
        prompt= text.strip() + "\nA:",
        temperature=0,
        max_tokens=100,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=["\n"]
        )
    return response["choices"][0]["text"]
