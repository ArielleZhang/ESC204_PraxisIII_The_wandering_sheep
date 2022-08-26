import sqlite3
import serial
import time
from datetime import datetime

#listens to the arduino serial monitor
def listenSerialMonitor(conn, cursor):
    ser = serial.Serial('COM14', baudrate = 115200, timeout = 1)
    while True:
        time.sleep(1)
        arduinoData = ser.readline()
        #print(arduinoData)
        val = arduinoData.decode("utf-8")
        print(val)
        #print(val)
        print(parseString(val))
        l = parseString(val)
        if(l != None and len(l) == 3):
            for x in range(len(l)):
                updateDB(conn, cursor, 'latitude', l[0], l[2][x])
                updateDB(conn, cursor, 'longitude', l[1], l[2][x])
            
#connects to the db
def connect(dbPath):
    conn = sqlite3.connect(dbPath)
    return conn
#gets the cursor object
def getCursor(conn):
    cursor = conn.cursor()
    return cursor
#stores all the db into the list records
def retrieveDB(cursor):
    cursor.execute("""SELECT * FROM SHEEPS;""")
    records = cursor.fetchall()
    return records

def retrieveDB2(cursor):
    cursor.execute("""SELECT * FROM MISSING;""")
    records = cursor.fetchall()
    return records

    #print(records)
#executes the given query
def executeQuery(conn, cursor, query):
    cursor.execute(query)
    conn.commit()
#updates the longitude or the langitude depending on the field
def updateDB(conn, cursor, field, newVal, id):
    if(field == 'longitude'):
        query = 'UPDATE SHEEPS SET ' + str(field.upper()) + ' = ' + str(newVal) + ' WHERE ID = ' + str(id) + ';'
        #print(query)
        executeQuery(conn, cursor, query)
    if(field == 'latitude'):
        query = 'UPDATE SHEEPS SET ' + str(field.upper()) + ' = ' + str(newVal) + ' WHERE ID = ' + str(id) + ';'
        executeQuery(conn, cursor, query)
    #if(field == 'cluster'):
    #    query = 

def missingSheep(db):
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


def updateMissing(conn2, cursor, cursor2):
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



def parseString(string):
    if(len(string) > 0 and string[0] == '_'):
        a = string.split('_')
        coord_str = a[1]
        c = coord_str.split('=')
        d = c[1].split(',')[0][1:]
        e = c[2][1:]
        id_str = a[2]
        b = id_str[1:].split('F')
        return [d,e,b]


if __name__ == '__main__':
    path = 'C:\\Users\\emrec\\OneDrive\\Desktop\\database.db'
    path2 = 'C:\\Users\\emrec\\OneDrive\\Desktop\\missing.db'
    #path = "E:\\University of Toronto\\FASE ESC Praxis III Teaching Team - 2022 Winter - Student Work - Team 1034A\\Design Milestones\\Prototype\\Back End\\new\\database.db"
    #path2 = "E:\\University of Toronto\\FASE ESC Praxis III Teaching Team - 2022 Winter - Student Work - Team 1034A\\Design Milestones\\Prototype\\Back End\\new\\missing.db"
    
    conn = connect(path)
    cursor = getCursor(conn)

    conn2 = connect(path2)
    cursor2 = getCursor(conn2)

    #executeQuery(conn, cursor, """UPDATE SHEEPS SET CLUSTER = '1001 1002' WHERE ID = 1000""")
    #executeQuery(conn2, cursor2, """INSERT INTO MISSING VALUES (1003, 4.3, 5.2, '12:54:13')""")
    #db = retrieveDB(cursor)
    #print(missingSheep(db))
    #updateMissing(conn2, cursor, cursor2)
    listenSerialMonitor(conn, cursor)

    #parseString('UPDATE_LATITUDE = 17.911847, LONGITUDE = 36.436322_L1000F1001F1002F1003F1004F1005')