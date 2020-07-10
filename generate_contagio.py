import numpy as np
import math
from matplotlib.animation import FuncAnimation
import random
import csv
import copy
#import files
import generate_first_cases as fc
import generate_taxis_infected_dict as td
import generate_tracks as gt
import generate_infec_conc as distinf

def generate_contagio(user):
    print("Initializing ...")

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
    contigioState = [3]*1660
    contigioStateOffset = []
    infetados = []
    infetadosOffset = [0]


    print("Contagion has begun")
    #intial contagio
    index = fc.firstCases(user)
    print(index[0])
    print(index[1])
    virusState[index[0]] = 1
    virusState[index[1]] = 1
    infetados.append(index[0])
    infetados.append(index[1])

    virus_copy = copy.deepcopy(virusState)  
    contagio_copy = copy.deepcopy(contigioState)  
    virusStateOffset.append(virus_copy)
    contigioStateOffset.append(contagio_copy)
    infetadosOffset.append(len(infetados))

    #contagio
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
                    if(dist <= 50):
                        if(random.randint(1,10) == 1):
                            #foi infectado
                            infetados.append(t)
                            virusState[t] = 1
                            contigioState[inf] += 3
                            infBool = True
                            print("infected on " + str(i) + " by " + str(inf) + " num of inf: " + str(len(infetados)))
        virus_copy = copy.deepcopy(virusState)  
        contagio_copy = copy.deepcopy(contigioState)  
        virusStateOffset.append(virus_copy)
        contigioStateOffset.append(contagio_copy)
        infetadosOffset.append(len(infetados))

    #escrever virusState
    print("Writting virus state")
    with open("files/virusState.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(virusStateOffset)

    #escrever sizeState
    print("Writting size state")
    with open("files/sizeState.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(contigioStateOffset)


    #escrever lenState
    print("Writting len state")
    with open("files/lenState.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(infetadosOffset)

    
    #gerar dict dos taxis infetados
    td.generate_taxis_infected_dict(user)
    #gerar tracks dos infetados
    gt.generate_tracks(user)
    #gerar inf em porto,libos
    distinf.generate_infec_conc(user)

if __name__ == "__main__":
    generate_contagio("brunopinto")
    