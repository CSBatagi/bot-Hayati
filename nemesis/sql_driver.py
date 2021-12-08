import mysql.connector
import os 

class Nemesis_Db:
  def __init__(self):
    self.connection = mysql.connector.connect(
      user=os.getenv("SQL_USER"),
      host=os.getenv("SQL_HOST"),
      password=os.getenv("SQL_PASSWORD"),
      database = "amxx_s06"
    )

    cursor = self.connection.cursor()
    cursor.execute("SHOW TABLES")
    tables = [a[0] for a in cursor]
    if "nemesis" not in tables: 
      cursor.execute("""CREATE TABLE nemesis (
                        date date, 
                        killer varchar(100),
                        victim varchar(100),
                        map varchar(64),
                        kills smallint(255),
                        primary key (date,killer,victim,map)
);""")
  def add(self, row):
    """sql_sel = "SELECT * FROM nemesis WHERE date = %s, killer=%s, victim=%s, map=%s"
    sql_val = (row['date'], row['killer'], row['victim'], row['map'])
    self.cursor.execute(sql_sel,sql_val)
    result = self.cursor.fetchone()
    if result:
      sql_upd = "UPDAhE nemesis SET kills = %s WHERE " """
    sql_upsert = "INSERT INTO nemesis (date,killer,victim,map,kills) VALUES (%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE kills = kills + 1"
    cursor = self.connection.cursor()
    cursor.execute(sql_upsert,row)
    self.connection.commit()
