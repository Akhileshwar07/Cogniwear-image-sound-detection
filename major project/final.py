import os
import textwrap
import google.generativeai as genai
import speech_recognition as sr
from threading import Thread
import pyttsx3

# Set up Google API key
os.environ['GOOGLE_API_KEY'] = "AIzaSyAipNFwJP5lAvmWjgy2QpaXCJPjX9BPOck"

# Configure GenerativeAI
genai.configure(api_key=os.environ['GOOGLE_API_KEY'])
model = genai.GenerativeModel('gemini-pro')

# Initialize pyttsx3 engine
engine = pyttsx3.init()

# Function to get user input from speech
def get_user_input_from_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        audio_feedback("Listening...")
        audio = recognizer.listen(source)

    try:
        audio_feedback("Recognizing...")
        text = recognizer.recognize_google(audio)
        audio_feedback("You said: " + text)
        return text
    except sr.UnknownValueError:
        audio_feedback("Sorry, I could not understand what you said.")
        return ""
    except sr.RequestError as e:
        audio_feedback("Error occurred; {0}".format(e))
        return ""

# Function to provide audio feedback
def audio_feedback(text):
    text_to_speech(text)

# Function to convert text to Markdown format
def to_markdown(text):
    text = text.replace('•', '')  # Remove bullet points
    text = text.replace('*', '')
    return textwrap.indent(text, '> ', predicate=lambda _: True)

# Function to convert text to speech
def text_to_speech(text):
    engine.say(text)
    engine.runAndWait()

# Function to perform speech synthesis
def perform_speech_synthesis(text):
    # Convert the response text to speech
    text_to_speech(text)
    # Signal that speech synthesis is complete
    global synthesis_complete
    synthesis_complete = True

# Get user question from speech
user_question = get_user_input_from_speech()

# Generate response
if user_question:
    response = model.generate_content(user_question)

    # Limit the response text to a certain number of words
    maximum_words = 50  # Adjust as needed
    response_text_words = response.text.split()[:maximum_words]  # Extract the first 'maximum_words' words
    limited_response_text = " ".join(response_text_words)  # Join the limited words back into a single string

    # Convert the limited response text to speech
    synthesis_complete = False
    synthesis_thread = Thread(target=perform_speech_synthesis, args=(limited_response_text,))
    synthesis_thread.start()

    # Wait for speech synthesis to complete or for Enter key press
    while not synthesis_complete:
        pass
