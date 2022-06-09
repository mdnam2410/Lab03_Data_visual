# -*- coding: utf-8 -*-
"""
Created on Tue Jan 27 02:33:19 2015

@author: nymph
"""

import io
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, WeekdayLocator
import matplotlib.ticker as ticker
import pandas as pd
import numpy as np


############################## Your code for loading and preprocess the data ##
file_io = open('household_power_consumption.txt')

# Extract the header
header = file_io.readline()
columns = header.strip().split(';')

# Extract only necessary rows
sliced = ''
for line in file_io:
    if line.startswith('1/2/2007') or line.startswith('2/2/2007'):
        sliced += line
        
# Load the data
df = pd.read_csv(io.StringIO(sliced), na_values='?', delimiter=';', header=None)
df.columns = columns

# Combine Date and Time column into a single Timestamp column
date_time_join = df[['Date', 'Time']].apply(
    func=lambda x: ' '.join([x['Date'], x['Time']]),
    axis=1
)
df['Timestamp'] = pd.to_datetime(date_time_join, dayfirst=True)
df.drop(columns=['Date', 'Time'], inplace=True)

############################ Complete the following 4 functions ###############

# There are 4 plots, 6 different charts. The 4th plot reuse two of the charts
# in the 2nd and 3rd plot.

# These functions create all the charts for the sake of reuse
def plot_gap_hist(fig, ax):
    """Plot historgram of Global Active Power (plot 1)
    """
    ax.hist(
        df['Global_active_power'],
        bins=np.arange(0, 8, 0.5),
        color='red',
        edgecolor='black',
    )

    ax.set_title('Global Active Power', fontdict={'fontweight': 'bold'})
    ax.set_xlabel('Global Active Power (kilowatts)')
    ax.set_ylabel('Frequency')

    ax.xaxis.set_major_locator(ticker.MultipleLocator(2))
    return ax

# Utility function
def set_weekday(axis):
    axis.set_major_locator(WeekdayLocator(byweekday=(1, 2, 3, 4, 5, 6, 7)))
    axis.set_major_formatter(DateFormatter('%a'))
    
def plot_gap_time(fig, ax):
    """Plot Global Active Power against timestamp (plot 2)
    """
    ax.plot(
        df['Timestamp'], df['Global_active_power'],
        color='black',
        linewidth=0.75,
    )

    ax.set_ylabel('Global Active Power (kilowatts)')
    # ax.xaxis.set_major_locator(WeekdayLocator(byweekday=(1, 2, 3, 4, 5, 6, 7)))
    # ax.xaxis.set_major_formatter(DateFormatter('%a'))
    set_weekday(ax.xaxis)
    return ax

def plot_esm_time(fig, ax):
    """Plot Energy Sub Metering against time (plot 3)
    """
    ax.plot(
        df['Timestamp'], df['Sub_metering_1'],
        color='black',
        linewidth=0.75,
    )

    ax.plot(
        df['Timestamp'], df['Sub_metering_2'],
        color='red',
        linewidth=0.75,
    )

    ax.plot(
        df['Timestamp'], df['Sub_metering_3'],
        color='blue',
        linewidth=0.75,
    )

    ax.legend(['Sub_metering_1', 'Sub_metering_2', 'Sub_metering_3'])
    ax.set_ylabel('Energy sub metering')
    # ax.xaxis.set_major_locator(WeekdayLocator(byweekday=(1, 2, 3, 4, 5, 6, 7)))
    # ax.xaxis.set_major_formatter(DateFormatter('%a'))
    set_weekday(ax.xaxis)
    return ax

def plot_voltage_time(fig, ax):
    ax.plot(
        df['Timestamp'], df['Voltage'],
        color='black',
        linewidth=0.75,
    )

    set_weekday(ax.xaxis)
    ax.set_ylabel('Voltage')
    return ax

def plot_grp_time(fig, ax):
    ax.plot(
        df['Timestamp'], df['Global_reactive_power'],
        color='black',
        linewidth=0.75,
    )

    ax.set_ylabel('Global Reactive Power')
    set_weekday(ax.xaxis)
    return ax

def plot1():
    fig, ax = plt.subplots()
    plot_gap_hist(fig, ax)
    fig.savefig('plot1.png')

def plot2():
    fig, ax = plt.subplots()
    plot_gap_time(fig, ax)
    fig.savefig('plot2.png')

def plot3():
    fig, ax = plt.subplots()
    plot_esm_time(fig, ax)
    fig.savefig('plot3.png')

def plot4():
    fig, axes = plt.subplots(2, 2, figsize=(8, 6))

    plot_gap_time(fig, axes[0][0])
    plot_voltage_time(fig, axes[0][1])
    plot_esm_time(fig, axes[1][0])
    plot_grp_time(fig, axes[1][1])
    fig.tight_layout(pad=3)

    fig.savefig('plot4.png')

if __name__ == '__main__':
    plot1()
    plot2()
    plot3()
    plot4()
