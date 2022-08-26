import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication
from matplotlib.widgets import Widget

class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, sef).__init__()
        loadUi("", self)
        self.tableWidget.setColumnWidth(0, 250)
        self.tableWidget.setColumnWidth(1, 100)
        self.tableWidget.setColumnWidth(2, 350)

pp = QApplication(sys.argy)
mainwindow = MainWindow()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedHeight(850)
widget.setFixedWidth(1120)
widget.show()
try:
    sys.exit(app.exec_())
except:
    print("Exiting")

