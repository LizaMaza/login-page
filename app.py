

from flask import Flask, render_template, request, redirect, url_for
import sqlite3 as sql

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        try:
            with sql.connect("database.db") as con:
                con.row_factory = sql.Row
                cur = con.cursor()
                cur.execute(
                    "SELECT * FROM users WHERE username = ? AND password = ?",
                    (username, password)
                )
                user = cur.fetchone()

                if user:
                    msg = f"Velkommen, {username}! Du er logget inn."
                else:
                    msg = "Feil brukernavn eller passord. Prøv igjen."
        except Exception as e:
            msg = f"Noe gikk galt: {e}"

        return render_template("result.html", msg=msg)

    return redirect(url_for('index'))

@app.route('/register')
def register():
    return render_template('register.html')



@app.route('/adduser', methods=['POST', 'GET'])
def adduser():
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']

            with sql.connect("database.db") as con:
                cur = con.cursor()
                cur.execute(
                    "INSERT INTO users (username, password) VALUES (?, ?)",
                    (username, password)
                )
                con.commit()
                msg = f"Bruker '{username}' er opprettet! Du kan nå logge inn."
        except sql.IntegrityError:
         
            msg = "Dette brukernavnet finnes allerede. Velg et annet."
        except Exception as e:
            msg = f"Feil ved oppretting av bruker: {e}"

        return render_template("result.html", msg=msg)

    return redirect(url_for('register'))

@app.route('/list')
def list_users():
    con = sql.connect("database.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT id, username FROM users")  
    rows = cur.fetchall()
    return render_template('list.html', rows=rows)


if __name__ == "__main__":
    app.run(debug=True)
