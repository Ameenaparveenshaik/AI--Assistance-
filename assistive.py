import streamlit as st
from PIL import Image
import pyttsx3
import os
from google.generativeai import client
import pytesseract
import google.generativeai as genai
from langchain_google_genai import GoogleGenerativeAI

# Set Tesseract OCR path (Update with your installation path)
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\ABCD\Tesseract-OCR'

# # Initialize Google Generative AI with API Key
# GEMINI_API_KEY = "API_KEY"  # Replace with your valid API key
# os.environ["GOOGLE_API_KEY"] = GEMINI_API_KEY

# # Set the API key
# os.environ["GOOGLE_API_KEY"] = "AIzaSyCJRYvNp7RBGZvn37znctUltn-rXpVCAwM"
# client.api_key = os.environ["GOOGLE_API_KEY"]


import os

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("API Key not found. Set the GEMINI_API_KEY environment variable.")
llm = GoogleGenerativeAI(model="gemini-1.5-pro", api_key=GEMINI_API_KEY)

# Initialize Text-to-Speech engine
engine = pyttsx3.init()

# Add custom CSS styles
st.markdown(
    """
    <style>
     .main-title {
        font-size: 48px;
        font-weight: bold;
        text-align: center;
        color: #0662f6;
        margin-top: -20px;
     }
     .subtitle {
        font-size: 18px;
        color: #555;
        text-align: center;
        margin-bottom: 20px;
     }
     .feature-header {
        font-size: 24px;
        color: #333;
        font-weight: bold;
     }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="main-title">AI-Assistive 👀 </div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">AI for Scene Understanding, Text Extraction & Speech for the Visually Impaired 🗣️</div>', unsafe_allow_html=True)

# Sidebar Features
logo_path = "assets/logo.png"# Updated path for logo
if os.path.exists(logo_path):
    st.sidebar.image(logo_path, width=250)
else:
    st.sidebar.warning("Logo image not found.")

st.sidebar.title("ℹ️ About")
st.sidebar.markdown(
    """
    📌 **Features**
    - 🔍 **Describe Scene**: Get AI insights about the image, including objects and suggestions.
    - 📝 **Extract Text**: Extract visible text using OCR.
    - 🔊 **Text-to-Speech**: Hear the extracted text aloud.

    💡 **How it helps**:
    Assists visually impaired users by providing scene descriptions, text extraction, and speech.

    🤖 **Powered by**:
    - **Google Gemini API** for scene understanding.
    - **Tesseract OCR** for text extraction.
    - **pyttsx3** for text-to-speech.
    """
)

st.sidebar.text_area(
    "📜 Instructions",
    "Upload an image to start. Choose a feature to interact with:  1 Describe the Scene, 2 Extract Text, 3 Listen to it",
)

# Functions for functionality
def extract_text_from_image(image):
    """Extracts text from the given image using OCR."""
    return pytesseract.image_to_string(image)

def text_to_speech(text):
    """Converts the given text to speech."""
    engine.say(text)
    engine.runAndWait()

def generate_scene_description(input_prompt, image_data):
    """Generates a scene description using Google Generative AI."""
    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content([input_prompt, image_data[0]])
    return response.text

def input_image_setup(uploaded_file):
    """Prepares the uploaded image for processing."""
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data,
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded.")

# Upload Image Section
st.markdown("<h3 class='feature-header'>📤 Upload an Image</h3>", unsafe_allow_html=True)
uploaded_file = st.file_uploader("Drag and drop or browse an image (JPG, JPEG, PNG)", type=["jpg", "jpeg", "png"])
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

# Buttons Section
st.markdown("<h3 class='feature-header'>⚙️ Features</h3>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

scene_button = col1.button("🔍 Describe Scene")
ocr_button = col2.button("📝 Extract Text")
tts_button = col3.button("🔊 Text-to-Speech")

# Input Prompt for Scene Understanding
input_prompt = """
You are an AI assistant helping visually impaired individuals by describing the scene in the image. Provide:
1. List of items detected in the image with their purpose.
2. Overall description of the image.
3. Suggestions for actions or precautions for the visually impaired.
"""

# Process user interactions
if uploaded_file:
    image_data = input_image_setup(uploaded_file)

    if scene_button:
        with st.spinner("Generating scene description..."):
            response = generate_scene_description(input_prompt, image_data)
            st.markdown("<h3 class='feature-header'>🔍 Scene Description</h3>", unsafe_allow_html=True)
            st.write(response)

    if ocr_button:
        with st.spinner("Extracting text from the image..."):
            text = extract_text_from_image(image)
            st.markdown("<h3 class='feature-header'>📝 Extracted Text</h3>", unsafe_allow_html=True)
            st.text_area("Extracted Text", text, height=150)

    if tts_button:
        with st.spinner("Converting text to speech..."):
            text = extract_text_from_image(image)
            if text.strip():
                text_to_speech(text)
                st.success("✅ Text-to-Speech Conversion Completed!")
            else:
                st.warning("No text found to convert.")

# Footer
st.markdown(
    """
    <hr>
    <footer style="text-align:center;">
        <p>Powered by <strong>Google Gemini API</strong> | Built with ❤️ using Streamlit</p>
    </footer>
    """,
    unsafe_allow_html=True,
)
