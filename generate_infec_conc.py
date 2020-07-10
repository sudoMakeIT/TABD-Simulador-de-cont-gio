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

def generate_infec_conc(user):

    conn = psycopg2.connect("dbname=postgres user=" + user)
    register(conn)
    cursor_psql = conn.cursor()

    taxis_inf = []
    with open('files/taxis_inf.csv', 'r') as csvFile:
        reader = csv.reader(csvFile)
        i = 0
        for row in reader:
            taxis_inf.append(row)


    ts_i = 1570665600
    ts_f = ts_f = ts_i + 10*8640
    # ts_f = ts_f = ts_i + 10*100
    infected = []

    for i in range(ts_i,ts_f,10):
        temp = []
        taxis_ids = str(taxis_inf[int((i-ts_i)/10)]).replace('[', '(').replace(']', ')')
        sql_porto = "select  count(distinct(t.taxi)) from tracks as t, cont_aad_caop2018 as f where t.taxi in " + taxis_ids + " and t.ts <= " + str(i)  + " and f.distrito = 'PORTO' and st_contains(f.proj_boundary,ST_StartPoint(t.proj_track))"
        sql_lisboa = "select count(distinct(t.taxi)) from tracks as t, cont_aad_caop2018 as f where t.taxi in " + taxis_ids + " and t.ts <= " + str(i)  + " and f.distrito = 'LISBOA' and st_contains(f.proj_boundary,ST_StartPoint(t.proj_track))"
        # print(sql_porto)
        cursor_psql.execute(sql_porto)
        results = cursor_psql.fetchall()
        cursor_psql.execute(sql_lisboa)
        results_lisboa = cursor_psql.fetchall()
        print(int((i-ts_i)/10))
        # print(results)
        infected.append([results[0][0], results_lisboa[0][0]])
        
    
    print("Writting infected PORTO,LISBOA")
    with open("files/distrito_inf.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(infected)

    conn.close()

if __name__ == "__main__":
    generate_infec_conc("brunopinto")