from flask import Blueprint, render_template, request, session
from .functions import generate_text, setup, save_text_to_file
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
        
        #handling user asking question
        user_input = request.form.get('user_input')
        if user_input:
            output = generate_text(chat_engine, user_input)
            session['conversation'].append({'type': 'User', 'text': user_input})
            session['conversation'].append({'type': 'Response', 'text': output})
            session.modified = True

            response_html = markdown.markdown(output)
            session['conversation'][-1]['text'] = response_html


        #handling user adding advice
        advice_input = request.form.get('advice_input')
        if advice_input and len(advice_input) < 200:
            save_text_to_file(advice_input)
            


    return render_template('index.html', conversation=session['conversation'])



