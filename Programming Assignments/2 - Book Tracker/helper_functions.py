from openai import AzureOpenAI, DefaultHttpxClient

client = AzureOpenAI(
    api_key="abcdefg",
    api_version="2024-02-01",
    azure_endpoint = "https://cour-external-playground.openai.azure.com/",
    http_client=DefaultHttpxClient(verify=False)
    )

def get_llm_response(prompt):
    """This function takes as input a prompt, which must be a string enclosed in quotation marks,
    and passes it to OpenAI's GPT3.5 model. The function then saves the response of the model as
    a string.
    """
    
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages = [
            {
                "role": "system", 
                "content": "You are a helpful but terse AI assistant who gets straight to the point."
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.0,
    )
    response = completion.choices[0].message.content
    return response
