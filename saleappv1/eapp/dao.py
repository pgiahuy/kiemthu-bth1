from sqlalchemy.exc import IntegrityError

from eapp.models import Category, Product, User, Receipt, ReceiptDetails
import hashlib
from eapp import app, db
import cloudinary.uploader
from flask_login import current_user
from sqlalchemy import func
from datetime import datetime


def load_categories():
    return Category.query.all()

def load_products(cate_id=None, kw=None, page=1):
    query = Product.query

    if kw:
        query = query.filter(Product.name.contains(kw))

    if cate_id:
        query = query.filter(Product.category_id.__eq__(cate_id))

    if page:
        start = (page - 1) * app.config['PAGE_SIZE']
        query = query.slice(start, start + app.config['PAGE_SIZE'])

    return query.all()


def count_products():
    return Product.query.count()


def get_user_by_id(id):
    return User.query.get(id)

def auth_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    return User.query.filter(User.username==username,
                             User.password==password).first()

def add_user(name, username, password, avatar):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    u = User(name=name.strip(), username=username.strip(), password=password)
    if avatar:
        res = cloudinary.uploader.upload(avatar)
        u.avatar = res.get("secure_url")

    db.session.add(u)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise Exception('Username đã tồn tại!')


def add_receipt(cart):
    if cart:
        r = Receipt(user=current_user)
        db.session.add(r)

        for c in cart.values():
            d = ReceiptDetails(quantity=c['quantity'], price=c['price'], product_id=c['id'], receipt=r)
            db.session.add(d)

        db.session.commit()


def revenue_by_product(kw=None):
    query = (db.session.query(Product.id, Product.name, func.sum(ReceiptDetails.quantity * ReceiptDetails.price))
             .join(ReceiptDetails, ReceiptDetails.product_id==Product.id, isouter=True))

    if kw:
        query = query.filter(Product.name.contains(kw))

    return query.group_by(Product.id).all()


def revenue_by_time(time="month", year=datetime.now().year):
    query = (db.session.query(func.extract(time, Receipt.created_date), func.sum(ReceiptDetails.quantity * ReceiptDetails.price))
             .join(ReceiptDetails, ReceiptDetails.receipt_id==Receipt.id)).filter(func.extract('year', Receipt.created_date)==year)

    return query.group_by(func.extract(time, Receipt.created_date)).all()


def count_product_by_cate():
    return (db.session.query(Category.id, Category.name, func.count(Product.id))
            .join(Product, Product.category_id==Category.id, isouter=True).group_by(Category.id).all())


if __name__ == '__main__':
    with app.app_context():
        print(count_product_by_cate())

