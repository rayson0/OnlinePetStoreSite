import sqlite3 as sql
from flask import Flask, render_template, request #подключаем библиотеки

app = Flask(__name__)

@app.route('/')
def main():
    connect = sql.connect('products.db')
    connect.row_factory = sql.Row
    cur = connect.cursor()
    cur.execute('SELECT * FROM products')
    inf = cur.fetchall()

    return render_template('main.html', inf=inf)

if __name__=='__main__':
    app.secret_key='admin123'
    app.run(debug=True)