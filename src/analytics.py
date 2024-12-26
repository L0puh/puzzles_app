from src.common import *
from src.application import *

from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QAction, QIcon, QPixmap, QBrush, QColor
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, 
                             QVBoxLayout, QPushButton, QListWidget, 
                             QMessageBox,QListWidgetItem, QComboBox, QHBoxLayout,
                             QDateEdit, QTableWidget, QTableWidgetItem, QRadioButton)
import datetime
import matplotlib.pyplot as plt


class Analytics(QWidget):
    def __init__(self, window):
        super().__init__()
        self.window = window
        self.production_orders_list = get_json(ORDERS_FILE, KEY_PRODUCTION_ORDERS)
        self.orders_list = get_json(ORDERS_FILE, KEY_ORDERS)
        self.init_UI()

    def init_UI(self):
        self.setWindowTitle("Аналитика")

        self.table = QTableWidget(self)

        self.sales_radio = QRadioButton("По продажам", self)
        self.products_radio = QRadioButton("По товарам", self)
        self.sales_radio.setChecked(True)  
        self.sales_radio.toggled.connect(self.toggle_sales)

        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Наименование", "Количество", "Сумма", "Дата выполнения"])

        self.filter_button = QPushButton("Фильтровать", self)
       
        self.date = QDateEdit(self)
        self.date.setCalendarPopup(True)
        self.date.setDate(datetime.date.today())
       
        self.label_from = QLabel("Дата с:")
        self.label_to = QLabel("Дата по:")
        self.date_from = QDateEdit(self)
        self.date_from.setDisplayFormat("dd/MM/yyyy")
        self.date_from.setCalendarPopup(True)
        self.date_from.setDate(datetime.date.today())
        self.date_to = QDateEdit(self)
        self.date_to.setCalendarPopup(True)
        self.date_to.setDisplayFormat("dd/MM/yyyy")
        self.date_to.setDate(datetime.date.today())
        self.date.setDisplayFormat("dd/MM/yyyy")

        self.date.hide()

        layout = QVBoxLayout()
        
        layout.addWidget(self.sales_radio)
        layout.addWidget(self.products_radio)
        layout.addWidget(self.label_from)
        layout.addWidget(self.date_from)
        layout.addWidget(self.label_to)
        layout.addWidget(self.date_to)
        layout.addWidget(self.date)
        layout.addWidget(self.filter_button)
        layout.addWidget(self.table)
        
        self.main_layout = layout
        self.setLayout(self.main_layout)
       
        self.filter_button.clicked.connect(self.filter_data)
   
    def toggle_sales(self):
        if self.products_radio.isChecked():
            self.date_to.hide()
            self.date_from.hide()
            self.label_to.hide()
            self.label_from.hide()
            self.date.show()
        else:
            self.label_to.show()
            self.label_from.show()
            self.date_from.show()
            self.date_to.show()
            self.date.hide()

    def filter_data(self):
        if self.sales_radio.isChecked():
            self.display_sales_data()
        else:
            self.display_products_data()
    
    def display_products_data(self):
        tommorow = datetime.datetime.now() + datetime.timedelta(days=1)
        tommorow = [tommorow.year, tommorow.month, tommorow.day]
        products = []
        for order in self.production_orders_list:
            if order["status"] == "Принято в производство":
                if order["register"] == list(self.date.date().getDate()):
                    for d in order["data"]:
                        products.append([d, order["done"]])
             
        self.table.setRowCount(len(products))
        self.table.setColumnCount(4)
        if len(products) == 0:
            QMessageBox.warning(self, "Не найдено", 
                            "Товары с указанной датой не обнаружены")
            return

        for row, prod in enumerate(products):
            name = prod[0]["name"]
            cnt = prod[0]["count"]
            done = prod[1]
            total = prod[0]["total"]
            
            date = f"{done[2]}/{done[1]}/{done[0]}"
            item1, item2 = QTableWidgetItem(name), QTableWidgetItem(str(cnt))
            item3, item4  = QTableWidgetItem(str(total)), QTableWidgetItem(date)
            if done == tommorow:
                item4.setBackground(QBrush(QColor(255, 0, 0)))

            self.table.setItem(row, 0, item1)
            self.table.setItem(row, 1, item2)
            self.table.setItem(row, 2, item3)
            self.table.setItem(row, 3, item4)


    def display_sales_data(self):
        products = []
        

        for order in self.orders_list:
            d = order["register"]
            d2 = self.date_from.date().getDate()
            d3 = self.date_to.date().getDate()
            t1 = d[0] >= d2[0] and d[1] >= d2[1] and d[2] >= d2[2]
            t2 = d[0] <= d3[0] and d[1] <= d3[1] and d[2] <= d3[2]
            if t1 and t2:
                products += order["data"]

             
        self.table.setRowCount(len(products))
        self.table.setColumnCount(3)
        if len(products) == 0:
            QMessageBox.warning(self, "Не найдено", 
                            "Товары с указанной датой не обнаружены")
            return
        for row, prod in enumerate(products):
            name = prod["name"]
            cnt = prod["count"]
            total = prod["total"]
            self.table.setItem(row, 0, QTableWidgetItem(name))
            self.table.setItem(row, 1, QTableWidgetItem(str(cnt)))
            self.table.setItem(row, 2, QTableWidgetItem(str(total)))
            
        self.plot_sales_graph(products)

    def plot_sales_graph(self, sales_data):
        labels, totals = [], []
        for p in sales_data:
            labels.append(p["name"])
            totals.append(p["total"])

        plt.bar(labels, totals)
        plt.xlabel("Товары")
        plt.ylabel("Сумма")
        plt.title("Продажи пазлов")
        def on_key(event):
            if event.key == 'escape':  
                plt.close() 
        plt.gcf().canvas.mpl_connect('key_press_event', on_key)

        plt.show()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.close()
