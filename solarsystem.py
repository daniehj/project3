from pylab import *
import time
import sys
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D


G = 6.67428e-11
AU = 149597871000   #m
day = 24*60*60
SUN_MASS = 1.98892 * 10**30
ONE_DAY = 24*3600
c = 299792458

class planets:
    
    def __init__(self,name,mass,x0,y0,z0,vx0,vy0,vz0):
        
        self.name = name
        self.mass = mass
        self.x0 = x0
        self.y0 = y0
        self.z0 = z0
        self.vx = vx0
        self.vy = vy0
        self.vz = vz0
        self.x_pos = []
        self.y_pos = []
        self.z_pos = []
        self.x_pos.append(x0)
        self.y_pos.append(y0)
        self.z_pos.append(z0)
        self.force = 0.
        self.pos = array([x0,y0,z0])
        self.orb_delr = []

def forcecalc(per=False):

    for body in bodies:
        body.force = 0. 

    for i in range(len(bodies)):
        body1 = bodies[i]
        for j in range(i+1,len(bodies)):
            body2 = bodies[j]


            delr = body2.pos - body1.pos

            dr = sqrt(delr[0]**2 + delr[1]**2 + delr[2]**2)

            body1.force += ((G*body1.mass*body2.mass)*(delr/dr**3))
            body2.force -= ((G*body1.mass*body2.mass)*(delr/dr**3))
            
            vel = [body2.vx,body2.vy,body2.vz]
            l = cross(delr,vel)
            
            
        if per:
            
            body1.force = body1.force*(1 + ((3*(l[0]**2 + l[1]**2 + l[2]**2))/((delr[0]**2 + delr[1]**2 + delr[2]**2)*c**2)))
            body2.force = body2.force*(1 + ((3*(l[0]**2 + l[1]**2 + l[2]**2))/((delr[0]**2 + delr[1]**2 + delr[2]**2)*c**2)))
            
            
                
def euler(dt,per=False):
    if per:
        forcecalc(True)
    else:
        forcecalc()
    for body in bodies:
        a = body.force/body.mass
        body.pos[0] = body.pos[0] + body.vx*dt
        body.vx = body.vx + a[0]*dt
        body.x_pos.append(body.pos[0])
        body.pos[1] = body.pos[1] + body.vy*dt
        body.vy = body.vy + a[1]*dt
        body.y_pos.append(body.pos[1])
        body.pos[2] = body.pos[2] + body.vz*dt
        body.vz = body.vz + a[2]*dt
        body.z_pos.append(body.pos[2])

    for body in bodies:
        body.force = 0.
            
def verlet(dt,per=False):
    
    if per:
        forcecalc(True)
    else:
        forcecalc()
    for body in bodies:
        a = body.force/body.mass
        
        body.pos[0] = body.pos[0] + body.vx*dt + a[0]*(dt**2/2.)
        body.x_pos.append(body.pos[0])
        
        body.pos[1] = body.pos[1] + body.vy*dt + a[1]*(dt**2/2.)
        body.y_pos.append(body.pos[1])
        
        body.pos[2] = body.pos[2] + body.vz*dt + a[2]*(dt**2/2.)
        body.z_pos.append(body.pos[2])
        #body.force = 0
        
        if per:
            forcecalc(True)
        else:
            forcecalc()
        
        #print body.force,'b'
        a_new = body.force/body.mass
        body.vx = body.vx + (a_new[0] + a[0])*(dt/2.)
        body.vy = body.vy + (a_new[1] + a[1])*(dt/2.)
        body.vz = body.vz + (a_new[2] + a[2])*(dt/2.)
    
    #for body in bodies:
        #body.force = 0.   
        
        
