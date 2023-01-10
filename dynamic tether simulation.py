import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import Wind_loading_generations as Wind_l


def plot_response(x, y):
    plt.plot(x, y, label="Tether")
    plt.plot(x[-1], y[-1], label="Balloon", c="black", marker=".", markersize=10)
    plt.xlabel("Horizontal distance [meters]")
    plt.ylabel("Altitude [meters]")
    plt.legend()
    plt.title(f"Final dynamic response to wind profile {wind_profile_select}\nBalloon has a lift force of {L}[N]")
    plt.show()


colorlist = ["green", "blue", "red", "pink"]


# def init():
#     line.set_data([], [])
#     balloon.set_data([], [])
#     return line, balloon,


wind_profile_select = 4
t_end = 5
L = 100000  # N



def run_progamm(Cd=1.2):
    nodes = 100
    h_balloon = 20000  # m
    h_ground = 0  # m

    D = 200  # N
    density = 1000  # tether-  kg/m^3
    r = 0.01  # m
    wind = 20  # uniform wind m/s
    # Cd = 1.2  # tether drag coeff
    rho = 0.5  # kg/m^3
    E = 100e9  # Pa
    g = 9.8  # m/s
    C = 100  # Ns/m

    plot_wind = False

    # Initiate nodes
    y = np.linspace(h_ground, h_balloon, nodes)  # altitude
    x = np.zeros(nodes)  # x pos
    Fx = np.zeros(nodes)  # sum of x forces on node
    Fy = np.zeros(nodes)  # sum of y forces on node
    vx = np.zeros(nodes)  # node velocity
    vy = np.zeros(nodes)
    ax = np.zeros(nodes)  # node acceleration
    ay = np.zeros(nodes)

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

    # plot_response(x, y)
    xlist = x
    ylist = y

    counter = 0

    while t < t_end and (np.any(abs(ax) > 0.0001) or t < 0.1):
        t += dt
        counter += 1
        if counter % 1000 == 0:
            # update list for animation every %""
            xlist = np.vstack([xlist, x])
            ylist = np.vstack([ylist, y])

        if counter % 10000 == 0:
            print(f"Has run {counter} loops")
        # print(t)

        # Calculate tension forces in all segments
        for seg in range(segments):
            # if (y[seg + 1] - y[seg]) == 0:
            #         print("please god help")
            # if (x[seg + 1] - x[seg]) == 0:
            #     print("please god help")
            T[seg] = crossA * E / L0 * (np.sqrt((y[seg + 1] - y[seg]) ** 2 + (x[seg + 1] - x[seg]) ** 2) - L0)
            theta[seg] = np.arctan2((x[seg + 1] - x[seg]), (y[seg + 1] - y[seg]))
        Tx = T * np.sin(theta)
        Ty = T * np.cos(theta)
        # print('Tx,Ty = ',Tx,Ty)

        # Calculate wind force
        wind_speed = Wind_l.wind_profile(y, wind_profile_select, plot_wind)
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
        # print('Fx,Fy = ',Fx,Fy)
        # print('ax,ay = ',ax,ay)

        vx = vx + ax * dt
        vy = vy + ay * dt

        x = x + vx * dt
        y = y + vy * dt

        x[0] = 0
        y[0] = h_ground
        plot_wind = False
    return xlist, ylist


xlist1, ylist1 = run_progamm()
# for runs in range(animations):
xlist2, ylist2 = run_progamm(2)

xlists = [xlist1, xlist2]
ylists = [ylist1, ylist2]

### animation ###

animations = 2


def animate(i):
    balloon_list = []
    line_list = []
    for item in range(animations):
        # line = lines[item]
        # balloon = balloons[item]
        xlist = xlists[item]
        ylist = ylists[item]
        x = xlist[i]
        y = ylist[i]
        # axis.plot([x], [y], lw=2, c=colorlist[item])
        balloon_x = xlist1[i][-1]
        balloon_y = ylist1[i][-1]
        line.set_data(x, y)  # update the data.
        # axis.plot([x[-1]], [y[-1]], marker='.', label="Balloon", c="gray", markersize=10)
        balloon.set_data(balloon_x, balloon_y)
        balloon_list.append(balloon)
        line_list.append(line)

    return line_list[0], balloon_list[0], line_list[1], balloon_list[1]



fig = plt.figure()
title = f"Final dynamic response to wind profile {wind_profile_select}\nBalloon has a lift force of {L}[N]," \
        f" animated for {t_end} [sec]"
axis = plt.axes(xlim=(-100, 10000), xlabel="Horizontal distance [meters]",
                ylim=(0, 25000), ylabel="Altitude [meters]", title=title)

for item in range(animations):
    line, = axis.plot([], [], c=colorlist[item], label=f"Tether {item+1}")
    balloon, = axis.plot([], [], marker='.', label=f"Balloon {item+1}", c="gray", markersize=10)

legend = plt.legend()

ani = animation.FuncAnimation(fig, animate, frames=int((len(xlist1))), interval=1000, blit=True)
plt.show()
