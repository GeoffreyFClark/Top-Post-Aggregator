import pandas as pd

# Read the CSV file into a pandas dataframe
df = pd.read_csv('stackoverflow_word_freq_composite.csv')

# Write the dataframe to an Excel file
writer = pd.ExcelWriter('stackoverflow_word_freq_composite.xlsx')
df.to_excel(writer, index=False)
writer.save()
