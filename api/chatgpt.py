import openai
# Set up the OpenAI API client
openai.api_key = "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"

# Set up the model and prompt
model_engine = "text-davinci-003"

# Generate a response
def getResultChatGPT(prompt):
    completion = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    response = completion.choices[0].text
    print(response)
    return response
