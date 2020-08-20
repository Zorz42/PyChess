from multiprocessing import Process


def _say(text: str) -> None:
    import pyttsx3
    engine = pyttsx3.init()
    engine.setProperty('rate', 170)

    engine.say(text)
    engine.runAndWait()


def say(text) -> None:
    thread = Process(name='TTS', target=_say, args=(text,))
    thread.start()
