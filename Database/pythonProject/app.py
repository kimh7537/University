import psycopg2
from flask import Flask, render_template, request, url_for, redirect

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
    cur.execute("SELECT ratings, uid, title, review, TO_CHAR(rev_time, 'YYYY-MM-DD HH24:MI:SS') FROM reviews JOIN movies ON movies.id = reviews.mid ORDER BY rev_time DESC;")
    reviews = cur.fetchall();

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
            return render_template("main.html", reviews = reviews, movies=movies, user = id)




@app.route('/movie_sort', methods=['POST'])
def movie_sort():
    id = request.form["id"]
    send = request.form["send"]
    cur.execute("SELECT ratings, uid, title, review, TO_CHAR(rev_time, 'YYYY-MM-DD HH24:MI:SS') FROM reviews JOIN movies ON movies.id = reviews.mid ORDER BY rev_time DESC;")
    reviews = cur.fetchall();

    if send == "latest":
        cur.execute("SELECT title, round(avg(ratings),1), director, genre, rel_date FROM movies LEFT JOIN reviews ON movies.id = reviews.mid GROUP BY title, director, genre, rel_date ORDER BY rel_date DESC;")
        movies = cur.fetchall();
    elif send == "genre":
        cur.execute("SELECT title, round(avg(ratings),1), director, genre, rel_date FROM movies LEFT JOIN reviews ON movies.id = reviews.mid GROUP BY title, director, genre, rel_date ORDER BY genre;")
        movies = cur.fetchall();
    elif send == "ratings":
        cur.execute("SELECT title, round(avg(ratings),1) as ratings_avg, director, genre, rel_date FROM movies LEFT JOIN reviews ON movies.id = reviews.mid GROUP BY title, director, genre, rel_date ORDER BY ratings_avg DESC;")
        movies = cur.fetchall();
    return render_template("main.html", reviews=reviews, movies=movies, user = id)



@app.route('/review_sort', methods=['POST'])
def review_sort():
    id = request.form["id"]
    send = request.form["send"]
    cur.execute("SELECT title, round(avg(ratings),1), director, genre, rel_date FROM movies LEFT JOIN reviews ON movies.id = reviews.mid GROUP BY title, director, genre, rel_date ORDER BY rel_date DESC;")
    movies = cur.fetchall();

    if send == "latest":
        cur.execute("SELECT ratings, uid, title, review, TO_CHAR(rev_time, 'YYYY-MM-DD HH24:MI:SS') FROM reviews JOIN movies ON movies.id = reviews.mid ORDER BY rev_time DESC;")
        reviews = cur.fetchall();
    elif send == "title":
        cur.execute("SELECT ratings, uid, title, review, TO_CHAR(rev_time, 'YYYY-MM-DD HH24:MI:SS') FROM reviews JOIN movies ON movies.id = reviews.mid ORDER BY title;")
        reviews = cur.fetchall();

    return render_template("main.html", reviews=reviews, movies=movies, user = id)


@app.route('/movie_info', methods=['POST', 'GET'])
def movie_info():
    id = request.form.get("id") or request.args.get("id")
    movie = request.form.get("movie") or request.args.get("movie") #movie name
    cur.execute("SELECT * FROM movies WHERE title = '{}';".format(movie))
    movie_info = cur.fetchone()

    cur.execute("""
        SELECT ratings, uid, review, TO_CHAR(rev_time, 'YYYY-MM-DD HH24:MI:SS')
        FROM reviews
        WHERE mid = '{}'
        AND uid NOT IN (SELECT opid FROM ties WHERE id = '{}' AND tie = 'mute');
        """.format(movie_info[0], id))
    reviews = cur.fetchall()

    cur.execute("SELECT ROUND(AVG(ratings), 1) FROM reviews WHERE mid = '{}';".format(movie_info[0]))
    average_rating = cur.fetchone()[0]

    return render_template("movie_info.html", movie_info=movie_info, reviews=reviews, average_rating=average_rating, user = id)



@app.route('/submit_review', methods=['POST'])
def submit_review():
    user_id = request.form['id']
    movie_id = request.form['movie']
    movie_name = request.form['movie_name']
    ratings = int(request.form['ratings'])
    review_text = request.form['review_text']

    # Check if the user has already reviewed this movie, and update if necessary
    cur.execute("SELECT * FROM reviews WHERE uid = '{}' AND mid = '{}';".format(user_id, movie_id))
    existing_review = cur.fetchone()

    if existing_review:
        cur.execute("""
            UPDATE reviews
            SET ratings = '{}', review = '{}', rev_time = CURRENT_TIMESTAMP
            WHERE uid = '{}' AND mid = '{}';
        """.format(ratings, review_text, user_id, movie_id))
    else:
        cur.execute("""
            INSERT INTO reviews (mid, uid, title, ratings, review, rev_time)
            VALUES ('{}', '{}', '{}', '{}', CURRENT_TIMESTAMP);
        """.format(movie_id, user_id, ratings, review_text))

    connect.commit()

    return redirect(url_for('movie_info', id=user_id, movie=movie_name))



@app.route('/user_info', methods=['POST', 'GET'])
def user_info():
    my_id = request.form.get("id") or request.args.get("id")  # The ID of the logged-in user
    target_user_id = request.form.get("review") or request.args.get("user_id")  # The ID of the user being viewed

    if not my_id or not target_user_id:
        return "My ID and Target User ID are required.", 400

    # Fetch reviews written by the target user
    cur.execute("""
        SELECT ratings, title, review, TO_CHAR(rev_time, 'YYYY-MM-DD HH24:MI:SS') AS formatted_time
        FROM reviews
        WHERE uid = %s
        ORDER BY rev_time DESC;
    """, (target_user_id,))
    reviews = cur.fetchall()

    # Determine the followers and people the user follows/mutes
    cur.execute("SELECT id FROM ties WHERE opid = %s AND tie = 'follow';", (target_user_id,))
    followers = cur.fetchall()

    cur.execute("SELECT opid FROM ties WHERE id = %s AND tie = 'follow';", (target_user_id,))
    followed_users = cur.fetchall()

    cur.execute("SELECT opid FROM ties WHERE id = %s AND tie = 'mute';", (target_user_id,))
    muted_users = cur.fetchall()

    # If the target user is an admin, skip follow/mute controls
    cur.execute("SELECT role FROM users WHERE id = %s;", (target_user_id,))
    role = cur.fetchone()[0]

    return render_template(
        "user_info.html",
        user=my_id,
        target_user_id=target_user_id,
        reviews=reviews,
        followers=followers,
        followed_users=followed_users,
        muted_users=muted_users,
        role=role
    )





@app.route('/main_page', methods=['POST', 'GET'])
def main_page():
    id = request.args["id"]

    cur.execute("SELECT title, round(avg(ratings),1), director, genre, rel_date FROM movies LEFT JOIN reviews ON movies.id = reviews.mid GROUP BY title, director, genre, rel_date ORDER BY rel_date DESC;")
    movies = cur.fetchall();
    cur.execute("SELECT ratings, uid, title, review, TO_CHAR(rev_time, 'YYYY-MM-DD HH24:MI:SS') FROM reviews JOIN movies ON movies.id = reviews.mid ORDER BY rev_time DESC;")
    reviews = cur.fetchall();

    return render_template("main.html", reviews = reviews, movies=movies, user = id)


if __name__ == '__main__':
    app.run()

