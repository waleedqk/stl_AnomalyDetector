
import os, sys, random, time
import numpy as np
import pandas as pd


df = pd.DataFrame(columns=["stlProp_322", "signalComp_970", "stlProp_500", "signalComp_532", "StlUntil_604", "StlNot_914", "StlConjDisj_853", "StlNot_706", "StlNot_495", "StlUntil_658", "StlNot_204", "Time", "p", "q"])


input_data_df = pd.read_csv('input_data.csv', sep=',', usecols=["Time", "p", "q"])
input_data_df = input_data_df.reset_index(drop=True)

for col in list(input_data_df.columns.values):
	df[col] = input_data_df[col]

df.fillna(0, inplace=True)

del input_data_df

df.set_index('Time', drop=False, inplace=True)

(df_rows, df_cols) = df.shape


if __name__ == '__main__':
    print('Starting monitor ecexution...')


    start_time = time.time()
    dff = df.query('95 <= Time <= 105').Time.values.tolist()
    end_time = time.time()
    print("{:.6f} :\t {} \tdf.query('95 <= Time <= 105')".format((end_time-start_time), dff))

    start_time = time.time()
    dff = df[df['Time'].between(95, 105, inclusive=True)].Time.values.tolist()
    end_time = time.time()
    print("{:.6f} :\t {} \tdf[df['Time'].between(95, 105, inclusive=True)]".format((end_time-start_time), dff))

    start_time = time.time()
    dff = df[(df['Time'] >= 95) & (df['Time'] <= 105)].Time.values.tolist()
    end_time = time.time()
    print("{:.6f} :\t {} \tdf[(df['Time'] >= 95) & (df['Time'] <= 105)]".format((end_time-start_time), dff))

    start_time = time.time()
    dff = df.loc[(df['Time'] >= 95) & (df['Time'] <= 105)].Time.values.tolist()
    end_time = time.time()
    print("{:.6f} :\t {} \tdf.loc[(df['Time'] >= 95) & (df['Time'] <= 105)]".format((end_time-start_time), dff))

    time_phe = []
    start_time = time.time()
    curr_iloc = df.index.get_loc(95)
    while ((df.iloc[curr_iloc].get('Time') <= 105) and curr_iloc < df_rows):
        i = df.iloc[curr_iloc].get('Time')
        time_phe.append(i)
        curr_iloc += 1
    end_time = time.time()
    print("{:.6f} :\t {} \tWhile logic]".format((end_time - start_time), time_phe))