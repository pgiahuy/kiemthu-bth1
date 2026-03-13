from eapp.dao import load_products
import pytest

from eapp.models import Product
from eapp.test.test_base import test_session, test_app


@pytest.fixture
def sample_products(test_session):
    #1
    p1 = Product(name="Iphone 17", price=309, category_id=2)
    p2 = Product(name="SamSung 33", price=350, category_id=1)

    #2
    p3 = Product(name="Iphone 17", price=130, category_id=1)
    p4 = Product(name="SamSung Galaxy", price=30, category_id=2)

    test_session.add_all([p1, p2, p3, p4])
    test_session.commit()
    return [p1,p2,p3,p4]

def test_all(sample_products):
    actual_products = load_products()
    assert len(actual_products) == len (sample_products)

def test_kw(sample_products):
    actual_products = load_products(kw="Iphone")
    assert len(actual_products) == 2
    assert all("Iphone" in p.name for p in actual_products)

def test_kw_none(sample_products):
    actual_products = load_products(kw="Oppo")
    assert len(actual_products) == 0

def test_cate(sample_products):
    actual_products = load_products(cate_id=1)
    assert len(actual_products) == 2
    assert all(p.category_id == 1 for p in actual_products)

def test_cate_none(sample_products):
    actual_products = load_products(cate_id=3)
    assert len(actual_products) == 0

def test_page(sample_products):
    actual_products = load_products(page=1)
    assert len(actual_products) == 2
    assert "Iphone 17" in actual_products[0].name
    assert "SamSung 33" in actual_products[1].name

def test_page_none(sample_products):
    actual_products = load_products(page=5)
    assert len(actual_products) == 0

#####

def test_kw_cate(sample_products):
    actual_products = load_products(cate_id=1, kw="Iphone")
    assert len(actual_products) == 1
    assert all(p.category_id == 1 and "Iphone" in p.name for p in actual_products)

def test_kw_page(test_app,sample_products):
    actual_products = load_products(kw="n", page=2)
    assert len(actual_products) == 2

def test_cate_page(test_app,sample_products):
    actual_products = load_products(cate_id=2,page=1)
    assert len(actual_products) == 2
    assert "17" in actual_products[0].name
    assert "Ga" in actual_products[1].name

####

def test_kw_cate_page(test_app,sample_products):
    kw = "Iphone"
    actual_products = load_products(cate_id=1,kw=kw,page=1)
    assert len(actual_products) == 1
    assert all(kw in p.name and p.category_id == 1 for p in actual_products)

def test_kw_cate_page_2(test_app,sample_products):
    kw = "SamSung"
    actual_products = load_products(cate_id=1,kw=kw,page=1)
    assert len(actual_products) == 1
    assert all(kw in p.name and p.category_id == 1 for p in actual_products)

def test_kw_cate_page_none( test_app,sample_products):
    kw = "Iphone"
    actual_products = load_products(cate_id=1,kw=kw,page=2)
    assert len(actual_products) == 0

