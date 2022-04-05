from PyQt5.Qt import *


def deal_menu(menubar):
    fileMenu = menubar.addMenu('&文件')
    openaction = fileMenu.addAction('&打开')
    openaction.setShortcut("Ctrl+O")
    openaction.triggered.connect(open_file)

    exitaction = fileMenu.addAction('&退出')
    exitaction.setShortcut("Ctrl+Q")
    exitaction.triggered.connect(qApp.quit)

    saveaction = fileMenu.addAction('&保存')
    saveaction.setShortcut("Ctrl+S")
    saveaction.triggered.connect(save_file)

    captureMenu = menubar.addMenu('&捕获')
    startaction = captureMenu.addAction('&开始')
    startaction.setShortcut("Ctrl+E")
    startaction.triggered.connect(start_capture)

    stopaction = captureMenu.addAction('&停止')
    stopaction.setShortcut("Ctrl+T")
    stopaction.triggered.connect(stop_capture)

    analyseMenu = menubar.addMenu('&分析')
    # TODO

    helpMenu = menubar.addMenu('&帮助')
    aboutaction = helpMenu.addAction('&关于')
    aboutaction.setShortcut("F11")
    aboutaction.triggered.connect(about_message)


def open_file():
    # TODO
    pass


def save_file():
    # TODO
    pass


def start_capture():
    # TODO
    pass


def stop_capture():
    # TODO
    pass


def about_message():
    # TODO
    pass
