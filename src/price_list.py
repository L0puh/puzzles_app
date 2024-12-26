from src.common import *
from src.application import *

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QIcon, QPixmap
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, 
                             QVBoxLayout, QPushButton, QListWidget, 
                             QListWidgetItem, QComboBox, QHBoxLayout)

class Price_list(QWidget):
    def __init__(self, window):
        super().__init__()
        self.window = window
        self.puzzles_list = get_json(PUZZLES_FILE, KEY_PUZZLES)
        self.init_UI()

    def init_UI(self):
        self.setWindowTitle("Прайс-лист")
        self.puzzles_input = QListWidget() 
        
        self.update_list()
       
        layout = QVBoxLayout()
        layout.addWidget(self.puzzles_input)
        self.setLayout(layout)

    def update_list(self):
        self.puzzles_list = get_json(PUZZLES_FILE, KEY_PUZZLES)
        self.puzzles_input.clear()
        for indx, data in enumerate(self.puzzles_list):
            item = QListWidgetItem()

            name_label = QLabel(f"Название: {data['name']}")
            price_label = QLabel(f"Цена: {data['price']}")



            open_button = QPushButton()
            open_button.setIcon(QIcon(os.path.join(ICONS_DIR, "edit.png")))
            open_button.setIconSize(open_button.sizeHint())
            open_button.setFixedSize(open_button.iconSize())
            
            open_button.setObjectName(str(indx))
            open_button.clicked.connect(self.open_puzzle)

            layout = QHBoxLayout()
            layout.addWidget(name_label)
            layout.addWidget(price_label)
            layout.addWidget(open_button)

            self.puzzles_input.addItem(item)
            widget = QWidget()
            widget.setLayout(layout)
            item.setSizeHint(widget.sizeHint())
            self.puzzles_input.addItem(item)
            self.puzzles_input.setItemWidget(item, widget)
    
    def open_puzzle(self):
        sender = self.sender()
        push_button = self.findChild(QPushButton, sender.objectName())
        indx = push_button.objectName()

        data = self.puzzles_list.pop(int(indx))
        update_json(PUZZLES_FILE, self.puzzles_list, KEY_PUZZLES)

        self.window.create_puzzle(editable=True, data=data)
        self.quit()

    def quit(self):
        update_json(PUZZLES_FILE, self.puzzles_list, KEY_PUZZLES)
        self.close()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape: self.quit()
    
