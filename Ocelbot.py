import praw
import bot #custom, to store username and password info
import sqlite3 # database for storing comment IDs
import time

USERAGENT ="Archer Ocelbot - the Babou reply bot"
USERNAME = bot.un # reddit username, usually bot specific
PASSWORD = bot.pw # reddit password, for bot username
SUBREDDIT = "test"
MAXPOSTS = 100
SETPHRASES = [ "BABOU" ] # there might be several things you want to search for
SETRESPONSE = "HE REMEMBERS ME!!" # only one response
WAIT = 20

sql = sqlite3.connect('sql.db')
cur = sql.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS oldposts(ID TEXT)")
sql.commit()
print("Opening database")

print("Logging in to reddit")
r=praw.Reddit(USERAGENT) #open a connection

r.login(USERNAME, PASSWORD) #log in

def replybot():
    print("Fetching subreddit", SUBREDDIT)
    subreddit = r.get_subreddit(SUBREDDIT) # put name of subreddit in quotes
    print("Fetching comments")
    comments = subreddit.get_comments(limit=MAXPOSTS) # call to reddit, gets MAXPOSTS items
    for comment in comments: # goes through the comments in the list
        cur.execute("SELECT * FROM oldposts WHERE ID=?", [comment.id])
        if not cur.fetchone():
            try:
                cauthor=comment.author.name
                if cauthor.lower() !=USERNAME.lower():
                    cbody = comment.body.lower() # automatically convert comment to lowercase
                    if any(key.lower() in cbody for key in SETPHRASES):
                        print("Replying to", cauthor)
                        comment.reply(SETRESPONSE)
            except AttributeError:
                pass
            cur.execute("INSERT INTO oldposts VALUES(?)", [comment.id])
            sql.commit()

while True:
    replybot()
    time.sleep(WAIT)
