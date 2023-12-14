import pyttsx3
from argostranslate.translate import translate

def text_to_speech(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.setProperty('voice', "en")
    engine.say(text)
    engine.runAndWait()

def translate_text(text, from_language, to_language):
    if text:
        translatedText = translate(
            text,
            from_language,
            to_language
        )
        return translatedText