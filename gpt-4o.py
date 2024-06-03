import os
import json
from llama_index.core import Document, VectorStoreIndex, SimpleDirectoryReader
from llama_index.llms.openai import OpenAI
from llama_index.core.memory import ChatMemoryBuffer
from langchain_community.utilities import SerpAPIWrapper

# Function to create document from text
def create_document_from_text(text, title="Web Document"):
    return Document(text_content=text, metadata={"title": title})

# Function to update knowledge base with search results
def update_knowledge_base(chatbot_data, user_query, search_results, data_dir="data"):
    # Add search results to the knowledge base
    for result in search_results:
        document = create_document_from_text(result, title="Web Document")
        chatbot_data.append(document)
    
    # Save user query and search results to a JSON file
    json_data = {"message": user_query, "search_results": search_results}
    with open(os.path.join(data_dir, "search_results.json"), 'w') as f:
        json.dump(json_data, f)
    
    return chatbot_data

# Function to load data from a JSON file
def load_from_json(filename):
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        return {"message": "", "search_results": []}

# Initialize chatbot data
chatbot_data = SimpleDirectoryReader(input_dir="data").load_data()

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
        "You are a chatbot, able to have normal interactions, as well as talk about various topics."
        " When asked about new information or current events, search the web to find relevant and up-to-date articles or news topics."
        " Here are the relevant documents for the context:\n"
        "{context_str}"
        "\nInstruction: Use the previous chat history, or the context above, to interact and help the user."
        " If you cannot find useful information from the context or chat history, then ask the user for more context."
        " For opinion-based inputs or questions, provide a general response without deep analysis."
    ),
)

# Setup the web search functionality
search = SerpAPIWrapper(serpapi_api_key='')

# Function to save search results to JSON file
def save_search_results_to_json(user_query, search_results, data_dir="data"):
    # Save user query and search results to a JSON file
    json_data = {"message": user_query, "search_results": search_results}
    with open(os.path.join(data_dir, "search_results.json"), 'w') as f:
        json.dump(json_data, f)

# Chat loop
def chat_with_user():
    global index, chat_engine, chatbot_data
    
    while True:
        message = input('Enter something...\n')
        if message.lower() == 'exit':
            break
        
        # Perform web search
        search_results = search.run(message)
        
        # Update knowledge base with search results
        chatbot_data = update_knowledge_base(chatbot_data, message, search_results)
        
        # Save search results to JSON file
        save_search_results_to_json(message, search_results)
        
        # Recreate index with updated knowledge base
        index = VectorStoreIndex.from_documents(chatbot_data)
        
        # Recreate chat engine with updated index
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
        
        # Retrieve response from the LLM
        response = chat_engine.chat(message)
        print(response)
        print('\n')

if __name__ == "__main__":
    chat_with_user()
