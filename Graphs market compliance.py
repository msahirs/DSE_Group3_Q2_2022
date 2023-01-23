import math
import numpy as np
import matplotlib.pyplot as plt

t = np.arange(0, 26, 1)
maint = 0.008
price = 70 #[€/MWh]
cost  = 2559640 + 2559640*maint*t
prod  = 2185*t - 11.412 * (t-1)
sub1  = 10
sub2  = 30
sub3  = 50
sub4  = 100

revenue_base = price*prod
revenue_sub1 = (price+sub1)*prod
revenue_sub2 = (price+sub2)*prod
revenue_sub3 = (price+sub3)*prod
revenue_sub4 = (price+sub4)*prod

fig, ax = plt.subplots()
ax.plot(t, cost, linestyle = 'solid', color='0')
ax.plot(t, revenue_base, linestyle = 'dashed', color='0')
ax.plot(t, revenue_sub1, linestyle = 'dashed', color='0')
ax.plot(t, revenue_sub2, linestyle = 'dashed', color='0')
ax.plot(t, revenue_sub3, linestyle = 'dashed', color='0')
ax.plot(t, revenue_sub4, linestyle = 'dashed', color='0')
ax.set_xlabel('Time [year]')
ax.set_ylabel('Value [€]')
ax.set_title('Revenue and cost over time')
plt.show()