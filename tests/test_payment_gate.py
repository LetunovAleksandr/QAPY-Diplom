import allure
import pytest

from tests.conftest import card_data
from utils.api_client import APIClient
from utils.helper import assert_status_code, assert_response

@allure.feature('Платежный шлюз')
class TestPaymentGate:
    @allure.title('Проверка обработки успешного запроса и отказа')
    @pytest.mark.parametrize(
        'path, card_number, status_code, key, message',[
            (
              'pay',
                '4444 4444 4444 4441',
                200,
              'status',
              'APPROVED'
            ),
            (
                'pay',
                '4444 4444 4444 4442',
                200,
                'status',
                'DECLINED'
            ),
            (
                'credit',
                '4444 4444 4444 4441',
                200,
                'status',
                'APPROVED'
            ),
            (
                'credit',
                '4444 4444 4444 4442',
                200,
                'status',
                'DECLINED'
            ),
            (
                'pay',
                '4444 4444 4444 4443',
                500,
                'message',
                '500 Internal Server Error'
            )
        ]
    )

    def test_payment_request(self, card_data, path, card_number, status_code, key, message):
        client = APIClient()
        card = card_data
        response = client.get_request(
            path,
            card_number,
            card['month'],
            card['year'],
            card['holder'],
            card['cvc']
        )
        assert_status_code(response, status_code)
        assert_response(response, key, message)
