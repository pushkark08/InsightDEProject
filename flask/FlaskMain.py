from flask import Flask
from flask import render_template, request
import pgdb

hostname = '<your-db-ip>'
username = '<your-username>'
password = '<your-password>'
database = '<your-dbname>'

conn = pgdb.connect(host=hostname, user=username, password=password, database=database)


app = Flask(__name__)
@app.route('/')
def index():
    return "SUCCESS"


@app.route("/tweets")
def show_tweets():
    cur = conn.cursor()

    get_query = "SELECT original_tweet, enriched_tweet FROM tweets ORDER BY tweet_id DESC LIMIT 20;"
    
    cur.execute(get_query)
    
    results= []
    
    for o, n in cur.fetchall():
        results.append((o, n))
    
    return render_template('viewTweets.html', values=results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
