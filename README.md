# GPT-scraper
## Download the requirements:
   ```pip install -r requirements.txt``` in the terminal.
## The four types of chatbots:
- ```webscraper.py``` - this chabot will always try to webscrape everytime in-order to update its Vector storage database and then answer the user's question.
- ```webscraper2.py``` - running this file in the terminal, will allow you to use a chatbot that will ask you for a yes/no after every output. If the answer is not satisfactory, then the user can simply reply no, in which case the webscraper component will retrieve urls to use as a resource for its reply.
- ```basicllm.py``` - this is a simple RAG chatbot which can work with textfiles or other supported filetypes.
- ```gpt.py``` - The latest version of the chatbot, which web searches every time the user enters any input and uses that search result to reply. ALso handles opinions with contextual reasoning.

## Installation for gpt.py (latest one): 
1. ``` pip install -r requirements.txt ``` in the terminal.
2. Ensure that the working dircetory has a folder named ``` data ```.
3. Create a ``` .env ``` file in the same working directory and enter the ```OPENAI_API_KEY = <YOUR_API>``` in it.
4. ``` search = SerpAPIWrapper(serpapi_api_key='<API KEY>') ``` enter the SerpAPI key here for the web searching feature.

## SerpAPI: 
You can get your SerpAPI key from this website : https://serpapi.com/

## Customization:
```
    chat_engine = index.as_chat_engine(
    chat_mode="condense_plus_context",
    memory=memory,
    llm=llm,
    context_prompt=(
        "You are a chatbot, able to have normal interactions, as well as talk about various topics."
        " When asked about new information or current events, search the web to find relevant and up-to-date articles or news topics."
        " Here are the relevant documents for the context:\n"
        "{context_str}"
        "\nInstruction: Use the previous chat history, or the context above, to interact and help the user."
        " If you cannot find useful information from the context or chat history, then ask the user for more context."
        " For opinion-based inputs or questions, provide a general response without deep analysis."
    ),
)
```
You can change the ``` context_prompt ``` here to make the chatbot behave in a certain way.

Note: all these models have the RAG functionality.

The ```data.txt``` has to be stored in a folder named ```data``` within this repo to work.

## .env:
Lastly create a ```.env``` file in the working directory and add the ```OPENAI_API_KEY = <YOUR_API>``` in it.

## Google Search API:
https://developers.google.com/custom-search/v1/overview - Click this link to quickly create the API Key

You can also refer to - https://joeyism.medium.com/custom-google-search-api-fbbafe4711eb blog to understand how to get the API key as well as the CSE ID.

Once you have them, use them under the 
 ```
    api_key = ""
    cse_id = ""
 ```
#### Typing ```exit``` in the terminal will exit the chat.
