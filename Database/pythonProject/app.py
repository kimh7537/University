import psycopg2
from flask import Flask, render_template, request

app = Flask(__name__)
connect = psycopg2.connect("dbname=term24 user=postgres password=kj003852@")
cur = connect.cursor()

@app.route('/')
def main():
    return render_template("main.html")

@app.route('/register', methods=['POST'])
def register():
    id = request.form['id']
    password = request.form['password']



if __name__ == '__main__':
    app.run()

