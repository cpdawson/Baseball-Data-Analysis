import pandas as pd

# Define file paths
player_team_file_path = 'MLB2024.xlsx'
correlation_file_path = 'positive_correlations_sorted.xlsx'
game_data_file_path = 'MLB2024.xlsx'

# Load the datasets
player_team_df = pd.read_excel(player_team_file_path).drop(columns=['Date',	'H-AB',	'RUNS',	'H',	'RBI',	'H+R+RBI',	'BASES','ID'])
correlation_df = pd.read_excel(correlation_file_path)
game_data_df = pd.read_excel(game_data_file_path, sheet_name='MLB2024SeasonStats')

# Print column names to verify data integrity
print("Game Data Columns:", game_data_df.columns)
print("Player Team Data Columns:", player_team_df.columns)
print("Correlation Data Columns:", correlation_df.columns)

# Add 'GameKey' column for easier identification of the same game
game_data_df['GameKey'] = game_data_df['Date'].astype(str) + '_' + game_data_df['Team']

# Merge this game information into the player_team_df if necessary or use it directly
player_game_data = game_data_df[['Player', 'GameKey']].drop_duplicates()
merged_game_data = player_game_data.merge(player_game_data, on='GameKey', suffixes=('_1', '_2'))

# Filter out entries where Player_1 is the same as Player_2
merged_game_data = merged_game_data[merged_game_data['Player_1'] != merged_game_data['Player_2']]

# Merge this game data with the correlation data
correlation_df = correlation_df.merge(merged_game_data, left_on=['Player1', 'Player2'], right_on=['Player_1', 'Player_2'], how='left')

# Count how many times they played together
correlation_df['TimesPlayedTogether'] = correlation_df.groupby(['Player1', 'Player2'])['GameKey'].transform('nunique')

# Clean up DataFrame by dropping unnecessary columns
correlation_df.drop(['Player_1', 'Player_2', 'GameKey'], axis=1, inplace=True)

# Remove duplicates
correlation_df.drop_duplicates(inplace=True)

correlation_df = correlation_df[correlation_df['TimesPlayedTogether'] > 45]
correlation_df.sort_values(by='Correlation', ascending=False, inplace=True)

# Save the enhanced correlation data with 'TimesPlayedTogether'
output_file_path = 'enhanced_correlation_data_2024.xlsx'
correlation_df.to_excel(output_file_path, index=False)

print("Enhanced correlation data saved successfully with 'TimesPlayedTogether'.")
