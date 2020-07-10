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
import re
import sys


csv.field_size_limit(sys.maxsize)

def animate(i):
    # adicionar timestamp
    ax.set_title(str(datetime.datetime.utcfromtimestamp(ts_i+i*10)))
    for (ax1,ay) in zip(xxx[i], yyy[i]):
        ax.plot(ax1,ay,linewidth=0.2,color='red')    

scale=1/3000000
conn = psycopg2.connect("dbname=postgres user=brunopinto")
register(conn)

xs_min, xs_max, ys_min, ys_max = -120000, 165000, -310000, 285000
width_in_inches = (xs_max-xs_min)/0.0254*1.1
height_in_inches = (ys_max-ys_min)/0.0254*1.1

ts_i = 1570665600

fig, ax = plt.subplots(figsize=(width_in_inches*scale, height_in_inches*scale))
# ax.axis('off')
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

tracks = []
with open('files/car_teste.csv', 'r') as csvFile:
    reader = csv.reader(csvFile)
    for row in reader:
        temp = []
        for l in row:
            temp.append(l)
        tracks.append(temp)


xxx = []
yyy = []

patt = '(\-?\d+\.\d+),\ (\-?\d+\.\d+)'
repatt = re.compile(patt)

for track in tracks:
    temp_xxx = []
    temp_yyy = []
    for x in track:
        temp_x = []
        temp_y = []
        for match in repatt.findall(x):
            # print(match[0])
            # print(match[1])
            temp_x.append(float(match[0]))
            temp_y.append(float(match[1]))
        temp_xxx.append(temp_x)
        temp_yyy.append(temp_y)
    xxx.append(temp_xxx)
    yyy.append(temp_yyy)
print(len(xxx))


# for x in offsets[0]:
#     xxx = []
#     yyy = []
#     for match in repatt.findall(x):
#         # print(match[0])
#         # print(match[1])
#         xxx.append(float(match[0]))
#         yyy.append(float(match[1]))
#     # print(len(xxx))
#     ax.plot(xxx,yyy,linewidth=1,color='red')    

# len(xxx)
# print(len(offsets))


ax.plot(xxx[0],yyy[0],linewidth=0.2,color='red')    
anim = FuncAnimation(fig, animate, interval=10, frames=len(tracks), repeat = False)

plt.show()
#anim.save('line.gif', writer='imagemagick', fps=30)