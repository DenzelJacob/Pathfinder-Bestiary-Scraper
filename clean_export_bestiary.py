import pandas as pd
import numpy as np
import time
import gspread
from google.oauth2.service_account import Credentials
from gspread_dataframe import set_with_dataframe

start_time = time.perf_counter()



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

grouped_data = read_data.groupby('type')

monster_types = grouped_data.groups.keys()






"""
# Authenticate and connect to Google Sheets
"""


scopes = ["https://www.googleapis.com/auth/spreadsheets"]
credentials = Credentials.from_service_account_file("credentials.json", scopes=scopes)
client = gspread.authorize(credentials)


sheet_id = "18EBsFhmgZUlHqUajsiY2crF57FE35VKYQly0mjo3eDg"


main_worksheet = client.open_by_key(sheet_id)


for monster_type in monster_types:
    print("Processing monster type:", monster_type)

    type_data = grouped_data.get_group(monster_type)
    
    try:
        worksheet = main_worksheet.worksheet(monster_type)
    except gspread.exceptions.WorksheetNotFound:
        worksheet = main_worksheet.add_worksheet(title=monster_type, rows= len(type_data), cols="6")
    
    
    
    # Clear existing content
    worksheet.clear()
    
    # Set headers
    headers = ["name", "url", "type", "cr" ]
    worksheet.append_row(headers)
    
    # Append data
    set_with_dataframe(worksheet, type_data, include_index=False)


    # Auto-resize columns
    requests = [
        {
            "autoResizeDimensions": {
                "dimensions": {
                    "sheetId": worksheet.id,
                    "dimension": "COLUMNS",
                    "startIndex": 0,  # Starting column index (0-based)
                    "endIndex": worksheet.col_count # Ending column index (exclusive)
                }
            }
        }
    ]

    main_worksheet.batch_update({"requests": requests})

    
    print(f"Updated worksheet for {monster_type} with {len(type_data)} entries.")

end_time = time.perf_counter()


print(f"Time taken: {(end_time - start_time) / 60} minutes")
  