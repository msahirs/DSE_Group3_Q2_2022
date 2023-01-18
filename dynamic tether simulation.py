import time
import math
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import scipy as sc
from matplotlib.animation import PillowWriter

import ISA_general
import Wind_loading_generations as Wind_l


def plot_response(x, y, loc_lists, end_tension_list, end_lift_list):
    ax, fig = plt.subplots(1, 2, gridspec_kw={'width_ratios': [2, 1]})
    global L
    plt.subplot(1, 2, 1)
    for item in range(len(x)):
        label = f"Tether {item + 1}, radius = {radius_items[item]} [m]"
        plt.plot(x[item][-1], y[item][-1], label=label, c=colorlist[item])
        plt.plot(x[item][-1][-1], y[item][-1][-1], c="black", marker=".", markersize=20, linestyle="None")
        for loc_frac in loc_lists[item]:
            if loc_frac:
                loc = round(loc_frac * len(x[item][-1]))
                plt.plot(x[item][-1][loc], y[item][-1][loc], c="gray", marker=".", markersize=10, linestyle="None")
    plt.xlabel("Horizontal distance [meters]")
    plt.ylabel("Altitude [meters]")
    plt.xlim(-100, 11000)
    plt.legend(loc="lower right")
    plt.grid()
    plt.title(f"Final dynamic response")
    figure_name = f"Final dynamic response to realistic windprofile, change on wire radius "
    plt.subplot(1, 2, 2)
    for numb, end_tension in enumerate(end_tension_list):
        rounded_lift = round(end_lift_list[numb] / 1000, 2)
        label = f"Max tension = {round(max(end_tension) / 10 ** 6, 2)} \nLift needed is going to be {rounded_lift} [kN]"
        plt.plot(end_tension / 10 ** 6, range(len(end_tension)), c=colorlist[numb], label=label)
    plt.xlabel("Stress [Mpa]")
    # plt.ylabel("Node numb")
    plt.title("Max tension in nodes")
    plt.legend(loc="lower right")
    plt.grid()
    plt.suptitle("Left, plot showing final steady state solution. Right showing tension over altitude")
    plt.savefig("./Figures/" + figure_name + ".png")
    plt.show()


