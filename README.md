This web application uses Python, Requests, and BeautifulSoup to scrape top posts from HackerNews, r/Programming, and r/LearnProgramming into an SQLite database for each source based on a user-selected timeframe. These top posts are then displayed in a consolidated manner using HTML/CSS served with Flask.

Technologies Used: 
- Python 
- HTML
- CSS
- Requests
- BeautifulSoup
- SQLite
- Flask

Usage: Copy the code, install the required packages using `pip install -r requirements.txt`, and simply run `python main.py` to view in a web browser at http://127.0.0.1:5000/.

![Frontend example](templates/frontend.png)

Updated with embedded CSS and removed all datetimes for a more modern look:
![Frontend example](templates/frontend_CSS.png)
