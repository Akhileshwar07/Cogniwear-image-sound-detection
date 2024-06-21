import os
import pathlib
import textwrap
import cv2
import google.generativeai as genai
from PIL import Image
import io
import matplotlib.pyplot as plt
from gtts import gTTS
import speech_recognition as sr

os.environ['GOOGLE_API_KEY'] = "AIzaSyAipNFwJP5lAvmWjgy2QpaXCJPjX9BPOck"

genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

def capture_image_from_camera():
    # Initialize the camera
    cap = cv2.VideoCapture(0)

    # Capture frame-by-frame
    ret, frame = cap.read()

    # Release the camera
    cap.release()

    # Convert the image to bytes
    ret, buffer = cv2.imencode('.jpg', frame)
    image_bytes = buffer.tobytes()

    return frame, image_bytes  # Return both the frame and image bytes


def generate_image_description(image_bytes, question=None):
    # Convert bytes to PIL image
    image = Image.open(io.BytesIO(image_bytes))

    model = genai.GenerativeModel('gemini-pro-vision')
    if question:
        # Concatenate question with image
        input_data = [question, image]
    else:
        input_data = image

    # Generate content
    response = model.generate_content(input_data, stream=True)
    response.resolve()
    return response.text


def text_to_speech(text, filename='output.mp3'):
    tts = gTTS(text=text, lang='en')
    tts.save(filename)
    # Play the generated audio
    os.system("start " + filename)  # For Windows


if __name__ == "__main__":
    # Capture image from camera
    frame, image = capture_image_from_camera()

    # Display the captured image
    plt.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    plt.axis('off')
    plt.show()

    # Initialize the recognizer
    recognizer = sr.Recognizer()

    # Record audio from the microphone for asking the question
    with sr.Microphone() as source:
        print("Ask a question about the image...")
        audio = recognizer.listen(source)

    # Use Google Web Speech API to convert speech to text
    try:
        print("Recognizing question...")
        question = recognizer.recognize_google(audio)
        print("Question:", question)
    except sr.UnknownValueError:
        print("Sorry, I could not understand what you said.")
        question = input("Ask a question about the image (or leave blank): ")
    except sr.RequestError as e:
        print("Error occurred; {0}".format(e))
    #    question = input("Ask a question about the image (or leave blank): ")

    # Generate description
    description = generate_image_description(image, question)

    # Print the description
    # print(textwrap.fill(description, width=80))

    # Convert description to speech
    text_to_speech(description)
