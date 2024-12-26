import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QMainWindow, QMessageBox, QVBoxLayout, QPushButton, QHBoxLayout 

from src.drawing import * 
from src.common import *
from src.application import *
from src.puzzle import *
from src.plywood import *
from src.orders import *
from src.price_list import *  
from src.analytics import Analytics

class Window(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle("APPLICATION")
        self.setGeometry(300, 300, 300, 300)

        self.central = QWidget(self)

        button_plywoods = QPushButton("Открыть список фанерных листов")
        button_plywoods.clicked.connect(self.open_plywood_list)
       
        button_puzzles = QPushButton("Открыть список пазлов")
        button_puzzles.clicked.connect(self.open_puzzles_list)
      
        button_pricelist = QPushButton("Открыть прайс-лист")
        button_pricelist.clicked.connect(self.open_price_list)
        
        button_pricelist.setFixedSize(button_pricelist.sizeHint())
        button_puzzles.setFixedSize(button_puzzles.sizeHint())
        button_plywoods.setFixedSize(button_plywoods.sizeHint())
        
        button_layout = QHBoxLayout()
        button_layout.addWidget(button_puzzles)
        button_layout.addWidget(button_plywoods)
        button_layout.addWidget(button_pricelist)
        
        button_layout.setSpacing(0)  
        button_layout.setContentsMargins(0, 0, 0, 0)  

            
        self.central.setLayout(button_layout)
        self.setCentralWidget(self.central)
        self.status_bar = self.statusBar()
       
        draw_menu(self)
        draw_objects(self)

    def docs(self):
        with open("./docs/docs.html", "r") as file:
            QMessageBox.about(self, "Docs", file.read())

    def about(self):
        with open("./docs/about.html", "r") as file:
            QMessageBox.about(self, "About", file.read())

    def quit(self): 
        exit(0)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.quit()

    def create_puzzle(self, editable=False, data={}):
        self.puzzle = Puzzles()
        if editable:
            self.puzzle.edit_puzzle(data)
        self.puzzle.show()

    def create_plywood(self, editable=False, name="", thickness=""):
        self.card = Plywood_card()
        if editable:
            self.card.edit_plywood(name, thickness)
        self.card.show()

    def open_plywood_list(self):
        self.plywood_list = Plywood_list(self)
        self.plywood_list.show()

    def open_puzzles_list(self):
        self.puzzles_list = Puzzles_list(self)
        self.puzzles_list.show()

    def open_price_list(self):
        self.price_list = Price_list(self)
        self.price_list.show()

    def create_order(self, editable = False, data = {}):
        self.order = Order(self)
        if editable: self.order.edit_order(data)
        self.order.show()
        
    def open_order_list(self):
        self.order_list = Orders_list(self)
        self.order_list.show()

    def create_production_order(self, order):
        self.production_order = Production_order(self, order)
        self.production_order.show()

    def deliver_order(self, order):
        self.production_order = Client_order(self, order)
        self.production_order.show()

    def analytics(self):
        self.analytics_widget = Analytics(self)
        self.analytics_widget.show()
        pass

