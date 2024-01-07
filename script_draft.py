from defined_methods import merge_csv
import pandas as pd



# device = tqdm(pd.read_csv('/Users/zonghe/Library/CloudStorage/OneDrive-UnitedNationsDevelopmentProgramme/Paper/Tube Strike Behaviour/travel_info_oa/device/device_rela_2022-03-01.csv'))
device_merged = merge_csv('/Users/zonghe/Library/CloudStorage/OneDrive-UnitedNationsDevelopmentProgramme/Paper/Tube Strike Behaviour/travel_info_oa/device')

# print(device.info())
print('-'*50)
print(device_merged.info())
print(device_merged['date'].unique())