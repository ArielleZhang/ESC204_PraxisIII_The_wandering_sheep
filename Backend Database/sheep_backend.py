import sqlite3
from urllib.request import BaseHandler

conn = sqlite3.connect("sheep.db")

c = conn.cursor()

c.execute("""CREATE TABLE sheep (
    update_time text, 
    leader_id integer, 
    location real,
    cluser_id integer,
    report_missing integer,
    missing id integer,
    missing_location real
    ) """
) 


#commit 
conn.commit()

#close
conn.close()
