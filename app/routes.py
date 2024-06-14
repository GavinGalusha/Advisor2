from flask import Blueprint, render_template, request, redirect, url_for

main = Blueprint('main', __name__)


# Load the environment variables from the .env file
from dotenv import load_dotenv
import os
from openai import OpenAI
load_dotenv()

# Access your API key from environment variables
openai_api_key = os.getenv('OPENAI_API_KEY')

# Initialize the OpenAI client with your API key
client = OpenAI(api_key=openai_api_key)







@main.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        render_template('index.html')
        user_input = request.form.get('user_input')
        return redirect(url_for('main.thank_you', user_input=user_input))
    return render_template('index.html')

@main.route('/thank_you')
def thank_you():
    user_input = request.args.get('user_input', 'No input')
    return f"Thank you! You entered: {user_input}"