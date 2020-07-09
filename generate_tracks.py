import numpy as np
import matplotlib.pyplot as plt
import psycopg2
import math
from matplotlib.animation import FuncAnimation
import datetime
from postgis import Polygon,MultiPolygon,LineString
from postgis.psycopg import register
import csv
import pandas as pd 

def generate_tracks(user):
    conn = psycopg2.connect("dbname=postgres user=" + user)
    register(conn)
    cursor_psql = conn.cursor()

    taxis_inf = []
    with open('files/taxis_inf.csv', 'r') as csvFile:
        reader = csv.reader(csvFile)
        i = 0
        for row in reader:
            taxis_inf.append(row)


    offset = []
    ts_i = 1570665600
    ts_f = ts_f = ts_i + 10*8640

    for i in range(ts_i,ts_f,10):
        temp = []
        taxis_ids = str(taxis_inf[int((i-ts_i)/10)]).replace('[', '(').replace(']', ')')
        sql = "select proj_track from tracks where taxi in " + taxis_ids + " and ts <= " + str(i)  + " and ts > " + str(i-10)
        # print(sql)
        cursor_psql.execute(sql)
        results = cursor_psql.fetchall()
        print(int((i-ts_i)/10))
        # print(len(results))
        for row in results:
            # print(row)
            temp_row = []
            if type(row[0]) is LineString:
                xy = row[0].coords
                first = 1
                for (x,y) in xy:
                    if first == 1:
                        temp_row.append([x,y])
                        previousx=x
                        previousy=y
                        first = 0
                    elif math.sqrt(abs(x-previousx)**2+abs(y-previousy)**2)<50:
                        temp_row.append([x,y])
                        previousx=x
                        previousy=y
            temp.append(temp_row)
        offset.append(temp)



    print("Writting virus state")
    with open("files/tracks_inf.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(offset)

    conn.close()

if __name__ == "__main__":
    generate_tracks("brunopinto")