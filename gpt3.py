# Install prerequisites
# Python 3 (3.8+ required)
# pip install --upgrade pip
# pip install openai
# pip install pyttsx3
# pip install pyaudio
# pip install SpeechRecognition
# pip install --upgrade google-api-python-client

# "python -m speech_recognition" to test if pyaudio is working

import openai
import pyttsx3
import speech_recognition as sr

# OpenAI API Key
openai.api_key = "YourAPIKeyHere"

# Initiate the TextToSpeechEngine
engine = pyttsx3.init()

# Declare GPT3 Response function
# See list of API calls at
# https://platform.openai.com/docs/api-reference/completions/create?lang=python
def generate_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_toxens=4097,
        n=1,
        stop=None,
        # Tweak temperature to improve precision of GPT response
        # Number between 0 and 1, 0 low creativity, 1 high creativity
        temperature=0.5,
    )
    return response["choices"][0]["text"]

# Generate speech from gpt text response
def speak_text(text):
    engine.say(text)
    engine.runAndWait()

def main():
    while True:
        # Access Microphone and wait for activation word to start transcribing audio to text
        print('Please say "Hello" to activate voice recognition...')
        with sr.Microphone() as source:
            recognizer = sr.Recognizer()
            audio = recognizer.listen(source)
            try:
                transcription = recognizer.recognize_google(audio)
                if transcription.lower() == "hello":

                    # Transcribe Audio to Text
                        with sr.Microphone() as source:
                            recognizer = sr.Recognizer()
                            print("Waiting for voice input...")
                            # Reduces background noise impact on transcription
                            # can be tweaked by adding ",duration=x" (where x is time in seconds)
                            # default is 1 second.
                            recognizer.adjust_for_ambient_noise(source)
                            audio = recognizer.listen(source)
                            try:
                                # Tweak language variable to help recognise your accent better
                                # See https://cloud.google.com/speech-to-text/docs/speech-to-text-supported-languages
                                text = recognizer.recognize_google(audio, language='en-us')
                            except Exception:
                                print("Did not catch that.")
                        if text:
                            print(f"Recognized speech: {text}")

                        # Generate response using Gpt-3 calling response function
                        response = generate_response(text)
                        print(f"GPT-3 says: {response}")

                        # Read response using text-to-speech
                        speak_text(response)
            except Exception as e:
                print("An error occured: {}".format(e))

if __name__ == "__main__":
    main()
