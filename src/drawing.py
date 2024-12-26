import os

from src.common import *
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget, QInputDialog
from PyQt6.QtGui import QAction, QIcon



def draw_menu(window):
    menu_bar = window.menuBar()
    menu_main = menu_bar.addMenu("&Меню")
    menu_list = menu_bar.addMenu("&Список")
    menu_help = menu_bar.addMenu("&Помощь")


    plywood = QAction(QIcon(os.path.join(ICONS_DIR, 'new_puzzle.png')), '&Создать лист', window)
    plywood.setStatusTip("Создать фанерный лист")
    plywood.triggered.connect(window.create_plywood)
    
    order = QAction(QIcon(os.path.join(ICONS_DIR, 'order.png')), '&Создать заказ', window)
    order.setStatusTip("Создать заказ")
    order.triggered.connect(window.create_order)
    
    order_list = QAction(QIcon(os.path.join(ICONS_DIR, 'orders.png')), '&Список заказов', window)
    order_list.setStatusTip("Список заказов")
    order_list.triggered.connect(window.open_order_list)

    
    pricelist = QAction(QIcon(os.path.join(ICONS_DIR, 'price_list.png')), '&Прайс лист', window)
    pricelist.setStatusTip("Прайс лист")
    pricelist.triggered.connect(window.open_price_list)

    new_puzzle = QAction(QIcon(os.path.join(ICONS_DIR, 'new_puzzle.png')), '&Создать пазл', window)
    new_puzzle.setStatusTip("Создать новый пазл")
    new_puzzle.triggered.connect(window.create_puzzle)

    exit_action = QAction(QIcon(os.path.join(ICONS_DIR, 'exit.png')), '&Выход', window)
    exit_action.setStatusTip('Выход')
    exit_action.setShortcut('Esc')
    exit_action.triggered.connect(window.quit)

    about_action = QAction(QIcon(os.path.join(ICONS_DIR, 'about.png')), '&О программе', window)
    about_action.setStatusTip('О программе')
    about_action.triggered.connect(window.about)

    docs_action = QAction(QIcon(os.path.join(ICONS_DIR, 'docs.png')), '&Документация', window)
    docs_action.setStatusTip('Документация')
    docs_action.triggered.connect(window.docs)


    analytics = QAction(QIcon(os.path.join(ICONS_DIR, 'analytics.png')), '&Аналитика', window)
    analytics.setStatusTip('Аналитика')
    analytics.triggered.connect(window.analytics)

    plywood_list_action = QAction(QIcon(os.path.join(ICONS_DIR, 'plywood.png')), "&Фанерные листы", window)
    plywood_list_action.setStatusTip('Фанерные листы')
    plywood_list_action.triggered.connect(window.open_plywood_list)

    puzzles_list_action = QAction(QIcon(os.path.join(ICONS_DIR, 'puzzles.png')), "&Пазлы", window)
    puzzles_list_action.setStatusTip('Пазлы')
    puzzles_list_action.triggered.connect(window.open_puzzles_list)

    # MAIN 
    menu_main.addAction(new_puzzle)
    menu_main.addAction(plywood)
    menu_main.addAction(order)
    menu_main.addAction(pricelist)
    menu_main.addAction(exit_action)

    # LIST
    menu_list.addAction(plywood_list_action)
    menu_list.addAction(puzzles_list_action)
    menu_list.addAction(order_list)

    # HELP
    menu_help.addAction(about_action)
    menu_help.addAction(docs_action)
    menu_help.addAction(analytics)

def draw_objects(window):
    label = QLabel('This is a QLabel widget')
    layout = QVBoxLayout()
    layout.addWidget(label)



