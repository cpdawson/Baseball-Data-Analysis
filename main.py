import pandas as pd

# Load the correlation matrix
correlation_matrix = pd.read_csv('correlation_matrix.csv', index_col=0)

# Ensure the index has a name for melting; if not, name it
if correlation_matrix.index.name is None:
    correlation_matrix.index.name = 'index'

# Melt the correlation matrix into a long format
correlation_long = correlation_matrix.reset_index().melt(id_vars='index')
correlation_long.columns = ['PlayerStat1', 'PlayerStat2', 'Correlation']  # Renaming columns right after melting for clarity

# Replace self-correlations with 0 (self-correlation entries should technically be exactly 1.0)
correlation_long['Correlation'].replace(1.0, 0, inplace=True)

# Filter to show only positive correlations that are less than 1
positive_correlations = correlation_long[(correlation_long['Correlation'] > 0) & (correlation_long['Correlation'] < 0.99999)]

# Remove self-correlations where PlayerStat1 is the same as PlayerStat2
positive_correlations = positive_correlations[positive_correlations['PlayerStat1'] != positive_correlations['PlayerStat2']]

# Sort by correlation value in descending order
positive_correlations_sorted = positive_correlations.sort_values(by='Correlation', ascending=False)

# Display or save the sorted positive correlations
print(positive_correlations_sorted.head(10))  # Display the top 10
positive_correlations_sorted.head(100000).to_excel('positive_correlations_sorted.xlsx', index=False)  # Save to Excel file
