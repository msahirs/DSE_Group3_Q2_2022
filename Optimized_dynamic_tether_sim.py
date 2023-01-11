import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import Wind_loading_generations as Wind_l
import scipy as sc

nodes = 50
h_balloon = 20000  # m
h_ground = 0  # m
L = 40000  # N
D = 4000  # N
density = 1000  # kg/m^3
r = 0.005  # m
Cd = 1
E = 100e9  # Pa
g = 9.81  # m/s
C = 4  # Ns/m

# Initiate nodes
y = np.linspace(h_ground, h_balloon, nodes)  # altitude
x = np.zeros(nodes)  # x pos
Fx = np.zeros(nodes)  # sum of x forces on node
Fy = np.zeros(nodes)  # sum of y forces on node
Ftandx = np.zeros(nodes)
Ftandy = np.zeros(nodes)
vx = np.zeros(nodes)  # node velocity
vy = np.zeros(nodes)
ax = np.zeros(nodes)  # node acceleration
ay = np.zeros(nodes)
xframes = np.zeros((1, nodes))
yframes = np.zeros((1, nodes))
theta_nodes = np.zeros(nodes)

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

# Set up animation
# Create the figure and axes to animate
fig, axs = plt.subplots(1)
# init_func() is called at the beginning of the animation
def init_func():
    axs.clear()
# update_plot() is called between frames
def update_plot(i):
    axs.clear()
    axs.plot(xframes[i, :], yframes[i, :], color='k')


# Create tandem balloon force
L1 = 0*20000  # Lift force [N] of the tandem balloon
D1 = 0*800  # Drag force [N] of the tandem balloon
loc1 = 0.7  # Fraction of the tether where the tandem balloon is located
node1 = round(nodes*loc1)

Ftandx[node1 - 1] = D1
Ftandy[node1 - 1] = L1

# Interpolate the wind profile function
dataset = np.array([[-1000, 0],
                    [0, 11],
                    [2500, 15],
                    [5000, 29],
                    [7500, 41],
                    [10000, 51],
                    [12000, 43],
                    [13500, 32],
                    [16000, 20],
                    [17000, 11],
                    [20000, 9],
                    [23000, 11],
                    [25500, 15]])
yset = 0.6 * dataset[:, 1]  # wind speed [m/s], about 30 m/s maximum
xset = dataset[:, 0]  # altitude [m]
windspeed_from_alt = sc.interpolate.interp1d(xset, yset, kind='quadratic')

# Set up simulation
t = 0
dt = 0.001
t_end = 100
max_stress = 0
counter = 0
while t < t_end:  # and np.any(abs(ax) > 0.1):

    if np.all(abs(ax) < 0.01) and np.all(abs(vx) < 0.1) and t > 30:
        print("Break because of low acceleration and speed")
        break

    t += dt
    counter += 1
    if counter % 10000 == 0:
        print(f"Has run {counter} loops")
        xframes = np.append(xframes, [x], axis=0)
        yframes = np.append(yframes, [y], axis=0)

    # Calculate tension forces in all segments
    T = crossA * E / L0 * (np.sqrt((y[1:] - y[:-1]) ** 2 + (x[1:] - x[:-1]) ** 2) - L0)
    theta = np.arctan2((x[1:] - x[:-1]), (y[1:] - y[:-1]))

    Tx = T * np.sin(theta)
    Ty = T * np.cos(theta)

    if np.max(T / crossA) > max_stress:
        max_stress = np.max(T / crossA)
        max_node = np.argmax(T / crossA)

    # Calculate wind force
    theta_nodes[0] = theta[0]
    theta_nodes[1:-1] = (theta[1:] + theta[:-1]) / 2
    theta_nodes[-1] = theta[-1]

    wind_speed = windspeed_from_alt(y)
    wind_perp = wind_speed * np.cos(theta_nodes)
    wind_par = wind_speed * np.sin(theta_nodes)
    Fperp = Wind_l.calc_drag_on_wire(x, y, wind_perp, L0, r, Cd)
    Fperpx = Fperp * np.cos(theta_nodes)
    Fperpy = Fperp * np.sin(theta_nodes)

    Fpar = Wind_l.calc_drag_on_wire(x, y, wind_par, L0, r, Cd)
    Fparx = Fpar * np.sin(theta_nodes)
    Fpary = Fpar * np.cos(theta_nodes)

    # Calculate resisting forces
    Fresx = C * vx
    Fresy = C * vy

    # Calculate total forces on all nodes
    Fx[0] = Tx[0] + Fperpx[0] / 2 - Fresx[0] + Fparx[0]/ 2
    Fy[0] = Ty[0] - W[0] - Fresy[0] - Fperpy[0]/2 + Fpary[0]/2
    Fx[1:-1] = Tx[1:] - Tx[0:-1] + Fperpx[1:-1] - Fresx[1:-1] + Fparx[1:-1]
    Fy[1:-1] = Ty[1:] - Ty[0:-1] - W[1:-1] - Fresy[1:-1] - Fperpy[1:-1] + Fpary[1:-1]
    Fx[-1] = D + Fperpx[-1] / 2 - Tx[-1] - Fresx[-1] + Fparx[-1]/ 2
    Fy[-1] = L - Ty[-1] - W[-1] - Fresy[-1] - Fperpy[-1]/2 + Fpary[-1]/ 2

    # Add tandem forces
    Fx = Fx + Ftandx
    Fy = Fy + Ftandy

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
# print('Fx,Fy = ', Fx, Fy)
print(T)
# print(T/(crossA * E / L0) + L0)
# print(T / crossA)
# print('ax,ay = ', ax, ay)
# print('vx,vy = ', vx, vy)
# print('x,y = ', x, y)
# print(theta)
print(np.sum(Fperpx))
print(f'Maximum stress is {max_stress} Pa at node {max_node}')

plt.plot(range(1,nodes),T)
plt.show()
