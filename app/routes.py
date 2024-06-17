from flask import Blueprint, render_template, request, session
from .functions import generate_text, setup
from dotenv import load_dotenv
import markdown

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
    if 'conversation' not in session:
        session['conversation'] = []

    if request.method == 'POST':
        user_input = request.form.get('user_input')
        if user_input:
            output = generate_text(chat_engine, user_input)
            session['conversation'].append({'type': 'User', 'text': user_input})
            session['conversation'].append({'type': 'Response', 'text': output})
            session.modified = True

            response_html = markdown.markdown(output)
            session['conversation'][-1]['text'] = response_html

    return render_template('index.html', conversation=session['conversation'])



