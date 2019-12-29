from settings import Settings
import pickle


class Save:
    def __init__(self, game):
        self.game = game
        self.save_path = Settings().save_path()

    @staticmethod
    def load():
        try:
            file = open(Settings().save_path(), "rb")
            ret = pickle.load(file)
            file.close()
            return ret
        except FileNotFoundError:
            return None

    def save(self):
        file = open(self.save_path, "wb")
        pickle.dump(self.game, file)
        file.close()
