import json, os
from collections import defaultdict

from src.common import *
import datetime

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, 
                             QVBoxLayout, QPushButton, QListWidget, 
                             QListWidgetItem, QComboBox, QHBoxLayout, QDoubleSpinBox)

from PyQt6.QtGui import QAction, QIcon, QPixmap


def get_images(location):
    try:
        files = os.listdir(location)
        files = [f for f in files if os.path.isfile(os.path.join(location, f))]
        return files
    except: 
        print("error in getting images:", location)
        return []

def scale_image(pixmap, max_width, max_height):
    original_width = pixmap.width()
    original_height = pixmap.height()
    width_ratio = max_width / original_width
    height_ratio = max_height / original_height
    scaling_factor = min(width_ratio, height_ratio)
    new_width = int(original_width * scaling_factor)
    new_height = int(original_height * scaling_factor)

    return pixmap.scaled(new_width, new_height) 



def get_json(file, key) -> list:
    file = open(os.path.join(JSON_DIR, file), "r", encoding="utf-8")
    assert(file)
    data = json.load(file)
    file.close()
    
    return data[key]

def update_json(file, new_data, key):
    path = os.path.join(JSON_DIR, file)
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)
        file.close()

    data[key] = new_data
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)
        file.close()

def update_dates():
    production = get_json(ORDERS_FILE, KEY_PRODUCTION_ORDERS)
    orders = get_json(ORDERS_FILE, KEY_ORDERS)

    today = datetime.date.today()

    for p in production:
        if p["status"] == "Принято в производство":
            d = p["done"]
            if d[0] <= today.year and d[1] <= today.month and d[2] <= today.day:
                for o in orders:
                    if o["id"] == p["id"]:
                        o["status"] = "Готов к отгрузке"
                        p["status"] = "Выполнен"
                        break

    update_json(ORDERS_FILE, orders, KEY_ORDERS)
    update_json(ORDERS_FILE, production, KEY_PRODUCTION_ORDERS)
