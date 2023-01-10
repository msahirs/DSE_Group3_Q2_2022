import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np

# creating a blank window
# for the animation
fig = plt.figure()
axis = plt.axes(xlim=(0, 5),
                ylim=(0, 5))

line, = axis.plot([], [], lw=2)


# what will our line dataset
# contain?
def init():
    line.set_data([], [])
    return line,


# initializing empty values
# for x and y co-ordinates
xdata, ydata = [], []

xlist = [[0, 1, 2], [1, 2, 3], [2, 3, 4]]
ylist = [[0, 1, 2], [1, 2, 3], [2, 3, 4]]

# animation function
def animate(i):
    line.set_data(xlist[i], ylist[i])

    return line,


# calling the animation function
anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=3, interval=200, blit=False)
plt.show()