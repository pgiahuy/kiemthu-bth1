import hashlib

from eapp.dao import add_user
from eapp.models import User
import pytest
from eapp.test.test_base import test_session, test_app, create_app, mock_cloudinary


def test_register_success(test_session):
    add_user(name="abc", username="giahuy", password="aA1234567", avatar=None)
    u = User.query.filter(User.username.__eq__("giahuy")).first()
    assert u
    assert u.name == "abc"
    assert u.password == str(hashlib.md5('aA1234567'.encode('utf-8')).hexdigest())

def test_register_invalid_existed(test_session):
    add_user(name="abc", username="giahuy", password="aA1234567", avatar=None)
    with pytest.raises(ValueError):
        add_user(name="abc", username="giahuy", password="aA1234567", avatar=None)

def test_register_active(test_session):
    add_user(name="abc", username="giahuy", password="aA1234567", avatar=None)
    u = User.query.filter(User.username.__eq__("giahuy")).first()
    assert u.active == True

def test_register_invalid_username(test_session):
    with pytest.raises(ValueError):
        add_user(name="abc", username="gi", password="aA1234567", avatar=None)


@pytest.mark.parametrize('password',[
    '1aB', '1'*8, 'a'*8, 'A'*8, 'a1'*4, 'A1'*8, 'Aa'*8
])

def test_invalid_password(password,test_session):
    with  pytest.raises(ValueError):
        add_user(name="abc", username="gi", password=password, avatar=None)

def test_register_invalid_pw_1(test_session):
    with pytest.raises(ValueError):
        add_user(name="abc", username="giahuy", password="aa", avatar=None)

def test_register_invalid_pw_2(test_session):
    with pytest.raises(ValueError):
        add_user(name="abc", username="giahuy", password="aa1234567", avatar=None)

def test_register_invalid_pw_3(test_session):
    with pytest.raises(ValueError):
        add_user(name="abc", username="giahuy", password="AA1234567", avatar=None)

def test_register_invalid_pw_4(test_session):
    with pytest.raises(ValueError):
        add_user(name="abc", username="giahuy", password="1231234567", avatar=None)

def test_register_invalid_pw_5(test_session):
    with pytest.raises(ValueError):
        add_user(name="abc", username="giahuy", password="asdfghjklwerty", avatar=None)




def test_register_invalid_long_name(test_session):
    add_user(name="abc"*100, username="giahuy", password="aA1234567", avatar=None)


def test_avatar(test_session, mock_cloudinary):
    add_user(name="abc", username="giahuy", password="aA1234567", avatar="aaaaaa")
    u = User.query.filter(User.username.__eq__("giahuy")).first()
    assert u.avatar == 'https://img.png'