def draw_plot(ode,year,dt,frac,names,tle):
    #print names
    t0 = time.clock()
    for i in range(int(year*frac*365)):
        if ode == 'euler':
            euler(dt)
        elif ode == 'verlet':
            verlet(dt)
        elif ode == '-verlet':
            verlet(dt,True)
            
    t1 = time.clock()
    tim = t1 - t0
    tle = '{}-{}'.format(tle,ode)
    print 'Time solving: {:.3f}s'.format(tim)
    figure(1)
    for body in bodies:
        
        plot(body.x_pos,body.y_pos)
        title(tle)
        legend(name_list,)
        xlabel('x in m')
        ylabel('y in m')
        grid(True)
        filename = str(tle + '.png')
        savefig(filename)
        
        
        #For 3d plot use this lines
        '''
        fig = figure(1)
        ax = fig.gca(projection='3d')
        ax.plot(body.x_pos,body.y_pos,body.z_pos)
        filname = str(tle + '3d.png')
        savefig(filename)
        '''                
    
        if ode == '-verlet' and body.name == 'Mercury':
            figure(2)
            x = perihelionPrecission()
            plot(x)
    show()
    
    

def perihelionPrecission():
    orb_delr_x = []
    orb_delr_y = []
    orb_delr_z = []
    for i in range(len(bodies)):
        body1 = bodies[i]
        for j in range(i+1,len(bodies)):
            body2 = bodies[j]


            orb_delr_x.append(body2.x_pos - body1.x_pos)
            orb_delr_y.append(body2.y_pos - body1.y_pos)
            orb_delr_z.append(body2.z_pos - body1.z_pos)
    orb_delr = norm(orb_delr_x,orb_delr_y,orb_delr_z)
    peri = []
    orb_num = []
    j = 0
    jc = 0
    for i in range(len(orb_delr)):
        orbit_time = 88.
        if i % orbit_time == 0:
            j += 1
            orb_num.append(j)
            peri.append(min(norm(orb_delr[jc:j])))
            jc = j
    print 'number of orbits:',int(ceil((300*365.)/88.))
    print j
    return peri


if sys.argv[1] == '1':
    
    bodies = [planets('Sun',1.988544e+30,0.,0.,0.,0.,0.,0.),
             planets('Earth',5.97219e+24,0.85899871088*AU,0.511068060555*AU,-0.000156862341583*AU,-0.00903113966644*(AU/day),0.0147625346234*(AU/day),-1.94313019813e-07*(AU/day))]
    
    name_list = []
    for names in bodies:
        name_list.append(names.name)
    ode = sys.argv[2]
    year = 1
    frac = 1000.
    dt = ONE_DAY/frac
    tle = '{}-{}-plot'.format(name_list[0],name_list[1])
    print 'Solvinng for planets:{} with ODE: {}'.format(str(name_list),ode)
    print '\ndt=1day/{}'.format(frac)
    
    draw_plot(ode,year,dt,frac,name_list,tle)
    
elif sys.argv[1] == '2':
    jmb = float(sys.argv[3])
    bodies = [planets('Sun',1.988544e+30,0.00218700306521*AU,0.00576816655911*AU,-0.000129414773435*AU,-5.28031574593e-06*(AU/day),5.46082726877e-06*(AU/day),1.24459055189e-07*(AU/day)),
              planets('Earth',5.97219e+24,0.85899871088*AU,0.511068060555*AU,-0.000156862341583*AU,-0.00903113966644*(AU/day),0.0147625346234*(AU/day),-1.94313019813e-07*(AU/day)),
              planets('Jupiter',1.89813e+27*jmb,-4.55674534816*AU,-2.96300845734*AU,0.114210860309*AU,0.00402529012703*(AU/day),-0.00596816594846*(AU/day),-6.52656607254e-05*(AU/day))]
    
    name_list = []
    for names in bodies:
        name_list.append(names.name)
    ode = sys.argv[2]
    year = 12
    frac = 30.
    dt = ONE_DAY/frac
    tle = '{}-{}-{}-plot Jupitermassx{}'.format(name_list[0],name_list[1],name_list[2],int(jmb))
    print 'Solvinng for planets:{} with ODE: {}'.format(name_list[0:],ode)
    print '\ndt=1day/{}'.format(frac)
    
    draw_plot(ode,year,dt,frac,name_list,tle)
    
