from pytest_mock import mocker

from eapp.test.test_base import test_client, test_app


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

    mock_add.assert_called_once()
