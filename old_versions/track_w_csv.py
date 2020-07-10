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

def animate(i):
    # adicionar timestamp
    scat.set_offsets(offsets[i])
    ax.set_title(str(datetime.datetime.utcfromtimestamp(ts_i+i)) + " " + str(infetadosOffset[i]))
    c = ["green" if t == 0 else "red" for t in virusStateOffset[i]]
    s = contigioStateOffset[i]
    scat.set_facecolors(c)
    scat.set_sizes(s)


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

virusStateOffset = []
contigioStateOffset = []
infetadosOffset = []

print("read offset")
# read virus state
with open('files/virusState.csv', 'r') as csvFile:
    reader = csv.reader(csvFile)
    i = 0
    for row in reader:
        l = []
        for j in row:
            x = j.split()
            l.append(x)
        virusStateOffset.append(l)

print("read offset virus")
# read size state
with open('files/sizeState.csv', 'r') as csvFile:
    reader = csv.reader(csvFile)
    i = 0
    for row in reader:
        l = []
        for j in row:
            x = j.split()
            l.append(x)
        contigioStateOffset.append(l)

print("read offset size")
# read len state
with open('files/lenState.csv', 'r') as csvFile:
    reader = csv.reader(csvFile)
    i = 0
    for row in reader:
        l = []
        for j in row:
            x = j.split()
            l.append(x)
        infetadosOffset.append(l)

print("read offset len")


c = ["green" if t == 0 else "red" for t in virusStateOffset[0]]

scat = ax.scatter(x,y, facecolor=c, s = contigioStateOffset[0])
anim = FuncAnimation(fig, animate, interval=10, frames=len(offsets)-1, repeat = False)

plt.draw()
plt.show()
#anim.save('line.gif', writer='imagemagick', fps=30)