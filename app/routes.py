from flask import Blueprint, render_template, request, session
from .functions import generate_text, setup, save_text_to_file
from flask import request, redirect, url_for
from .database import db_session, Advice
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
chat_engine1, chat_engine2 = setup()




@main.route('/', methods=['GET', 'POST'])
def index():
    if 'conversation' not in session:
        session['conversation'] = []


    if 'search_mode' not in session:
        session['search_mode'] = 'Academic Expert'  # Default value

    if request.method == 'POST':
        # Toggle search mode based on checkbox
        if request.form.get('search-mode') == 'on':
            session['search_mode'] = 'Academic Expert'
        else:
            session['search_mode'] = 'General Advice'


    
    if request.method == 'POST':
        #handling user asking question
        user_input = request.form.get('user_input')
        search_mode = 'Academic Expert' if request.form.get('search-mode') == 'on' else 'General Advice'

        print(search_mode, " activated")

        if search_mode == 'Academic Expert':
            chat_engine = chat_engine1
        else:
            chat_engine = chat_engine2

        if user_input:
            output = generate_text(chat_engine, user_input)
            session['conversation'].append({'type': 'User', 'text': user_input})
            session['conversation'].append({'type': 'Response', 'text': output})
            session.modified = True

            response_html = markdown.markdown(output)
            session['conversation'][-1]['text'] = response_html


        #handling user adding advice
        
    return render_template('index.html', conversation=session['conversation'], search_mode=session['search_mode'])




@main.route('/submit_advice', methods=['POST'])
def submit_advice():
    if request.method == 'POST':
        advice_text = request.form['advice_input']

        # evaluate advice here, some kind of sentiment analysis to test if it's apropriate





        new_advice = Advice(text=advice_text)
        db_session.add(new_advice)
        db_session.commit()

        print("advice submitted in flask database")
        return redirect(url_for('main.index'))  # Redirect to the homepage or any other page



