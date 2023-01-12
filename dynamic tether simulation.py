import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import PillowWriter
import pandas as pd
import time
import Wind_loading_generations as Wind_l
import scipy as sc

def plot_response(x, y):
    global L
    for item in range(len(x)):
        label = f"Tether {item + 1}, Cd = {cd_items[item]}, radius = {radius_items[item]}, excess Lift = {excess_L_list[item]}"
        plt.plot(x[item][-1], y[item][-1], label=label, c=colorlist[item])
        plt.plot(x[item][-1][-1], y[item][-1][-1], c="black", marker=".", markersize=10)
    plt.xlabel("Horizontal distance [meters]")
    plt.ylabel("Altitude [meters]")
    plt.legend()
    plt.title(f"Final dynamic response to wind profile {wind_profile_select}\nBalloon has a lift force of {round(L/1000, 2)}[kN]")
    figure_name = f"Final dynamic response to wind profile {wind_profile_select}. Balloon has a lift force of {round(L/1000, 2)}[kN]"
    plt.savefig("./Figures/"+figure_name+".png")
    plt.show()


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
yset = 0.6 * dataset[:, 1]  # wind speed
xset = dataset[:, 0]  # altitude
windspeed_from_alt = sc.interpolate.interp1d(xset, yset, kind='quadratic')

colorlist = ["green", "blue", "red", "pink"]


def run_progamm(Cd=1.2, r=0.01, h_balloon=20000, nodes=50):

    # nodes = 50
    # h_balloon = 15000  # m
    h_ground = 0  # m

    # top balloon parameters
    diameter_top_balloon = 50  # meters
    Cd_top_balloon = 0.1

    # tandem balloon parameters
    diameter_tan_balloon = 10  # meters
    Cd_tan_balloon = 0.1

    # Create tandem balloon force
    L_tandem = 10000  # Lift force [N] of the tandem balloon
    D_tandem = 50
    loc_lst = [0.5]  # Fractions of the tether where the tandem balloon is located


    D = 0  # N
    density = 950  # tether-  kg/m^3
    # r = 0.01  # m
    # Cd = 1.2  # tether drag coeff
    E = 100e9  # Pa
    g = 9.81  # m/s
    C = 4  # Ns/m
    plot_wind = False

    # Initiate nodes
    y = np.linspace(h_ground, h_balloon, nodes)  # altitude
    x = np.zeros(nodes)  # x pos
    Fx = np.zeros(nodes)  # sum of x forces on node
    Fy = np.zeros(nodes)  # sum of y forces on node
    Ftandx = np.zeros(nodes)  # vector containing forces from tandem balloon in x
    Ftandy = np.zeros(nodes)  # vector containing forces from tandem balloon in y
    vx = np.zeros(nodes)  # node velocity
    vy = np.zeros(nodes)
    ax = np.zeros(nodes)  # node acceleration
    ay = np.zeros(nodes)
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
    global L
    L = np.sum(W) + excess_L - len(loc_lst)*L_tandem

    for loc in loc_lst:
        tandem_node = round(nodes * loc)
        Ftandx[tandem_node - 1] = D_tandem
        Ftandy[tandem_node - 1] = L_tandem
    t = 0
    dt = 0.001

    # plot_response(x, y)
    xlist = x
    ylist = y

    counter = 0
    max_stress = 0
    while t < t_end:  # and (np.any(abs(ax) > 0.0001) or t < 0.1):
        if np.all(abs(ax) < 0.01) and np.all(abs(vx) < 0.1) and t > 30:
            print("Break because of low acceleration and speed")
            break

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
        T = crossA * E / L0 * (np.sqrt((y[1:] - y[:-1]) ** 2 + (x[1:] - x[:-1]) ** 2) - L0)
        theta = np.arctan2((x[1:] - x[:-1]), (y[1:] - y[:-1]))

        Tx = T * np.sin(theta)
        Ty = T * np.cos(theta)

        if np.max(T / crossA) > max_stress:
            max_stress = np.max(T / crossA)

        # Calculate wind force
        theta_nodes[0] = theta[0]
        theta_nodes[1:-1] = (theta[1:] + theta[:-1]) / 2
        theta_nodes[-1] = theta[-1]

        wind_speed = windspeed_from_alt(y)
        if plot_wind:
            Wind_l.show_wind_profile(wind_speed, y)
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
        Fx[0] = Tx[0] + Fperpx[0] / 2 - Fresx[0] + Fparx[0] / 2
        Fy[0] = Ty[0] - W[0] - Fresy[0] - Fperpy[0] / 2 + Fpary[0] / 2
        Fx[1:-1] = Tx[1:] - Tx[0:-1] + Fperpx[1:-1] - Fresx[1:-1] + Fparx[1:-1]
        Fy[1:-1] = Ty[1:] - Ty[0:-1] - W[1:-1] - Fresy[1:-1] - Fperpy[1:-1] + Fpary[1:-1]
        Fx[-1] = D + Fperpx[-1] / 2 - Tx[-1] - Fresx[-1] + Fparx[-1] / 2
        Fy[-1] = L - Ty[-1] - W[-1] - Fresy[-1] - Fperpy[-1] / 2 + Fpary[-1] / 2

        # Add tandem forces
        Fx = Fx + Ftandx  # note! these are 2 vectors
        Fy = Fy + Ftandy  # note! these are 2 vectors

        ax[1:] = Fx[1:] / m[1:] * min(t, 1)
        ay[1:] = Fy[1:] / m[1:] * min(t, 1)

        vx = vx + ax * dt
        vy = vy + ay * dt

        x = x + vx * dt
        y = y + vy * dt
        plot_wind = False
    return xlist, ylist, max_stress


