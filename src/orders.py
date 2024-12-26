from src.common import *
from src.application import *

from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QAction, QIcon, QPixmap
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, 
                             QVBoxLayout, QPushButton, QListWidget, 
                             QMessageBox,QListWidgetItem, QComboBox, QHBoxLayout,
                             QDateEdit, QTableWidget, QTableWidgetItem)
import datetime

class Order(QWidget):
    def __init__(self, window):
        super().__init__()
        self.window = window
        self.clients = get_json(CLIENTS_FILE, KEY_CLIENTS)
        self.statuses = get_json(CLIENTS_FILE, KEY_STATUSES)
        self.puzzles = get_json(PUZZLES_FILE, KEY_PUZZLES)
        self.orders = get_json(CLIENTS_FILE, KEY_ORDERS)

        self.init_UI()
        
        self.chosen_puzzles = []
        self.status_input.addItems(self.statuses)
        self.client_input.addItems(self.clients)
        self.update_puzzle()
        self.current_sum = 0

    def init_UI(self):
        self.setWindowTitle("Заказ")

        self.status_label = QLabel("Статус:")
        self.status_input = QComboBox(self)
        self.status_input.setCurrentText(self.statuses[0])

        self.date_label = QLabel("Дата регистрации заказа:")
        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDisplayFormat("dd/MM/yyyy")
        self.date_input.setDate(datetime.date.today())


        self.client_label = QLabel("Клиент:")
        self.client_input = QComboBox(self)

        self.done_label = QLabel("Дата выполнения:")
        self.done_input = QDateEdit()
        self.done_input.setDisplayFormat("dd/MM/yyyy")
        self.done_input.setCalendarPopup(True)
        self.done_input.setDate(datetime.date.today())

        self.puzzles_label = QLabel("Пазлы:")
        self.puzzles_input = QListWidget()
        self.puzzles_input.itemClicked.connect(self.add_puzzle)

        self.puzzle_table = QTableWidget()
        self.puzzle_table.setColumnCount(4)
        self.puzzle_table.setHorizontalHeaderLabels(["Товар", "Цена", "Количество", "Сумма"])
        self.puzzle_table.currentCellChanged.connect(self.update_sum)

        self.save_btn = QPushButton("Сохранить")
        self.save_btn.clicked.connect(self.save)

        layout = QVBoxLayout()
        layout.addWidget(self.status_label)
        layout.addWidget(self.status_input)
        layout.addWidget(self.date_label)
        layout.addWidget(self.date_input)
        layout.addWidget(self.client_label)
        layout.addWidget(self.client_input)
        layout.addWidget(self.done_label)
        layout.addWidget(self.done_input)
        layout.addWidget(self.puzzles_label)
        layout.addWidget(self.puzzles_input)
        layout.addWidget(self.puzzle_table)
        layout.addWidget(self.save_btn)
        
        self.setLayout(layout)

    def edit_order(self, data):
        self.status_input.setCurrentText(data["status"])

        d = data["register"]
        self.date_input.setDate(QDate(d[0], d[1], d[2]))
        self.client_input.setCurrentText(data["client"])

        d = data["done"]
        self.done_input.setDate(QDate(d[0], d[1], d[2]))


        for i in data["data"]:
            for n in self.puzzles:
                if i["name"] == n["name"]:
                    self.puzzles.pop(self.puzzles.index(n))
            self.chosen_puzzles.append(i)

        self.update_table()
        self.update_puzzle()


    def save(self):
        today = datetime.date.today()
        if self.date_input.date() < today or self.done_input.date() < today:
            QMessageBox.warning(self, "Ошибка", "Дата введена неверно")
            return
        for row in range(len(self.chosen_puzzles)):
            self.update_sum(row)

        data = {
            "id": self.orders[-1]["id"] + 1 if self.orders else 0,
            "status": self.status_input.currentText(),\
            "register": self.date_input.date().getDate(),
            "client": self.client_input.currentText(),
            "done": self.done_input.date().getDate(),
            "data": self.chosen_puzzles,
            "shipped": ()
        }
        self.orders.append(data)
        update_json(CLIENTS_FILE, self.orders, KEY_ORDERS)
        self.close()


    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.save()
            update_dates()
            self.close()

    def update_puzzle(self):
        self.puzzles_input.clear()
        for indx, data in enumerate(self.puzzles, 1):
            item = QListWidgetItem(f"{indx}. {data['name']}")
            self.puzzles_input.addItem(item)

    def add_puzzle(self, item: QListWidgetItem):
        text = item.text()
        i = text.find(".")
        indx = int(text[:i])-1

        data = self.puzzles.pop(indx)
        self.chosen_puzzles.append( {"name": data["name"], "price": data["price"], "total": data["price"], "count": 1})
        self.update_table()
        self.update_puzzle()
        if (len(self.puzzles) == 0):
            self.puzzles_input.close()

    def update_table(self):
        self.puzzle_table.clear()
        L = len(self.chosen_puzzles)
        self.puzzle_table.setRowCount(L)
        for row in range(L):
            puzzle = self.chosen_puzzles[row]["name"]
            total = self.chosen_puzzles[row]["total"]
            price = self.chosen_puzzles[row]["price"]
            cnt = self.chosen_puzzles[row]["count"]

            item = QTableWidgetItem(str(puzzle))
            item2 = QTableWidgetItem(str(price))
            item3 = QTableWidgetItem(str(total))

            for i in [item, item2, item3]:
                i.setFlags(i.flags() & ~Qt.ItemFlag.ItemIsEditable)

            self.puzzle_table.setItem(row, 0, item)
            self.puzzle_table.setItem(row, 1, item2)
            self.puzzle_table.setItem(row, 2, QTableWidgetItem(str(cnt)))  
            self.puzzle_table.setItem(row, 3, item3)  

    def update_sum(self, row: int):
        price = self.puzzle_table.item(row, 1)
        cnt = self.puzzle_table.item(row, 2)
        if price and cnt:
            price = float(price.text()) if price.text() else 0
            cnt = int(cnt.text()) if cnt.text() else 0
            total = price * cnt if cnt else price
            self.puzzle_table.item(row, 3).setText(str(total))
            self.chosen_puzzles[row]["total"] = total
            self.chosen_puzzles[row]["count"] = cnt



