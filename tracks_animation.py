import numpy as np
import matplotlib.pyplot as plt
import psycopg2
import math
from matplotlib.animation import FuncAnimation
import datetime
import csv
from postgis import Polygon,MultiPolygon
from postgis.psycopg import register
import random
import matplotlib.animation as animation
import copy


def animate(i):
    # adicionar timestamp
    scat.set_offsets(offsets[i])
    ax.set_title(str(datetime.datetime.utcfromtimestamp(ts_i+i)) + " " + str(infetadosOffset[i]))
    c = ["green" if t == 0 else "red" for t in virusStateOffset[i]]
    s = contigioStateOffset[i]
    scat.set_facecolors(c)
    scat.set_sizes(s)

def contagio():
    for i in range(1, len(offsets)):
        for t in range(0,1659):
            x,y = offsets[i][t]
            #t not in infected
            if(x != -120000.0 and y != -310000.0 and t not in infetados):
                infBool = False
                for inf in infetados:
                    if(infBool):
                        #testar se isto só afeta o loop dos infetados
                        break
                    xi,yi = offsets[i][inf]
                    #calcular distancia
                    dist = math.hypot(x - xi, y - yi)
                    if(dist <= 10):
                        if(random.randint(1,10) == 1):
                            #foi infectado
                            infetados.append(t)
                            virusState[t] = 1
                            contigioState[inf] += 1
                            infBool = True
                            print("infected on " + str(i) + " by " + str(inf) + " num of inf: " + str(len(infetados)))
        virus_copy = copy.deepcopy(virusState)  
        contagio_copy = copy.deepcopy(contigioState)  
        virusStateOffset.append(virus_copy)
        contigioStateOffset.append(contagio_copy)
        infetadosOffset.append(len(infetados))

scale=1/3000000
conn = psycopg2.connect("dbname=postgres user=brunopinto")
register(conn)

xs_min, xs_max, ys_min, ys_max = -120000, 165000, -310000, 285000
width_in_inches = (xs_max-xs_min)/0.0254*1.1
height_in_inches = (ys_max-ys_min)/0.0254*1.1

ts_i = 1570665600

fig, ax = plt.subplots(figsize=(width_in_inches*scale, height_in_inches*scale))
ax.axis('off')
ax.set(xlim=(xs_min, xs_max), ylim=(ys_min, ys_max))

cursor_psql = conn.cursor()

sql = "select distrito,st_union(proj_boundary) from cont_aad_caop2018 group by distrito"

cursor_psql.execute(sql)
results = cursor_psql.fetchall()
xs , ys = [],[]
for row in results:
    geom = row[1]
    if type(geom) is MultiPolygon:
        for pol in geom:
            xys = pol[0].coords
            xs, ys = [],[]
            for (x,y) in xys:
                xs.append(x)
                ys.append(y)
            ax.plot(xs,ys,color='black',lw='0.2')
    if type(geom) is Polygon:
        xys = geom[0].coords
        xs, ys = [],[]
        for (x,y) in xys:
            xs.append(x)
            ys.append(y)
        ax.plot(xs,ys,color='black',lw='0.2')

offsets = []
with open('files/offsets3.csv', 'r') as csvFile:
    reader = csv.reader(csvFile)
    i = 0
    for row in reader:
        l = []
        for j in row:
            x,y = j.split()
            x = float(x)
            y= float(y)
            if(x == 0.0 and y == 0.0):
                x = -120000
                y = -310000
            l.append([x,y])
        offsets.append(l)

x,y = [],[]
for i in offsets[0]:
    x.append(i[0])
    y.append(i[1])

virusState = [0]*1660
virusStateOffset = []
contigioState = [1]*1660
contigioStateOffset = []
infetados = []
infetadosOffset = [0]



print("Inicio do contagio")
#intial contagio
for i in range(0,10):
    r = random.randint(0,1659)
    if(r not in infetados):
        infetados.append(r)
        virusState[r] = 1

virus_copy = copy.deepcopy(virusState)  
contagio_copy = copy.deepcopy(contigioState)  
virusStateOffset.append(virus_copy)
contigioStateOffset.append(contagio_copy)
infetadosOffset.append(len(infetados))

contagio()

c = ["green" if t == 0 else "red" for t in virusStateOffset[0]]

scat = ax.scatter(x,y, facecolor=c, s = contigioStateOffset[0])
anim = FuncAnimation(fig, animate, interval=10, frames=len(offsets)-1, repeat = False)

plt.draw()
plt.show()
#anim.save('line.gif', writer='imagemagick', fps=30)