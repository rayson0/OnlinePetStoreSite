import sqlite3 as sql
from flask import Flask, render_template, request
from forms import LoginForm, LikeForm, RegistrationForm
from datetime import datetime

app = Flask(__name__)


def min_price():
    connect = sql.connect('products.db')
    connect.row_factory = sql.Row
    cur = connect.cursor()
    cur.execute('SELECT MIN(price), price FROM products')
    res = cur.fetchall()
    connect.close()
    return res


def max_price():
    connect = sql.connect('products.db')
    connect.row_factory = sql.Row
    cur = connect.cursor()
    cur.execute('SELECT MAX(price), price FROM products')
    res = cur.fetchall()
    connect.close()
    return res


def sale():
    connect = sql.connect('products.db')
    connect.row_factory = sql.Row
    cur = connect.cursor()
    cur.execute('SELECT price FROM products WHERE sale = "1"')
    res = cur.fetchall()
    connect.close()
    return res


def len_brends():
    connect = sql.connect('products.db')
    connect.row_factory = sql.Row
    cur = connect.cursor()
    cur.execute('SELECT COUNT(DISTINCT brand) AS brand FROM products')
    res = cur.fetchall()
    print(res)
    connect.close()
    return res


def brends():
    connect = sql.connect('products.db')
    connect.row_factory = sql.Row
    cur = connect.cursor()
    cur.execute('SELECT COUNT(*), brand FROM products GROUP BY brand ORDER BY brand ASC')
    res = cur.fetchall()
    connect.close()
    return res


def count_brends():
    connect = sql.connect('products.db')
    connect.row_factory = sql.Row
    cur = connect.cursor()
    res = []
    cur.execute('SELECT COUNT(*) AS count FROM products GROUP BY brand ORDER BY brand ASC')
    res += cur.fetchall()
    connect.close()
    print(res)
    return res


def len_classes():
    connect = sql.connect('products.db')
    connect.row_factory = sql.Row
    cur = connect.cursor()
    cur.execute('SELECT COUNT(DISTINCT class) AS class FROM products')
    res = cur.fetchall()
    print(res)
    connect.close()
    return res


def classes():
    connect = sql.connect('products.db')
    connect.row_factory = sql.Row
    cur = connect.cursor()
    cur.execute('SELECT COUNT(*), class FROM products GROUP BY class ORDER BY class ASC')
    res = cur.fetchall()
    connect.close()
    return res


def count_classes():
    connect = sql.connect('products.db')
    connect.row_factory = sql.Row
    cur = connect.cursor()
    res = []
    cur.execute('SELECT COUNT(*) AS count FROM products GROUP BY class ORDER BY class ASC')
    res += cur.fetchall()
    connect.close()
    print(res)
    return res


def new():
    connect = sql.connect('products.db')
    connect.row_factory = sql.Row
    cur = connect.cursor()
    res = []
    cur.execute('SELECT COUNT(new_prds) AS new FROM products WHERE new_prds="1"')
    res += cur.fetchall()
    connect.close()
    return res


@app.route('/')
def main():
    connect = sql.connect('products.db')
    connect.row_factory = sql.Row
    cur = connect.cursor()
    cur.execute('SELECT * FROM products')
    all = cur.fetchall()
    count = len(all)
    if len(all) % 5 != 0:
        count = len(all) + 5
    connect.close()
    return render_template('main.html', inf=all, length=count,
                           length_inf=len(all), min_price=min_price(), max_price=max_price(),
                           length_sale=len(sale()), brends=brends(), len_brends=len_brends(),
                           count_brends=count_brends(), classes=classes(), len_classes=len_classes(),
                           count_classes=count_classes(), new=new())


@app.route('/reviews', methods=['post', 'get'])
def reviews_page():
    msg = False
    connect = sql.connect('reviews.db')
    connect.row_factory = sql.Row
    cur = connect.cursor()
    form = LoginForm()  # добавляем форму
    print(form)
    user = request.form.get('user')
    grade = request.form.get('grade')
    text = request.form.get('text')
    submit = request.form.get('submit')
    cur.execute('SELECT * FROM reviews')
    rows = cur.fetchall()
    date_now = datetime.now()
    if form.validate_on_submit() and request.method == 'POST':  # вместо request.method=='POST' — проверяет, все ли требования модулей проверки выполняются (или же проверяет нажатие кнопки)
        if len(str(date_now.day)) == 1:
            day = '0' + str(date_now.day)
        else:
            day = str(date_now.day)
        if len(str(date_now.month)) == 1:
            month = '0' + str(date_now.month)
        else:
            month = str(date_now.month)
        users = set()
        cur.execute('SELECT user FROM reviews')
        for i in cur.fetchall():
            users.add(i[0])
        print(users, user)
        if user in users:
            msg = 'Вы не можете оставлять сразу 2 отзыва'
        else:
            cur.execute(
                'INSERT INTO reviews (user, grade, description, like, date, dislike) VALUES ("' + user + '","' + str(
                    grade) + '","' + text + '", "0", "' + day
                + '.' + month + '.' + str(date_now.year) + '", 0)')
        connect.commit()
        connect.close()
    return render_template('reviews.html', form=form, datas=rows, msg=msg)


@app.route('/read_reviews', methods=['post', 'get'])
def read_reviews():
    link_background = 'static/empty_like.png'
    connect = sql.connect('reviews.db')
    connect.row_factory = sql.Row
    cur = connect.cursor()
    form2 = LikeForm()
    dislike = request.form.get('dislike')
    cur.execute('SELECT * FROM reviews')
    rows = cur.fetchall()
    print(form2.validate_on_submit(), request.method == 'POST')
    if request.method == 'POST':
        link_background = 'static/full_like.png'
        print(0, request.form.get('self.index'))
    connect.close()
    return render_template('read_reviews.html', form=form2, datas=rows, chng_back=link_background)


@app.route('/registration', methods=['post', 'get'])
def reg():
    form_reg = RegistrationForm()
    user = request.form.get('user')
    password = request.form.get('password')
    submit = request.form.get('submit')
    return render_template('registration.html', form=form_reg)


app.config['SECRET_KEY'] = 'you_cant_guess_this_key'

# @app.route('/products_for_dogs')
# def dog():
#     connect = sql.connect('products.db')
#     connect.row_factory = sql.Row
#     cur = connect.cursor()
#     cur.execute('SELECT * FROM products')
#     all = cur.fetchall()
#     cur1 = connect.cursor()
#     cur1.execute('SELECT MIN(price) FROM products')
#     min = cur1.fetchall()
#     cur2 = connect.cursor()
#     cur2.execute('SELECT MAX(price) FROM products')
#     max = cur2.fetchall()
#     print(min, max, all)
#     count = len(all)
#     if len(all) % 5 != 0:
#         count = len(all) + 5
#     return render_template('dogs.html', inf=all, length=count, length_inf=len(all), min_price=min, max_price=max)
#
#
# @app.route('/products_for_cats')
# def cat():
#     connect = sql.connect('products.db')
#     connect.row_factory = sql.Row
#     cur = connect.cursor()
#     cur.execute('''SELECT * FROM products
#                     SELECT MIN(price) FROM products
#                     SELECT MAX(price) FROM products
#                     SELECT 1 FROM products WHERE sale = "1"''')
#     all = cur.fetchall()
#     print(all)
#     print(len(all))
#     count = len(all)
#     if len(all) % 5 != 0:
#         count = len(all) + 5
#     return render_template('cats.html', inf=all, length=count, length_inf=len(all), min_price=min, max_price=max)


if __name__ == '__main__':
    app.secret_key = 'admin123'
    app.run(debug=True)