class Orders_list(QWidget):
    def __init__(self, window):
        super().__init__()
        self.window = window
        self.orders = get_json(ORDERS_FILE, KEY_ORDERS)
        self.statuses = get_json(ORDERS_FILE, KEY_STATUSES)
        self.init_UI()

    def init_UI(self):
        self.setWindowTitle("Заказы")
        self.orders_input = QListWidget() 
        
        self.update_list()
       
        layout = QVBoxLayout()
        layout.addWidget(self.orders_input)
        self.setLayout(layout)

    def update_list(self):
        self.orders_input.clear()
        for indx, data in enumerate(self.orders):
            item = QListWidgetItem()

            
            name_label = QLabel(f"ID: {data['id']}")
            status_label = QLabel(f"Статус: {data['status']}")

            open_button = QPushButton()
            open_button.setIcon(QIcon(os.path.join(ICONS_DIR, "edit.png")))
            open_button.setIconSize(open_button.sizeHint())
            open_button.setFixedSize(open_button.iconSize())
            
            if data['status'] == self.statuses[1]:
                create_button = QPushButton()
                create_button.setIcon(QIcon(os.path.join(ICONS_DIR, "production.png")))
                create_button.setIconSize(create_button.sizeHint())
                create_button.setFixedSize(create_button.iconSize())
                create_button.clicked.connect(self.create_order)
                create_button.setObjectName(str(indx))

            if data['status'] == "Готов к отгрузке":
                deliver_button = QPushButton()
                deliver_button.setIcon(QIcon(os.path.join(ICONS_DIR, "deliver.png")))
                deliver_button.setIconSize(deliver_button.sizeHint())
                deliver_button.setFixedSize(deliver_button.iconSize())
                deliver_button.clicked.connect(self.deliver_order)
                deliver_button.setObjectName(str(indx))

            delete_button = QPushButton()
            delete_button.setIcon(QIcon(os.path.join(ICONS_DIR, "delete.png")))
            delete_button.setIconSize(delete_button.sizeHint())
            delete_button.setFixedSize(delete_button.iconSize())
            delete_button.clicked.connect(self.delete)
            delete_button.setObjectName(str(indx))
            
            open_button.setObjectName(str(indx))
            open_button.clicked.connect(self.open_order)

            layout = QHBoxLayout()
            layout.addWidget(name_label)
            layout.addWidget(status_label)
            layout.addWidget(open_button)
            if data['status'] == self.statuses[1]:
                layout.addWidget(create_button)
            elif data['status'] == "Готов к отгрузке":
                layout.addWidget(deliver_button)
            
            layout.addWidget(delete_button)
            self.orders_input.addItem(item)
            widget = QWidget()
            widget.setLayout(layout)
            item.setSizeHint(widget.sizeHint())
            self.orders_input.addItem(item)
            self.orders_input.setItemWidget(item, widget)
    
    def deliver_order(self):
        sender = self.sender()
        push_button = self.findChild(QPushButton, sender.objectName())
        indx = push_button.objectName()

        data = self.orders[int(indx)]
        self.window.deliver_order(data)
        self.quit()

    def create_order(self):
        sender = self.sender()
        push_button = self.findChild(QPushButton, sender.objectName())
        indx = push_button.objectName()

        data = self.orders[int(indx)]
        self.window.create_production_order(data)
        self.quit()

    def delete(self):
        sender = self.sender()
        push_button = self.findChild(QPushButton, sender.objectName())
        indx = push_button.objectName()

        data = self.orders.pop(int(indx))
        update_json(ORDERS_FILE, self.orders, KEY_ORDERS)
        self.update_list()

    def open_order(self):
        sender = self.sender()
        push_button = self.findChild(QPushButton, sender.objectName())
        indx = push_button.objectName()

        data = self.orders.pop(int(indx))
        update_json(ORDERS_FILE, self.orders, KEY_ORDERS)

        self.window.create_order(editable=True, data=data)
        self.quit()

    def quit(self):
        update_json(ORDERS_FILE, self.orders, KEY_ORDERS)
        update_dates()
        self.close()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape: self.quit()
    


