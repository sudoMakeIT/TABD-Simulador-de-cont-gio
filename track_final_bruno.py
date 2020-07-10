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
import re
import sys


def show_plot(user, mode):

    def animate(i):
        # adicionar timestamp
        fig.suptitle(str(datetime.datetime.utcfromtimestamp(ts_i+i*10)))
        line.set_data(x1[:i], y1[:i])
        line.axes.axis([0, x1[i]*1.2, 0, y1[i]*1.5])
        my = max((porto[i]*1.5),(lisboa[i]*1.5))
        lineP.set_data(x2[:i], porto[:i])
        lineP.axes.axis([0, x2[i]*1.2, 0, my])
        lineL.set_data(x2[:i], lisboa[:i])
        lineL.axes.axis([0, x2[i]*1.2, 0, my])
        if(mode != 2):
            scat.set_offsets(offsets[i])
            s = contigioStateOffset.loc[i].to_list()
            scat.set_facecolors(c[i])
            scat.set_sizes(s)
        if(mode != 1):
            for (ax1,ay) in zip(xxx[i], yyy[i]):
                ax[0].plot(ax1,ay,linewidth=0.2,color='black')

    debug = True
    csv.field_size_limit(sys.maxsize)
    frames = 8640

    if debug:
        print("Setup")

    scale=1/3000000
    conn = psycopg2.connect("dbname=postgres user=" + user)
    register(conn)

    xs_min, xs_max, ys_min, ys_max = -120000, 165000, -310000, 285000
    width_in_inches = (xs_max-xs_min)/0.0254*1.1
    height_in_inches = (ys_max-ys_min)/0.0254*1.1

    ts_i = 1570665600

    fig = plt.figure(figsize=(width_in_inches*scale*2.2, height_in_inches*scale))
    gs1 = gridspec.GridSpec(2,2)

    ax = []
    ax.append(fig.add_subplot(gs1[0:2, 0]))
    ax.append(fig.add_subplot(gs1[0, 1]))
    ax.append(fig.add_subplot(gs1[1, 1]))
    ax[0].axis('off')

    cursor_psql = conn.cursor()

    if debug:
        print("Query para mapa")


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

    if debug:
        print("Offsets")

    if(mode != 2):
        offsets = []
        offsetspd = pd.read_csv('files/offsets3.csv', header=None, low_memory=True)
        for i in range(0,8640):
            l = []
            for j in offsetspd.loc[i]:
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

    if debug:
        print("Contágio")


    virusStateOffset = pd.read_csv('files/virusState.csv', header=None, low_memory=True)
    contigioStateOffset = pd.read_csv('files/sizeState.csv', header=None,low_memory=True)
    infetadosOffset = pd.read_csv('files/lenState.csv', header=None, low_memory=True)
    infetadosOffset = pd.read_csv('files/lenState.csv', header=None, low_memory=True)
    dsit = pd.read_csv('files/distrito_inf.csv', header=None, low_memory=True)

    #gráfico de infetados
    x1 = np.linspace(0, 86400, 8641)
    y1 = infetadosOffset.loc[0].to_list()
    porto = dsit[0].to_list()
    lisboa = dsit[1].to_list()

    #grafico da evo
    ax[1].title.set_text("Total de Infetados")
    line, = ax[1].plot(x1, y1, color='k')
    ax[1].set_xlabel('tempo (s)')
    ax[1].set_ylabel('Infetados')

    #grafico por dist
    x2 = np.linspace(0, 86400, 8640)
    ax[2].title.set_text("Infetados no Porto e Lisboa")
    lineP, = ax[2].plot(x2, porto, color='blue')
    lineP.set_label('Porto')
    lineL, = ax[2].plot(x2, lisboa, color='orange')
    lineL.set_label('Lisboa')
    ax[2].set_xlabel('tempo (s)')
    ax[2].set_ylabel('Infetados')
    ax[2].legend(loc='best')

    if debug:
        print("tracks")

    #tracks
    if(mode != 1):
        tracks = []
        with open('files/tracks_inf.csv', 'r') as csvFile:
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
            for t in track:
                temp_x = []
                temp_y = []
                for match in repatt.findall(t):
                    # print(match[0])
                    # print(match[1])
                    temp_x.append(float(match[0]))
                    temp_y.append(float(match[1]))
                temp_xxx.append(temp_x)
                temp_yyy.append(temp_y)
            xxx.append(temp_xxx)
            yyy.append(temp_yyy)


    #cores
    if debug:
        print("Cores")

    c = []
    for i in range(0,8640):
        c.append(["green" if t == 0 else "red" for t in virusStateOffset.loc[i].to_list()])

    if(mode != 2):
        scat = ax[0].scatter(x,y, facecolor=c[0], s = contigioStateOffset.loc[i].to_list())
    # scat = ax[0].scatter(x,y, facecolor=c[0], s = 3)
    if(mode != 1):
        ax[0].plot(xxx[0],yyy[0],linewidth=0.2,color='black') 

    anim = FuncAnimation(fig, animate, interval=10, frames=frames, repeat = False)

    plt.draw()
    plt.show()

if __name__ == "__main__":
    show_plot("brunopinto", 1)
    # show_plot("brunopinto", 2)
    # show_plot("brunopinto", 3)

