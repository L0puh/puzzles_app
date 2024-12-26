from src.common import *
from src.application import *

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QIcon, QPixmap
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, 
                             QVBoxLayout, QPushButton, QListWidget, 
                             QListWidgetItem, QComboBox, QHBoxLayout)


class Puzzles_list(QWidget):
    def __init__(self, window):
        super().__init__()
        self.window = window
        self.puzzles_list = get_json(PUZZLES_FILE, KEY_PUZZLES)
        self.init_UI()

    def init_UI(self):
        self.setWindowTitle("Список")
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

            delete_icon = QIcon(os.path.join(ICONS_DIR, 'delete.png'))
            edit_icon   = QIcon(os.path.join(ICONS_DIR, 'edit.png'))

            item_label = QLabel()
            info_label = QLabel(f"Название: {data['name']}\nКоличество деталей(шт.): {data['count']}\nФанерные листы: {data['plywood']}\nЦена:{data['price']}")

            pixmap = QPixmap(os.path.join(IMAGES_DIR, data["image"])) 
            pixmap = scale_image(pixmap, 300, 300)
            item_label.setPixmap(pixmap)
            item_label.resize(pixmap.width(), pixmap.height())

            edit_button = QPushButton()
            edit_button.setIcon(edit_icon)
            edit_button.setIconSize(edit_button.sizeHint())
            edit_button.setFixedSize(edit_button.iconSize())

            delete_button = QPushButton()
            delete_button.setIcon(delete_icon)
            delete_button.setIconSize(delete_button.sizeHint())
            delete_button.setFixedSize(delete_button.iconSize())
            
            edit_button.setObjectName(str(indx))
            delete_button.setObjectName(str(indx))
            edit_button.clicked.connect(self.edit_puzzle)
            delete_button.clicked.connect(self.delete_puzzle)

            button_layout = QHBoxLayout()
            button_layout.addWidget(item_label)
            button_layout.addWidget(info_label)
            button_layout.addWidget(edit_button)
            button_layout.addWidget(delete_button)
            
            button = QWidget()
            button.setLayout(button_layout)
            item.setSizeHint(button.sizeHint())
            self.puzzles_input.addItem(item)
            self.puzzles_input.setItemWidget(item, button)
    
    def edit_puzzle(self):
        sender = self.sender()
        push_button = self.findChild(QPushButton, sender.objectName())
        indx = push_button.objectName()

        data = self.puzzles_list.pop(int(indx))
        update_json(PUZZLES_FILE, self.puzzles_list, KEY_PUZZLES)

        self.window.create_puzzle(editable=True, data=data)
        self.quit()

    def delete_puzzle(self):
        sender = self.sender()
        push_button = self.findChild(QPushButton, sender.objectName())
        indx = push_button.objectName()
        self.puzzles_list.pop(int(indx))
        update_json(PUZZLES_FILE, self.puzzles_list, KEY_PUZZLES)
        self.update_list()

    def quit(self):
        update_json(PUZZLES_FILE, self.puzzles_list, KEY_PUZZLES)
        self.close()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape: self.quit()
    

class Puzzles(QWidget):
    def __init__(self):
        super().__init__()
        self.puzzles = defaultdict(list)
        
        self.thickenss_list = get_json(WOOD_FILE, KEY_THICKNESS) 
        self.plywoods_list  = get_json(WOOD_FILE, KEY_PLYWOOD)
        self.images_list    = get_images(IMAGES_DIR)
        self.puzzles_list   = get_json(PUZZLES_FILE, KEY_PUZZLES)

        self.init_UI()
        self.plywood_input.addItems(self.plywoods_list)
        self.image_input.addItems(self.images_list)

        if self.plywoods_list:
            self.current_wood = self.plywoods_list[0]
        else: 
            self.current_wood = "не найдено" 
        if self.images_list:
            self.current_image = self.images_list[0]
        else:
            self.current_image = "не найдено"

        self.current_price = 0


    def init_UI(self):
        self.setWindowTitle("Пазл")
        self.name_label = QLabel("Название пазла:")
        self.name_input = QLineEdit()

        self.plywood_label = QLabel("Фанерный лист:")
        self.plywood_input = QListWidget()
        self.plywood_input.itemClicked.connect(self.get_plywood)

        self.image_label = QLabel("Макет:")
        self.image_input = QListWidget()
        self.image_input.itemClicked.connect(self.get_image)

        self.count_label = QLabel("Количесто деталей (шт.):")
        self.count_input = QLineEdit()

        self.price_label = QLabel("Цена:")
        self.price_input = QDoubleSpinBox()
        self.price_input.setMaximum(1000000)
        self.price_input.setMinimum(0)

        self.create_button = QPushButton("Создать")
        self.create_button.clicked.connect(self.create_puzzle)

        layout = QVBoxLayout()
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)
        layout.addWidget(self.image_input)
        layout.addWidget(self.image_label)
        layout.addWidget(self.plywood_label)
        layout.addWidget(self.plywood_input)
        layout.addWidget(self.count_label)
        layout.addWidget(self.count_input)
        layout.addWidget(self.price_label)
        layout.addWidget(self.price_input)
        layout.addWidget(self.create_button)

        self.setLayout(layout)
   
    def edit_puzzle(self, data):
        self.name_input.setText(data["name"])
        self.count_input.setText(str(data["count"]))
        self.current_image = data["image"]
        self.current_wood = data["plywood"]
        self.current_price = data["price"]
        self.price_input.setValue(self.current_price)
        for index in range(self.image_input.count()):
            item = self.image_input.item(index)
            if item.text() == self.current_image:
                self.get_image(item)
                break
        for index in range(self.plywood_input.count()):
            item = self.plywood_input.item(index)
            if item.text() == self.current_wood:
                self.plywood_input.setCurrentItem(item)
                break


    def create_puzzle(self):
        name = self.name_input.text()
        image = self.current_image
        plywood = self.current_wood
        price = self.price_input.value()
        cnt = self.count_input.text()
        if name and image and plywood and cnt.isdigit() and price > 0:
            d = { "name": name, "image": image, "plywood": plywood, "count": cnt, "price": price}
            self.puzzles_list.append(d)
            update_json(PUZZLES_FILE, self.puzzles_list, KEY_PUZZLES)
            self.close()


    def get_image(self, item):
        name = item.text()
        if name:
            pixmap = QPixmap(os.path.join(IMAGES_DIR, name)) 
            pixmap = scale_image(pixmap, 300, 300)
            self.image_label.setPixmap(pixmap)
            self.image_label.resize(pixmap.width(), pixmap.height())
            self.current_image = name
    
    
    def get_plywood(self, item):
        self.current_wood = item.text()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.create_puzzle()
            self.close()


