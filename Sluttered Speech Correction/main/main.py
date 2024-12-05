import speech_recognition as sr
import spacy
import pyttsx3

# Initialize recognizer and NLP
recognizer = sr.Recognizer()
nlp = spacy.load('en_core_web_sm')
engine = pyttsx3.init()

# Adjust microphone listening behavior
def adjust_recognizer_settings():
    recognizer.energy_threshold = 300  # Lower this if your speech is quiet, increase if too sensitive
    recognizer.pause_threshold = 2  # Allows for longer pauses before assuming you're done
    recognizer.dynamic_energy_threshold = True  # Adjusts sensitivity dynamically

def speech_to_text():
    adjust_recognizer_settings()  # Apply the adjusted settings
    
    with sr.Microphone() as source:
        print("Please speak now...")
        audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)  # Listen for longer

        try:
            # Convert speech to text using Google's API
            text = recognizer.recognize_google(audio)
            print("Original (Stuttered) Speech:", text)  # Print stuttered speech
            return text
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
            return ""
        except sr.RequestError:
            print("Sorry, the service is unavailable.")
            return ""

def clean_text(text):
    doc = nlp(text)
    
    # Split text into words and remove repetitions
    words = text.split()
    cleaned_words = []
    for i, word in enumerate(words):
        if i == 0 or word.lower() != words[i-1].lower():
            cleaned_words.append(word)
    
    cleaned_text = ' '.join(cleaned_words)
    print("Cleaned Speech:", cleaned_text)  # Print cleaned speech
    return cleaned_text

def text_to_speech(text):
    engine.say(text)
    engine.runAndWait()

# Main workflow
if __name__ == "__main__":
    # Step 1: Convert speech to text
    raw_text = speech_to_text()

    if raw_text:
        # Step 2: Clean the text
        cleaned_text = clean_text(raw_text)

        # Step 3: Convert the cleaned text back to speech (optional)
        text_to_speech(cleaned_text)
