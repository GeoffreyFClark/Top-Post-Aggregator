import requests
from bs4 import BeautifulSoup
import pandas as pd

# Set the URL of the Stack Overflow "Top Questions of the Week" page
url = 'https://stackoverflow.com/?tab=month'

# Send a GET request to the URL and parse the response using BeautifulSoup
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Find all the links to the top questions on the page
links = soup.select('.question-hyperlink')[0:]

# Initialize an empty list to store all the question titles
all_titles = []

# Loop through all the links and extract the question titles
for link in links:
    all_titles.append(link.text)

# Convert list of titles to a single string
titles_string = ' '.join(all_titles)

# Convert the string to lowercase
titles_string = titles_string.lower()

# Split the string into individual words
words = titles_string.split()

# Count the frequency of each word using a dictionary
word_freq = {}
for word in words:
    if word in word_freq:
        word_freq[word] += 1
    else:
        word_freq[word] = 1

# Convert the dictionary to a pandas dataframe
df = pd.DataFrame.from_dict(word_freq, orient='index', columns=['frequency'])

# Add the "name" column to the dataframe
df['name'] = df.index

# Set the order of the columns in the dataframe
df = df[['name', 'frequency']]

# Sort the dataframe by frequency in descending order
df = df.sort_values('frequency', ascending=False)

# Save the dataframe to a CSV file
df.to_csv('stackoverflow_word_freq.csv', index=False)
