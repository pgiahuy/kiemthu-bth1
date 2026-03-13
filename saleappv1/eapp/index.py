from flask import render_template, request, redirect, jsonify, session

from eapp import app, dao, login, utils
from flask_login import login_user, logout_user, current_user, login_required
import math
from eapp.dao import add_user


@app.route('/')
def index():
    products = dao.load_products(cate_id=request.args.get('category_id'),
                                 kw=request.args.get('kw'),
                                 page=int(request.args.get('page', 1)))

    return render_template('index.html', products=products,
                           pages=math.ceil(dao.count_products()/app.config['PAGE_SIZE']))


@app.route('/login')
def login_view():
    return render_template('login.html')


@app.route('/register')
def register_view():
    return render_template('register.html')

@app.route('/register', methods=['post'])
def register_process():
    data = request.form

    password = data.get('password')
    confirm = data.get('confirm')
    if password != confirm:
        err_msg = 'Mật khẩu không khớp!'
        return render_template('register.html', err_msg=err_msg)

    try:
        add_user(name=data.get('name'), username=data.get('username'), password=password, avatar=request.files.get('avatar'))
        return redirect('/login')
    except Exception as ex:
        return render_template('register.html', err_msg=str(ex))



@app.route('/logout')
def logout_process():
    logout_user()
    return redirect('/login')


@app.route('/login', methods=['post'])
def login_process():
    username = request.form.get('username')
    password = request.form.get('password')

    user = dao.auth_user(username=username, password=password)
    if user:
        login_user(user=user)

    next = request.args.get('next')
    return redirect(next if next else '/')

@app.route('/api/carts', methods=['post'])
def add_to_cart():
    '''
        {
            "1", {
                "id": "1",
                "name": "aaaa",
                "price": 123,
                "quantity": 2
            }, "2", {
                "id": "2",
                "name": "aaaa",
                "price": 123,
                "quantity": 1
            }
        }
    '''
    # print(request.json)
    cart = session.get('cart')
    if not cart:
        cart = {}

    id = str(request.json.get('id'))

    if id in cart:
        cart[id]["quantity"] += 1
    else:
        name = request.json.get('name')
        price = request.json.get('price')
        cart[id] = {
            "id": id,
            "name": name,
            "price": price,
            "quantity": 1
        }

    session['cart'] = cart

    return jsonify(utils.stats_cart(cart))

@app.route('/api/carts/<id>', methods=['put'])
def update_to_cart(id):
    cart = session.get('cart')

    if cart and id in cart:
        cart[id]["quantity"] = int(request.json.get("quantity"))

    session['cart'] = cart

    return jsonify(utils.stats_cart(cart))


@app.route('/api/carts/<id>', methods=['delete'])
def delete_to_cart(id):
    cart = session.get('cart')

    if cart and id in cart:
        del cart[id]

    session['cart'] = cart

    return jsonify(utils.stats_cart(cart))


@app.route('/api/pay', methods=['post'])
@login_required
def pay():
    try:
        dao.add_receipt(cart=session.get('cart'))
        del session['cart']

        return jsonify({'status': 200})
    except Exception as ex:
        return jsonify({'status': 400, 'err_msg': str(ex)})


@app.route('/cart')
def cart_view():
    return render_template('cart.html')


@app.context_processor
def common_responses():
    return {
        'categories': dao.load_categories(),
        'cart_stats': utils.stats_cart(session.get('cart'))
    }

@login.user_loader
def load_user(id):
    return dao.get_user_by_id(id)


if __name__ == '__main__':
    from eapp import admin
    app.run(debug=True)
