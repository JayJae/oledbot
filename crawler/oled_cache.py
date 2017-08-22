from oled_database import OledDatabase

class OledCache :
    oled_db = None

    def __init__(self) :
        self.oled_db = OledDatabase()

