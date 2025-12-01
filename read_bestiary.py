import pandas as pd
import numpy as np


pd.set_option('display.max_colwidth', None)
#pd.set_option('display.max_rows', None) 

read_data = pd.read_csv("pathfinder_monsters_raw.csv")

#start cleaning data
 
#fix special cases
read_data['cr'] = read_data['cr'].replace(
    {
        '1/2': '0.5',
        '1/3': '0.333',
        '1/4': '0.25',
        '1/6': '0.166',
        '1/8': '0.125',
        'Â½': '0.5',
        'Â¼': '0.25',
        '6 5': '6',
        '4/1': '4',
        '.': np.nan,
        '6 51': '6',
        '+0,': '2',
        'â\x80\x94': np.nan # em dash
    })


# remove any non numeric characters except for the decimal point
read_data['cr'] = read_data['cr'].str.replace(r'[^0-9.]', '', regex=True)

read_data['cr'] = read_data['cr'].replace('.', np.nan)
read_data = read_data.replace({'cr': {'': np.nan}})

read_data= read_data.dropna(subset=['cr'])


read_data['cr'] = read_data['cr'].astype(float)

# sort by type and sort by cr
read_data = read_data.sort_values(by=['type', 'cr'])

#print(read_data['cr'].unique())

# possibly not needed because spreadsheet software can handle decimal cr values
read_data['cr'] = read_data['cr'].replace(
    {
        0.5: '1/2',
        0.333: '1/3',
        0.25: '1/4',
        0.166: '1/6',
        0.125: '1/8'
    })

read_data = read_data.reset_index(drop=True)


print(read_data)