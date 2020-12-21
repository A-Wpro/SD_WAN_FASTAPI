import fastapi
import mysql.connector


mydb = mysql.connector.connect(
  host="127.0.0.1",
  user="root",
  password="molomo2404",
    database = "SD_Wan"
)

print(mydb)

from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from typing import Optional
import codecs
import os


def actions_RL():
    return "hello"


test = actions_RL()
app = FastAPI()
file = codecs.open("Index.html", "r")


@app.get("/", response_class=HTMLResponse)
def Docu():
    docuStr = "Voici la liste des features : GenerateOnosStruc(Param1: int, Param2: int, Param3: int, Param4: int) that generate Onos struc"

    return file.read()


@app.get("/GenerateOnosStruc")
def GenerateOnosStruc():
    print(test)
    return {"message": "World" + test}



# PARTIE MYSQL a completer plus tard
"""
mycursor = mydb.cursor()

sql = "INSERT INTO Graph_Onos (address) VALUES (%s, %s)"
val = ("John", "Highway 21")
mycursor.execute(sql, val)



# mydb.commit()

def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        binaryData = file.read()
        print(binaryData)
    return binaryData

def insertBLOB(photo):
    print("Inserting BLOB into python_employee table")
    try:
        connection = mysql.connector.connect(host="127.0.0.1",
                                             user="root",
                                             password="molomo2404",
                                             database = "SD_Wan")

        cursor = connection.cursor()
        sql_insert_blob_query = ""INSERT INTO Graph_Onos (Graph) VALUES (%s)""

        empPicture = convertToBinaryData(photo)
        # empPicture = photo
        # Convert data into tuple format
        insert_blob_tuple = (empPicture,)
        result = cursor.execute(sql_insert_blob_query, insert_blob_tuple)
        connection.commit()
        print("Image and file inserted successfully as a BLOB into python_employee table", result)

    except mysql.connector.Error as error:
        print("Failed inserting BLOB data into MySQL table {}".format(error))

    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

insertBLOB("/Users/tomwilliams/Downloads/minion.jpg")
# insertBLOB("D:\Python\Articles\my_SQL\images\scott_photo.png")






def write_file(data, filename):
    # Convert binary data to proper format and write it on Hard Disk
    with open(filename, 'wb') as file:
        file.write(data)

def readBLOB(id, photo):
    print("Reading BLOB data from python_employee table")

    try:
        connection = mysql.connector.connect(host="127.0.0.1",
                                             user="root",
                                             password="molomo2404",
                                             database = "SD_Wan")

        cursor = connection.cursor()
        sql_fetch_blob_query = ""SELECT * from Graph_Onos where Num_Graph = %s""
        print(sql_fetch_blob_query)
        cursor.execute(sql_fetch_blob_query, (id,))
        record = cursor.fetchall()
        for row in record:
            print("Id = ", row[0], )
            image = row[1]
            print("Storing employee image and bio-data on disk \n")
            write_file(image, photo)
    except mysql.connector.Error as error:
        print("Failed to read BLOB data from MySQL table {}".format(error))

    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

readBLOB(5, "/Users/tomwilliams/OneDrive - ESME/Esme_inge_3/Majeur_IA/SD_WAN/minion.jpg")
"""