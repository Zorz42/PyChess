from multiprocessing import Process


def _say(text: str):
    import pyttsx3
    engine = pyttsx3.init()
    engine.setProperty('rate', 170)

    engine.say(text)
    engine.runAndWait()


def say(text):
    thread = Process(name='TTS', target=_say, args=(text, ))
    thread.start()
