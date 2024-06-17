from flask import Flask, request, render_template, jsonify
from google.cloud import speech
from google.oauth2 import service_account
import google.generativeai as genai
import os
import logging

app = Flask(__name__)

# Path to your service account key file for Speech-to-Text
service_account_path = r''

# Configure Google Speech-to-Text API with direct credentials
credentials = service_account.Credentials.from_service_account_file(service_account_path)
speech_client = speech.SpeechClient(credentials=credentials)

# Set up Google AI Studio API key for Generative AI
os.environ["GEMINI_API_KEY"] = ''
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Configure logging
logging.basicConfig(level=logging.INFO)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/transcribe', methods=['POST'])
def transcribe():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400
    audio_file = request.files['audio']
    if audio_file:
        audio_content = audio_file.read()
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.MP3,  # Set encoding to MP3
            sample_rate_hertz=16000,  # Ensure this matches your MP3 file
            language_code='en-US'
        )
        try:
            response = speech_client.recognize(config=config, audio=speech.RecognitionAudio(content=audio_content))
            transcript = ' '.join([result.alternatives[0].transcript for result in response.results])
            return jsonify({'transcript': transcript})
        except Exception as e:
            app.logger.error(f"Error during transcription: {e}")
            return jsonify({'error': str(e)}), 500
    return jsonify({'error': 'Invalid file'}), 400

@app.route('/api/text-input', methods=['POST'])
def handle_text_input():
    user_input = request.json.get('input')
    if not user_input:
        return jsonify({'error': 'No input provided'}), 400
    response = generate_text_response(user_input)
    return jsonify(response)

def generate_text_response(user_input):
    try:
        main_response = get_google_ai_response(user_input, 150, 0.7)

        if "Response blocked" in main_response or "Error processing" in main_response:
            return {
                'input': user_input,
                'reply': main_response,
                'follow_up_questions': []
            }

        follow_up_prompt = f"Based on the conversation text: '{main_response}', suggest follow-up questions."
        follow_up_questions = get_google_ai_response(follow_up_prompt, 100, 1.0, 3, ["\n", ".", "?"])

        if not isinstance(follow_up_questions, list):
            follow_up_questions = [follow_up_questions]

        return {
            'input': user_input,
            'reply': main_response,
            'follow_up_questions': follow_up_questions
        }
    except Exception as e:
        app.logger.error(f"Error response: {e}")
        return jsonify({'error': 'Failed to process your request'}), 500

def get_google_ai_response(prompt, max_tokens, temperature, n=1, stop=None):
    try:
        response = genai.generate_text(
            prompt=prompt,
            max_output_tokens=max_tokens,
            temperature=temperature
        )
        if response.result is None:
            app.logger.error(f"Response blocked: {response}")
            return "Response blocked safety concerns or other issues."

        generated_text = response.result.strip()
        return generated_text
    except AttributeError as e:
        app.logger.error(f"AttributeError: {e}. Full response: {response}")
        return "Error response from AI service."
    except Exception as e:
        if 'quotaExceeded' in str(e):
            return "API usage limit exceeded. Try again"
        raise

if __name__ == '__main__':
    app.run(debug=True)
