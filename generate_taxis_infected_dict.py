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



conn = psycopg2.connect("dbname=postgres user=brunopinto")
register(conn)
cursor_psql = conn.cursor()

sql = """select distinct taxi from tracks order by 1"""
cursor_psql.execute(sql)
results = cursor_psql.fetchall()

taxis_dict = {}
i = 0
for taxi in results:
    taxis_dict[i] = taxi[0]
    i+=1

print(taxis_dict[16])

infected_ids = []
virusStateOffset = pd.read_csv('files/virusState.csv', header=None, low_memory=True)
# print(virusStateOffset.loc[0].to_list())

for i in range(0,8640):
    inf = virusStateOffset.loc[i].to_list()
    index = 0
    temp = []
    for x in inf:
        if x == 1:
            # print(index)
            temp.append(taxis_dict[index])
        index += 1
    infected_ids.append(temp)

print("Writting infected ids")
with open("files/taxis_inf.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(infected_ids)

conn.close()