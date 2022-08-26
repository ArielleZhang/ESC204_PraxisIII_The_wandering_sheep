import sqlite3
import serial
import time

def record_data(records, db_list):
	for row in records:
		if(row[4] != None):
			temp = []
			temp2 = row[4].split()
			for x in range(len(temp2)):
				temp.append(int(temp2[x]))
			temp3 = {"id":row[0], 'owner': row[1], 'latitude': row[2], 'longitude': row[3], 'cluster':temp, 'belongs': row[5]}
			db_list.append(temp3)
		else:
			temp3 = {"id":row[0], 'owner': row[1], 'latitude': row[2], 'longitude': row[3], 'cluster':row[4], 'belongs': row[5]}
			db_list.append(temp3)
	
def get_records(cursor):
	query = """SELECT * FROM SHEEPS;"""
	cursor.execute(query)
	records = cursor.fetchall()
	return records

def update_table(conn, cursor, query):
	update = query
	cursor.execute(update)
	conn.commit()

def reset_table(conn, cursor):
	query = """UPDATE SHEEPS SET OWNER = 'A', LATITUDE = 14.3, LONGITUDE = 14.7, CLUSTER = '1001 1002 1003', BELONGS = 1000 WHERE ID = 1000"""
	update_table(conn, cursor, query)
	query = """UPDATE SHEEPS SET OWNER = 'A', LATITUDE = 14.5, LONGITUDE = 14.8, CLUSTER = NULL, BELONGS = 1000 WHERE ID = 1001"""
	update_table(conn, cursor, query)
	query = """UPDATE SHEEPS SET OWNER = 'A', LATITUDE = 14.2, LONGITUDE = 14.5, CLUSTER = NULL, BELONGS = 1000 WHERE ID = 1002"""
	update_table(conn, cursor, query)
	query = """UPDATE SHEEPS SET OWNER = 'A', LATITUDE = 14.2, LONGITUDE = 14.5, CLUSTER = NULL, BELONGS = 1000 WHERE ID = 1003"""
	update_table(conn, cursor, query)
	query = """UPDATE SHEEPS SET OWNER = 'B', LATITUDE = 15.2, LONGITUDE = 15.5, CLUSTER = '2001 2002', BELONGS = 2000 WHERE ID = 2000"""
	update_table(conn, cursor, query)
	query = """UPDATE SHEEPS SET OWNER = 'B', LATITUDE = 15.2, LONGITUDE = 15.5, CLUSTER = NULL, BELONGS = 2000 WHERE ID = 2001"""
	update_table(conn, cursor, query)
	query = """UPDATE SHEEPS SET OWNER = 'B', LATITUDE = 15.6, LONGITUDE = 15.2, CLUSTER = NULL, BELONGS = 2000 WHERE ID = 2002"""
	update_table(conn, cursor, query)
	query = """UPDATE SHEEPS SET OWNER = 'C', LATITUDE = 16.1, LONGITUDE = 16.2, CLUSTER = '3001 3002 3003', BELONGS = 3000 WHERE ID = 3000"""
	update_table(conn, cursor, query)
	query = """UPDATE SHEEPS SET OWNER = 'C', LATITUDE = 16.4, LONGITUDE = 16.6, CLUSTER = NULL, BELONGS = 3000 WHERE ID = 3001"""
	update_table(conn, cursor, query)
	query = """UPDATE SHEEPS SET OWNER = 'C', LATITUDE = 16.7, LONGITUDE = 16.8, CLUSTER = NULL, BELONGS = 3000 WHERE ID = 3002"""
	update_table(conn, cursor, query)
	query = """UPDATE SHEEPS SET OWNER = 'C', LATITUDE = 16.8, LONGITUDE = 16.9, CLUSTER = NULL, BELONGS = 3000 WHERE ID = 3003"""
	update_table(conn, cursor, query)
	
