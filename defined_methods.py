import os
import pandas as pd
from datetime import datetime
import gzip
import shutil
def decompression(directory):
    # Get a list of all the gzip files
    gzip_files = [f for f in os.listdir(directory) if f.endswith('.gz')]

    # Loop through gzip files, decompress each into a csv file, and save to the same directory
    for file in gzip_files:
        with gzip.open(os.path.join(directory, file), 'rb') as f_in:
            with open(os.path.join(directory, file[:-3]), 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
def merge_csv(directory):
    # Get a list of all the csv files
    csv_files = [f for f in os.listdir(directory) if f.endswith('.csv')]

    # Initialize an empty list to hold dataframes
    dfs = []

    # Loop through csv files, read each into a dataframe, and append to the list
    for file in csv_files:
        # Extract date from filename, assuming the date is in format 'traffic_flow_YYYY_MM_DD'
        date_str = file.split('.')[0].split('_')[-1].split('-')[-3:]  # This gives ['YYYY', 'MM', 'DD']
        date = datetime.strptime('-'.join(date_str), '%Y-%m-%d').date()

        df = pd.read_csv(os.path.join(directory, file))

        # Add date as a new column
        df['date'] = date.strftime('%m/%d/%y')

        dfs.append(df)

    # Concatenate all dataframes in the list into one dataframe
    merged_df = pd.concat(dfs, ignore_index=True).drop_duplicates()

    # Return the merged dataframe
    return merged_df

# decompression('/Users/zonghe/Library/CloudStorage/OneDrive-Personal/Paper/Tube Strike Behaviour/travel_info_oa')