wind_profile_select = 4
t_end = 20

xlists = []
ylists = []
max_stress_list = []


### animation ###

animations = 2
cd_items = [0.6, 0.6, 0.6, 0.6]
excess_L_list = [750, 750, 750, 750]
radius_items = [0.005, 0.005, 0.005, 0.005]
height_items = [20000, 20000, 20000, 20000]
node_amount = [50, 75, 100, 150]
for i in range(animations):
    begin_time = time.time()
    excess_L = excess_L_list[i]  # N - excess lift
    xlist, ylist, max_stress = run_progamm(Cd=cd_items[i], r=radius_items[i], h_balloon=height_items[i], nodes=node_amount[i])
    xlists.append(xlist)
    ylists.append(ylist)
    max_stress_list.append(max_stress / 10 ** 6)
    print(f"Done with tether {i + 1}, it took {time.time()-begin_time}")
print(max_stress_list)


def animate(i):
    item_list = []
    for item in range(animations):
        line = lines[item]
        balloon = balloons[item]
        xlist = xlists[item]
        ylist = ylists[item]
        # if already done reprint last state
        if i >= len(xlist):
            x = xlist[-1]
            y = ylist[-1]
        else:
            x = xlist[i]
            y = ylist[i]
        balloon_x = x[-1]
        balloon_y = y[-1]
        line.set_data(x, y)  # update the data.
        balloon.set_data(balloon_x, balloon_y)
        # add to total return list
        item_list.append(line)
        item_list.append(balloon)

    # time text update
    time_text.set_text(time_template % (i))

    item_list.append(time_text)

    return tuple(item_list)


# define plot scales for animation
max_x_value = 0
min_x_value = 0

for i in range(len(xlists)):
    for xlist in xlists[i]:
        for x_time_list in xlists:
            for xnodes in x_time_list:
                for x in xnodes:
                    if x > max_x_value:
                        max_x_value = x
                    if x < min_x_value:
                        min_x_value = x

fig = plt.figure()
title = f"Final dynamic response to wind profile {wind_profile_select}\n"\
        f" animated for a total of {t_end} [sec]"
axis = plt.axes(xlim=(min_x_value-100, max_x_value+100), xlabel="Horizontal distance [meters]",
                ylim=(-100, 20000+2000), ylabel="Altitude [meters]", title=title)

# make lists for objects
lines = []
balloons = []

# initialize objects
for item in range(animations):
    label = f"Tether {item + 1}, Cd = {cd_items[item]}, radius = {radius_items[item]}, excess Lift = {excess_L_list[item]}"
    line, = axis.plot([], [], c=colorlist[item], label=label)
    balloon, = axis.plot([], [], marker='.', label=f"Balloon {item + 1}", c="black", markersize=10)
    lines.append(line)
    balloons.append(balloon)

# initialize time text
time_template = 'time= %.1fs'
time_text = axis.text(00.5, 0.9, "")

gridlines_big = axis.grid(which="major")
legend = plt.legend()

# check longest time duration
t_longest = 0
for i in xlists:
    if len(i) > t_longest:
        t_longest = len(i)

ani = animation.FuncAnimation(fig, animate, frames=t_longest, interval=60, blit=True)

# save animation to Animations folder
name = f'prr {t_longest}'
save_name = ("./Animations/"+name+".gif")
ani.save(save_name, dpi=300, writer=PillowWriter(fps=25))
plt.show()
plot_response(xlists, ylists)
