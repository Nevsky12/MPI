import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import pandas as pd
import numpy as np

def t(m, alpha, beta):
    return alpha + beta * m

def C(m, alpha, beta):
    return m / (alpha + beta * m)

fig, axs = plt.subplots(2, 3)

sendType = ['Send', 'Bsend', 'Ssend']

for i in range(3):
    stateI = pd.read_csv('band' + sendType[i] + 'One.txt', sep=',', header=None, names=['time', 'bandwidth', 'size'])
    xI  = np.array(stateI['size'])
    y1I = np.array(stateI['time'])
    y2I = np.array(stateI['bandwidth'])

    poptTI, pcovTI = curve_fit(t, xI, y1I, maxfev=600000)
    poptBI, pcovBI = curve_fit(C, xI, y2I, maxfev=600000)

    axs[0, i].plot(xI, t(xI, *poptTI), 'r-', label='fit: alpha=%5.3f, beta=%5.3f' % tuple(poptTI))
    #axs[0, i].plot(xI, t(xI, *poptBI), label='fit: alpha=%5.3f, beta=%5.3f' % tuple(poptBI))
    axs[0, i].scatter(xI, y1I)
    axs[0, i].set_title(sendType[i])
    axs[0, i].set_xlabel('Размер сообщения, байт')
    axs[0, i].set_ylabel('Время передачи сообщения, мкс')
    axs[0, i].legend()


    axs[1, i].plot(xI[1000:-1], C(xI[1000:-1], *poptTI), 'r-', label='fit: alpha=%5.3f, beta=%5.3f' % tuple(poptTI))
    #axs[1, i].plot(xI, C(xI, *poptBI), label='fit: alpha=%5.3f, beta=%5.3f' % tuple(poptBI))
    axs[1, i].scatter(xI, y2I)
    axs[1, i].set_xlabel('Размер сообщения, байт')
    axs[1, i].set_ylabel('Пропускная способность, МБайт/с')
    axs[1, i].legend()
 
fig.show()
plt.show()
