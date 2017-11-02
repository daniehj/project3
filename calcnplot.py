import sqlite3
from sqlite3 import Error
from pylab import *
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D

db_name = './project3db.db'
ONE_DAY = 24*3600

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    try:
        conn = sqlite3.connect(db_file)
        print 'Connection to DB OK, SQLite version:',sqlite3.version
        
        return conn
        
    except Error as e:
        print(e)

def get_planets_db(conn,planets):
    
    c = conn.cursor()
    
    for planet in planets:
        c.execute('''SELECT * FROM planets
                  WHERE planetId = {}'''.format(planet))
        arr = c.fetchall()
        name,mass,x,y,z,vx,vy,vz = arr[0][1:]
        solver(name,float(mass),float(x),float(y),float(z),float(vx),float(vy),float(vz))

        
def planetplot(x,y,z,color,tle,n):
    
    print 'Plotting...'
    
    figure(n)
    plot(x,y,color)
    title(tle)
    xlabel('x in m')
    ylabel('y in m')
    legend(['Sun','Earth'],)
    grid(True)
    filename = str(tle + '.png')
    
    savefig(filename)
    
    #Change to this for 3d plot
    '''
    fig = figure(1)
    ax = fig.gca(projection='3d')
    ax.plot(body.x_pos,body.y_pos,body.z_pos)
    filename = str(tle + '3d.png')
    savefig(filename)
    '''
def solver(name,mass,x0,y0,z0,vx0,vy0,vz0):

    if name == 'Sun':
        x0,y0,z0,vx0,vy0,vz0 = 0,0,0,0,0,0
        color = 'oy'
    
    else:
        color = ''
    
    #Init vars
    G = 6.673E-11
    M = 1.98855E+30
    t0 = 0.0
    
    AU = 149597871000   #m
    day = 24*60*60      #s

    n = int(10E3)
    dt = (372*24*60*60)/(n)
    
    
    
    #Making arrays
    x = zeros(n)
    y = zeros(n)
    z = zeros(n)
    
    vx = zeros(n)
    vy = zeros(n)
    vz = zeros(n)
    
    t = zeros(n)
    
    x[0] = x0*AU
    y[0] = y0*AU
    z[0] = z0*AU
    
    vx[0] = vx0*(AU/day)
    vy[0] = vy0*(AU/day)
    vz[0] = vz0*(AU/day)
    
    
    #Process for Euler's method
    for i in range(n-1):
        x[i+1] = x[i] + vx[i]*dt
        y[i+1] = y[i] + vy[i]*dt
        z[i+1] = z[i] + vz[i]*dt
        r = [x[i],y[i],z[i]]
        dr = sqrt((x[i]**2) + (y[i]**2) + (z[i]**2))
        a = -((G*M)*(r/dr**3))
        vx[i+1] = vx[i] + a[0]*dt
        vy[i+1] = vy[i] + a[1]*dt
        vz[i+1] = vz[i] + a[2]*dt
        t[i+1] = t[i] + dt
    
    title = 'Eulers method'
    planetplot(x,y,z,color,title,1)
    
    #Process for Verlet method
    if name == 'Sun':
        x.fill(0)
        y.fill(0)
        z.fill(0)
    else:
        for i in range(n-1):
            r = [x[i],y[i],z[i]]
            dr = sqrt((x[i]**2) + (y[i]**2) + (z[i]**2))
            a = -((G*M)*(r/dr**3))
            
            x[i+1] = x[i] + vx[i]*dt + (dt**2/2.)*a[0]
            y[i+1] = y[i] + vy[i]*dt + (dt**2/2.)*a[1]
            z[i+1] = z[i] + vz[i]*dt + (dt**2/2.)*a[2]
            r = [x[i],y[i],z[i]]
            dr = sqrt((x[i]**2) + (y[i]**2) + (z[i]**2))
            a_new = -((G*M)*(r/dr**3))
            vx[i+1] = vx[i] + (dt/2.)*(a_new[0] + a[0])
            vy[i+1] = vy[i] + (dt/2.)*(a_new[1] + a[1])
            vz[i+1] = vz[i] + (dt/2.)*(a_new[2] + a[2])
    
    title = 'Verlet method'
    
    planetplot(x,y,z,color,title,2)
    

get_planets_db(create_connection(db_name),planets=[10,399])

show()
    