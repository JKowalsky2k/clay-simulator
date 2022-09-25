# import speech_recognition

# class SpeechRecognizer:
#     def __init__(self) -> None:
#         self.speech_recognizer = speech_recognition.Recognizer()

#     async def getText(self):
#         with speech_recognition.Microphone() as speech_source:
#             try:
#                 print("Waiting for command!")
#                 audio = self.speech_recognizer.listen(speech_source)
#                 recognized_text = self.speech_recognizer.recognize_google(audio, language="pl-PL")
#                 if recognized_text == "":
#                     return None
#             except:
#                 return None
#         return recognized_text