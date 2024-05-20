from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.llms.openai import OpenAI


llm = OpenAI(model="gpt-3.5-turbo")
data = SimpleDirectoryReader(input_dir="data").load_data()
index = VectorStoreIndex.from_documents(data)

from llama_index.core.memory import ChatMemoryBuffer

memory = ChatMemoryBuffer.from_defaults(token_limit=3900)

chat_engine = index.as_chat_engine(
    chat_mode="condense_plus_context",
    memory=memory,
    llm=llm,
    context_prompt=(
        "You are a chatbot, able to have normal interactions, as well as talk"
        " about pokemon."
        "Here are the relevant documents for the context:\n"
        "{context_str}"
        "\nInstruction: Use the previous chat history, or the context above, to interact and help the user."
    ),
)

message = input('Enter something...\n')
response = chat_engine.chat(message)
print(response)
print('\n')

while message != 'exit' :
    message = input()
    response = chat_engine.stream_chat(message)
    for token in response.response_gen:
        print(token, end='')
    print('\n')    

