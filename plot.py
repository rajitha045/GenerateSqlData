import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

plt.plot([50, 100, 1000, 10000], [0.31, 0.64, 9, 200],label='label1',color="red")
plt.plot([50, 100, 1000, 10000 ], [3600, 7200, 14400, 21600],label='label2',color="blue")


plt.ylabel('time (seconds)')
plt.xlabel('Data Size')
red_patch = mpatches.Patch(color='red', label='Machine')
blue_patch = mpatches.Patch(color='blue', label='Man')

plt.legend(handles=[red_patch, blue_patch])

plt.show()