import matplotlib.pyplot as plt
import numpy as np

from math import atan2, degrees
import numpy as np

# function from stack overflow to label line
def labelLine(line, x, label=None, align=True, **kwargs):

    ax = line.axes
    xdata = line.get_xdata()
    ydata = line.get_ydata()

    if (x < xdata[0]) or (x > xdata[-1]):
        print('x label location is outside data range!')
        return

    # Find corresponding y co-ordinate and angle of the line
    ip = 1
    for i in range(len(xdata)):
        if x < xdata[i]:
            ip = i
            break

    y = ydata[ip-1] + (ydata[ip]-ydata[ip-1]) * \
        (x-xdata[ip-1])/(xdata[ip]-xdata[ip-1])

    if not label:
        label = line.get_label()

    if align:
        # Compute the slope
        dx = xdata[ip] - xdata[ip-1]
        dy = ydata[ip] - ydata[ip-1]
        ang = degrees(atan2(dy, dx))

        # Transform to screen co-ordinates
        pt = np.array([x, y]).reshape((1, 2))
        trans_angle = ax.transData.transform_angles(np.array((ang,)), pt)[0]

    else:
        trans_angle = 0

    # Set a bunch of keyword arguments
    if 'color' not in kwargs:
        kwargs['color'] = line.get_color()

    if ('horizontalalignment' not in kwargs) and ('ha' not in kwargs):
        kwargs['ha'] = 'center'

    if ('verticalalignment' not in kwargs) and ('va' not in kwargs):
        kwargs['va'] = 'center'

    if 'backgroundcolor' not in kwargs:
        kwargs['backgroundcolor'] = ax.get_facecolor()

    if 'clip_on' not in kwargs:
        kwargs['clip_on'] = True

    if 'zorder' not in kwargs:
        kwargs['zorder'] = 2.5

    ax.text(x, y, label, rotation=trans_angle, **kwargs)


def labelLines(lines, align=True, xvals=None, **kwargs):

    ax = lines[0].axes
    labLines = []
    labels = []

    # Take only the lines which have labels other than the default ones
    for line in lines:
        label = line.get_label()
        if "_line" not in label:
            labLines.append(line)
            labels.append(label)

    if xvals is None:
        xmin, xmax = ax.get_xlim()
        xvals = np.linspace(xmin, xmax, len(labLines)+2)[1:-1]

    for line, x, label in zip(labLines, xvals, labels):
        labelLine(line, x, label, align, **kwargs)


font = {'family' : 'normal',
        'weight' : 'normal',
        'size'   : 12}
boldFont = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 12}
titleFont = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 16}

plt.rc('font', **font)

data = np.array([
    [2003, 28290, 10.82, 0, np.NAN],
    [2004, 28714, 10.98, 0, np.NAN],
    [2005, 29145, 11.14, 0, 1474],
    [2005.5, 30165, 11.53, 0, 1474],
    [2006, 31211, 11.93, 0, 1465],
    [2007, 32782, 12.53, 0, 1450],
    [2008, 33274, 12.72, 0, 1567],
    [2009, 33274, 12.72, 0, 1476],
    [2010, 33274, 12.72, 0, 1454],
    [2011, 33939, 12.97, 0, 1442],
    [2011.5, 34618, 13.23, 0, 1442],
    [2012, 35310, 13.49, 0, 1465],
    [2013, 35310, 13.49, 0, 1476],
    [2014, 37076, 14.16, .015, 1513],
    [2015, 38559, 14.73, .015, 1552],
    [2016, 40102, 15.32, .015, 1643],
    [2017, 41306, 15.78, .015, 1685],
    [2018, 42546, 16.26, .02, 1666],
    [2019, 43823, 16.75, .02, 1664],
    [2020, 45138, 17.26, .02, np.NAN],
])

dates = data[:, 0]
ta_actual_wage = data[:, 1]
tutor_actual_wage = data[:, 2]
uc_offers = data[:, 3]

x_ticks = range(int(dates[0]), int(dates[-1]) + 1)

data_cleaned = data[~np.isnan(data).any(axis=1)]
rent_dates = data[:, 0]
average_rent_cost = data[:, 4]

uc_ta_wage = np.asarray([ta_actual_wage[0]] * len(ta_actual_wage))
uc_tutor_wage = np.asarray([tutor_actual_wage[0]] * len(tutor_actual_wage))

for i in range(len(uc_ta_wage)):
    if i > 0:
        uc_ta_wage[i] = uc_ta_wage[i-1] * (1 + uc_offers[i])
        uc_tutor_wage[i] = uc_tutor_wage[i-1] * (1 + uc_offers[i])

'''
TA Wage Graph
'''

plt.plot(dates, (ta_actual_wage / 2) / 9, color='red',
         linestyle='-.', label="Union-Won 50% TA Wage")
plt.plot(dates, (uc_ta_wage / 2) / 9, color='darkorange',
         linestyle='-.', label="UC-Offered 50% TA Wage")
plt.plot(rent_dates, (average_rent_cost * 3.333), color='blue',
         linestyle='-.', label="Non-Rent Burden Wage")

# naming the y axis
plt.ylabel('Monthly Wage ($)', fontdict=titleFont)
plt.ylim(ymin=0) 

# naming the x axis
plt.xlabel('Year', fontdict=titleFont)
plt.xticks(ticks=x_ticks)
plt.xlim(xmin=x_ticks[0], xmax=x_ticks[-1])

plt.rc('font', **boldFont)
lines = plt.gca().get_lines()
labelLines(lines, align=False)

plt.grid(axis='y')

# function to show the plot
plt.show()


'''
Tutor Wage Graph
'''

plt.plot(dates, tutor_actual_wage, color='red',
         linestyle='-.', label="Union-Won Tutor Wage")
plt.plot(dates, uc_tutor_wage, color='darkorange',
         linestyle='-.', label="UC-Offered Tutor Wage")
plt.plot(rent_dates, (average_rent_cost * 3 * 12) / (20 * 52.1429), color='blue',
         linestyle='-.', label="Non-Rent Burden Wage")

# naming the y axis
plt.ylabel('Hourly Wage ($)', fontdict=titleFont)
plt.ylim(ymin=0) 

# naming the x axis
plt.xlabel('Year', fontdict=titleFont)
plt.xticks(ticks=x_ticks)
plt.xlim(xmin=x_ticks[0], xmax=x_ticks[-1])

plt.rc('font', **boldFont)
lines = plt.gca().get_lines()
labelLines(lines, align=False)

plt.grid(axis='y')

plt.show()