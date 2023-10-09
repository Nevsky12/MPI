import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import pandas as pd
import numpy as np

def t(m, alpha, beta):
    return alpha + beta * m

def C(m, alpha, beta):
    return m / (alpha + beta * m)

fig, axs = plt.subplots(2, 3, figsize=(30, 20))

sendType = ['Send', 'Ssend', 'Bsend']

before = 15

for i in range(3):
    stateI = pd.read_csv('oneNode/band' + sendType[i] + 'One.txt', sep=',', header=None, names=['time', 'bandwidth', 'size'])
    stateJ = pd.read_csv('twoNode/band' + sendType[i] + 'Two.txt', sep=',', header=None, names=['time', 'bandwidth', 'size'])
    
    xI  = np.array(stateI['size'])
    xJ  = np.array(stateJ['size'])[before:-1]
    xJC = xJ.copy()[before:-1]

    y1I = np.array(stateI['time'])
    y1J = np.array(stateJ['time'])[before:-1]
    y1JC = y1J.copy()[before:-1]

    if sendType[i] == 'Send' or sendType[i] == 'Ssend':
        y1I += 30

    y2I = np.array(stateI['bandwidth'])
    y2J = np.array(stateJ['bandwidth'])[before:-1]
    y2JC = y2J.copy()[before:-1]

    poptTI, pcovTI = curve_fit(t, xI, y1I, maxfev=600000)
    poptTJ, pcovTJ = curve_fit(t, xJC, y1JC, maxfev=600000)

    #poptBI, pcovBI = curve_fit(C, xI, y2I, maxfev=600000)

    axs[0, i].plot(xI, t(xI, *poptTI), 'r-', label='Один узел, теория: alpha=%5.3f, beta=%5.3f' % tuple(poptTI))
    axs[0, i].plot(xJ, t(xJ, *poptTJ), 'g-', label='Два узла теория: alpha=%5.3f, beta=%5.3f' % tuple(poptTJ))
    #axs[0, i].plot(xI, t(xI, *poptBI), label='fit: alpha=%5.3f, beta=%5.3f' % tuple(poptBI))
    axs[0, i].scatter(xI, y1I, label='Один узел, эксперимент', marker='+')
    axs[0, i].scatter(xJ, y1J, label='Два узла, эксперимент', marker='+')
    axs[0, i].set_title(sendType[i])
    axs[0, i].set_xlabel('Размер сообщения, байт')
    axs[0, i].set_ylabel('Время передачи сообщения, мкс')
    axs[0, i].legend()


    axs[1, i].plot(xI, C(xI, *poptTI), 'r-') #label='Один узел, теория: alpha=%5.3f, beta=%5.3f' % tuple(poptTI)) 
    axs[1, i].plot(xJ, C(xJ, *poptTJ), 'g-') #label='Два узла, теория: alpha=%5.3f, beta=%5.3f' % tuple(poptTJ))
   #axs[1, i].plot(xI, C(xI, *poptBI), label='fit: alpha=%5.3f, beta=%5.3f' % tuple(poptBI))
    axs[1, i].scatter(xI, y2I,  marker='+')
    axs[1, i].scatter(xJ, y2J,  marker='+')
    axs[1, i].set_xlabel('Размер сообщения, байт')
    axs[1, i].set_ylabel('Пропускная способность, МБайт/с')
    axs[1, i].legend()
 
fig.show()
plt.show()
