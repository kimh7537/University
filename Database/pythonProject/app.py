import psycopg2
from flask import Flask, render_template, request

app = Flask(__name__)
connect = psycopg2.connect("dbname=term24 user=postgres password=kj003852@")
cur = connect.cursor()

@app.route('/')
def main():
    return render_template("login.html")

@app.route('/register', methods=['POST'])
def register():
    id = request.form['id']
    password = request.form['password']
    send = request.form["send"]

    if send == "sign up":
        cur.execute("SELECT id FROM users WHERE id = '{}';".format(id))
        result = cur.fetchone()
        if result or id == "":
            return render_template("signup_fail.html")
        elif not result and id != "":
            cur.execute("INSERT INTO users VALUES('{}', '{}', '{}');".format(id, password, 'user'))
            connect.commit()
            return render_template("main.html")
    elif send == "sign in":
        cur.execute("SELECT id, password FROM users WHERE id = '{}' and password='{}';".format(id, password))
        result = cur.fetchone()
        if not result:
            return render_template("signin_fail.html")
        elif result[0] == id and result[1] == password:
            return render_template("main.html")




if __name__ == '__main__':
    app.run()

