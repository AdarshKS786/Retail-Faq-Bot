# app.py

import os
from flask import Flask, render_template, request, jsonify
from chatbot.model import FAQBot
from gtts import gTTS

app = Flask(__name__)

# Initialize the chatbot model
faq_bot = FAQBot(filepath='faqs.csv')

# Ensure a directory exists for storing audio files
if not os.path.exists('static/audio'):
    os.makedirs('static/audio')

@app.route('/')
def index():
    """Render the main chat page."""
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    """Handle user queries and return the bot's response."""
    data = request.get_json()
    user_question = data.get('question')

    if not user_question:
        return jsonify({'error': 'No question provided'}), 400

    # Get the text answer from the bot
    text_answer = faq_bot.get_answer(user_question)
    
    # Generate speech from the text answer
    try:
        tts = gTTS(text=text_answer, lang='en')
        audio_filename = 'response.mp3'
        audio_filepath = os.path.join('static', 'audio', audio_filename)
        tts.save(audio_filepath)
        audio_url = f'/{audio_filepath}'
    except Exception as e:
        print(f"Error generating TTS audio: {e}")
        audio_url = None

    return jsonify({
        'text_answer': text_answer,
        'audio_url': audio_url
    })

if __name__ == '__main__':
    app.run(debug=True)