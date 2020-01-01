from configparser import ConfigParser
from constants import *
from exceptions import *


class Settings:
    def __init__(self):
        self._parser = ConfigParser()
        self._parser.read("settings.ini")

    def valid(self):
        self.ships()
        self.height()
        self.width()
        self.first()
        self.ai()
        self.ui()

    def ships(self):
        ca = int(self._parser.get("settings", "carriers"))
        ba = int(self._parser.get("settings", "battleships"))
        cr = int(self._parser.get("settings", "cruisers"))
        de = int(self._parser.get("settings", "destroyers"))
        for s in (ca, ba, cr, de):
            if s < 0:
                raise SettingsError("No negative ships")
        return {CARRIER: ca, BATTLESHIP: ba, CRUISER: cr, DESTROYER: de}

    def set_ships(self, dictionary):
        for key, value in dictionary.items():
            if value < 0:
                raise SettingsError("No negative ships")
        self._parser.set("settings", "carriers", str(dictionary[CARRIER]))
        self._parser.set("settings", "battleships", str(dictionary[BATTLESHIP]))
        self._parser.set("settings", "cruisers", str(dictionary[CRUISER]))
        self._parser.set("settings", "destroyers", str(dictionary[DESTROYER]))
        self._save()

    def height(self):
        x = int(self._parser.get("settings", "height"))
        if x not in range(0, 27):
            raise SettingsError("Invalid height")
        return x

    def set_height(self, value):
        if value not in range(0, 27):
            raise SettingsError("Invalid height")
        self._parser.set("settings", "height", str(value))
        self._save()

    def width(self):
        x = int(self._parser.get("settings", "width"))
        if x not in range(0, 19):
            raise SettingsError("Invalid width")
        return x

    def set_width(self, value):
        if value not in range(0, 19):
            raise SettingsError("Invalid width")
        self._parser.set("settings", "width", str(value))
        self._save()

    def first(self):
        first = self._parser.get("settings", "first")
        if first not in ("player", "computer", "random"):
            raise SettingsError("Invalid choice")
        return first

    def set_first(self, value):
        if value not in ("player", "computer", "random"):
            raise SettingsError("Invalid choice")
        self._parser.set("settings", "first", value)
        self._save()

    def ai(self):
        ai = self._parser.get("settings", "difficulty")
        if ai not in ("easy", "normal", "advanced"):
            raise SettingsError("Invalid choice")
        return ai

    def set_ai(self, value):
        if value not in ("easy", "normal", "advanced"):
            raise SettingsError("Invalid choice")
        self._parser.set("settings", "difficulty", value)
        self._save()

    def ui(self):
        aux = self._parser.get("settings", "ui")
        if aux not in ("ui", "gui"):
            raise SettingsError("Invalid choice")
        return aux

    def save_path(self):
        return self._parser.get("settings", "save_path")

    def _save(self):
        file = open("settings.ini", "w")
        self._parser.write(file)
        file.close()
