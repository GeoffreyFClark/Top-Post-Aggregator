import requests
from bs4 import BeautifulSoup
import sqlite3
from datetime import timedelta, datetime
import subprocess

def fetch_top_posts(dates):
    top_posts = []
    base_url = 'https://news.ycombinator.com/front?day='

    for date in dates:
        url = base_url + date
        print('Fetching posts for date:', date)  # Added for debugging
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}

        while url:
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')

            title_elements = soup.find_all('td', class_='title')
            subtext_elements = soup.find_all('td', class_='subtext')

            for i, title_element in enumerate(title_elements):
                if i % 2 == 1:  # We only want the actual title elements (odd indices)
                    title_line = title_element.find('span', class_='titleline')
                    title = title_line.find('a').text
                    link = title_line.find('a')['href']
                                        
                    subtext_element = subtext_elements[i // 2]
                    
                    # Extract the points from the subtext element
                    score_element = subtext_element.find('span', class_='score')
                    points = int(score_element.text.replace(' points', '')) if score_element else 0
                    date_posted = subtext_element.find('span', class_='age')['title']

                    if points > 500:
                        top_posts.append({
                            'title': title,
                            'link': link,
                            'points': points,
                            'date_posted': date_posted,
                        })
                    
            more_link = soup.find('a', string='More')
            url = base_url + more_link['href'] if more_link else None
            print('Next Page URL:', url)
            
    return top_posts

def save_posts_to_db(hn_posts, programming_posts, learnprogramming_posts):
    # Connect to SQLite database (or create it if it doesn't exist)
    conn_hn = sqlite3.connect('hacker_news_posts.db')
    cursor_hn = conn_hn.cursor()
    cursor_hn.execute('DROP TABLE IF EXISTS hackernews_posts')

    # Create 'hackernews_posts' table
    cursor_hn.execute('''
    CREATE TABLE IF NOT EXISTS hackernews_posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        link TEXT NOT NULL,
        points INTEGER NOT NULL,
        date_posted TEXT NOT NULL
    )
    ''')
    for post in hn_posts:
        cursor_hn.execute('SELECT * FROM hackernews_posts WHERE title = ? AND link = ?', (post['title'], post['link']))
        if cursor_hn.fetchone() is None:
            cursor_hn.execute('INSERT INTO hackernews_posts (title, link, points, date_posted) VALUES (?, ?, ?, ?)',
                        (post['title'], post['link'], post['points'], post['date_posted']))
    conn_hn.commit()
    conn_hn.close()

    # Create 'programming_posts' table
    conn_prog = sqlite3.connect('programming_posts.db')
    cursor_prog = conn_prog.cursor()
    cursor_prog.execute('DROP TABLE IF EXISTS programming_posts')
    cursor_prog.execute('''
    CREATE TABLE IF NOT EXISTS programming_posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        link TEXT NOT NULL,
        points INTEGER NOT NULL,
        date_posted TEXT NOT NULL
    )
    ''')
    for post in programming_posts:
        cursor_prog.execute('SELECT * FROM programming_posts WHERE title = ? AND link = ?', (post['title'], post['link']))
        if cursor_prog.fetchone() is None:
            cursor_prog.execute('INSERT INTO programming_posts (title, link, points, date_posted) VALUES (?, ?, ?, ?)',
                        (post['title'], post['link'], post['points'], post['date_posted']))
    conn_prog.commit()
    conn_prog.close()

    # Create 'learnprogramming_posts' table
    conn_learn = sqlite3.connect('learnprogramming_posts.db')
    cursor_learn = conn_learn.cursor()
    cursor_learn.execute('DROP TABLE IF EXISTS learnprogramming_posts')
    cursor_learn.execute('''
    CREATE TABLE IF NOT EXISTS learnprogramming_posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        link TEXT NOT NULL,
        points INTEGER NOT NULL,
        date_posted TEXT NOT NULL
    )
    ''')
    for post in learnprogramming_posts:
        cursor_learn.execute('SELECT * FROM learnprogramming_posts WHERE title = ? AND link = ?', (post['title'], post['link']))
        if cursor_learn.fetchone() is None:
            cursor_learn.execute('INSERT INTO learnprogramming_posts (title, link, points, date_posted) VALUES (?, ?, ?, ?)',
                        (post['title'], post['link'], post['points'], post['date_posted']))
    conn_learn.commit()
    conn_learn.close()

def fetch_top_reddit_posts(subreddit_name, timeframe):
    base_url = 'https://www.reddit.com/r/{}/top.json'.format(subreddit_name)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
    params = {
        't': timeframe,
        'limit': 20
    }
    
    response = requests.get(base_url, headers=headers, params=params)
    
    if response.status_code != 200:
        print('Failed to fetch the posts from Reddit:', response.status_code)
        return []
    
    posts_data = response.json()['data']['children']
    reddit_posts = []
    
    for post_data in posts_data:
        post = post_data['data']
        reddit_posts.append({
            'title': post['title'],
            'link': post['url'],
            'points': post['score'],
            'date_posted': datetime.utcfromtimestamp(post['created_utc']).strftime('%Y-%m-%d %H:%M:%S')
        })
        
    return reddit_posts

# Here the timeframe should be one of ('day', 'week', 'month', 'year', 'all')
def main(timeframe='day'):
    

    if timeframe == 'day':
        hn_timeframe = 1
    if timeframe == 'week':
        hn_timeframe = 7
    if timeframe == 'month':
        hn_timeframe = 30
    if timeframe == 'year':
        hn_timeframe = 365

    today = datetime.now()
    date_list = [(today - timedelta(days=x)).strftime('%Y-%m-%d') for x in range(hn_timeframe)]
    top_hn_posts = fetch_top_posts(date_list)
    
    top_learnprogramming_posts = fetch_top_reddit_posts('learnprogramming', timeframe)
    top_programming_posts = fetch_top_reddit_posts('programming', timeframe)
    
    
    save_posts_to_db(top_hn_posts, top_programming_posts, top_learnprogramming_posts)

    print('Successfully saved', len(top_hn_posts + top_programming_posts + top_learnprogramming_posts), 'posts to the database.')

    # View in browser at http://127.0.0.1:5000/

if __name__ == "__main__":
    # main()
    subprocess.Popen(["python", "front_end.py"], shell=True)