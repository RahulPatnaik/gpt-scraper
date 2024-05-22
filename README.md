# GPT-scraper
## Download the requirements:
   ```pip install -r requirements.txt``` in the terminal.
## The three types of chatbots:
- ```webscraper.py``` - running this file in the terminal, will allow you to use a chatbot that will ask you for a yes/no after every output. If the answer is not satisfactory, then the user can simply reply no, in which case the webscraper component will retrieve urls to use as a resource for its reply.
- ```webscraper2.py``` - this is a chatbot that will webscrape when it does not find the answer in the GPT database, and then store it in a documents.json so it can answer better next time without scraping the web.
- ```basicllm.py``` - this is a simple RAG chatbot which can work with textfiles or other supported filetypes.

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
