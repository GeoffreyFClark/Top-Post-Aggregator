This web application's backend uses Python, Requests, and BeautifulSoup to scrape top posts from HackerNews, r/Programming, and r/LearnProgramming into an SQLite database for each source based on a user-selected timeframe. These top posts are then displayed in a consolidated manner using HTML/CSS in a Flask frontend.

Technologies Used: 
- Python 
- HTML
- CSS
- Requests
- BeautifulSoup
- SQLite
- Flask

To use this application, copy the code, install the required packages using `pip install -r requirements.txt`, and run `python main.py` to view in a web browser at http://127.0.0.1:5000/.

![Frontend example](templates/frontend.png)

Updated with CSS and removed all datetimes for a more modern look:
![Frontend example](templates/frontend_CSS.png)
