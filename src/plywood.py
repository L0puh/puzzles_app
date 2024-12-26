from src.common import *
from src.application import *

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QIcon, QPixmap
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, 
                             QVBoxLayout, QPushButton, QListWidget, 
                             QListWidgetItem, QComboBox, QHBoxLayout)



class Plywood_card(QWidget):
    def __init__(self):
        super().__init__() 
        self.names_list = get_json(WOOD_FILE, KEY_WOODS)
        self.plywood_list = get_json(WOOD_FILE, KEY_PLYWOOD) 
        self.init_UI()
        self.current_thickness = 3
        if self.names_list:
            self.current_type = self.names_list[0]
        else: 
            self.current_type = "не найдено"


    def init_UI(self):
        self.setWindowTitle("Древесина")

        self.name_label = QLabel("Название листа:")
        self.name_input = QLabel()

        self.wood_type_label = QLabel("Вид древесины")
        self.wood_type_input = QListWidget()
        self.wood_type_input.itemClicked.connect(self.wood_type_clicked)

        self.thickness_label = QLabel("Толщина, мм")
        self.thickness_input = QLineEdit()
        self.thickness_input.textEdited.connect(self.thickness_edited)

        self.add_button = QPushButton("Сохранить изменения")
        self.add_button.clicked.connect(self.add_plywood)

        layout = QVBoxLayout()
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)
        layout.addWidget(self.wood_type_label)
        layout.addWidget(self.wood_type_input)
        layout.addWidget(self.thickness_label)
        layout.addWidget(self.thickness_input)
        layout.addWidget(self.add_button)
        self.setLayout(layout)
        
        self.update_names()
    
    def thickness_edited(self):
        if self.thickness_input.text().isdigit():
            self.current_thickness = int(self.thickness_input.text())
            s = f"{self.current_type}, {self.current_thickness}мм"
            self.name_input.setText(s)

    def wood_type_clicked(self, item):
        self.current_type = item.text()
        s = f"{self.current_type}, {self.current_thickness}мм"
        self.name_input.setText(s)


    def edit_plywood(self, name, thickness):
        for index in range(self.wood_type_input.count()):
            item = self.wood_type_input.item(index)
            if item.text() == name:
                self.wood_type_input.setCurrentItem(item)
                self.thickness_input.setText(thickness)
                break


    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.quit()
    
    def quit(self):
        self.plywood_list.sort()
        update_json(WOOD_FILE, self.plywood_list, KEY_PLYWOOD) 
        self.close()

    def add_plywood(self):
        wood = self.wood_type_input.currentItem()
        thickness = self.thickness_input.text().strip()
        if thickness.isdigit() and wood:
            wood = wood.text().strip()
            s = f"{wood}, {thickness}мм"
            self.name_input.setText(s)
            if s not in self.plywood_list:
                self.plywood_list.append(s)
            self.quit()

        self.thickness_input.clear()

    def update_names(self):
        self.wood_type_input.clear()
        self.wood_type_input.addItems(self.names_list)


class Plywood_list(QWidget):
    def __init__(self, window):
        super().__init__()
        self.window = window
        self.plywoods = get_json(WOOD_FILE, KEY_PLYWOOD)
        self.init_UI()

    def init_UI(self):
        self.setWindowTitle("Список")
        self.plywood_input = QListWidget() 
        
        self.update_list()
       
        layout = QVBoxLayout()
        layout.addWidget(self.plywood_input)
        self.setLayout(layout)
    
    
    def update_list(self):
        self.plywoods = get_json(WOOD_FILE, KEY_PLYWOOD)
        self.plywood_input.clear()
        for indx, plywood in enumerate(self.plywoods):
            item = QListWidgetItem()

            delete_icon = QIcon(os.path.join(ICONS_DIR, 'delete.png'))
            edit_icon   = QIcon(os.path.join(ICONS_DIR, 'edit.png'))

            item_label = QLabel(plywood)
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
            edit_button.clicked.connect(self.edit_plywood)
            delete_button.clicked.connect(self.delete_plywood)

            button_layout = QHBoxLayout()
            button_layout.addWidget(item_label)
            button_layout.addWidget(edit_button)
            button_layout.addWidget(delete_button)
            
            button = QWidget()
            button.setLayout(button_layout)
            item.setSizeHint(button.sizeHint())
            self.plywood_input.addItem(item)
            self.plywood_input.setItemWidget(item, button)

    def delete_plywood(self):
        sender = self.sender()
        push_button = self.findChild(QPushButton, sender.objectName())
        indx = push_button.objectName()
        self.plywoods.pop(int(indx))
        update_json(WOOD_FILE, self.plywoods, KEY_PLYWOOD)
        self.update_list()
    
    def edit_plywood(self):
        sender = self.sender()
        push_button = self.findChild(QPushButton, sender.objectName())
        indx = int(push_button.objectName())
        update_json(WOOD_FILE, self.plywoods, KEY_PLYWOOD)
        
        s = self.plywoods[indx].split(",")
        name, thickness = s[0], s[1][1:-2]
        self.plywoods.pop(indx)
        update_json(WOOD_FILE, self.plywoods, KEY_PLYWOOD)
        self.window.create_plywood(editable=True, name=name, thickness=thickness)
        self.quit()
        
    def quit(self):
        update_json(WOOD_FILE, self.plywoods, KEY_PLYWOOD)
        self.close()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape: self.quit()
