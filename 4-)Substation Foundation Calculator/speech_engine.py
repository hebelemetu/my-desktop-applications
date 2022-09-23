# importing the pyttsx library
import pyttsx3
from pyttsx3.drivers import sapi5

class speech_text:
    def __init__(self):
        self.engine = pyttsx3.init()

    def progress_completed(self):
        self.engine.say("PROCESS IS COMPLETED!")
        self.engine.runAndWait()

    def welcome(self,name):
        self.engine.setProperty("rate", 130)
        self.engine.say("WELCOME MR {}! WHAT CAN I DO FOR YOU".format(name))
        self.engine.runAndWait()

    def progress_completed_turkish(self):
        self.engine.say("HESAPLAMALAR TAMAMLANDI!")
        self.engine.runAndWait()

    def missing_input(self):
        self.engine.say("Please Enter Feeder Quantity and Choose Conductor type!")
        self.engine.runAndWait()

    def duplicated_names(self):
        self.engine.say("Please change duplicated building names!!")
        self.engine.runAndWait()

    def missing_input_turkish(self):
        self.engine.say("Lütfen gerekli bütün alanları doldurunuz!")
        self.engine.runAndWait()

    def speak_turkish(text):
        engine = pyttsx3.init()
        engine.setProperty("rate", 170)  # konuşma hızı
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[64].id)  # Türkçe
        engine.say(text)
        engine.runAndWait()

if __name__ == '__main__':
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    for voice in voices:
        print("Voice: %s" % voice.name)
        print(" - ID: %s" % voice.id)
        print(" - Languages: %s" % voice.languages)
        print(" - Gender: %s" % voice.gender)
        print(" - Age: %s" % voice.age)
        print("\n")