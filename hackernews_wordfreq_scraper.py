import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta

# Initialize empty list of URLs to scrape
urls = []

# Set the time window for the last 7 days
time_window = datetime.now() - timedelta(days=6)

# Initialize an empty list to store the dates
dates = []

# Loop through the last 7 days and append the dates to the list
for i in range(7):
    # Calculate the date for the current day
    date = (time_window + timedelta(days=i)).strftime('%Y-%m-%d')
    # Append the date to the list
    dates.append(date)

# Use dates to generate HackerNews URLs for the last 7 days
for date in dates:
    urls += [f'https://news.ycombinator.com/front?day={date}']

print(urls)

# Initialize an empty list to store the dataframes
dfs = []

# Loop through all the URLs and scrape the data
for url in urls:
    # Send a GET request to the URL and parse the response using BeautifulSoup
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all the top post titles on the page
    links = soup.select('.titleline a')[0:]

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

    # Add the "word" column to the dataframe
    df['word'] = df.index

    # Set the order of the columns in the dataframe
    df = df[['word', 'frequency']]

    # Append the dataframe to the list of dataframes
    dfs.append(df)

# Concatenate all the dataframes into a single dataframe
result = pd.concat(dfs, ignore_index=True)

# Group the dataframe by the word and sum the frequency
result = result.groupby('word')['frequency'].sum().reset_index()

# Sort the dataframe by frequency in descending order
result = result.sort_values('frequency', ascending=False)

# Save the dataframe to a CSV file
result.to_csv('hackernews_word_freq.csv', index=False)