class Production_order(QWidget):
    def __init__(self, window, order):
        super().__init__()
        self.window = window
        self.statuses = ["Принято в производство", "Выполнен"]
        self.puzzles = order["data"]
        
        self.id = order["id"]
        self.order = order
        reg = order["register"]
        done = order["done"]
        self.reg_date = QDate(reg[0], reg[1], reg[2])
        self.done_date = QDate(done[0], done[1], done[2])

        self.init_UI()
        self.status_input.addItems(self.statuses)
        self.update_table()

    def init_UI(self):
        self.setWindowTitle("Заказ")

        self.status_label = QLabel("Статус:")
        self.status_input = QComboBox(self)
        self.status_input.setCurrentText(self.statuses[0])

        self.date_label = QLabel("Дата регистрации заказа:")
        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDisplayFormat("dd/MM/yyyy")
        self.date_input.setDate(self.reg_date)


        self.done_label = QLabel("Дата выполнения:")
        self.done_input = QDateEdit()
        self.done_input.setDisplayFormat("dd/MM/yyyy")
        self.done_input.setCalendarPopup(True)
        self.done_input.setDate(self.done_date)

        self.puzzle_table = QTableWidget()
        self.puzzle_table.setColumnCount(2)
        self.puzzle_table.setHorizontalHeaderLabels(["Товар","Количество"])

        self.save_btn = QPushButton("Сохранить")
        self.save_btn.clicked.connect(self.save)

        layout = QVBoxLayout()
        layout.addWidget(self.status_label)
        layout.addWidget(self.status_input)
        layout.addWidget(self.date_label)
        layout.addWidget(self.date_input)
        layout.addWidget(self.done_label)
        layout.addWidget(self.done_input)
        layout.addWidget(self.puzzle_table)
        layout.addWidget(self.save_btn)
        
        self.setLayout(layout)


    def save(self):
        today = datetime.date.today()
        if self.date_input.date() < today or self.done_input.date() < today:
            QMessageBox.warning(self, "Ошибка", "Дата введена неверно")
            return

        data = {
            "id": self.id, 
            "status": self.status_input.currentText(),\
            "register": self.date_input.date().getDate(),
            "done": self.done_input.date().getDate(),
            "data": self.puzzles
        }

        orders = get_json(CLIENTS_FILE, KEY_PRODUCTION_ORDERS)
        orders.append(data)
        update_json(CLIENTS_FILE, orders, KEY_PRODUCTION_ORDERS)
        self.update_order(data["status"])
        self.close()

    def update_order(self, status):
        orders = get_json(CLIENTS_FILE, KEY_ORDERS)
        for i, d in enumerate(orders):
            if d["id"] == self.id:
                if status == self.statuses[0]:
                    orders[i]["status"] = "На производстве"
                else:
                    orders[i]["status"] = "Готов к отгрузке"
                break
        update_json(CLIENTS_FILE, orders, KEY_ORDERS)


    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.save()
            self.close()

    def update_table(self):
        self.puzzle_table.clear()
        L = len(self.puzzles)
        self.puzzle_table.setRowCount(L)
        for row in range(L):
            puzzle = self.puzzles[row]["name"]
            cnt = self.puzzles[row]["count"]

            item = QTableWidgetItem(str(puzzle))
            item2 = QTableWidgetItem(QTableWidgetItem(str(cnt)))
            
            for i in [item, item2]:
                i.setFlags(i.flags() & ~Qt.ItemFlag.ItemIsEditable)

            self.puzzle_table.setItem(row, 0, item)
            self.puzzle_table.setItem(row, 1, item2)  


