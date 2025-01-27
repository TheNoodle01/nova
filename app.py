from flask import Flask, request, jsonify
import requests
import pyttsx3
import os
import speech_recognition as sr
import subprocess

app = Flask(__name__)

# Initialize eSpeak engine for Text-to-Speech (TTS)
engine = pyttsx3.init()

# Function to recognize speech using eSpeak and SpeechRecognition
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for your question...")
        audio = recognizer.listen(source)
        try:
            # Use Google Web Speech API for speech-to-text conversion
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            return "Sorry, I couldn't understand."
        except sr.RequestError:
            return "Sorry, I'm having trouble connecting to the service."

# Function to convert text to speech using eSpeak (through pyttsx3)
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to call GPT-Neo model
def ask_ai(question):
    API_URL = "https://your-app-name.railway.app/ask"  # Replace with your Railway API URL
    data = {
        "question": question
    }
    response = requests.post(API_URL, json=data)
    if response.status_code == 200:
        return response.json().get("response", "Error: No response from AI.")
    else:
        return "Error: Unable to get response from AI."

@app.route('/')
def home():
    return "Welcome to the Voice-Activated AI!"

@app.route('/ask', methods=['POST'])
def ask():
    question = request.json.get("question")
    if question:
        ai_response = ask_ai(question)
        return jsonify({"response": ai_response})
    else:
        return jsonify({"response": "Error: No question provided."})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
    
