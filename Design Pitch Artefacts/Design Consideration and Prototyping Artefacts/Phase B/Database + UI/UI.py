from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog
from PyQt5.uic import loadUi
import sys
from datetime import datetime
import sqlite3

from pyparsing import col

#TODO Emre could you make another database that just stores the missing sheep ID, location and time?
#we are gonna use this for the UI

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("XhosaUI.ui", self)
        self.tableWidget.setColumnWidth(0, 60)
        self.tableWidget.setColumnWidth(1, 150)
        self.tableWidget.setColumnWidth(2, 150)
        self.tableWidget.setColumnWidth(3, 78)
        self.tableWidget.setRowCount(150)

        self.btn_load.clicked.connect(self.loadData)
        

        #self.loadMissingSheep()

    '''
    def loadMissingSheep(self):
        #Update = [{"ID": "F1001", "Location": "Lon:12.123456, Lat:10.123456", "Time": "10:00"}]
        #update to the frontend missing sheep table whenever it detects missing sheep
        #TODO Still don't know if the row number can be reset or not
        self.tableWidget.setRowCount(150)
        row = 0
        update = [{"ID": "F1001", "Latitude": "10.123456", "Longitude": "12.123456", "Time": "12:00"}, {"ID": "F1000", "Latitude": "11.123456", "Longitude": "11.123456", "Time": "12:02"}, {"ID": "F3000", "Latitude": "10.123456", "Longitude": "10.123456", "Time": "12.03"}]
        
        for sheep in update:
            self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(sheep["ID"]))
            self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(sheep["Latitude"]))
            self.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(sheep["Longitude"]))
            self.tableWidget.setItem(row, 3, QtWidgets.QTableWidgetItem(sheep["Time"]))
            row = row + 1
    '''
    
    def loadData(self):
        connection = sqlite3.connect("missing.db")
        query = "SELECT * FROM MISSING;"
        result = connection.execute(query)
        for row_number, row_data in enumerate(result):
            #self.tableWidget.insertRow(row_number)
            for colum_number, data in enumerate(row_data):
                if colum_number == 0:
                    self.tableWidget.setItem(row_number, colum_number, QtWidgets.QTableWidgetItem(str(data)))
                if colum_number == 1:
                    #Latitude
                    self.tableWidget.setItem(row_number, 1, QtWidgets.QTableWidgetItem(str(data)))
                if colum_number == 2:
                    #Longitude
                    self.tableWidget.setItem(row_number, 2, QtWidgets.QTableWidgetItem(str(data)))
                if colum_number == 3:
                    self.tableWidget.setItem(row_number, 3, QtWidgets.QTableWidgetItem(str(data)))
                #if colum_number == 4:
                #    self.tableWidget.setItem(row_number, 2, QtWidgets.QTableWidgetItem(str(data)))


        connection.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainwindow = MainWindow()
    widget = QtWidgets.QStackedWidget()
    widget.addWidget(mainwindow)
    widget.setFixedHeight(600)
    widget.setFixedWidth(800)
    widget.show()


    try:
        sys.exit(app.exec_())
    except:
        print("Exiting")