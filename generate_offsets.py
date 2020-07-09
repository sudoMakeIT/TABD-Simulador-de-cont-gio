import numpy as np
import matplotlib.pyplot as plt
import psycopg2
import math
from matplotlib.animation import FuncAnimation
import datetime
from postgis import Polygon,MultiPolygon
from postgis.psycopg import register
import csv


def generate_offsets(user):
    #define the step in seconds of the animation
    step = 10
    debug = True
    print("Generating offsets")

    conn = psycopg2.connect("dbname=postgres user=" + user)
    register(conn)
    cursor_psql = conn.cursor()

    sql = """select distinct taxi from tracks order by 1"""
    cursor_psql.execute(sql)
    results = cursor_psql.fetchall()

    taxis_x ={}
    taxis_y ={}

    ts_i = 1570665600
    ts_f = ts_i + 10*8630

    array_size = int(24*60*60/step)

    for row in results:
        taxis_x[int(row[0])] = np.zeros(array_size)
        taxis_y[int(row[0])] = np.zeros(array_size)

    if debug:
        print("query")
    for i in range(ts_i,ts_f,10):
        if(debug):
            print((ts_i-i)/10)
        sql = "select taxi,st_pointn(proj_track," + str(i) + "-ts) from tracks where ts<" + str(i) + " and ts+st_numpoints(proj_track)>" + str(i)
        cursor_psql.execute(sql)
        results = cursor_psql.fetchall()
        for row in results:
            x,y = row[1].coords
            taxis_x[int(row[0])][int((i-ts_i)/10)] = x
            taxis_y[int(row[0])][int((i-ts_i)/10)] = y

    offsets = []

    for i in range(array_size):
        l = []
        for j in taxis_x:
            l.append([taxis_x[j][i],taxis_y[j][i]])
        offsets.append(l)

    print("Writting offsets")
    with open("files/offsets3.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(offsets)
    conn.close()