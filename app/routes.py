from flask import Blueprint, render_template, request
from app.functions import generate_text, setup
from dotenv import load_dotenv
import os
from openai import OpenAI
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage,
)

main = Blueprint('main', __name__)

# -----------------------------------------------------------
chat_engine = setup()




@main.route('/', methods=['GET', 'POST'])
def index():
    output = None
    if request.method == 'POST':
        user_input = request.form.get('user_input')
        output = generate_text(chat_engine, user_input)
    return render_template('index.html', output=output)



@main.route('/thank_you')
def thank_you():
    user_input = request.args.get('user_input', 'No input')
    return f"Thank you! You entered: {user_input}"