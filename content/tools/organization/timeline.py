import argparse
import json
import os
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates

# Default configuration with scrubbed name_date_tuples
default_config = {
    "date_format": "%Y-%m-%d %I:%M%p",
    "num_days_lookahead": 28,
    "plot_style": 'dark_background',
    "figure_size": (8.8, 4),
    "stem_color": "tab:red",
    "marker_color": "w",
    "marker_face_color": "b",
    "output_file": "timeline.png",
    "name_date_tuples": [
        ('Task A', '2024-02-06 5:00pm'),
        ('Task B', '2024-02-13 5:00pm'),
        ('Task C', '2024-02-20 5:00pm'),
        ('Task D', '2024-02-27 5:00pm'),
        ('Assignment 1', '2024-02-17 9:00pm'),
        ('Project 1', '2024-02-09 11:00am'),
        ('Assignment 2', '2024-02-23 11:59pm'),
        ('Activity 1', '2024-02-12 11:00pm'),
        ('Meeting', '2024-02-16 1:00pm'),
        ('Event 1', '2024-02-26 7:00pm'),
    ]
}

def load_config(config_file):
    if not os.path.isfile(config_file):
        print(f"Config file '{config_file}' does not exist.")
        return default_config
    
    with open(config_file, 'r') as file:
        return json.load(file)

def generate_sample_config(filename):
    with open(filename, 'w') as file:
        json.dump(default_config, file, indent=4)
    print(f"Sample config file '{filename}' generated.")

def main():
    parser = argparse.ArgumentParser(description="Generate a timeline plot from a config file.")
    parser.add_argument('-c', '--config', type=str, default='config.json',
                        help='Path to the configuration file.')
    parser.add_argument('--generate-sample-config', action='store_true',
                        help='Generate a sample configuration file.')
    
    args = parser.parse_args()
    
    if args.generate_sample_config:
        generate_sample_config(args.config)
        return
    
    config = load_config(args.config)
    
    name_date_tuples = config.get("name_date_tuples", default_config["name_date_tuples"])
    date_format = config.get("date_format", default_config["date_format"])
    num_days_lookahead = config.get("num_days_lookahead", default_config["num_days_lookahead"])

    name_date_tuples = sorted(name_date_tuples, key=lambda t: t[1])
    name_date_tuples.insert(0, ('today', datetime.today().strftime(date_format)))

    days_in_a_week = 7
    num_days_lookahead = num_days_lookahead

    name_date_tuples = filter(
        lambda t: (datetime.strptime(t[1], date_format) - datetime.today()).days <= num_days_lookahead,
        name_date_tuples
    )

    names, dates = zip(*name_date_tuples)
    dates = [datetime.strptime(d, date_format) for d in dates]
    levels = np.tile([-5, 5, -3, 3, -1, 1], int(np.ceil(len(dates) / 6)))[:len(dates)]

    plt.style.use(config.get("plot_style", default_config["plot_style"]))
    fig, ax = plt.subplots(figsize=config.get("figure_size", default_config["figure_size"]), layout="constrained")
    ax.set(title=f"Timeline: {num_days_lookahead} day lookahead")

    ax.vlines(dates, 0, levels, color=config.get("stem_color", default_config["stem_color"]))
    ax.plot(dates, np.zeros_like(dates), "-o", color=config.get("marker_color", default_config["marker_color"]),
            markerfacecolor=config.get("marker_face_color", default_config["marker_face_color"]))

    for d, l, r in zip(dates, levels, names):
        ax.annotate(r, xy=(d, l), xytext=(-3, np.sign(l) * 3), textcoords="offset points",
                    horizontalalignment="center",
                    verticalalignment="bottom" if l > 0 else "top")

    date_locator = mdates.DayLocator()
    ax.xaxis.set_major_locator(date_locator)
    ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(date_locator))
    plt.setp(ax.get_xticklabels(), rotation=30, ha="right")

    ax.yaxis.set_visible(False)
    ax.spines[["left", "top", "right"]].set_visible(False)

    ax.margins(y=0.1)
    plt.savefig(config.get("output_file", default_config["output_file"]))

if __name__ == "__main__":
    main()
