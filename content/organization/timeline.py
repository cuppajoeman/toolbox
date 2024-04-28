from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np

import matplotlib.dates as mdates

name_date_tuples = [
    ('ex3 csc324', '2024-02-06 5:00pm'),
    ('ex3 csc324', '2024-02-13 5:00pm'),
    ('ex3 csc324', '2024-02-20 5:00pm'),
    ('ex3 csc324', '2024-02-27 5:00pm'),
    ('mat401 hw3', '2024-02-17 9:00pm'),
    ('csc373 m1', '2024-02-09 11:00am'),
    ('csc373 a2', '2024-02-23 11:59pm'),
    ('csc384 a1', '2024-02-12 11:00pm'),
    ('sta347 t', '2024-02-16 1:00pm'),
    ('csc384 t1', '2024-02-26 7:00pm'),
]

# sorting so that when levels (bar heights) assigned they follow a nice decreasing shape (not random)
name_date_tuples = sorted(name_date_tuples, key=lambda t : t[1]) 

name_date_tuples.insert(0, ('today', datetime.today().strftime('%Y-%m-%d %I:%M%p')))

days_in_a_week = 7
num_days_lookahead = 4 * days_in_a_week

name_date_tuples = filter(lambda t: (datetime.strptime(t[1], "%Y-%m-%d %I:%M%p") - datetime.today()).days <= num_days_lookahead, name_date_tuples)

names, dates = zip(*name_date_tuples)

# Convert date strings (e.g. 2014-10-18) to datetime
dates = [datetime.strptime(d, "%Y-%m-%d %I:%M%p") for d in dates]

# Choose some nice levels how high the red things go
levels = np.tile([-5, 5, -3, 3, -1, 1],
                 int(np.ceil(len(dates)/6)))[:len(dates)]

plt.style.use('dark_background')
# Create figure and plot a stem plot with the date
fig, ax = plt.subplots(figsize=(8.8, 4), layout="constrained")
ax.set(title=f"cjm's timeline: {num_days_lookahead} day lookahead")

ax.vlines(dates, 0, levels, color="tab:red")  # The vertical stems.
ax.plot(dates, np.zeros_like(dates), "-o",
        color="w", markerfacecolor="b")  # Baseline and markers on it.

# annotate lines
for d, l, r in zip(dates, levels, names):
    ax.annotate(r, xy=(d, l),
                xytext=(-3, np.sign(l)*3), textcoords="offset points",
                horizontalalignment="center",
                verticalalignment="bottom" if l > 0 else "top")

# format x-axis with 4-month intervals
date_locator = mdates.DayLocator()
ax.xaxis.set_major_locator(date_locator)
#ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(date_locator))
plt.setp(ax.get_xticklabels(), rotation=30, ha="right")

# remove y-axis and spines
ax.yaxis.set_visible(False)
ax.spines[["left", "top", "right"]].set_visible(False)

ax.margins(y=0.1)
#plt.show()
plt.savefig('timeline.png')