# Interpolate the wind profile function
dataset = np.array([[-100000, 0],
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

colorlist = ["turquoise", "indigo", "red", "lime"]


def run_progamm(Cd=0.3, r=0.01, h_balloon=20000, nodes=50, loc_lst=[], dt=0.001):
    R = 8.31446261815324  # J/K/mol
    MH2 = 2 * 1.00784  # u = g/mol
    RH2 = R / MH2  # J/K/mol / [g/mol] = J*mol/K/mol/g = J/K/g = kJ/K.kg

    def tandem_volume(h, l):
        Temp, pres, rho = ISA_general.ISA(h)
        rhoH = pres / RH2 / Temp  # [J/m3] / [kJ/kg.K] / [K] = [J/m3].[kg] / [kJ] = [kg/m3]/[J/kJ] = [g/m3]
        rhoH = rhoH / 1000

        rhodif = rho - rhoH  # [kg/m3], Difference in weight between air and hydrogen at altitude h
        L_over_V = rhodif * g  # [N/m3], lift force per m3 of hydrogen
        V = l / L_over_V
        return V, rho

    def update_tandem(cd_tandem):
        for i in range(len(loc_lst)):
            vol, rho = tandem_volume(y[node_lst[i]], L_tandem)
            R = (vol * 3 / 4 / np.pi) ** (1 / 3)
            D_tandem = cd_tandem * 0.5 * rho * (wind_speed[node_lst[i]] - vx[node_lst[i]]) * abs(
                (wind_speed[node_lst[i]] - vx[node_lst[i]])) * np.pi * R ** 2
            Ftandx[tandem_node] = D_tandem

    # nodes = 50
    # h_balloon = 15000  # m
    h_ground = 0  # m

    # drag coeff for balloons
    Frontal_area = 1225.2  #m^2
    Cd_top_balloon = 0.112
    Cd_tan_balloon = 0.2

    # Create tandem balloon force
    L_tandem = 1000  # Lift force [N] of the tandem balloon
    D_tandem = 50
    # loc_lst = [0.2]  # Fractions of the tether where the tandem balloon is located

    rho_umpf = 950  # UHMWPE density, kg/m^3
    rho_al = 2710  # aluminium density, kg/m^3
    A_umpf = 100e-6  # initial guess, m^2
    r1 = 0.000782390181755427  # m
    r2 = 0.00365342418165717  # m
    r3 = 0.00373626051656261  # m
    A_al = np.pi * (r1**2 - r2**2 + r3**2)  # m^2
    A_umpf = np.pi * r ** 2 - A_al # initial guess, m^2
    sigma_max = 250e6  # maximum allowable stress, Pa
    # Cd = 1.2  # tether drag coeff
    E = 100e9  # Pa
    g = 9.81  # m/s
    C = 0.5  # Ns/m
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

    node_lst = []
    for loc in loc_lst:
        tandem_node = round(nodes * loc)
        node_lst.append(tandem_node)
        Ftandx[tandem_node - 1] = D_tandem
        Ftandy[tandem_node - 1] = L_tandem
    t = 0
    radius_list = []
    # dt = 0.001

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

        # if counter % 1000 == 0:
        #     print(f"Has run for {t} sec in animation")

        # Calculate new area and mass
        crossA = A_umpf + A_al  # m^2
        r = np.sqrt(crossA / np.pi)  # m
        radius_list.append(r*1000)  # mm
        m = L0 * (rho_umpf * A_umpf + rho_al * A_al) * np.ones(nodes)
        m[0] = m[0] * 0.5
        m[-1] = m[-1] * 0.5
        W = m * g

        # Calculate tension forces in all segments
        Tension = A_umpf * E / L0 * (np.sqrt((y[1:] - y[:-1]) ** 2 + (x[1:] - x[:-1]) ** 2) - L0)
        theta = np.arctan2((x[1:] - x[:-1]), (y[1:] - y[:-1]))

        Tx = Tension * np.sin(theta)
        Ty = Tension * np.cos(theta)

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

        # Balloon lift and drag
        D = 0.5 * ISA_general.ISA(y[[-1]])[2] * (wind_speed[-1] - vx[-1]) * abs(
            wind_speed[-1] - vx[-1]) * Frontal_area * Cd_top_balloon
        global L
        L = np.sum(W) + excess_L - len(loc_lst) * L_tandem  # lift top balloon

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
        # def update_tandem(cd_tandem):
        #     for i in range(len(loc_lst)):
        #         vol, rho = tandem_volume(y[node_lst[i]], L_tandem)
        #         R = (vol * 3 / 4 / np.pi) ** (1 / 3)
        #         D_tandem = cd_tandem * 0.5 * rho * (wind_speed[node_lst[i]] - vx[node_lst[i]]) * abs(
        #             (wind_speed[node_lst[i]] - vx[node_lst[i]])) * np.pi * R ** 2
        #         Ftandx[tandem_node] = D_tandem
        # if counter % 100 == 0:
        #     update_tandem(Cd_tan_balloon)

        if counter % 100 == 0:
            update_tandem(Cd_tan_balloon)
        Fx = Fx + Ftandx  # note! these are 2 vectors
        Fy = Fy + Ftandy  # note! these are 2 vectors

        ax[1:] = Fx[1:] / m[1:] * min(t, 1)
        ay[1:] = Fy[1:] / m[1:] * min(t, 1)

        if t > 10 and counter % 1000 == 0:
            A_umpf = A_umpf * np.max(Tension / A_umpf) / sigma_max
            # print(f'Area of the UHMWPE is {A_umpf} m^2')
            # L += (250e6 - np.max(Tension / crossA)) * crossA

        vx = vx + ax * dt
        vy = vy + ay * dt

        x = x + vx * dt
        y = y + vy * dt
        plot_wind = False
    print(f'The final location is ({round(x[-1]/1000,2)}, {round(y[-1]/1000,2)})')
    print(f'The final maximum stress is {np.max(Tension / A_umpf)} Pa, total lift is {L/1000} kN')
    print(f'Area of the UHMWPE is {A_umpf * 1e6} mm^2, total radius is {r*1000} mm')
    print(f'The tether weighs {np.sum(W)/1000} kN')
    print(f'The aluminium core weighs {rho_al * A_al * (h_balloon - h_ground) * g / 1000} kN')
    return xlist, ylist, Tension / A_umpf, L, radius_list


wind_profile_select = 4
t_end = 5000
xlists = []
ylists = []
max_stress_list = []
end_tension_list = []
end_lift_list = []
radius_lists_during_programm = []

### animation ###

animations = 2
cd_items = [0.3, 0.3, 0.3, 0.3]  # drag coeff of tether
excess_L_list = [7000, 6000, 3000, 500]  # excess lift of top balloon
radius_items = [0.004, 0.004, 0.004, 0.004]  # radius of tether
height_items = [17000, 17000, 19000, 19000]  # top balloon height
node_amount = [100, 100, 100, 100]  # amount of nodes to use
dt_list = [0.0025, 0.0025, 0.0025, 0.0025]
loc_lsts = [[], [], [], []]  # fraction on where tendem balloon is located
for i in range(animations):
    begin_time = time.time()
    excess_L = excess_L_list[i]  # N - excess lift
    xlist, ylist, End_Tension, end_lift, radius_list_during_program = run_progamm(Cd=cd_items[i],
                                                                                  r=radius_items[i],
                                                                                  h_balloon=height_items[i],
                                                                                  nodes=node_amount[i],
                                                                                  loc_lst=loc_lsts[i],
                                                                                  dt=dt_list[i])
    xlists.append(xlist)
    ylists.append(ylist)
    end_tension_list.append(End_Tension)
    end_lift_list.append(end_lift)
    radius_lists_during_programm.append(radius_list_during_program)
    time_in_sec = round(time.time() - begin_time)
    time_in_min = 0
    if time_in_sec >= 60:
        time_in_min = math.floor((time.time() - begin_time) / 60)
    time_in_sec = time_in_sec - time_in_min * 60
    print(f"Done with tether {i + 1}, it took {time_in_min} min and {time_in_sec} sec")
begin_time = time.time()


def animate(i):
    item_list = []
    for item in range(animations):  # get animation number

        # get correct object from the lists for current animation
        line = lines[item]
        balloon = balloons[item]
        xlist = xlists[item]
        ylist = ylists[item]

        # if already done reprint last state
        if i >= len(xlist):
            x = xlist[-1]
            y = ylist[-1]
        else:  # otherwise update to next frame
            x = xlist[i]
            y = ylist[i]

        balloon_x = x[-1]  # top item = top balloon
        balloon_y = y[-1]
        line.set_data(x, y)  # update the data.
        balloon.set_data(balloon_x, balloon_y)
        # add to objects list
        item_list.append(line)
        item_list.append(balloon)

        # now for tand balloons
        loc_lst = loc_lsts[item]
        tand_x = []
        tand_y = []
        if loc_lst:
            tand_balloon = tand_balloons[item]
            for loc_frac in loc_lst:  # loop
                loc = round(loc_frac * len(x))
                tand_x.append(x[loc])
                tand_y.append(y[loc])
            tand_balloon.set_data(tand_x, tand_y)
            item_list.append(tand_balloon)

    # time text update
    time_text.set_text(time_template % (i))

    item_list.append(time_text)

    return tuple(item_list)


# define plot scales for animation
# max_x_value = 0
# min_x_value = 0

# for i in range(len(xlists)):
#     for xlist in xlists[i]:
#         for x_time_list in xlists:
#             for xnodes in x_time_list:
#                 for x in xnodes:
#                     if x > max_x_value:
#                         max_x_value = x
#                     if x < min_x_value:
#                         min_x_value = x

fig = plt.figure()
title = f"Final dynamic response to wind profile {wind_profile_select}\n" \
        f" animated for a total of {t_end} [sec]"
axis = plt.axes(xlim=(-100, 20000 + 2000), xlabel="Horizontal distance [meters]",
                ylim=(-100, 20000 + 2000), ylabel="Altitude [meters]", title=title)

# make lists for objects
lines = []
balloons = []
tand_balloons = []

# initialize objects
for item in range(animations):
    label = f"Tether {item + 1}, Cd = {cd_items[item]}, radius = {radius_items[item]}, excess Lift = {excess_L_list[item]}"
    line, = axis.plot([], [], c=colorlist[item], label=label)
    balloon, = axis.plot([], [], marker='.', linestyle="None", label=f"Balloon {item + 1}", c="black", markersize=20)
    if loc_lsts[item] != []:
        tand_balloon, = axis.plot([], [], marker='.', linestyle="None", label=f"tand_balloons {item + 1}", c="gray",
                                  markersize=10)
        tand_balloons.append(tand_balloon)
    else:
        tand_balloons.append([])
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
save_name = ("./Animations/" + name + ".gif")

ani.save(save_name, dpi=300, writer=PillowWriter(fps=25))
print(f"Animating took {time.time() - begin_time} [sec]")
plt.show()

plot_response(xlists, ylists, loc_lsts, end_tension_list, end_lift_list)

for item in range(len(radius_lists_during_programm)):
    label = f"Tether {item + 1}, excess lift = {excess_L_list[item]} [m]"
    plt.plot(np.array(radius_lists_during_programm[item]), label=label, c=colorlist[item])
plt.legend()
plt.show()
