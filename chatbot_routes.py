from flask import Blueprint, request, jsonify, render_template
import openai
import os
from dotenv import load_dotenv

load_dotenv()

bp = Blueprint('chatbot_routes', __name__, url_prefix='/ask-bot')

openai.api_key = os.getenv("OPENAI_API_KEY")

@bp.route('/', methods=['GET'])
def chatbot_page():
    return render_template('chatbot.html')

@bp.route('/', methods=['POST'])
def ask_bot():
    data = request.json
    question = data.get('question')
    if not question:
        return jsonify({'error': 'Question is required'}), 400

    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Answer the following farming question in detail:\n{question}",
            max_tokens=150,
            temperature=0.7,
        )
        answer = response.choices[0].text.strip()
        return jsonify({'answer': answer})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
