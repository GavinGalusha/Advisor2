from flask import Blueprint, render_template, request, session, render_template_string
from .functions import generate_text, setup #is_inappropriate
from flask import request, redirect, url_for
from .database import db_session, Advice
from dotenv import load_dotenv
import markdown
import re
import os
from openai import OpenAI

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
        
        # Input validation and sanitization
        advice_text = re.sub(r'[<>]', '', advice_text)  # Remove HTML tags
        
        # Limit input length
        if len(advice_text) > 500:
            return "Input too long", 400

        # Escape output
        advice_text = render_template_string('{{ advice_text }}', advice_text=advice_text)

        # Save the sanitized and validated advice_text to your database here

        return redirect(url_for('main.index'))  # Redirect to the homepage or any other page  # Redirect to the homepage or any other page



