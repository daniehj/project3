import telnetlib, time, re, sys
#from pylab import *

global planets
planets = {'Sun':'10','Mercury':'199','Venus':'299','Earth':'399','Mars':'499','Jupiter':'599','Saturn':'699','Uranus':'799','Neptun':'899','Pluto':'999'}

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


def get_planet_info(planetId):
    HOST = 'ssd.jpl.nasa.gov'
    PORT = '6775'
    TIMEOUT = 10.
    
    telnet = telnetlib.Telnet()
    telnet.open(HOST, PORT, TIMEOUT)
    telnet.set_debuglevel(0)
    print '\nConnection to ',HOST,':',PORT,' OK'
    print 'Starting download\n'
    time.sleep(3)
    telnet.write(planetId.encode("ascii")+b"\r\n")
    time.sleep(2)
    telnet.write(('e').encode("ascii")+b"\r\n")
    time.sleep(2)
    telnet.write(('v').encode("ascii")+b"\r\n")
    time.sleep(2)
    telnet.write(('500@0').encode("ascii")+b"\r\n")
    time.sleep(2)
    telnet.write((b"\r\n").encode("ascii")+b"\r\n")
    time.sleep(2)
    telnet.write(('eclip').encode("ascii")+b"\r\n")
    time.sleep(2)
    telnet.write(b"\r\n")
    time.sleep(2)
    telnet.write(b"\r\n")
    time.sleep(2)
    telnet.write(('1d').encode("ascii")+b"\r\n")
    time.sleep(2)
    telnet.write(('y').encode("ascii")+b"\r\n")
    time.sleep(3)
    temp = telnet.read_until('\r\n LT')
    telnet.close()
    
    vec = []
    mass_index = temp.find('Mass',0)
    mass =  temp[mass_index:mass_index+50]
    mass = mass.split('kg')
    E = mass[0].split('^')
    E = int(E[1])
    mass = mass[1]
    mass = mass.split('+-')
    mass = mass[0]
    mass = re.sub('[^0-9.]','',mass)
    mass = float(mass)*10**E
    print 'Data for {} downloaded'.format(arg)
    print 'Mass:',mass
    temp = temp.split('=')
    pos_vel = temp[-6:]
    for line in pos_vel:
        line = re.sub('[VXYZLT\r\n]', '', line)
        line = float(line)
        vec.append(line)
    
    
    print 'Pos-Vel\n',vec
    
    write_to_db(create_connection(db_name),planetId,arg,mass,vec)
    
    return planetId,arg,mass,vec

argnums = len(sys.argv)
for arg in sys.argv[1:]:

    get_planet_info(planets[arg])
    
