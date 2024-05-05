import psycopg2
from flask import Flask, render_template, request

app = Flask(__name__)
connect = psycopg2.connect("dbname=tutorial user=postgres password=kj003852@")
cur = connect.cursor()  # create cursor


@app.route('/')
def main():
    return render_template("main.html")


@app.route('/return', methods=['post'])
def re_turn():
    return render_template("main.html")


@app.route('/print_table', methods=['post'])
def print_table():
    cur.execute("SELECT * FROM users;")
    result = cur.fetchall()

    return render_template("print_table.html", users=result)


@app.route('/register', methods=['post'])
def register():
    id = request.form["id"]
    password = request.form["password"]
    send = request.form["send"]

    if send == 'login':
        cur.execute("SELECT id, password FROM users WHERE id='{}' and password='{}';".format(id, password))
        result = cur.fetchone()
        if not result:
            return render_template("login_fail.html")
        elif result[0] == id and result[1] == password:
            return render_template("login_success.html")
    elif send == 'sign up':
        cur.execute("SELECT id FROM users WHERE id='{}';".format(id))
        result = cur.fetchone()
        if result:
            return render_template("ID_collision.html")
        elif not result:
            cur.execute("INSERT INTO users VALUES('{}', '{}');".format(id, password))
            connect.commit()
            return render_template("login_success.html")

if __name__ == '__main__':
    app.run()
