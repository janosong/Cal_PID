import serial
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import TextBox
import time

_max_X = 100
_max_Y = 80
ser = serial.Serial('COM2', 115200, timeout=0)


dis = np.zeros(_max_X + 1)
dis2 = dis
fig, ax = plt.subplots()



line, = ax.plot(dis, '.-', markersize=2, markerfacecolor='k', markeredgecolor='k' )
ax.set_ylim(10, _max_Y)
ax.set_xlim(1, _max_X)
plt.grid(True)
ax.set_ylabel("Temperature C")
ax.set_xlabel("time") 
#颜色设置
plt.setp(line, 'color', 'g', 'linewidth', 1.0)



def make_xtick(n):
    a = [i for i in range(0,int(n/10))]
    xtik=[]
    for i in a:
        xtik.append(i)
        for j in range(1 ,10):
            if 5==j:
                xtik.append(i+0.5)
            else:
                xtik.append('')
    xtik.append(int(n/10))
    #print(xtik)
    return xtik

def make_ytick(n):
    a = [i for i in range(0,int(n/10))]
    xtik=[]
    for i in a:
        xtik.append(i*10)
        for j in range(1 ,10):
            if 5==j:
                xtik.append(i*10+5)
            else:
                xtik.append('')
    xtik.append(int(n))
    #print(xtik)
    return xtik
    
plt.xticks(np.linspace(0,_max_X, _max_X+1), make_xtick(_max_X))
plt.yticks(np.linspace(0,_max_Y+10, _max_Y+1+10), make_ytick(_max_Y+10))

def update(frame):
    global dis
    global dis2
    global line   
    
    #读入模拟
    a = ser.read(5)
    #绘图数据生成  
    if b''!=a:
        dis[0:-1] = dis2[1:] 
        #dis[-1] = 3* np.sin(float(a)) + 30
        dis[-1] = float(a)
        dis2 = dis
    #绘图 
        line.set_ydata(dis)    
    #颜色设置
    #    plt.setp(line, 'color', 'r', 'linewidth', 2.0)
    #else:
    #    plt.setp(line, 'color', 'b', 'linewidth', 2.0)
    return line,
tstart = time.time()   
def init():
    global tstart
    print ('FPS:' , 100/(time.time()-tstart))
    tstart = time.time()
    return line,
tstart = time.time()
ani = animation.FuncAnimation(fig, update,frames=100, init_func=init, interval=20, blit=True)
#PID 参数设置框
axprev = plt.axes([0.8,0.9, 0.1,0.05])
D_TB =TextBox(axprev,'D:', initial='1')
axprev = plt.axes([0.65,0.9, 0.1,0.05])
I_TB =TextBox(axprev,'I:', initial='2')
axprev = plt.axes([0.5,0.9, 0.1,0.05])
P_TB =TextBox(axprev,'P:', initial='3')

def p_submit(text):
    data = eval(text)
    ser.write(text.encode())
def i_submit(text):
    data = eval(text)
    ser.write(text.encode())
def d_submit(text):
    data = eval(text)
    ser.write(text.encode())

P_TB.on_submit(p_submit)
I_TB.on_submit(i_submit)
D_TB.on_submit(d_submit)
plt.show()
ser.close()
print ('FPS:' , 100/(time.time()-tstart))