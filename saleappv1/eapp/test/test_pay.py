from pytest_mock import mocker


from eapp.models import User, Product, Receipt, ReceiptDetails
from eapp.test.test_base import test_client, test_app, test_session


def test_pay_success(test_client, mocker):
    class FakeUser:
        is_authenticated = True

    mocker.patch('flask_login.utils._get_user', return_value = FakeUser())

    mocker.patch('eapp.dao.current_user', new = FakeUser())

    with test_client.session_transaction() as sess:
        sess['cart'] = {
            "1" : {
                "id" : 1,
                "name": "Iphone 19",
                "price" : 5000,
                "quantity": 3
            }
        }
    mock_add = mocker.patch('eapp.dao.add_receipt')

    res = test_client.post('api/pay')

    assert res.status_code == 200
    assert res.get_json()['status'] == 200

    with test_client.session_transaction() as sess:
        assert 'cart' not in sess

    mock_add.assert_called_once()

def test_pay_failure(test_client,mocker):
    class FakeUser:
        is_authenticated = True

    mocker.patch('flask_login.utils._get_user', return_value=FakeUser())
    mocker.patch('eapp.dao.current_user', new=FakeUser())
    with test_client.session_transaction() as sess:
        sess['cart'] = {
            "1": {
                "id": 1,
                "name": "Iphone 19",
                "price": 5000,
                "quantity": 3
            }
        }
    mock_add = mocker.patch('eapp.dao.add_receipt', side_effect = Exception("Bug"))
    res = test_client.post('api/pay')

    assert res.status_code == 200

    assert res.get_json()['status'] == 400
    assert 'Bug' in res.get_json()['err_msg']

    with test_client.session_transaction() as sess:
        assert 'cart' in sess

    mock_add.assert_called_once()


def test_all(test_client,test_session, mocker):
    class FakeUser:
        is_authenticated = True

    mocker.patch('flask_login.utils._get_user', return_value=FakeUser())

    u = User(name='a', username='demo', password='123')
    test_session.add(u)

    p = Product(name="Iphone", price=500, category_id=1)
    test_session.add(p)
    test_session.commit()

    mocker.patch('eapp.dao.current_user', u)

    test_client.post('api/carts', json={
        'id': 1,
        'name': 'Iphone 17',
        'price': 5000
    })
    test_client.post('api/carts', json={
        'id': 1,
        'name': 'Iphone 17',
        'price': 5000
    })
    res = test_client.post('api/pay')

    assert res.status_code ==200

    with test_client.session_transaction() as sess:
        assert 'cart' not in sess

    assert Receipt.query.count() == 1
    assert ReceiptDetails.query.count() == 1

    d = ReceiptDetails.query.first()

    assert d.product_id == 1
    assert d.quantity == 2
