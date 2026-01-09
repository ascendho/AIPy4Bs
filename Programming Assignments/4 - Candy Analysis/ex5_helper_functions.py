from openai import AzureOpenAI, DefaultHttpxClient

client = AzureOpenAI(
    api_key="abcdefg",
    api_version="2024-02-01",
    azure_endpoint = "https://cour-external-playground.openai.azure.com/",
    http_client=DefaultHttpxClient(verify=False)
    )