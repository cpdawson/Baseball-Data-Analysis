import pandas as pd

# Load the Excel file
file_path = 'positive_correlations_sorted.xlsx'  # Update with the actual path of your file
df = pd.read_excel(file_path)

# Define a function to split the statistic and player name
def split_stat_player(col):
    parts = col.split()
    stat = parts[0]  # The statistic is the first part
    player = ' '.join(parts[1:])  # The rest is the player name
    return stat, player

# Apply the function to split PlayerStat1 and PlayerStat2
df['Stat1'], df['Player1'] = zip(*df['PlayerStat1'].apply(split_stat_player))
df['Stat2'], df['Player2'] = zip(*df['PlayerStat2'].apply(split_stat_player))

# Save back to the same Excel file
df.drop(['PlayerStat1', 'PlayerStat2'], axis=1, inplace=True)  # Drop the original columns
df.to_excel(file_path, index=False)  # Set index=False to not write row indices

print("File processed and saved successfully.")
