import sqlite3 as sql
import click
from flask import current_app, Flask, g, render_template, request 
from flask.cli import with_appcontext

app = Flask(__name__)

conn = sql.connect('message_db.db')
conn.execute('CREATE TABLE IF NOT EXISTS messages (id INTEGER, message TEXT, name TEXT)')
conn.close()

def insert_message(request):
    message = request.form["message"]
    name = request.form["name"]

    conn = sql.connect('message_db.db')
    c = conn.cursor()
    c.execute("SELECT * FROM messages") 
    number_of_rows = 0 + len(c.fetchall())
    c.execute("INSERT INTO messages (id, message, name) VALUES (?, ?, ?)",
                (number_of_rows + 1, message, name))
    conn.commit()
    conn.close()
    return 

def random_messages(n):
    conn = sql.connect('message_db.db')
    c = conn.cursor()
    c.execute(f"SELECT * FROM messages ORDER BY RANDOM() LIMIT {n}")
    rows = c.fetchall()
    conn.close()
    return rows

@app.route("/")
def main():
    return render_template("base.html")


@app.route('/submit/', methods=['POST', 'GET'])
def submit():
    if request.method == 'GET':
        return render_template("submit.html")
    else:
        message = request.form["message"]
        name = request.form["name"]
        try:
            insert_message(request)
            return render_template("submit.html", 
                                    message = message, 
                                    name = name, 
                                    thanks = True)
        except:
            return "An error!"

@app.route('/view/')
def view():  
    try: 
        rows = random_messages(3)
        return render_template("view.html", 
                                row = rows)
    except: 
        return "Error!"











