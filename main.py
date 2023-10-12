import openai
import time
import pyttsx3
import speech_recognition as sr
import os
from dotenv import load_dotenv
load_dotenv()
#  Enter 1 for text to text and 2 for speech to text

x=int(input("Enter 1 for text to text and 2 for speech to text: "))
while x!=1 and x!=2:
    x=int(input("Enter 1 for text to text and 2 for speech to text: "))
# Set up OpenAI API key
openai.api_key = os.getenv('api_key')# enter your own api key here

# Define language models
models = {
    "en": "text-davinci-002",
    "fr": "text-davinci-002",
    "English": "text-davinci-002",
    "French": "text-davinci-002"
}
if x==1:
    # Define language detection function
    def detect_language(text):
        response = openai.Completion.create(
            engine=models["en"],
            prompt="Detect the language of the following text:\n\n" + text + "\n\nLanguage:",
            max_tokens=1
        )
        language = response.choices[0].text.strip()
        if language == "French":
            return "fr"
        elif language == "English":
            return "en"
            
        

    # Define conversation function
    def converse():
        # Initialize conversation
        context = ""
        language = "en"
        while True:
            # Listen for user input
            text = input("You: ")
            # Detect language
            lang = detect_language(text)
            # Switch language model if necessary
            if lang != language:
                model = models.get(lang, "English")  # Use default model if lang not found
                language = lang
                print(f"Switching to {language} mode...")
            else:
                model = models[language]
            # Generate AI response
            response = openai.Completion.create(
                engine=model,
                prompt=context + text + "\nAI:",
                max_tokens=1024,
                temperature=0.7,
                n=1,
                stop=None,
                frequency_penalty=0,
                presence_penalty=0
            )
            ai_text = response.choices[0].text.strip()
            # Print AI response
            time.sleep(1)
            print("AI:", ai_text)
            time.sleep(1)
            # Update conversation context
            context += text + "\nAI:" + ai_text + "\n"

    # Start conversation
    converse()
elif x==2:
# Set up text-to-speech engine
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    for voice in voices:
        print(voice.id, voice.name)
    # Define language models
    models = {
        "en": "text-davinci-002",
        "fr": "text-davinci-002",
        "English": "text-davinci-002",
        "French": "text-davinci-002"
    }

    # Define voices
    VOICES = {
        'en':  'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0',
        'fr': 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_FR-FR_HORTENSE_11.0'
    }

    # Define conversation function
    def converse():
        # Initialize conversation
        context = ""
        language= "en"
        r = sr.Recognizer()
        mic = sr.Microphone()

        with mic as source:
            print("Say something!")
            r.adjust_for_ambient_noise(source,duration=0)  # Adjust mic levels to account for ambient noise
            audio = r.listen(source)  # Listen for user input

        # Detect language
        try:
            text = r.recognize_google(audio, language="en-US")  # Use English language model for speech recognition
            print("English input detected!")
            lang = "en"
        except sr.UnknownValueError:
            try:
                text = r.recognize_google(audio, language="fr-FR")  # Use French language model for speech recognition
                print("French input detected!")
                lang = "fr"
            except sr.UnknownValueError:
                print("Sorry, I couldn't understand that.")
                return

        # Generate AI response
        model = models[lang]
        response = openai.Completion.create(
            engine=model,
            prompt=context + text + "\nAI:",
            max_tokens=1024,
            temperature=0.7,
            n=1,
            stop=None,
            frequency_penalty=0,
            presence_penalty=0
        )
        ai_text = response.choices[0].text.strip()

        # Print AI response
        print("AI:", ai_text)

        # Convert AI response to speech
        engine.setProperty('voice', VOICES[lang])
        engine.say(ai_text)
        engine.runAndWait()

        # Update conversation context
        context += text + "\nAI:" + ai_text + "\n"

    # Start conversation
    while True:
        converse()
