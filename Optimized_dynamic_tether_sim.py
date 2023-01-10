import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import Wind_loading_generations as Wind_l

nodes = 50
h_balloon = 20000  # m
h_ground = 0  # m
L = 80000  # N
D = 1000  # N
density = 1000  # kg/m^3
r = 0.005  # m
wind = 20  # m/s
Cd = 1.2
rho = 0.5  # kg/m^3
E = 100e9  # Pa
g = 9.8  # m/s
C = 4  # Ns/m
wind_profile_select = 4

# Initiate nodes
y = np.linspace(h_ground, h_balloon, nodes)  # altitude
x = np.zeros(nodes)  # x pos
Fx = np.zeros(nodes)  # sum of x forces on node
Fy = np.zeros(nodes)  # sum of y forces on node
vx = np.zeros(nodes)  # node velocity
vy = np.zeros(nodes)
ax = np.zeros(nodes)  # node acceleration
ay = np.zeros(nodes)
xframes = np.zeros((1, nodes))
yframes = np.zeros((1, nodes))

# Initiate segments
segments = nodes - 1
L0 = (h_balloon - h_ground) / segments  # length of a segment
crossA = r ** 2 * np.pi  # m^2
S_front = 2 * r * L0
theta = np.arctan(np.zeros(segments))
T = np.zeros(segments)

# Initiate node mass and weight (first and last node have half the mass of the rest)
m = L0 * crossA * density * np.ones(nodes)
m[0] = m[0] * 0.5
m[-1] = m[-1] * 0.5
W = m * g

# print('W = ', W)

t = 0
dt = 0.001
t_end = 500

# Create the figure and axes to animate
fig, axs = plt.subplots(1)


# init_func() is called at the beginning of the animation
def init_func():
    axs.clear()


# update_plot() is called between frames
def update_plot(i):
    axs.clear()
    axs.plot(xframes[i, :], yframes[i, :], color='k')


counter = 0
while t < t_end:  # and np.any(abs(ax) > 0.1):

    if np.all(abs(ax) < 0.01) and np.all(abs(vx) < 0.1) and t > 30:
        print("Break because of low acceleration and speed")
        break

    t += dt
    counter += 1
    if counter % 10000 == 0:
        print(f"Has run {counter} loops")
        # print(y)
        xframes = np.append(xframes, [x], axis=0)
        yframes = np.append(yframes, [y], axis=0)
    # print(t)

    # Calculate tension forces in all segments
    for seg in range(segments):
        if (y[seg + 1] - y[seg]) == 0:
            print("please god help")
        # if (x[seg + 1] - x[seg]) == 0:
        #     print("please god help")
        T[seg] = crossA * E / L0 * (np.sqrt((y[seg + 1] - y[seg]) ** 2 + (x[seg + 1] - x[seg]) ** 2) - L0)
        theta[seg] = np.arctan2((x[seg + 1] - x[seg]), (y[seg + 1] - y[seg]))
    Tx = T * np.sin(theta)
    Ty = T * np.cos(theta)
    # print('Tx,Ty = ',Tx,Ty)

    # Calculate wind force
    wind_speed = Wind_l.wind_profile(y, wind_profile_select, plot=False)
    Fwind = Wind_l.calc_drag_on_wire(x, y, wind_speed, L0, r, Cd)

    # Calculate resisting forces
    Fresx = C * vx
    Fresy = C * vy

    # Calculate total forces on all nodes
    Fx[0] = Tx[0] + Fwind[0] / 2 - Fresx[0]
    Fy[0] = Ty[0] - W[0] - Fresy[0]
    for node in range(1, nodes - 1):
        Fx[node] = Tx[node] - Tx[node - 1] + Fwind[node] - Fresx[node]
        Fy[node] = Ty[node] - Ty[node - 1] - W[node] - Fresy[node]
    Fx[-1] = D + Fwind[-1] / 2 - Tx[-1] - Fresx[-1]
    Fy[-1] = L - Ty[-1] - W[-1] - Fresy[-1]

    ax[1:] = Fx[1:] / m[1:] * min(t, 1)
    ay[1:] = Fy[1:] / m[1:] * min(t, 1)
    Rx = -Fx
    Ry = -Fy

    vx = vx + ax * dt
    vy = vy + ay * dt

    x = x + vx * dt
    y = y + vy * dt

anim = animation.FuncAnimation(fig, update_plot, frames=xframes.shape[0], init_func=init_func)
plt.show()

# print(xframes, yframes)
print('Fx,Fy = ', Fx, Fy)
# print(T)
# print(T/(crossA * E / L0) + L0)
print(T / crossA)
print('ax,ay = ', ax, ay)
print('vx,vy = ', vx, vy)
print('x,y = ', x, y)
# print(theta)

plt.plot(x, y)
plt.show()