import openai
import os
# Set up the OpenAI API client
openai.api_key = os.environ.get('API_Key')

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

    if(len(prompt.split())<8):
        response = completion.choices[0].text
        ot = 0
    else:
        response = completion.choices[0].text
        ot = 1

    print(response,ot)
    return response,ot
