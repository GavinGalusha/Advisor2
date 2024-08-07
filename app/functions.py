import os
from dotenv import load_dotenv
import openai
from urllib.parse import urlparse
#from detoxify import Detoxify

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
    openai.api_key = openai_api_key

    # Define the persistence directory
    PERSIST_DIR = "./index_storage"
    PERSIST_DIR2 = "./index_storage2"

    # Check if storage already exists
    def create_index(directory, persist_dir):
        documents = SimpleDirectoryReader(directory).load_data()
        index = VectorStoreIndex.from_documents(documents)
        index.storage_context.persist(persist_dir=persist_dir)
        return index

    # Creating index for advising
    if not os.path.exists(PERSIST_DIR):
        os.makedirs(PERSIST_DIR)
        index = create_index("app/data/RAG_DATA", PERSIST_DIR)
    else:
        try:
            # Load the existing index
            storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
            index = load_index_from_storage(storage_context)
            print("Index loaded successfully for advising")
        except (ValueError, FileNotFoundError) as e:
            print(f"Error loading index: {e}")
            index = create_index("app/data/RAG_DATA", PERSIST_DIR)


    # Creating index for casual
    if not os.path.exists(PERSIST_DIR2):
        os.makedirs(PERSIST_DIR2)
        index2 = create_index("app/data/Advice", PERSIST_DIR2)
    else:
        try:
            # Load the existing index
            storage_context2 = StorageContext.from_defaults(persist_dir=PERSIST_DIR2)
            index2 = load_index_from_storage(storage_context2)
            print("Index loaded successfully for casual")
        except (ValueError, FileNotFoundError) as e:
            print(f"Error loading index: {e}")
            index2 = create_index("app/data/Advice", PERSIST_DIR2)

    chat_engine1 = index.as_chat_engine(chat_mode="context", verbose=True)
    chat_engine2 = index2.as_chat_engine(chat_mode="context", verbose=True)
    print("Setup tasks done, engines created")
    return chat_engine1, chat_engine2

def generate_text(chat_engine, prompt):
    response = chat_engine.chat(prompt)
    print(f"Response: {response}")
    html_response = '<p>' + '</p><p>'.join(response.response.split('\n')) + '</p>'
    return html_response






''' 
def is_inappropriate(text):
    results = Detoxify('original').predict(text)
    return results





#----------------------------------------------------- inserting into index



print(is_inappropriate("Have a nice day"))


 '''
