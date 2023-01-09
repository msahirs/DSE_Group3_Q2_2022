import numpy as np

nodes = 5
h_balloon = 50  # m
h_ground = 0  # m
L = 3000  # N
density = 1000  # kg/m^3
r = 5  # mm
wind = 50  # m/s
Cd = 0.25
rho = 0.5  # kg/m^3
E = 1000  # MPa
g = 9.8  # m/s

# Initiate nodes
y = np.linspace(h_ground, h_balloon, nodes)
x = np.zeros(nodes)
Fx = np.zeros(nodes)
Fy = np.zeros(nodes)
vx = np.zeros(nodes)
vy = np.zeros(nodes)

# Initiate segments
segments = nodes - 1
L0 = (h_balloon - h_ground) / (segments)
crossA = r ** 2 * np.pi  # mm^2
S_front = 2 * r * L0
tantheta = np.zeros(segments)
theta = np.arctan(tantheta)
T = np.zeros(segments)

# Initiate node mass and weight (first and last node have half the mass of the rest)
m = L0 * crossA * density * np.ones(nodes)
m[0] = m[0] * 0.5
m[-1] = m[-1] * 0.5
W = m * g

t = 0
dt = 0.01
t_end = 1

while t < t_end:
    t += dt
    print(t)

    # Calculate tension forces in all segments
    for seg in range(segments):
        T[seg] = crossA * E / L0 * (np.sqrt((y[seg + 1] - y[seg]) ** 2 + (x[seg + 1] - x[seg]) ** 2) - L0)
        theta[seg] = np.arctan((x[seg + 1] - x[seg]) / (y[seg + 1] - y[seg]))
    Tx = T * np.sin(theta)
    Ty = T * np.cos(theta)

    # Calculate wind force
    Fwind = Cd * 0.5 * rho * wind ** 2 * S_front

    # Calculate total forces on all nodes
    Fx[0] = Tx[0] + Fwind / 2
    Fy[0] = Ty[0] - W[0]
    for node in range(1, nodes - 1):
        Fx[node] = Tx[node] - Tx[node - 1] + Fwind
        Fy[node] = Ty[node] - Ty[node - 1] - W[node]
    Fx[-1] = Fwind / 2 - Tx[-1]
    Fy[-1] = L - Ty[-1] - W[-1]

    ax = Fx / m
    ay = Fy / m

    vx = vx + ax * dt
    vy = vy + ay * dt

    x = x + vx * dt
    y = y + vy * dt

    x[0] = 0
    y[0] = h_ground

print(x,y)