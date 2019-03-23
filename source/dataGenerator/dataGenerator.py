"""
References:

Closest time row
    https://codereview.stackexchange.com/questions/204549/lookup-closest-value-in-pandas-dataframe
    https://stackoverflow.com/questions/30112202/how-do-i-find-the-closest-values-in-a-pandas-series-to-an-input-number/43112103#43112103

loc vs iloc
    https://stackoverflow.com/questions/31593201/how-are-iloc-ix-and-loc-different

"""

import os, sys, time
import re
import random
import glob

import numpy as np
import pandas as pd

# For plotting the data
import matplotlib.pyplot as plt

SCRIPT_DIR = sys.path[0]
SCRIPT_NAME = str(sys.argv[0]).split("/")[-1]
FILE_NAME =  os.path.basename(sys.argv[0])
HOME = os.environ['HOME']
COMPUTE2_HOME = "/rhome/wqkhan"

'''
GLOBAL VARIABLES
'''
# Creating valid data for formula
# p -> F[3,5]q
trend_samples = [
    pd.DataFrame(np.array([[1, 0], [0, 0], [0, 0], [0, 1], [0, 1], [0, 1]]), columns=['p', 'q']),
    pd.DataFrame(np.array([[1, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 1]]), columns=['p', 'q']),
    pd.DataFrame(np.array([[1, 0], [0, 0], [0, 0], [0, 0], [0, 1], [0, 1]]), columns=['p', 'q']),
    pd.DataFrame(np.array([[1, 0], [0, 0], [0, 0], [0, 0], [0, 1], [0, 0]]), columns=['p', 'q']),
    pd.DataFrame(np.array([[1, 0], [0, 0], [0, 0], [0, 1], [0, 1], [0, 0]]), columns=['p', 'q'])
]
temporal_depth = 5



def df_init(maxTime, data_cols):
    """

    :param maxTime:     the max time from 0, along which the Time column will increase, time will have natural numbers, so number of rows will be equal to max time
    :param data_cols:   the additional columns that will be added to the DataFrame along with Time
    :return:            a DataFrame, with a Time column, and any other additional columns all set to zero
    """

    # the time column
    time = np.linspace(0, maxTime, maxTime, endpoint=False).reshape(maxTime,1)

    index = np.arange(maxTime)


    # data columns, initially set to zeros
    zero_matrix = np.zeros((maxTime, len(data_cols)))

    # stack the arrays
    data_matrix = np.hstack((time, zero_matrix))
    # data_matrix = np.stack((time, zero_matrix), axis=1)

    # Arrays to stack
    data_arrays = ['Time'] + data_cols

    # Get the shape of the data
    (rows, cols) = data_matrix.shape

    # convert the nympy matrix to a dataframe
    df = pd.DataFrame(data=data_matrix,
                     columns=data_arrays)

    return df


def insert_trends(df, data_sample, temporal_depth, num_of_anamoly):

    """

    :param df:              the input DataFrame
    :param data_sample:     the list of type of trends to be inserserted
    :param temporal_depth:  the temporal depth of the STL formula
    :param num_of_anamoly:  the number of anamolies that are going to be inserted
    :return:                a DataFrame, the anmolies inserted
    """

    (df_rows, df_cols) = df.shape

    if (df_rows < temporal_depth*num_of_anamoly):
        print("Error: Number of requested anamolies increse length of trace")
        return

    # trend can be added starting what time
    insert_start_time = 4

    # after a trend has been inserted, how long to wait before entering the next value
    time_step = int((df_rows - (num_of_anamoly * temporal_depth)) / num_of_anamoly)
    # print("Step Size: {}".format(time_step))


    t = insert_start_time
    max_time = df['Time'].idxmax()

    while((t + temporal_depth) <= max_time):

        # # Find the closest time value in the dataframe
        # closest_row = df.iloc[(df['Time'] - t).abs().argsort()[:1]]
        # t = closest_row.iloc[0]['Time']

        # pick a random trend from the sample
        df_trend = data_sample[random.sample(range(0, len(data_sample)),1)[0]]

        # overwrite section of df with the trend
        for df_trend_index, df_trend_row in df_trend.iterrows():
            df.loc[df['Time'] == t + df_trend_index, ['p', 'q']] = [df_trend_row['p'], df_trend_row['q']]

        # update the time for next trend overwrite
        t = t + time_step + temporal_depth

    return df


if __name__ == '__main__':

    print("Starting script {}".format(FILE_NAME))

    # First file to contain how many data points, equals to max time value
    N = 1000

    # number of times N will be multiplied by to get rows of new data - number of 0's added to N
    Decible_copies = 4

    # create the first empty dataframe
    df = df_init(maxTime=N, data_cols=['p', 'q'])

    # insert the anamoly trends into the empty dataframe
    df = insert_trends(df=df, data_sample=trend_samples, temporal_depth=temporal_depth, num_of_anamoly=98)

    # Output CSV file
    output_csv = "input_data_{}.csv".format(N)
    df.to_csv(output_csv, sep=",", index=False)

    '''
    After the first data file has been created
    basically replicate the same data to increase the signal length
    by magnitudes of 10 each iteration
    '''

    for _ in range(Decible_copies):
        N = N*10

        output_csv = "input_data_{}.csv".format(N)

        # make a copy of the data
        dff = df

        for i in range(9):
            df = df.append(dff, ignore_index = True)
        
        df['Time'] = np.linspace(0, N, N, endpoint=False).reshape(N,1)

        print("Shape: row - {} \tcol - {}".format(df.shape[0], df.shape[1]))

        df.to_csv(output_csv, sep=",", index=False)

        del dff


