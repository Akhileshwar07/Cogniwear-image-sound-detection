import os
import cv2
import google.generativeai as genai
from PIL import Image
import io
import pyttsx3
import time

os.environ['GOOGLE_API_KEY'] = "AIzaSyAipNFwJP5lAvmWjgy2QpaXCJPjX9BPOck"

genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

def capture_and_describe_video():
    """
    Captures video from the camera for 30 seconds, generates descriptions for each frame,
    and speaks them.
    """
    cap = cv2.VideoCapture(0)
    start_time = time.time()
    duration = 30  # seconds

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        # Convert frame to bytes
        ret, buffer = cv2.imencode('.jpg', frame)
        image_bytes = buffer.tobytes()

        # Generate description
        description = generate_image_description(image_bytes)

        # Speak the description
        speak(description)

        # Check for 30 seconds duration
        if time.time() - start_time > duration:
            break

        # Check for Enter key press to stop early
        key = cv2.waitKey(1)
        if key == 13:  # Enter key code
            break

    cap.release()
    cv2.destroyAllWindows()

def generate_image_description(image_bytes):
    """
    Generates a description for the given image bytes.

    Args:
        image_bytes: Bytes of the image.

    Returns:
        str: The generated description.
    """
    image = Image.open(io.BytesIO(image_bytes))
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content(image)
    return response.text

def speak(text):
    """
    Converts text to speech and plays it using pyttsx3.
    
    Args:
        text: The text to be spoken.
    """
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

if __name__ == "__main__":
    capture_and_describe_video()
