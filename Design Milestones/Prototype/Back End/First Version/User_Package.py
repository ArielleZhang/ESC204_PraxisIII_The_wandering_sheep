import sqlite3
import serial
import time
from datetime import datetime


from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog
from PyQt5.uic import loadUi
import sys
from datetime import datetime
import sqlite3

from pyparsing import col



class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("XhosaUI.ui", self)
        self.tableWidget.setColumnWidth(0, 60)
        self.tableWidget.setColumnWidth(1, 150)
        self.tableWidget.setColumnWidth(2, 150)
        self.tableWidget.setColumnWidth(3, 78)
        self.tableWidget.setRowCount(150)

        #self.btn_load.clicked.connect(self.loadMissingSheep)
        
        path = 'E:\\University of Toronto\\FASE ESC Praxis III Teaching Team - 2022 Winter - Student Work - Team 1034A\\Design Milestones\\Prototype\\Back End\\new\\database.db'
        #path2 = 'E:\\University of Toronto\\FASE ESC Praxis III Teaching Team - 2022 Winter - Student Work - Team 1034A\\Design Milestones\\Prototype\\Back End\\new\\missing.db'
        #conn2 = connect(path2)
        #cursor2 = getCursor(conn2)

        self.listenSerialMonitor(self.connect(path), self.getCursor(self.connect(path)))
        self.loadData()

    #executeQuery(conn, cursor, """UPDATE SHEEPS SET CLUSTER = '1001 1002' WHERE ID = 1000""")
    #executeQuery(conn2, cursor2, """INSERT INTO MISSING VALUES (1003, 4.3, 5.2, '12:54:13')""")
    #db = retrieveDB(cursor)
    #print(missingSheep(db))
    #updateMissing(conn2, cursor, cursor2)
    

    #parseString('UPDATE_LATITUDE = 17.911847, LONGITUDE = 36.436322_L1000F1001F1002F1003F1004F1005')
    
    
    def loadData(self):
        connection = sqlite3.connect("missing.db")
        query = "SELECT * FROM MISSING;"
        result = connection.execute(query)
        for row_number, row_data in enumerate(result):
            #self.tableWidget.insertRow(row_number)
            for colum_number, data in enumerate(row_data):
                if colum_number == 0:
                    now = datetime.now()
                    self.tableWidget.setItem(row_number, colum_number, QtWidgets.QTableWidgetItem(str(data)))
                    self.tableWidget.setItem(row_number, 3, QtWidgets.QTableWidgetItem(now.strftime("%H:%M:%S")))
                if colum_number == 1:
                    #Latitude
                    self.tableWidget.setItem(row_number, 1, QtWidgets.QTableWidgetItem(str(data)))
                if colum_number == 2:
                    #Longitude
                    self.tableWidget.setItem(row_number, 2, QtWidgets.QTableWidgetItem(str(data)))

        connection.close()

    #listens to the arduino serial monitor
    def listenSerialMonitor(self, conn, cursor):
        ser = serial.Serial('COM4', baudrate = 115200, timeout = 1)
        while True:
            time.sleep(1)
            arduinoData = ser.readline()
            
            #print(arduinoData)
            val = arduinoData.decode("utf-8")
            print(val)
            #print(val)
            print(self.parseString(val))
            l = self.parseString(val)
            if(l != None and len(l) == 3):
                for x in range(len(l)):
                    self.updateDB(conn, cursor, 'latitude', l[0], l[2][x])
                    self.updateDB(conn, cursor, 'longitude', l[1], l[2][x])
            
    #connects to the db
    def connect(self, dbPath):
        conn = sqlite3.connect(dbPath)
        return conn

    #gets the cursor object
    def getCursor(self, conn):
        cursor = conn.cursor()
        return cursor

    #stores all the db into the list records
    def retrieveDB(self, cursor):
        cursor.execute("""SELECT * FROM SHEEPS;""")
        records = cursor.fetchall()
        return records

    def retrieveDB2(self, cursor):
        cursor.execute("""SELECT * FROM MISSING;""")
        records = cursor.fetchall()
        return records

        #print(records)
    #executes the given query
    def executeQuery(self, conn, cursor, query):
        cursor.execute(query)
        conn.commit()
    #updates the longitude or the langitude depending on the field

    def updateDB(self, conn, cursor, field, newVal, id):
        if(field == 'longitude'):
            query = 'UPDATE SHEEPS SET ' + str(field.upper()) + ' = ' + str(newVal) + ' WHERE ID = ' + str(id) + ';'
            #print(query)
            executeQuery(conn, cursor, query)
        if(field == 'latitude'):
            query = 'UPDATE SHEEPS SET ' + str(field.upper()) + ' = ' + str(newVal) + ' WHERE ID = ' + str(id) + ';'
            executeQuery(conn, cursor, query)
        #if(field == 'cluster'):
        #    query = 

    def missingSheep(self, db):
        follower_ids = []
        sheeps_in_cluster = []
        missing = []
        for x in range(len(db)):
            if(db[x][4] != None and db[x][4] != ''):
                ids = db[x][4].split()
                for aydi in ids:
                    sheeps_in_cluster.append(int(aydi))
            else:
                follower_ids.append([db[x][0], db[x][2], db[x][3]])
        for x in range(len(follower_ids)):
            if(follower_ids[x][0] not in sheeps_in_cluster):
                missing.append([follower_ids[x][0], follower_ids[x][1], follower_ids[x][2], datetime.now().strftime("%H:%M:%S")])
                #print('missing sheep id:'+ str(follower_ids[x][0]) + ', latitude:' +str(follower_ids[x][1]) + ', longitude:' +str(follower_ids[x][2]) + ', time:' + datetime.now().strftime("%H:%M:%S"))
        return missing


        #print(follower_ids)
        #print(sheeps_in_cluster)


    def updateMissing(self, conn2, cursor, cursor2):
        db2 = retrieveDB2(cursor2)#missing sheep database
        db = retrieveDB(cursor)#sheeps databse
        missing = missingSheep(db)
        sheep_ids = [x[0] for x in db]
        missing_ids = [x[0] for x in  db2]
        new_missing_ids = [x[0] for x in missing]
        for x in range(len(new_missing_ids)):
            if(new_missing_ids[x] in missing_ids):
                executeQuery(conn2, cursor2, "UPDATE MISSING SET LATITUDE = "+ str(missing[x][1]) + ', LONGITUDE = '+ str(missing[x][2]) + ", TIME = '" + missing[x][3] + "' WHERE ID = " + str(missing[x][0]) + ';')
            else:
                executeQuery(conn2, cursor2, "INSERT INTO MISSING VALUES ("+ str(missing[x][0])+','+str(missing[x][1])+','+str(missing[x][2])+','+"'"+missing[x][3]+"');")

        #print(sheep_ids)
        #print(missing_ids)
        #print(new_missing_ids)
        #print(missing)

    def parseString(self, string):
        if(len(string) > 0 and string[0] == '_'):
            a = string.split('_')
            coord_str = a[1]
            c = coord_str.split('=')
            d = c[1].split(',')[0][1:]
            e = c[2][1:]
            id_str = a[2]
            b = id_str[1:].split('F')
            return [d,e,b]

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


