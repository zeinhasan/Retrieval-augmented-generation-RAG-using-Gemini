import streamlit as st
import speech_recognition as sr
import pyttsx3
import google.generativeai as genai

# Initialize pyttsx3
engine = pyttsx3.init()

# Set up the Google Gemini API
genai.configure(api_key="AIzaSyAUss8YOLSCp_XlB6anfR_QZgKWQSnOzXY")

# Set up the model configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 0,
    "max_output_tokens": 8192,
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
]

# Initialize the Gemini model
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro-latest",
    generation_config=generation_config,
    safety_settings=safety_settings
)

convo = model.start_chat(history=[])

# Function to get response from Gemini
def get_response(user_input):
    convo.send_message(user_input)
    gemini_reply = convo.last.text
    return gemini_reply

# Streamlit interface
st.title("Voice Assistant with Google Gemini")

# Record audio
if st.button("Start Listening"):
    st.write("Listening... (Say 'Google' to activate)")
    
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        
        try:
            response = recognizer.recognize_google(audio)
            st.write(f"You said: {response}")
            
            if "Google" in response.lower():
                # Send the user input to Gemini and get the response
                response_from_gemini = get_response(response)
                st.write(f"Google response: {response_from_gemini}")

                # Speak the response
                engine.say(response_from_gemini)
                engine.runAndWait()

            else:
                st.write("Please say the wake word 'Google' to activate.")

        except sr.UnknownValueError:
            st.write("Could not understand the audio.")
        except sr.RequestError as e:
            st.write(f"Could not request results from Google Speech Recognition service; {e}")

