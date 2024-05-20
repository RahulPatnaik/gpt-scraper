import requests
from bs4 import BeautifulSoup
from googleapiclient.discovery import build
from llama_index.core import Document, VectorStoreIndex, SimpleDirectoryReader
from llama_index.llms.openai import OpenAI
from llama_index.core.memory import ChatMemoryBuffer

# Function to search Google for relevant URLs based on the user query
def search_google(query):
    api_key = "AIzaSyCClUbP0_OWfCqG-uSnOQEVslOVnJOpLS8"
    cse_id = "84ab08697df3d4ff9"
    
    service = build("customsearch", "v1", developerKey=api_key)
    result = service.cse().list(q=query, cx=cse_id).execute()
    return result['items']

# Function to scrape webpage and extract text
def scrape_webpage(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raises HTTPError for bad responses
        soup = BeautifulSoup(response.content, 'html.parser')
        paragraphs = soup.find_all('p')
        text = ' '.join([p.get_text() for p in paragraphs])
        return text
    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve {url}: {e}")
        return ""

# Function to create document from text
def create_document_from_text(text, title="Web Document"):
    return Document(text_content=text, metadata={"title": title})

# Function to update knowledge base with scraped content
def update_knowledge_base(chatbot_data, urls):
    scraped_data = []
    for url in urls:
        content = scrape_webpage(url)
        if content:  # Only add content if scraping was successful
            document = create_document_from_text(content, title=f"Document from {url}")
            scraped_data.append(document)
    updated_data = chatbot_data + scraped_data
    return updated_data

# Load data from directory
initial_data = SimpleDirectoryReader(input_dir="data").load_data()

# Initialize chatbot data
chatbot_data = initial_data

# Setup the LLM and memory
llm = OpenAI(model="gpt-3.5-turbo")
memory = ChatMemoryBuffer.from_defaults(token_limit=3900)

# Create the chat engine
index = VectorStoreIndex.from_documents(chatbot_data)
chat_engine = index.as_chat_engine(
    chat_mode="condense_plus_context",
    memory=memory,
    llm=llm,
    context_prompt=(
        "You are a chatbot, able to have normal interactions, as well as talk"
        " about various topics."
        " Here are the relevant documents for the context:\n"
        "{context_str}"
        "\nInstruction: Use the previous chat history, or the context above, to interact and help the user."
    ),
)

# Chat loop
def chat_with_user():
    global chatbot_data, chat_engine
    
    while True:
        message = input('Enter something...\n')
        if message.lower() == 'exit':
            break
        
        # Try to answer the query using the built-in knowledge base
        response = chat_engine.chat(message)
        print("GPT Response:", response)
        
        # Ask the user if the response was satisfactory
        user_feedback = input("Was this answer helpful? (yes/no)\n")
        
        if user_feedback.lower() == 'yes':
            continue
        
        # If the response was not satisfactory, proceed with web scraping
        search_results = search_google(message)
        urls = [result['link'] for result in search_results[:3]]  # Limit to top 3 URLs
        
        if urls:
            print("Retrieved URLs from Google search:", urls)
            
            # Update knowledge base with scraped content
            chatbot_data = update_knowledge_base(chatbot_data, urls)
            
            # Clear the URLs list to save memory
            urls = []
            
            # Recreate index with updated knowledge base
            index = VectorStoreIndex.from_documents(chatbot_data)
            
            # Recreate chat engine with updated index
            chat_engine = index.as_chat_engine(
                chat_mode="condense_plus_context",
                memory=memory,
                llm=llm,
                context_prompt=(
                    "You are a chatbot, able to have normal interactions, as well as talk"
                    " about various topics."
                    " Here are the relevant documents for the context:\n"
                    "{context_str}"
                    "\nInstruction: Use the previous chat history, or the context above, to interact and help the user."
                ),
            )
            
            print("Knowledge base updated with scraped content.")
            # Get a new response after updating the knowledge base
            response = chat_engine.chat(message)
            print("Updated GPT Response:", response)
        else:
            print("No relevant URLs found.")

if __name__ == "__main__":
    chat_with_user()
