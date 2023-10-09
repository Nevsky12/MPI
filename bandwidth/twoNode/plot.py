import matplotlib.pyplot as plt
import pandas as pd


jobNumber = ['', '', '', '', '', '']

fig, axs = plt.subplots(6)

for i in range(3):
    stateI = pd.read_csv('bandwidth.o1848' + jobNumber[i], sep=',', header=None, names=['time', 'bandwidth', 'size'])
    axs[i * 2    ].plot(stateI['size'], stateI['time'     ])
    axs[i * 2 + 1].plot(stateI['size'], stateI['bandwidth'])
   
axs.show()
