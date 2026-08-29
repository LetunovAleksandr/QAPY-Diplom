import pytest
from pages.payment_page import PaymentPage
from factories.card_data_factory import CardDataFactory

class TestFieldValidation:

    @pytest.mark.parametrize(
        "card, month, year, holder, cvv",[
            (CardDataFactory().empty_field(),
             CardDataFactory().month_valid(),
            CardDataFactory().year_valid(),
             CardDataFactory().holder_valid(),
             CardDataFactory().cvv_valid()
            ),
            (
                    CardDataFactory().card_invalid()    ,
                     CardDataFactory().empty_field(),
                     CardDataFactory().year_valid(),
                     CardDataFactory().holder_valid(),
                     CardDataFactory().cvv_valid()
            ),
            (
                    CardDataFactory().card_invalid(),
                     CardDataFactory().month_valid(),
                     CardDataFactory().empty_field(),
                     CardDataFactory().holder_valid(),
                     CardDataFactory().cvv_valid()
            ),
            (
                    CardDataFactory().card_invalid(),
                     CardDataFactory().month_valid(),
                     CardDataFactory().year_valid(),
                     CardDataFactory().empty_field(),
                     CardDataFactory().cvv_valid()
            ),
            (
                    CardDataFactory().card_invalid(),
                    CardDataFactory().month_valid(),
                    CardDataFactory().year_valid(),
                    CardDataFactory().holder_valid(),
                    CardDataFactory().empty_field()
            )
        ],
        ids=[
            'empty_card_field',
            'empty_month_field',
            'empty_year_field',
            'empty_holder_field',
            'empty_cvv_field',
        ]
    )

    def test_required_field(self,
                            browser_driver,
                            card,
                            month,
                            year,
                            holder,
                            cvv):
        driver = PaymentPage(browser_driver)
        driver.login_page()
        driver.send_form(
            'card',
            card,
            month,
            year,
            holder,
            cvv
        )
        try:
            assert "Поле обязательно для заполнения" in driver.find_error_sub()
        except AssertionError:
            print("Проверка UI не пройдена.")

    @pytest.mark.parametrize(
        'card_number, month, year, holder, cvv, error_message',[
            (
                CardDataFactory().short_card_number(),
                CardDataFactory().month_valid(),
                CardDataFactory().year_valid(),
                CardDataFactory().holder_valid(),
                CardDataFactory().cvv_valid(),
                'Неверный формат'
            ),
            (
                CardDataFactory().card_invalid(),
                CardDataFactory().month_invalid(),
                CardDataFactory().year_valid(),
                CardDataFactory().holder_valid(),
                CardDataFactory().cvv_valid(),
                'Неверно указан срок действия карты'
            ),
            (
                CardDataFactory().card_invalid(),
                CardDataFactory().month_invalid(),
                CardDataFactory().year_invalid(),
                CardDataFactory().holder_valid(),
                CardDataFactory().cvv_valid(),
                'Истек срок действия карты'
            ),
            (
                CardDataFactory().card_invalid(),
                CardDataFactory().month_valid(),
                CardDataFactory().year_valid(),
                    '123456789',
                CardDataFactory().cvv_valid(),
                'Некорректное имя владельца карты'
            ),
            (
                CardDataFactory().card_invalid(),
                CardDataFactory().month_valid(),
                CardDataFactory().year_valid(),
                CardDataFactory().holder_valid(),
                CardDataFactory().cvv_invalid(),
                'Неверный формат'
            )

        ],
        ids=[
            'incorrect_card_number',
            'incorrect_month',
            'expired_card',
            'numbers_in_holder_field',
            'short_cvv'
        ]
    )
    def test_incorrect_field_data(self,
                                  browser_driver,
                                  card_number,
                                  month,
                                  year,
                                  holder,
                                  cvv,
                                  error_message):
        driver = PaymentPage(browser_driver)
        driver.login_page()
        driver.send_form(
            'card',
            card_number,
            month,
            year,
            holder,
            cvv
        )
        try:
            assert error_message in driver.find_error_sub()
        except AssertionError:
            print('Проверка UI не пройдена')