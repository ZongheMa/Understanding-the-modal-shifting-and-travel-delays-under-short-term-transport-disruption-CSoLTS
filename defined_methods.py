import os
import pandas as pd
from datetime import datetime
import gzip
import shutil
import matplotlib.pyplot as plt
def decompression(directory,delete_gz = False):
    # Get a list of all the gzip files
    gzip_files = [f for f in os.listdir(directory) if f.endswith('.gz')]

    # Loop through gzip files, decompress each into a csv file, and save to the same directory
    for file in gzip_files:
        with gzip.open(os.path.join(directory, file), 'rb') as f_in:
            with open(os.path.join(directory, file[:-3]), 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        if delete_gz:
            os.remove(os.path.join(directory, file))

    return
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

def merge_csv_flow(directory):
    # Get a list of all the csv files
    csv_files = [f for f in os.listdir(directory) if f.endswith('.csv')]

    # Initialize an empty list to hold dataframes
    dfs = []

    # Loop through csv files, read each into a dataframe, and append to the list
    for file in csv_files:
        # Extract date from filename, assuming the date is in format 'traffic_flow_YYYY_MM_DD'
        date_str = file.split('.')[0].split('_')[-3:]  # This gives ['YYYY', 'MM', 'DD']
        date = datetime.strptime('_'.join(date_str), '%Y_%m_%d').date()

        df = pd.read_csv(os.path.join(directory, file))

        # Add date as a new column
        df['date'] = date.strftime('%m/%d/%y')

        dfs.append(df)

    # Concatenate all dataframes in the list into one dataframe
    merged_df = pd.concat(dfs, ignore_index=True).drop_duplicates()

    # Return the merged dataframe
    return merged_df

def normalize_plot(gdf, column, date, cmap='viridis', legend=True):
    # Filter the GeoDataFrame for the specified date
    geo_df = gdf[gdf['date'] == date].copy()

    # Ensure the column is numeric
    geo_df[column] = pd.to_numeric(geo_df[column],
                                   errors='coerce')  # Convert to numeric, set errors to 'coerce' to handle non-numeric values by converting them to NaN

    # Drop rows where column is NaN after conversion (if any)
    geo_df.dropna(subset=[column], inplace=True)

    # Normalize the column
    min_val = geo_df[column].min()
    max_val = geo_df[column].max()
    normalized_col_name = f"{column}_normalized"
    geo_df[normalized_col_name] = (geo_df[column] - min_val) / (max_val - min_val)

    # Plotting
    geo_df.plot(figsize=(10, 10), column=normalized_col_name, cmap=cmap, legend=legend)

    # Additional plotting setup
    plt.title(f"{column} on {date}")
    plt.axis('off')
    plt.show()