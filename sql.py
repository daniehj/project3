import sqlite3
from sqlite3 import Error

db_name = './project3db.db'

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
        
        return conn
        
    except Error as e:
        print(e)

        
def write_to_db(conn,planetId,name,mass,vec):
    
    c = conn.cursor()    
    c.execute('''CREATE TABLE IF NOT EXISTS planets (
               planetId integer PRIMARY KEY,
               name text NOT NULL UNIQUE,
               mass text NOT NULL,
               x text NOT NULL,
               y text NOT NULL,
               z text NOT NULL,
               vx text NOT NULL,
               vy text NOT NULL,
               vz text NOT NULL
               );''')
    try:
         c.execute('''INSERT INTO planets (planetId,name,mass,x,y,z,vx,vy,vz)
                    VALUES ({},'{}','{}','{}','{}','{}','{}','{}','{}')'''.format(planetId,name,mass,vec[0],vec[1],vec[2],vec[3],vec[4],vec[5]))
    except Error as e:
         c.execute('''UPDATE planets
                   SET
                   x = '{}',
                   y = '{}',
                   z = '{}',
                   vx = '{}',
                   vy = '{}',
                   vz = '{}'
                   ;'''.format(vec[0],vec[1],vec[2],vec[3],vec[4],vec[5]))
    conn.commit()
    c.execute('''SELECT * FROM planets''')
    print c.fetchall()
    conn.close()
    
write_to_db(create_connection(db_name),planetId=11,name='venus',mass='10E24',vec=[1,1,1,0.1,0.1,0.1])