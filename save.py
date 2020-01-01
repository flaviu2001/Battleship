import pickle
from settings import Settings


class Save:
    def __init__(self, save_path=None, game=None):
        if save_path is None:
            save_path = Settings().save_path()
        self.game = game
        self.save_path = save_path

    def load(self):
        try:
            file = open(self.save_path, "rb")
            ret = pickle.load(file)
            file.close()
            return ret
        except FileNotFoundError:
            return None

    def save(self):
        file = open(self.save_path, "wb")
        pickle.dump(self.game, file)
        file.close()
