from ui import UI
from settings import Settings
try:
    Settings().valid()
    UI().start()
except Exception as e:
    print(e)
