import psycopg2
import random
import numpy as np

def firstCases():
    conn = psycopg2.connect("dbname=postgres user=brunopinto")
    cursor_psql = conn.cursor()

    #primeiros 10 no porto
    sql_porto= "select distinct(t.taxi), t.ts from tracks as t, cont_aad_caop2018 as f where f.concelho = 'PORTO' and st_contains(f.proj_boundary,ST_StartPoint(t.proj_track)) order by t.ts  limit 10" 

    cursor_psql.execute(sql_porto)
    results = cursor_psql.fetchall()
    porto = []
    for row in results:
        porto.append(row[0])

    #primeiros 10 em lisboa
    sql_lisboa =  "select distinct(t.taxi), t.ts from tracks as t, cont_aad_caop2018 as f where f.concelho = 'LISBOA' and st_contains(f.proj_boundary,ST_StartPoint(t.proj_track)) order by t.ts limit 10"

    cursor_psql.execute(sql_lisboa)
    results = cursor_psql.fetchall()
    row = results[0]
    lisboa = []
    for row in results:
        lisboa.append(row[0])


    rp= random.randint(0,9)
    rl= random.randint(0,9)

    sql = """select distinct taxi from tracks order by 1"""
    cursor_psql.execute(sql)
    results = cursor_psql.fetchall()

    taxis_x ={}
    taxis_y ={}

    array_size = int(24*60*60/10)

    for row in results:    
        taxis_x[int(row[0])] = np.zeros(array_size)
        taxis_y[int(row[0])] = np.zeros(array_size)

    i=0
    infIndex = []
    for j in taxis_x:
        # print(type(j))
        if(str(j) == porto[rp] or str(j) == lisboa[rl]):
            infIndex.append(i)
        i += 1


    conn.close()
    return infIndex