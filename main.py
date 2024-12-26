import sys
from src.window import Window
from PyQt6.QtWidgets import QApplication

from src.application import * 
from src.common import *

import datetime



if __name__ == "__main__":
    app = QApplication(sys.argv)
   
    update_dates()
    window = Window()
    window.show()
    sys.exit(app.exec())
