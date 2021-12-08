import mysql.connector
import os 
from dotenv import load_dotenv

class nemesis_db:
  def __init__():
    load_dotenv()
    mydb = mysql.connector.connect(
      user=os.getenv("SQL_USER"),
      host=os.getenv("SQL_HOST"),
      password=os.getenv("SQL_PASSWORD"),
    )

    mycursor = mydb.cursor()
    mycursor.execute("SHOW DATABASES")
    for database in mycursor:
      mycursor.
    mycursor.execute("CREATE DATABASE nemesis")