import pandas as pd 
import glob 
import os 
  
joined_files = os.path.join("f:/lichess_data/csv_data/", "*.csv") 

# A list of all joined files is returned 
joined_list = glob.glob(joined_files) 

df = pd.concat(map(pd.read_csv, joined_list), ignore_index=True) 

game_mapping = {
    'Blitz': 'Blitz',
    'Bullet': 'Bullet',
    'Classical': 'Classical',
    'Correspondence': 'Correspondence'
}

# Function to extract game type
def get_game_type(event):
    for key, value in game_mapping.items():
        if key in event:
            return value
    return 'Other'

df['GameType'] = df['Event'].apply(get_game_type)

df.to_csv(f"f:/lichess_data/merged_data/2013_merged_files.csv")