from eapp.test.test_base import test_client, test_app

def test_add_cart_success(test_client):
    res = test_client.post('api/carts', json={
        'id' : 1,
        'name' : 'Iphone 17',
        'price': 5000
    })

    assert res.status_code == 200

    data = res.get_json()

    assert data['total_quantity'] == 1

    with test_client.session_transaction() as sess:
        assert 'cart' in sess
        assert '1' in sess['cart']


def test_add_increase_quantity(test_client):
    test_client.post('api/carts', json={
        'id': 1,
        'name': 'Iphone 17',
        'price': 5000
    })
    res = test_client.post('api/carts', json={
        'id': 1,
        'name': 'phone 17',
        'price': 5000
    })
    res = test_client.post('api/carts', json={
        'id': 2,
        'name': 'Iphone 11',
        'price': 5000
    })

    data = res.get_json()
    assert res.status_code == 200
    assert data['total_quantity'] == 3

    with test_client.session_transaction() as sess:
        assert sess['cart']['1']['quantity'] == 2
        assert sess['cart']['2']['quantity'] == 1
        assert len(sess['cart']) == 2



def test_delete_cart_success(test_client):
    with test_client.session_transaction() as sess:
        sess['cart'] = {
            "1": {
                "id": 1,
                "name": "Iphone 19",
                "price": 5000,
                "quantity": 1
            },
            "2": {
                "id": 1,
                "name": "Iphone 19",
                "price": 5000,
                "quantity": 4
            }
        }

    res = test_client.delete('api/carts/1')

    assert  res.status_code == 200

    data = res.get_json()

    assert data['total_quantity'] == 4

    with test_client.session_transaction() as sess:
        assert 'cart' in sess
        assert '1' not in sess['cart']
        assert '2' in sess['cart']
        assert len(sess['cart']) == 1


def test_update_cart_success(test_client):
    with test_client.session_transaction() as sess:
        sess['cart'] = {
            "1": {
                "id": 1,
                "name": "Iphone 19",
                "price": 5000,
                "quantity": 5
            },
        }

    with test_client.session_transaction() as sess:
        assert 'Iphone 19' in sess['cart']['1']['name']
        assert sess['cart']['1']['quantity'] == 5

    test_client.put('api/carts/1', json={
        'quantity': 11
    })

    with test_client.session_transaction() as sess:
        assert 'Iphone 19' in sess['cart']['1']['name']
        assert sess['cart']['1']['quantity'] == 11