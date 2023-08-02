import mysql.connector

db = mysql.connector.connect(
)

cursor = db.cursor()

def sqlExecute(cmd):
    cursor.execute(cmd)
    db.commit()

def sqlExecuteValues(cmd, values):
    cursor.execute(cmd, values)
    db.commit()