import sys
import os
import json
import time
import speech_recognition as sr
import pyttsx3
from dotenv import load_dotenv
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton,
    QLabel, QHBoxLayout, QComboBox, QSlider
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from vertex_client import VertexAIPredictor
from request_formatter import RequestFormatter

# Load .env file
load_dotenv()

# GCP Vertex AI Configuration
PROJECT_ID = os.getenv("PROJECT_ID")
ENDPOINT_ID = os.getenv("ENDPOINT_ID")
LOCATION = os.getenv("LOCATION")
API_ENDPOINT = os.getenv("API_ENDPOINT")
GOOGLE_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

# Set Google Cloud authentication
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GOOGLE_CREDENTIALS

# Initialize text-to-speech engine
engine = pyttsx3.init()

class SpeechThread(QThread):
    """ Runs speech recognition in a separate thread to prevent UI freezing. """
    speech_recognized = pyqtSignal(str)  # Signal to send recognized text back

    def run(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            self.speech_recognized.emit("🎤 Listening... Speak now.")
            recognizer.adjust_for_ambient_noise(source)

            try:
                audio = recognizer.listen(source, timeout=5)  # Capture voice
                text = recognizer.recognize_google(audio)  # Convert to text
                self.speech_recognized.emit(text)  # Send text to UI
            except sr.UnknownValueError:
                self.speech_recognized.emit("❌ Could not understand speech.")
            except sr.RequestError:
                self.speech_recognized.emit("❌ Speech recognition failed.")


class ChatThread(QThread):
    """ Handles API calls in a separate thread to keep UI responsive. """
    response_received = pyqtSignal(str)

    def __init__(self, user_input, temperature, max_tokens):
        super().__init__()
        self.user_input = user_input
        self.temperature = temperature
        self.max_tokens = max_tokens

    def run(self):
        try:
            # Prepare input data
            instances = [
                {
                    "prompt": self.user_input,
                    "max_tokens": self.max_tokens,
                    "temperature": self.temperature,
                    "top_p": 0.8,
                    "top_k": 40,
                    "raw_response": False
                }
            ]

            # Query AI model
            predictor = VertexAIPredictor(PROJECT_ID, ENDPOINT_ID, LOCATION, API_ENDPOINT)
            predictions = predictor.predict(RequestFormatter.format_instances(instances))

            # all_predictions =  [f"\n {prediction}" for prediction in predictions]
            # Extracting only the last statement from the AI response
            print(predictions)
            if predictions:
                cleaned_response = predictions[0]
                # cleaned_response = self.extract_last_sentence(raw_response)
            else:
                cleaned_response = "No response received."

            self.response_received.emit(cleaned_response)
        except Exception as e:
            self.response_received.emit(f"Error: {str(e)}")

    def extract_last_sentence(self, response):
        """ Extracts the last meaningful sentence from AI output """
        sentences = response.strip().split("\n")  # Split response into lines
        meaningful_sentences = [s.strip() for s in sentences if s.strip()]  # Remove empty lines

        return meaningful_sentences[-1] if meaningful_sentences else response  # Return the last meaningful sentence


class ChatWindow(QWidget):
    """ Main Chat Window UI """

    def __init__(self):
        super().__init__()
        self.latest_ai_response = ""
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Dawood's AI Chat")
        self.setGeometry(200, 200, 700, 600)

        layout = QVBoxLayout()

        # Title
        self.title = QLabel("Dawood's AI Chat")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(self.title)

        # Chat Display
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        layout.addWidget(self.chat_display)

        # User Input
        input_layout = QHBoxLayout()
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Type your message here...")
        self.user_input.returnPressed.connect(self.send_message)
        input_layout.addWidget(self.user_input)

        # Send Button
        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.send_message)
        input_layout.addWidget(self.send_button)

        # Voice Input Button
        self.voice_button = QPushButton("🎤 Speak")
        self.voice_button.clicked.connect(self.speech_to_text)
        input_layout.addWidget(self.voice_button)

        layout.addLayout(input_layout)

        # Speak Response Button (New)
        self.speak_response_button = QPushButton("🔊 Speak Response")
        self.speak_response_button.clicked.connect(self.speak_response)
        self.speak_response_button.setEnabled(False)  # Disabled initially
        layout.addWidget(self.speak_response_button)

        # Settings Layout
        settings_layout = QHBoxLayout()

        # Theme Toggle
        self.theme_toggle = QComboBox()
        self.theme_toggle.addItems(["Light Mode", "Dark Mode"])
        self.theme_toggle.currentIndexChanged.connect(self.toggle_theme)
        settings_layout.addWidget(QLabel("Theme:"))
        settings_layout.addWidget(self.theme_toggle)

        # Temperature Slider
        self.temp_slider = QSlider(Qt.Orientation.Horizontal)
        self.temp_slider.setMinimum(1)
        self.temp_slider.setMaximum(10)
        self.temp_slider.setValue(7)
        settings_layout.addWidget(QLabel("Creativity:"))
        settings_layout.addWidget(self.temp_slider)

        # Max Tokens Slider
        self.token_slider = QSlider(Qt.Orientation.Horizontal)
        self.token_slider.setMinimum(100)
        self.token_slider.setMaximum(5000)
        self.token_slider.setValue(1000)
        settings_layout.addWidget(QLabel("Max Tokens:"))
        settings_layout.addWidget(self.token_slider)

        layout.addLayout(settings_layout)
        self.setLayout(layout)

        # Default Theme
        self.toggle_theme(0)

    def send_message(self):
        """ Handle user message input """
        user_text = self.user_input.text().strip()
        if user_text:
            self.chat_display.append(f"🧑‍💻 You: {user_text}")
            self.user_input.clear()
            self.fetch_ai_response(user_text)

    def fetch_ai_response(self, user_text):
        """ Calls DeepSeek model and updates chat """
        temperature = self.temp_slider.value() / 10  # Scale 1-10 to 0.1-1.0
        
        # Set max_tokens dynamically based on user input length
        estimated_tokens = 100000  # Approx 3 tokens per word, max 500

        self.chat_thread = ChatThread(user_text, temperature, estimated_tokens)
        self.chat_thread.response_received.connect(self.display_ai_response)
        self.chat_thread.start()


    def display_ai_response(self, ai_text):
        """ Display AI's response in the chat window """
        self.chat_display.append(f"🤖 Dawood's AI Chat: {ai_text}\n")
        self.latest_ai_response = ai_text
        self.speak_response_button.setEnabled(True)  # Enable button

    def toggle_theme(self, index):
        """ Switch between Light Mode and Dark Mode """
        if index == 0:
            self.setStyleSheet("background-color: white; color: black;")
            self.chat_display.setStyleSheet("background-color: white; color: black;")
            self.user_input.setStyleSheet("background-color: white; color: black;")
        else:
            self.setStyleSheet("background-color: #121212; color: white;")
            self.chat_display.setStyleSheet("background-color: #1e1e1e; color: white;")
            self.user_input.setStyleSheet("background-color: #1e1e1e; color: white;")

    def speech_to_text(self):
        """ Start voice recognition in a background thread. """
        self.speech_thread = SpeechThread()
        self.speech_thread.speech_recognized.connect(self.process_speech_result)
        self.speech_thread.start()

    def process_speech_result(self, text):
        """ Handle recognized speech text. """
        self.chat_display.append(f"🧑‍💻 You (Voice): {text}")

        # If speech was successful, send it to the AI
        if "❌" not in text:
            self.fetch_ai_response(text)


    def speak_response(self):
        """ Speak the latest AI response when the button is clicked """
        if self.latest_ai_response:
            engine.say(self.latest_ai_response)
            engine.runAndWait()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChatWindow()
    window.show()
    sys.exit(app.exec())
