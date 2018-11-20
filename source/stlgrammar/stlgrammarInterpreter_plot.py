import os, sys, time
import re
import glob

import numpy as np
import pandas as pd

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

import plotly
import plotly.plotly as py
import plotly.graph_objs as go

SCRIPT_DIR = sys.path[0]
SCRIPT_NAME = str(sys.argv[0]).split("/")[-1]
FILE_NAME =  os.path.basename(sys.argv[0])
HOME = os.environ['HOME']

expr_col = ['signalComp_', 'stlProp_']

def plot_Comp_Prop(dataFolder, plotFolder):
    '''

    :param dataFolder: The location of the csv files that have a column for voltage value recorded by the digitizer
    :param plotFolder: The location of where the plots are to be saved
    :return:
    '''

    csvFile = glob.glob(dataFolder + "/*populated.csv")[0]

    base = os.path.basename(csvFile)
    file_name, file_ext = os.path.splitext(base)  

    df = pd.read_csv(csvFile, sep=",")

    (row, col) = df.shape
    columnNames = list(df.columns.values)

    print("Number of Rows: {} and Col: {}".format(row, col))
    print("Data has columns: {}".format(columnNames))

    # list of columns that need to be plotted
    signal_cols = [x for x in columnNames if x != 'Time']

    # load the numpy dict that has the func name key to expr value
    signal_dict = np.load('signal_dict.npy').item()

    print(signal_dict)

    data = []

    for i in signal_cols:
        # Create a trace
        trace = go.Scatter(
            x=df.Time,
            y=df[i],
            mode='lines',
            name=signal_dict[i]
        )
        
        data.append(trace)


    layout = dict(
        title='STL Check',
        xaxis=dict(
            title='Time',
            showticklabels=True,
            tickangle=45,
            rangeslider=dict(
                visible=True
            ),
        ),
        yaxis = dict(
            title='Value',
            titlefont=dict(
                family='Courier New, monospace',
                size=18,
                color='#7f7f7f'
            ),
            # range=[min_signal - (abs(min_signal)*0.1), max_signal + (max_signal*0.1)],
        )
    )

    fig = dict(data=data, layout=layout)

    plotly.offline.plot(
        fig,
        filename=plotFolder + '/STL_check_Plot.html',
        auto_open=False)

if __name__ == '__main__':

    print("Starting script {}".format(FILE_NAME))

    plot_Comp_Prop(dataFolder=SCRIPT_DIR, plotFolder=SCRIPT_DIR)