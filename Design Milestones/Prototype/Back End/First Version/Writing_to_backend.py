import sqlite3
import serial
import time
from datetime import datetime


#listens to the arduino serial monitor
def listenSerialMonitor(conn, cursor, conn2, cursor2):
    
    ser = serial.Serial('COM13', baudrate = 115200, timeout = 1)
    while True:
        time.sleep(1)
        arduinoData = ser.readline()
        print(arduinoData)
        try:
            val = arduinoData.decode("utf-8")
        except:
            pass
        print(val)
        #print(val)
        print(parseString(val))
        info = parseString(val)

        if(info != None and len(info) == 5):
            updateDB(conn, info[3], cursor, info[0], info[1], info[2], info[4])
            if(info[2][0] == "3000"):
                updateMissingSheep(cursor, info[3], conn2, cursor2)
        
        #then update the missing sheep database here

    #string format should be ULA = 17.00, LO = 36.00UL3000F3001F30040071 (last four digit starting from 1111 increase)
    #info = parseString("ULA = 22.08, LO = 38.45UL30001321", cursor)
    
    #if(info != None and len(info) == 5):
    #   updateDB(conn, info[3], cursor, info[0], info[1], info[2], info[4])
    
    #print(info[2][0])
    


    # 3 is info [3] i think
        
        #then update the missing sheep database here




            
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
def updateDB(conn, update, cursor, lat, lon, ids, key):
        cluster = ""
        for i in ids:
            cluster = cluster + str(i)
        query = "INSERT INTO SHEEPS VALUES (" + key  + ", " + str(ids[0]) + ", " + str(lat) + ", " + str(lon) + ", " + str(cluster) + "," + str(update) +");"
        executeQuery(conn, cursor, query)
    
    



def MissingSheep(cursor, update):

    #from the database get the results
    #assume one missing sheep at a time
    cursor.execute("SELECT * FROM SHEEPS WHERE BELONGS = " + str(update) + ";")
    news = cursor.fetchall()

    cursor.execute("SELECT * FROM SHEEPS WHERE BELONGS = " + str(update-1) + ";")
    olds = cursor.fetchall()


    #first check NULL
    for new in news:
        if(len(new[4]) == 4):
            print([new[1], new[2], new[3], datetime.now().strftime("%H:%M:%S")])
            return [new[1], new[2], new[3], datetime.now().strftime("%H:%M:%S")]
    
    new_cmp = []
    old_cmp = []
    missing = ["", "", "", ""]
    missing_loc = ""

    for old in olds:
        old_clusters = []
        for a in range(len(old[4])//4):
            old_clusters.append(old[4][a*4:(a*4+4)])
        old_cmp.append(old_clusters)
                
    for new in news:       
        new_clusters = []   
        for b in range(len(new[4])//4):
            new_clusters.append(new[4][b*4:(b*4+4)])
        new_cmp.append(new_clusters)
    
    for new in new_cmp:
        for old in old_cmp:
            if new[0] == old[0]:
                for old_id in old:
                    if(not old_id in new):
                        for rec_new in new_cmp:
                            for item in rec_new:
                                if item == old_id:
                                    return
                                else:
                                    missing[0] = old_id
                                    missing[3] = datetime.now().strftime("%H:%M:%S")
                                    missing_loc = new[0]
    
    for new in news:
        if new[1] == missing_loc:
            missing[1] = new[2]
            missing[2] = new[3]
    
    return missing


def updateMissingSheep(cursor, update, conn2, cursor2):
    missing = MissingSheep(cursor, update)
    if(not missing[0] == ""):
        query = "INSERT INTO MISSING VALUES ("+ missing[0] + ',' + str(missing[1]) + ','+ str(missing[2]) + ',' + "'" + missing[3] + "'" + ");"
        print(query)
        executeQuery(conn2, cursor2, query)





def parseString(string, cursor):
    if(len(string) > 0 and string[0] == 'U'):
        key = string[-4:-1]
        print(key)
        string = string[0:-4]
        a = string.split('U')
        coord_str = a[1]
        c = coord_str.split('=')
        lat = c[1].split(',')[0][1:]
        lon = c[2][1:]
        id_str = a[2]
        ids = id_str[1:].split('F')
        cursor.execute("SELECT * FROM SHEEPS WHERE OWNER = " + str(ids[0]) + ";")
        records = cursor.fetchall()
        print(records)

        update = 1 + records[-1][-1]
        print(update)
        print([lat,lon,ids, update, key])##
        return [lat,lon,ids, update, key]


if __name__ == '__main__':
    #path = 'C:\\Users\\emrec\\OneDrive\\Desktop\\database.db'
    #path2 = 'C:\\Users\\emrec\\OneDrive\\Desktop\\missing.db'
    path = "E:\\University of Toronto\\FASE ESC Praxis III Teaching Team - 2022 Winter - Student Work - Team 1034A\\Design Milestones\\Prototype\\Back End\\new\\database.db"
    path2 = "E:\\University of Toronto\\FASE ESC Praxis III Teaching Team - 2022 Winter - Student Work - Team 1034A\\Design Milestones\\Prototype\\Back End\\new\\missing.db"
    
    conn = connect(path)
    cursor = getCursor(conn)

    conn2 = connect(path2)
    cursor2 = getCursor(conn2)

    #executeQuery(conn, cursor, """UPDATE SHEEPS SET CLUSTER = '1001 1002' WHERE ID = 1000""")
    #executeQuery(conn2, cursor2, """INSERT INTO MISSING VALUES (1003, 4.3, 5.2, '12:54:13')""")
    #db = retrieveDB(cursor)
    #print(missingSheep(db))
    #updateMissing(conn2, cursor, cursor2)
    listenSerialMonitor(conn, cursor, conn2, cursor2)

    #parseString('UPDATE_LATITUDE = 17.911847, LONGITUDE = 36.436322_L1000F1001F1002F1003F1004F1005')