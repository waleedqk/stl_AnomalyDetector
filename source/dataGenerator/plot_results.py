#!/usr/bin/python3

'''
REFERENCES:
https://plot.ly/python/box-plots/
https://plot.ly/python/error-bars/
https://plot.ly/pandas/error-bars/
https://stackoverflow.com/questions/44016069/creating-custom-tick-labels-in-a-plot-in-plotly-in-python
'''

import os, sys, time
import glob
import argparse

import pandas as pd
import numpy as np
import matplotlib
# matplotlib.use('Agg')
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

import plotly
import plotly.plotly as py
import plotly.graph_objs as go

pd.set_option('display.width',140)
pd.set_option('display.max_rows',10)

dirname, filename = os.path.split(os.path.abspath(__file__))
parent_dir = os.path.dirname(dirname)

plot_dir = dirname + '/plots'
csv_dir = dirname


# x_data = ["1000", "10000", "100000", "1000000"]

colors = ['rgba(93, 164, 214, 0.5)', 'rgba(255, 144, 14, 0.5)', 'rgba(44, 160, 101, 0.5)', 'rgba(255, 65, 54, 0.5)']

symbols = ['diamond', 'x-dot', 'triangle-up', 'cross-dot']

def get_data():
    # location of csv file
    csv_file = csv_dir + "/timing_results.csv"

    # load the csv as a df
    df = pd.read_csv(csv_file, delimiter=',')

    # df.set_index('MsgID', inplace=True)

    return df


def df_specifics(df):

    row, col = df.shape
    print("Number of Rows: {} and Cols:{}".format(row, col))

    column_headers = list(df.columns.values)
    print("Column headers are:\n{}".format(column_headers))


def gen_plots(df):

    df_stats = pd.DataFrame(columns=['Trace_length', 'et_count', 'et_mean', 'et_std', 'et_25', 'et_50', 'et_75', 'et_max', 'et_median'])

    for trace_name, trace_group in df.groupby('Trace_length'):

        df_stats = df_stats.append(
        {'Trace_length': trace_name,
        'et_mean': trace_group['Execution_Time (sec)'].mean(),
        'et_count': trace_group['Execution_Time (sec)'].count(), 'et_median': trace_group['Execution_Time (sec)'].median(),
        'et_std': trace_group['Execution_Time (sec)'].std(), 'et_max': trace_group['Execution_Time (sec)'].max(),
        'et_25': trace_group['Execution_Time (sec)'].quantile(.25), 'et_50': trace_group['Execution_Time (sec)'].quantile(.5),
        'et_75': trace_group['Execution_Time (sec)'].quantile(.75) },
        ignore_index=True)

    x_data = df['Trace_length'].unique().tolist()

    dff = pd.DataFrame()

    for trace_name, trace_group in df.groupby('Trace_length'):
        dff[trace_name] = df.loc[df['Trace_length'] == trace_name, 'Execution_Time (sec)'].values

    x_data = list(dff.columns.values)
    x_data = ["{}".format(x) for x in x_data]
    x_data = list( map(str, x_data) )

    y_data = dff.values.T.tolist()
    # Log the results so the graph isnt sparse
    # y_data = np.log10(y_data)

    traces = []

    for xd, yd, cls in zip(x_data, y_data, colors):
        traces.append(go.Box(
            y=yd,
            name="`{}".format(xd),
            boxpoints='all',
            boxmean='sd', # or True
            jitter=0.5,
            whiskerwidth=0.2,
            fillcolor=cls,
            marker=dict(
                size=2,
            ),
            line=dict(width=1),
        ))

    layout = go.Layout(
        title='Computation time for different trace lengths',
        xaxis=dict(
            title='Trace Length',

        ),
        yaxis=dict(
            title='log(Time (s))',
            type='log',
            autorange=True,
            showgrid=True,
            zeroline=True,
            # dtick=5, # shows y-axis ticks in the specified increments
            gridcolor='rgb(255, 255, 255)',
            gridwidth=1,
            zerolinecolor='rgb(255, 255, 255)',
            zerolinewidth=2,
        ),
        margin=dict(
            l=40,
            r=30,
            b=80,
            t=100,
        ),
        paper_bgcolor='rgb(243, 243, 243)',
        plot_bgcolor='rgb(243, 243, 243)',
        showlegend=True
    )

    fig = dict(data=traces, layout=layout)

    plotly.offline.plot(
            fig,
            filename=plot_dir + '/Experimental-Results.html'.format(),
            auto_open=False)







    traces = []

    for xd, yd, cls, sym in zip(x_data, y_data, colors, symbols):
        traces.append(go.Scatter(
            x= ["`{}".format(xd)]*len(yd),
            y=yd,
            name="{} samples".format(xd),
            mode='markers',
            # fillcolor=cls,
            marker=dict(
                size=12,
                # line=dict(width=0),
                color=cls,
                symbol=sym,
            ),
            # text=xd
        ))

    layout = go.Layout(
        title='Computation Time vs Trace Length',
        xaxis=dict(
            title='Trace Length',

        ),
        yaxis=dict(
            title='log(Time (s))',
            type='log',
            autorange=True,
            showgrid=True,
            zeroline=True,
            # dtick=5, # shows y-axis ticks in the specified increments
            gridcolor='rgb(255, 255, 255)',
            gridwidth=1,
            zerolinecolor='rgb(255, 255, 255)',
            zerolinewidth=2,
        ),
        margin=dict(
            l=40,
            r=30,
            b=80,
            t=100,
        ),
        paper_bgcolor='rgb(243, 243, 243)',
        plot_bgcolor='rgb(243, 243, 243)',
        showlegend=True
    )

    fig = dict(data=traces, layout=layout)

    plotly.offline.plot(
            fig,
            filename=plot_dir + '/Experimental-Results-2.html'.format(),
            auto_open=False)




    # data = []
    #
    # for trace_name, trace_group in df_stats.groupby('Trace_length'):
    #
    #     trace = go.Box(
    #         # x=str(trace_name), #trace_group['Trace_length'].values.tolist(),
    #         y=trace_group['et_mean'].values.tolist(),
    #         # mode='lines',
    #         name='{} samples'.format(trace_name),
    #
    #         # # Add range/error bars for each data point
    #         # error_y=dict(
    #         #     type='data',
    #         #     # value=df_stats['et_std'],
    #         #     # thickness=1,
    #         #     # width=0,
    #         #     # color='#444',
    #         #     # opacity=0.8,
    #         #     # symmetric=False,
    #         #     array=trace_group['et_std'].values.tolist(),
    #         #     # arrayminus=ns_group['td_25'].values.tolist(),
    #         # ),
    #     )
    #
    #     data.append(trace)
    #
    # layout = dict(
    #     title='Execution Time (s)'.format(),
    #     xaxis=dict(
    #         title='Trace Length',
    #         tickvals=[k for k in range(1,6)],
    #         ticktext=x_data,
    #     ),
    #     yaxis=dict(
    #         title='Time (s)',
    #         titlefont=dict(
    #             family='Courier New, monospace',
    #             # size=18,
    #             # color='#7f7f7f'
    #         )
    #     )
    # )
    #
    # fig = dict(data=data, layout=layout)
    #
    # plotly.offline.plot(
    #         fig,
    #         filename=plot_dir + '/Experimental-Results.html'.format(),
    #         auto_open=False)

    pass


if __name__ == "__main__":

    df = get_data()

    df_specifics(df=df)

    gen_plots(df=df)