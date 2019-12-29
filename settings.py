from configparser import ConfigParser
from random import choice
from ai import *


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

    def ships(self):
        ca = int(self._parser.get("settings", "carriers"))
        ba = int(self._parser.get("settings", "battleships"))
        cr = int(self._parser.get("settings", "cruisers"))
        de = int(self._parser.get("settings", "destroyers"))
        for s in (ca, ba, cr, de):
            if s < 0:
                raise SettingsError("No negative ships")
        return {CARRIER: ca, BATTLESHIP: ba, CRUISER: cr, DESTROYER: de}

    def height(self):
        x = int(self._parser.get("settings", "height"))
        if x not in range(0, 27):
            raise SettingsError("Invalid height")
        return x

    def width(self):
        x = int(self._parser.get("settings", "width"))
        if x not in range(0, 15):
            raise SettingsError("Invalid width")
        return x

    def first(self):
        first = self._parser.get("settings", "first")
        if first == "player":
            return PLAYER
        if first == "computer":
            return COMPUTER
        if first == "random":
            return choice(PLAYER, COMPUTER)
        raise SettingsError("Invalid choice")

    def ai(self):
        ai = self._parser.get("settings", "difficulty")
        if ai == "easy":
            return EasyAI
        if ai == "normal":
            return NormalAI
        if ai == "advanced":
            return AdvancedAI
        raise SettingsError("Invalid choice")

    def save_path(self):
        return self._parser.get("settings", "save_path")
