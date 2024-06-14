from flask import Blueprint, render_template, request
from app.functions import generate_text
from dotenv import load_dotenv
import os
from openai import OpenAI

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
    output = None
    if request.method == 'POST':
        user_input = request.form.get('user_input')
        output = generate_text(user_input)
    return render_template('index.html', output=output)



@main.route('/thank_you')
def thank_you():
    user_input = request.args.get('user_input', 'No input')
    return f"Thank you! You entered: {user_input}"