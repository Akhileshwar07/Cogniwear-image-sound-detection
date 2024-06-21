import os
import cv2
import google.generativeai as genai
from PIL import Image
import io
import time
import speech_recognition as sr
from gtts import gTTS

# Set up Google API key
os.environ['GOOGLE_API_KEY'] = "AIzaSyAipNFwJP5lAvmWjgy2QpaXCJPjX9BPOck"
genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

# Function to convert text to speech using gTTS
def text_to_speech(text, filename='output.mp3'):
    tts = gTTS(text=text, lang='en')
    tts.save(filename)
    os.system(f"mpg321 {filename}")

# Function to get user input from speech
def get_user_input_from_speech(prompt=""):
    text_to_speech(prompt)
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        text_to_speech(f"You said: {text}")
        return text.lower()  # Convert to lower case for easier comparison
    except sr.UnknownValueError:
        text_to_speech("I didn't catch that. Could you repeat, please?")
        return ""
    except sr.RequestError as e:
        text_to_speech(f"Error occurred; {e}")
        return ""

# Function to capture image from camera
def capture_image_from_camera():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()
    if not ret:
        text_to_speech("Failed to capture image.")
        return None
    ret, buffer = cv2.imencode('.jpg', frame)
    return buffer.tobytes()

# Function to generate image description
def generate_image_description(image_bytes, question=None):
    image = Image.open(io.BytesIO(image_bytes))
    model = genai.GenerativeModel('gemini-pro-vision')
    input_data = [question, image] if question else [image]
    try:
        response = model.generate_content(input_data)
        return response.text
    except Exception as e:
        text_to_speech(f"Failed to generate image description: {e}")
        return "No description available."

# Function to capture and describe video
def capture_and_describe_video():
    cap = cv2.VideoCapture(0)
    start_time = time.time()
    duration = 30  # seconds

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        ret, buffer = cv2.imencode('.jpg', frame)
        image_bytes = buffer.tobytes()

        description = generate_image_description(image_bytes)
        text_to_speech(description)

        if time.time() - start_time > duration:
            break

        key = cv2.waitKey(1)
        if key == 13:  # Enter key code
            break

    cap.release()
    cv2.destroyAllWindows()

# Main logic to handle voice commands and execute respective functions
if __name__ == "__main__":
    text_to_speech("Please choose a mode: 1 for Microphone, 2 for Camera, 3 for Video.")
    mode = input("Please choose a mode: 1 for Microphone, 2 for Camera, 3 for Video: ").strip()

    if mode == "1":
        user_question = get_user_input_from_speech("What is your question?")
        if user_question:
            model = genai.GenerativeModel('gemini-pro')
            try:
                response = model.generate_content([user_question])
                # Truncate response to 50 words
                response_text = ' '.join(response.text.split()[:50])
                text_to_speech(response_text)
            except Exception as e:
                text_to_speech(f"Failed to generate response: {e}")

    elif mode == "2":
        image = capture_image_from_camera()
        if image:
            question = get_user_input_from_speech("Ask a question about the image...")
            description = generate_image_description(image, question)
            text_to_speech(description)

    elif mode == "3":
        capture_and_describe_video()

    else:
        text_to_speech("Invalid mode selected. Please restart the program and choose a valid mode.")
