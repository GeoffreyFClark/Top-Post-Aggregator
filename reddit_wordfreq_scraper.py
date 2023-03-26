import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# List of URLs to scrape
urls = ['https://www.reddit.com/r/learnprogramming/top/?t=month',
        'https://www.reddit.com/r/computerscience/top/?t=month',
        'https://www.reddit.com/r/programming/top/?t=month',
        'https://www.reddit.com/r/codetogether/top/?t=month',
        'https://www.reddit.com/r/coding/top/?t=month',
        'https://www.reddit.com/r/compsci/top/?t=month',
        'https://www.reddit.com/r/cscareerquestions/top/?t=month',
        'https://www.reddit.com/r/programmingtools/top/?t=year',
]

# Initialize an empty list to store the dataframes
dfs = []

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}

# Loop through all the URLs and scrape the data
for url in urls:
    # Send a GET request to the URL and parse the response using BeautifulSoup
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all the titles and associated posts in a given page
    elements = soup.select('h3._eYtD2XCVieq6emjKBH3m, p._1qeIAgB0cPwnLhDF9XSiJM')

    titles_posts_list = []

    # Loop through all the elements and extract the question titles
    for element in elements:
        titles_posts_list.append(element.text)

    # Convert list to a single string
    titles_posts_string = ' '.join(titles_posts_list)

    # Convert the string to lowercase
    titles_posts_string = titles_posts_string.lower()

    # Split the string into individual words
    words = titles_posts_string.split()

    # Count the frequency of each word using a dictionary
    word_freq = {}
    for word in words:
        print(word)
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

    # Add a delay before making the next request
    time.sleep(5)
    print(url)

# Concatenate all the dataframes into a single dataframe
result = pd.concat(dfs, ignore_index=True)

# Group the dataframe by the word and sum the frequency
result = result.groupby('word')['frequency'].sum().reset_index()

# Sort the dataframe by frequency in descending order
result = result.sort_values('frequency', ascending=False)

# Save the dataframe to a CSV file
result.to_csv('reddit_word_freq.csv', index=False)
