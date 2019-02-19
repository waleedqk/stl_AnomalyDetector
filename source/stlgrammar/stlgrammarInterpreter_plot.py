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
    # print("Data has columns: {}".format(columnNames))

    '''
    some columns just add clutter to the final plot
    will add them to this list to remove from the final plot
    '''
    exclude_columns = ['stlProp_']

    # list of columns that need to be plotted - remove the ones from the exclude list
    signal_cols = [x for x in columnNames if (x != 'Time') and (any(s not in x for s in exclude_columns))]
    print("Data has columns: {}".format(signal_cols))

    # load the numpy dict that has the func name key to expr value
    signal_dict = np.load('signal_dict.npy').item()

    # delete the entrys that match the exclude columns list
    for key in list(signal_dict.keys()):
        if any(s in key for s in exclude_columns):
            del signal_dict[key]

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
        title='STL Check: {}'.format(signal_dict['STL_rule']),
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