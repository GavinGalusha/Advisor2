import os
from dotenv import load_dotenv
from openai import OpenAI
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage,
)
from llama_index.core.storage.docstore.simple_docstore import SimpleDocumentStore
from llama_index.core.storage.kvstore.simple_kvstore import SimpleKVStore

# Load the environment variables from the .env file

def setup():
    load_dotenv()
    # Access your API key from environment variables
    openai_api_key = os.getenv('OPENAI_API_KEY')

    # Initialize the OpenAI client with your API key
    client = OpenAI(api_key=openai_api_key)

    # Define the persistence directory
    PERSIST_DIR = "./index_storage"


    # Check if storage already exists
    def create_index():
        documents = SimpleDirectoryReader("app/data/Course_Data").load_data()
        #chunked_documents = chunk_documents(documents)
        index = VectorStoreIndex.from_documents(documents)
        index.storage_context.persist(persist_dir=PERSIST_DIR)
        return index

    if not os.path.exists(PERSIST_DIR):
        os.makedirs(PERSIST_DIR)
        index = create_index()
    else:
        try:
            # Load the existing index
            storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
            index = load_index_from_storage(storage_context)
        except (ValueError, FileNotFoundError) as e:
            print(f"Error loading index: {e}")
            index = create_index()

    query_engine = index.as_query_engine(similarity_top_k=5)
    chat_engine = index.as_chat_engine()
    return chat_engine


chat_engine = setup()
print("setup tasks done")

def generate_text(chat_engine, prompt):
    response = chat_engine.chat(prompt)
    return response.response

def retrieve():
    pass

print(generate_text(chat_engine, "What are the mandatory classes for computer science major?"))
