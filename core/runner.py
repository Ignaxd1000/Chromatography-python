from shared.database import database
from shared.config import Config


class runner:

    def __init__(self):
        self.config = Config()
        self.db = database(self.config.cfg.dbPath)