class Client_order(QWidget):
    def __init__(self, window, order):
        super().__init__()
        self.window = window
        self.puzzles = order["data"]
        self.id = order["id"]
        self.order = order
        self.init_UI()
        self.update_table()

    def init_UI(self):
        self.setWindowTitle("Заказ клиента")

        self.puzzle_table = QTableWidget()
        self.puzzle_table.setColumnCount(4)
        self.puzzle_table.setHorizontalHeaderLabels(["Товар", "Цена", "Количество", "Сумма"])

        self.done_label = QLabel("Дата отгрузки:")
        self.deliver_date = QDateEdit()
        self.deliver_date.setReadOnly(True)
        self.deliver_date.setDisplayFormat("dd/MM/yyyy")
        self.deliver_date.setDate(datetime.date.today())

        self.save_btn = QPushButton("Сохранить")
        self.save_btn.clicked.connect(self.save)

        layout = QVBoxLayout()
        layout.addWidget(self.done_label)
        layout.addWidget(self.deliver_date)
        layout.addWidget(self.puzzle_table)
        layout.addWidget(self.save_btn)
        
        self.setLayout(layout)


    def save(self):
        self.update_order(self.order["status"])
        self.close()

    def update_order(self, status):
        orders = get_json(CLIENTS_FILE, KEY_ORDERS)
        for i, d in enumerate(orders):
            if d["id"] == self.id:
                orders[i]["status"] = "Отгружен клиенту"
                orders[i]["shipped"] = self.deliver_date.date().getDate() 
                break
        update_json(CLIENTS_FILE, orders, KEY_ORDERS)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.save()
            update_dates()
            self.close()

    def update_table(self):
        self.puzzle_table.clear()
        L = len(self.puzzles)
        self.puzzle_table.setRowCount(L)
        for row in range(L):
            puzzle = self.puzzles[row]["name"]
            total = self.puzzles[row]["total"]
            price = self.puzzles[row]["price"]
            cnt = self.puzzles[row]["count"]

            item = QTableWidgetItem(str(puzzle))
            item2 = QTableWidgetItem(str(price))
            item3 = QTableWidgetItem(str(total))
            item4 = QTableWidgetItem(str(cnt))

            for i in [item, item2, item3, item4]:
                i.setFlags(i.flags() & ~Qt.ItemFlag.ItemIsEditable)

            self.puzzle_table.setItem(row, 0, item)
            self.puzzle_table.setItem(row, 1, item2)
            self.puzzle_table.setItem(row, 2, item3)  
            self.puzzle_table.setItem(row, 3, item4)  


