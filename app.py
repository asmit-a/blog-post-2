'''
In this example, we are going to look at creating, serving, and deploying a *very simple* webapp. In the following several lecture, we'll see how to add some interesting interactivity to our app. 

# Prerequisites

- You need to have the flask package installed in your PIC16B Anaconda environment. 
- You need a Heroku account.
- You need the Heroku command line interface: 
    - To install, at the command line (for MacOS)
    brew tap heroku/brew && brew install heroku

- At the command line, run 
    conda activate PIC16B

# Local Preview

At the command line: 

export FLASK_ENV=development; flask run

# Deployment

*Note*: these notes are written for the version of the app that Phil is using, which is indeed called pic16b-minimal-demo. In order to make your own version, you would need to give the app a different name (because one with this name already exists on the internet now).

Sign up for Heroku, create app called pic16b-minimal-demo

```
heroku login
heroku git:remote -a pic16b-minimal-demo

git add *.
git commit -m'add files for heroku'
git push heroku
```

Then, the website is at 
https://pic16b-minimal-demo.herokuapp.com

    
# Sources

This set of lecture notes is based in part on previous materials developed by [Erin George](https://www.math.ucla.edu/~egeo/) (UCLA Mathematics) and the tutorial [here](https://stackabuse.com/deploying-a-flask-application-to-heroku/). 
'''

import sqlite3 as sql
import click
from flask import current_app, Flask, g, render_template, request 
from flask.cli import with_appcontext

# def get_db():
#     if 'db' not in g:
#         g.db = sqlite3.connect(current_app.config['DATABASE'],
#                                 detect_types=sqlite3.PARSE_DECLTYPES)
#         g.db.row_factory = sqlite3.Row
#     return g.db

# def close_db(e = None):
#     db = g.pop('db', None)

#     if db is not None:
#         db.close()

app = Flask(__name__)

conn = sql.connect('message_db.db')
conn.execute('CREATE TABLE IF NOT EXISTS messages (id INTEGER, message TEXT, name TEXT)')
conn.close()

@app.route("/")
def main():
    return render_template("base.html")


@app.route('/submit/', methods=['POST', 'GET'])
def submit():
    if request.method == 'GET':

        return render_template("submit.html")
    else:
        # read data from form 
        message = request.form["message"]
        name = request.form["name"]

        # store into database here
        try:
            conn = sql.connect('message_db.db')
            c = conn.cursor()

            c.execute("INSERT INTO messages (id, message, name) VALUES (?, ?, ?)",
                        (1, message, name))
            conn.commit()
            return render_template("submit.html", 
                                    message = message, 
                                    name = name, 
                                    thanks = True)
        except conn.Error as err:
            return "An error!"
        finally:
            conn.close()


       


@app.route('/view/')
def view(): 
    try: 
        conn = sql.connect('message_db.db')
        c = conn.cursor()
        c.execute("SELECT name, message FROM messages WHERE id = 1" )
        temp = c.fetchall()
        return render_template("view.html", 
                                row = temp)
    except conn.Error as err: 
        return "error!"
    finally:
        conn.close()











