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

    cur.execute("SELECT title, round(avg(ratings),1), director, genre, rel_date FROM movies LEFT JOIN reviews ON movies.id = reviews.mid GROUP BY title, director, genre, rel_date ORDER BY rel_date DESC;")
    movies = cur.fetchall();

    if send == "sign up" and len(id) >=1 and len(password) >=1:
        cur.execute("SELECT id FROM users WHERE id = '{}';".format(id))
        result = cur.fetchone()
        if result:
            return render_template("signup_fail.html")
        elif not result:
            cur.execute("INSERT INTO users VALUES('{}', '{}', '{}');".format(id, password, 'user'))
            connect.commit()
            return render_template("login.html")
    elif send == "sign in":
        cur.execute("SELECT id, password FROM users WHERE id = '{}' and password='{}';".format(id, password))
        result = cur.fetchone()
        if not result:
            return render_template("signin_fail.html")
        elif result[0] == id and result[1] == password:
            return render_template("main.html", movies=movies, user = id)

@app.route('/movie_sort', methods=['POST'])
def movie_sort():
    id = request.form["id"]
    send = request.form["send"]

    if send == "latest":
        cur.execute("SELECT title, round(avg(ratings),1), director, genre, rel_date FROM movies LEFT JOIN reviews ON movies.id = reviews.mid GROUP BY title, director, genre, rel_date ORDER BY rel_date DESC;")
        movies = cur.fetchall();
    elif send == "genre":
        cur.execute("SELECT title, round(avg(ratings),1), director, genre, rel_date FROM movies LEFT JOIN reviews ON movies.id = reviews.mid GROUP BY title, director, genre, rel_date ORDER BY genre;")
        movies = cur.fetchall();
    elif send == "ratings":
        cur.execute("SELECT title, round(avg(ratings),1) as ratings_avg, director, genre, rel_date FROM movies LEFT JOIN reviews ON movies.id = reviews.mid GROUP BY title, director, genre, rel_date ORDER BY ratings_avg DESC;")
        movies = cur.fetchall();
    return render_template("main.html", movies=movies, user = id)

if __name__ == '__main__':
    app.run()