elif sys.argv[1] == '3':
    bodies = [planets('Sun',1.988544e+30,0.00218700306521*AU,0.00576816655911*AU,-0.000129414773435*AU,-5.28031574593e-06*(AU/day),5.46082726877e-06*(AU/day),1.24459055189e-07*(AU/day)),
              planets('Mercury',3.302e+23,-0.213937059057*AU,-0.402881466933*AU,-0.0136941992387*AU,0.0191960511041*(AU/day),-0.0117893972477*(AU/day),-0.00272519497198*(AU/day)),
              planets('Venus',4.8685e+24,-0.691541141102*AU,0.190770765634*AU,0.042440805912*AU,-0.00531814981792*(AU/day),-0.019629462525*(AU/day),3.73756409999e-05*(AU/day)),
              planets('Earth',5.97219e+24,0.85899871088*AU,0.511068060555*AU,-0.000156862341583*AU,-0.00903113966644*(AU/day),0.0147625346234*(AU/day),-1.94313019813e-07*(AU/day)),
              planets('Mars',6.4185e+23,-1.59048840324*AU,0.487978869337*AU,0.049062647997*AU,-0.00353637999869*(AU/day),-0.0121922534029*(AU/day),-0.00016882510410*(AU/day)),
              planets('Jupiter',1.89813e+27,-4.55674534816*AU,-2.96300845734*AU,0.114210860309*AU,0.00402529012703*(AU/day),-0.00596816594846*(AU/day),-6.52656607254e-05*(AU/day)),
              planets('Saturn',5.68319e+26,-0.315846708532*AU,-10.0506502803*AU,0.187322229868*AU,0.00527027697425*(AU/day),-0.00019273383115*(AU/day),-0.00020666333310*(AU/day)),
              planets('Uranus',8.68103e+25,17.8472461699*AU,8.83322534256*AU,-0.198407207614*AU,-0.00177348124804*(AU/day),0.0033416412139*(AU/day),3.53285945946e-05*(AU/day)),
              planets('Neptun',1.0241e+26,28.6201604663*AU,-8.80020967934*AU,-0.478357279456*AU,0.000901431510895*(AU/day),0.00301873686261*(AU/day),-8.31111408346e-05*(AU/day)),
              planets('Pluto',1.307e+22,10.5683511697*AU,-31.7102327441*AU,0.33618653909*AU,0.00303648707396*(AU/day),0.000333847720309*(AU/day),-0.00090584102741*(AU/day))]
    
    name_list = []
    for names in bodies:
        name_list.append(names.name)
    ode = sys.argv[2]
    year = 250.
    frac = 1./8
    dt = ONE_DAY/frac
    tle = 'full-solarsystem'
    print 'Solvinng for planets: {} with ODE: {}'.format(tle,ode)
    print '\ndt=1day/{}'.format(frac)


    draw_plot(ode,year,dt,frac,name_list,tle)
    
elif sys.argv[1] == '4':
    bodies = [planets('Sun',1.988544e+30,0.00218700306521*AU,0.00576816655911*AU,-0.000129414773435*AU,-5.28031574593e-06*(AU/day),5.46082726877e-06*(AU/day),1.24459055189e-07*(AU/day)),
              planets('Mercury',3.302e+23,-0.213937059057*AU,-0.402881466933*AU,-0.0136941992387*AU,0.0191960511041*(AU/day),-0.0117893972477*(AU/day),-0.00272519497198*(AU/day))]
    name_list = []
    for names in bodies:
        name_list.append(names.name)
    year = 300
    frac = 1.
    dt = ONE_DAY/frac
    ode = '-verlet'
    tle = 'perihelion-precission'
    print 'Solvinng for planets:{} with ODE: {}{}'.format(name_list[0:],tle,ode)
    print '\ndt=1day/{}'.format(frac)

    draw_plot(ode,year,dt,frac,name_list,tle)

