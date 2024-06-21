import os
import textwrap
import google.generativeai as genai
from threading import Thread
import pyttsx3
import string  # for punctuation removal

# Set up Google API key (replace with your own)
os.environ['GOOGLE_API_KEY'] = "AIzaSyAipNFwJP5lAvmWjgy2QpaXCJPjX9BPOck"

# Configure GenerativeAI
genai.configure(api_key=os.environ['GOOGLE_API_KEY'])
model = genai.GenerativeModel('gemini-pro')

# Initialize pyttsx3 engine
engine = pyttsx3.init()

# Function to convert text to speech (moved up)
def text_to_speech(text):
  # Set speaking rate (values between 150 and 900)
  engine.setProperty('rate', 140)  # Adjust this value for slower speech
  engine.say(text)
  engine.runAndWait()

# Predefined question (text input)
user_question = "Who is Modi?"

# Generate response
if user_question:
  response = model.generate_content(user_question)

  # Limit the response text to a certain number of words
  maximum_words = 50  # Adjust as needed
  response_text_words = response.text.split()[:maximum_words]  # Extract first 'maximum_words'

  # Remove leading/trailing whitespace and replace multiple spaces with a single space
  response_text_words = [word.strip() for word in response_text_words]
  limited_response_text = ' '.join(response_text_words).replace('  ', ' ')

  # Remove punctuation characters (optional)
  punctuation = string.punctuation
  limited_response_text = ''.join([char for char in limited_response_text if char not in punctuation])

  # Convert the limited response text to speech (only reads words)
  text_to_speech(limited_response_text)
