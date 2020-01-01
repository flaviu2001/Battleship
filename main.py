from ui import UI
from gui import GUI
from settings import Settings
try:
    Settings().valid()
    if Settings().ui() == "ui":
        UI().start()
    else:
        GUI().start()
except Exception as e:
    raise e
    print(e)
