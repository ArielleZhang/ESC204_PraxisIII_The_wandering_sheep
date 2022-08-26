import serial
import time


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

ser.close()



while True:
    arduinoData = ser.readline()
    print(arduinoData)
