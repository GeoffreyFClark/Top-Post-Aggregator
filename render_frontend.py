from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__, template_folder='templates')

@app.route('/', methods=['GET', 'POST'])
def show_top_posts():
    timeline = 'day'  # Default timeline is 'day'
    if request.method == 'POST':
        timeline = request.form.get('timeline', 'day').lower()

    from main import main
    main(timeline)

    conn_hn = sqlite3.connect('hacker_news_posts.db')
    cursor_hn = conn_hn.cursor()
    cursor_hn.execute('SELECT * FROM hackernews_posts ORDER BY points DESC LIMIT 20')
    hn_posts = [{'title': post[1], 'link': post[2], 'points': post[3], 'date_posted': post[4]} for post in cursor_hn.fetchall()]
    conn_hn.close()

    conn_prog = sqlite3.connect('programming_posts.db')
    cursor_prog = conn_prog.cursor()
    cursor_prog.execute('SELECT * FROM programming_posts ORDER BY points DESC LIMIT 20')
    programming_posts = [{'title': post[1], 'link': post[2], 'points': post[3], 'date_posted': post[4]} for post in cursor_prog.fetchall()]
    conn_prog.close()

    conn_learn = sqlite3.connect('learnprogramming_posts.db')
    cursor_learn = conn_learn.cursor()
    cursor_learn.execute('SELECT * FROM learnprogramming_posts ORDER BY points DESC LIMIT 20')
    learnprogramming_posts = [{'title': post[1], 'link': post[2], 'points': post[3], 'date_posted': post[4]} for post in cursor_learn.fetchall()]
    conn_learn.close()

    return render_template('top_posts.html', hn_posts=hn_posts, programming_posts=programming_posts, learnprogramming_posts=learnprogramming_posts, timeline=timeline.upper())



if __name__ == '__main__':
    app.run(debug=False)
    # View in browser at http://127.0.0.1:5000/