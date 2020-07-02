import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd





def update(num, x, y, line):
    line.set_data(x[:num], y[:num])
    line.axes.axis([0, x[num]*1.2, 0, y[num]*1.5])
    return line,


offsets = 8640-1
infetadosOffset = pd.read_csv('files/lenState.csv', header=None, low_memory=True)


fig, ax = plt.subplots()
x = np.linspace(0, 8640, 8641)
y = infetadosOffset.loc[0].to_list()
line, = ax.plot(x, y, color='k')

ani = animation.FuncAnimation(fig, update, fargs=[x, y, line], interval=1, frames=offsets , repeat= False)

plt.show()