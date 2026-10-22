import allure
import pytest
import requests

from tests.conftest import card_data
from utils.api_client import APIClient
from utils.helper import assert_status_code, assert_response

@allure.feature('API запросы к платежному шлюзу')
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
            ),
            (
                    'credit',
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

    @allure.title("Негативные проверки даты выпуска карты")
    @pytest.mark.parametrize(
        'path, month, year',[
            ('pay','08', '21'),
            ('credit', '08', '21'),
            ('pay', '08', '26'),
            ('credit', '08', '26'),
            ('pay', '', '31'),
            ('credit', '', '31'),
            ('credit', '12', ''),
            ('pay', '12', ''),
            ('credit', '', ''),
            ('pay', '', ''),
            ('credit', 'abc', '31'),
            ('pay', 'abc', '31'),
            ('credit', '12', 'dfg'),
            ('pay', '12', 'dfg'),
            ('credit', 'abc', 'dfg'),
            ('pay', 'abc', 'dfg'),
            ('credit', '!@#', '31'),
            ('pay', '!@#', '31'),
            ('credit', '12', '!@#'),
            ('pay', '12', '!@#'),
            ('credit', '!@#', '!@#'),
            ('pay', '!@#', '!@#'),
            ('credit', '122', '31'),
            ('pay', '122', '31'),
            ('credit', '12', '311'),
            ('pay', '12', '311'),
        ]
    )
    def test_negative_with_invalid_release_date(self,card_data, path, month, year):
        client = APIClient()
        card = card_data
        response = client.get_request(
            path,
            card['card'],
            month,
            year,
            card['holder'],
            card['cvc']
        )
        assert_status_code(response, 400)
        assert_response(response, 'error', 'Bad Request')

    @allure.title('Негативные проверки поля "Владелец"')
    @pytest.mark.parametrize(
        'path, holder',[
            ('pay', ''),
            ('credit', ''),
            ('pay', '12345'),
            ('credit', '12345'),
            ('pay', '!@#$$'),
            ('credit', '!@#$$'),
            ('pay', 'Иван Иванов'),
            ('credit', 'Иван Иванов'),
            ('pay', 'Иван'),
            ('credit', 'Иван'),
            ('pay', "Ivan"),
            ('credit', 'Ivan'),
        ]
    )
    def test_negative_with_invalid_holder_data(self,card_data, path, holder):
        client = APIClient()
        card = card_data
        response = client.get_request(
            path,
            card['card'],
            card['month'],
            card['year'],
            holder,
            card['cvc']
        )
        assert_status_code(response, 400)
        assert_response(response, 'error', 'Bad Request')

    @allure.title('Негативная проверка поля "CVC"')
    @pytest.mark.parametrize(
        'path, cvc',[
            ('pay', ''),
            ('credit', ''),
            ('pay', '9'),
            ('credit', '9'),
            ('pay', '99'),
            ('credit', '99'),
            ('pay', '9999'),
            ('credit', '9999'),
            ('pay', 'abc'),
            ('credit', 'abc'),
            ('pay', '!@#$'),
            ('credit', '!@#$'),
        ]
    )
    def test_negative_with_invalid_cvc(self,card_data, path, cvc):
        client = APIClient()
        card = card_data
        response = client.get_request(
            path,
            card['card'],
            card['month'],
            card['year'],
            card['holder'],
            cvc
        )
        assert_status_code(response, 400)
        assert_response(response, 'error', 'Bad Request')

    @allure.title('Неверный HTTP-метод в запросе')
    @pytest.mark.parametrize(
        'method', ['credit', 'pay']
    )
    def test_request_with_incorrect_http_method(self,card_data, method):
        client = APIClient()
        card = card_data
        response = requests.put(f'{client.BASE_URL}/{method}', json=card)

        assert_status_code(response, 405)
        assert_response(response, 'error', 'Method Not Allowed')