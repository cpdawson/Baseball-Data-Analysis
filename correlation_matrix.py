import pandas as pd

# Load data from CSV
data = pd.read_excel('MLB2024.xlsx', sheet_name='MLB2024SeasonStats')
df = pd.DataFrame(data)
# Remove the 'H-AB' column
df.drop('H-AB', axis=1, inplace=True)
data = df
# Assuming 'H-AB' is not directly needed and preprocessing to ensure numeric conversions
data['H'] = pd.to_numeric(data['H'], errors='coerce')
data['RUNS'] = pd.to_numeric(data['RUNS'], errors='coerce')
data['RBI'] = pd.to_numeric(data['RBI'], errors='coerce')
data['H+R+RBI'] = pd.to_numeric(data['H+R+RBI'], errors='coerce')
data['BASES'] = pd.to_numeric(data['BASES'], errors='coerce')

# Pivot the data to wide format
wide_data = pd.pivot_table(data, values=['RUNS', 'H', 'RBI', 'H+R+RBI', 'BASES'],
                           index='Date', columns='Player', fill_value=0, aggfunc='sum')

# Flatten the columns to create a single level index (e.g., 'BASES Aaron Judge')
wide_data.columns = [' '.join(col).strip() for col in wide_data.columns.values]

# Compute the correlation matrix
correlation_matrix = wide_data.corr()

# Save or print the correlation matrix
correlation_matrix.to_csv('correlation_matrix.csv')
print(correlation_matrix)