def case1(conn, cursor):#no missing sheep only mixing sheep
	query = """UPDATE SHEEPS SET OWNER = 'A', LATITUDE = 14.3, LONGITUDE = 14.7, CLUSTER = '1001 2001 1003', BELONGS = 1000 WHERE ID = 1000"""
	update_table(conn, cursor, query)
	query = """UPDATE SHEEPS SET OWNER = 'A', LATITUDE = 14.5, LONGITUDE = 14.8, CLUSTER = NULL, BELONGS = 1000 WHERE ID = 1001"""
	update_table(conn, cursor, query)
	query = """UPDATE SHEEPS SET OWNER = 'A', LATITUDE = 14.2, LONGITUDE = 14.5, CLUSTER = NULL, BELONGS = 1000 WHERE ID = 1002"""
	update_table(conn, cursor, query)
	query = """UPDATE SHEEPS SET OWNER = 'A', LATITUDE = 14.2, LONGITUDE = 14.5, CLUSTER = NULL, BELONGS = 1000 WHERE ID = 1003"""
	update_table(conn, cursor, query)
	query = """UPDATE SHEEPS SET OWNER = 'B', LATITUDE = 15.2, LONGITUDE = 15.5, CLUSTER = '2002', BELONGS = 2000 WHERE ID = 2000"""
	update_table(conn, cursor, query)
	query = """UPDATE SHEEPS SET OWNER = 'B', LATITUDE = 15.2, LONGITUDE = 15.5, CLUSTER = NULL, BELONGS = 2000 WHERE ID = 2001"""
	update_table(conn, cursor, query)
	query = """UPDATE SHEEPS SET OWNER = 'B', LATITUDE = 15.6, LONGITUDE = 15.2, CLUSTER = NULL, BELONGS = 2000 WHERE ID = 2002"""
	update_table(conn, cursor, query)
	query = """UPDATE SHEEPS SET OWNER = 'C', LATITUDE = 16.1, LONGITUDE = 16.2, CLUSTER = '3001 3002 3003 1002', BELONGS = 3000 WHERE ID = 3000"""
	update_table(conn, cursor, query)
	query = """UPDATE SHEEPS SET OWNER = 'C', LATITUDE = 16.4, LONGITUDE = 16.6, CLUSTER = NULL, BELONGS = 3000 WHERE ID = 3001"""
	update_table(conn, cursor, query)
	query = """UPDATE SHEEPS SET OWNER = 'C', LATITUDE = 16.7, LONGITUDE = 16.8, CLUSTER = NULL, BELONGS = 3000 WHERE ID = 3002"""
	update_table(conn, cursor, query)
	query = """UPDATE SHEEPS SET OWNER = 'C', LATITUDE = 16.8, LONGITUDE = 16.9, CLUSTER = NULL, BELONGS = 3000 WHERE ID = 3003"""
	update_table(conn, cursor, query)


def read_from_monitor(conn, cursor):
	ser = serial.Serial('COM14', baudrate = 115200, timeout=1)

	# Read and record the data
	data =[]                       # empty list to store the data
	while True:
		line = ser.readline()         # read a byte string
		if line:
			string_n = line.decode()  # decode byte string into Unicode  
			string = string_n.rstrip() # remove \n and \r
			print(string)
			data.append(string)           # add to the end of data list

			if(string and string[0] == "U"):
				print("reached update")
				#Decode the Sheep IDs with a sample data shape:
				#'''UPDATESL1000F1001F1002'''
				query = ""
				if string[6] == "S":
					#S Stands for Sheep
					i = 7
					while i in range(len(string)):
						if(string[i] == "L"):
						#then this means this is a leader sheep, update this leader sheep is
							query = "id = " + string[i:i+5] + ", " + "cluster = "
						else:
							#fill in the cluster for this leader sheep 
							query = query + string[i:i+5] + ", "
						i+=5
					query = query[0:-1]

				if string[6] == "G":
					#UPDATEGLATITUDE: 12.12345, LONGITUDE:10.12345
					#G Stands for GPS
					query = string[7:len(string)]
						
				print(query)
		
		time.sleep(0.1)            # wait (sleep) 0.1 seconds

def get_info_by_id(id_no, initial_db):
	for x in range(len(initial_db)):
		if(initial_db[x]['id'] == id_no):
			return initial_db[x]
	

def detect_mixed(initial_db):
	for x in range(len(initial_db)):
		if(initial_db[x]['cluster'] != None):
			num = int(str(initial_db[x]['id'])[0])
			for y in range(len(initial_db[x]['cluster'])):
				temp = int(str(initial_db[x]['cluster'][y])[0])
				if(num != temp):
					a = get_info_by_id(initial_db[x]['cluster'][y], initial_db)['owner']
					print("mixed sheep id:" + str(initial_db[x]['cluster'][y]) + " belongs to owner: "+ a)
			
initial_db = []
conn = sqlite3.connect('E:/University of Toronto/FASE ESC Praxis III Teaching Team - 2022 Winter - Student Work - Team 1034A/Design Milestones/Prototype/Back End/database.db')
cursor = conn.cursor()
case1(conn, cursor)
records = get_records(cursor)
record_data(records, initial_db)
for x in range(len(initial_db)):
	print(initial_db[x])
	print(' ')
	
detect_mixed(initial_db)

