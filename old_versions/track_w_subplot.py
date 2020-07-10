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
import pandas as pd
import matplotlib.gridspec as gridspec

def animate(i):
    # adicionar timestamp
    scat.set_offsets(offsets[i])
    fig.suptitle(str(datetime.datetime.utcfromtimestamp(ts_i+i*10)))
    s = contigioStateOffset.loc[i].to_list()
    c = ["green" if t == 0 else "red" for t in virusStateOffset.loc[i].to_list()]
    scat.set_facecolors(c)
    scat.set_sizes(s)
    line.set_data(x1[:i], y1[:i])
    line.axes.axis([0, x1[i]*1.2, 0, y1[i]*1.5])


scale=1/3000000
conn = psycopg2.connect("dbname=postgres user=brunopinto")
register(conn)

xs_min, xs_max, ys_min, ys_max = -120000, 165000, -310000, 285000
width_in_inches = (xs_max-xs_min)/0.0254*1.1
height_in_inches = (ys_max-ys_min)/0.0254*1.1

ts_i = 1570665600

# fig, ax = plt.subplots(figsize=(width_in_inches*scale, height_in_inches*scale))
# ax.axis('off')
# ax.set(xlim=(xs_min, xs_max), ylim=(ys_min, ys_max))
# fig, ax = plt.subplots(1,2, gridspec_kw={'width_ratios': [2, 1]})
# 


fig = plt.figure(figsize=(width_in_inches*scale*2, height_in_inches*scale))
gs1 = gridspec.GridSpec(3,2)

ax = []
ax.append(fig.add_subplot(gs1[0:3, 0]))
ax.append(fig.add_subplot(gs1[0, 1]))
ax[0].axis('off')

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
            ax[0].plot(xs,ys,color='black',lw='0.2')
    if type(geom) is Polygon:
        xys = geom[0].coords
        xs, ys = [],[]
        for (x,y) in xys:
            xs.append(x)
            ys.append(y)
        ax[0].plot(xs,ys,color='black',lw='0.2')

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

    
virusStateOffset = pd.read_csv('files/virusState.csv', header=None, low_memory=True)
contigioStateOffset = pd.read_csv('files/sizeState.csv', header=None,low_memory=True)
infetadosOffset = pd.read_csv('files/lenState.csv', header=None, low_memory=True)


#gráfico de infetados
x1 = np.linspace(0, 86400, 8641)
y1 = infetadosOffset.loc[0].to_list()

line, = ax[1].plot(x1, y1, color='k')
ax[1].set_xlabel('time (s)')
ax[1].set_ylabel('Infetados')



c = ["green" if t == 0 else "red" for t in virusStateOffset.loc[0].to_list()]

scat = ax[0].scatter(x,y, facecolor=c, s = virusStateOffset.loc[0].to_list())
anim = FuncAnimation(fig, animate, interval=10, frames=len(offsets), repeat = False)

plt.draw()
plt.show()