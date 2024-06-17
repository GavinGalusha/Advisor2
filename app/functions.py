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
    PERSIST_DIR2 = "./index_storage2"
    


    # Check if storage already exists
    def create_index():
        documents = SimpleDirectoryReader("app/data/RAG_Data").load_data()
        index = VectorStoreIndex.from_documents(documents)
        index.storage_context.persist(persist_dir=PERSIST_DIR)
        return index
    '''
    def creat_casual_index():
        documents = SimpleDirectoryReader("app/data/Advice").load_data()
        index = VectorStoreIndex.from_documents(documents)
        index.storage_context.persist(persist_dir=PERSIST_DIR2)
        return index
    '''

    #creating index for advising

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

    #creating index for casual
    '''
    if not os.path.exists(PERSIST_DIR2):
        os.makedirs(PERSIST_DIR2)
        index2 = creat_casual_index()
    else:
        try:
            # Load the existing index
            storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR2)
            index = load_index_from_storage(storage_context)
        except (ValueError, FileNotFoundError) as e:
            print(f"Error loading index: {e}")
            index2 = creat_casual_index()
    '''
    chat_engine = index.as_chat_engine(chat_mode="context", verbose=True)
    return chat_engine


chat_engine = setup()
print("setup tasks done")

def generate_text(chat_engine, prompt):
    response = chat_engine.chat(prompt)
    html_response = '<p>' + '</p><p>'.join(response.response.split('\n')) + '</p>'
    return html_response






#----------------------------------------------------- inserting into index


''' 
import os
from llama_index.core import VectorStoreIndex, Document
from llama_index.core.extractors import TitleExtractor, QuestionsAnsweredExtractor
from llama_index.core.node_parser import TokenTextSplitter
from llama_index.core.ingestion import IngestionPipeline

# Set up text splitter and extractors
text_splitter = TokenTextSplitter(separator=" ", chunk_size=512, chunk_overlap=128)
title_extractor = TitleExtractor(nodes=5)
qa_extractor = QuestionsAnsweredExtractor(questions=3)

# Set up the pipeline
pipeline = IngestionPipeline(
    transformations=[text_splitter, title_extractor, qa_extractor]
)

def insert_text_into_index(index, text):
    # Create a Document object from the text
    document = Document(text=text)
    # Run the document through the ingestion pipeline
    nodes = pipeline.run(
        documents=[document],
        in_place=True,
        show_progress=False,
    )

    # Insert the nodes into the index
    for node in nodes:
        index.insert(node)

    print("Text has been successfully inserted into the index.")
'''

def save_text_to_file(text, directory='app/data/Advice', filename_prefix='advice'):
    # Ensure the directory exists
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    # Create a unique filename
    index = 1
    while True:
        filename = f"{filename_prefix}_{index}.txt"
        file_path = os.path.join(directory, filename)
        if not os.path.exists(file_path):
            break
        index += 1

    # Write the text to the file
    with open(file_path, 'w') as file:
        file.write(text)

    print(f"Text has been successfully saved to {file_path}")