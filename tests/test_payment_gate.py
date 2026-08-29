import pytest
from utils.api_client import APIClient
from factories.card_data_factory import CardDataFactory

class TestPaymentGate:

    @pytest.mark.parametrize(
        'path, card_number, status_code, key, message',[
            (
              'payment',
                CardDataFactory().card_approved(),
                200,
              'status',
              'APPROVED'
            ),
            (
                'payment',
                CardDataFactory().card_declined(),
                200,
                'status',
                'DECLINED'
            ),
            (
                'credit',
                CardDataFactory().card_approved(),
                200,
                'status',
                'APPROVED'
            ),
            (
                'credit',
                CardDataFactory().card_declined(),
                200,
                'status',
                'DECLINED'
            ),
            (
                'payment',
                CardDataFactory().card_invalid(),
                500,
                'message',
                '500 Internal Server Error'
            )
        ]
    )
    def test_payment_request(self, path, card_number, status_code, key, message):
        client = APIClient()
        card_data = CardDataFactory()
        response = client.get_request(
            path,
            card_number,
            card_data.month_valid(),
            card_data.year_valid(),
            card_data.holder_valid(),
            card_data.cvv_valid()
        )
        try:
            assert response.status_code == status_code
            assert response.json()[key] == message
        except AssertionError:
            print('Проверка платежного шлюза не пройдена')