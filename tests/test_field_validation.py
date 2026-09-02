import allure
import pytest
from pages.payment_page import PaymentPage
from utils.helper import assert_ui

@allure.feature('Форма оплаты банковской картой')
class TestFieldValidation:
    @allure.title('Проверка обязательных полей ввода данных')
    @pytest.mark.parametrize(
        "card, month, year, holder, cvv",[
            ('', '12', '31', 'Ivan Ivanov','999'),
            ('4444 4444 4444 4444', '', '31', 'Ivan Ivanov', '999' ),
            ('4444 4444 4444 4444', '12', '', 'Ivan Ivanov', '999' ),
            ('4444 4444 4444 4444', '12', '31', '', '999'),
            ('4444 4444 4444 4444', '12', '31', 'Ivan Ivanov', ''),
        ],
        ids=[
            'empty_card_field',
            'empty_month_field',
            'empty_year_field',
            'empty_holder_field',
            'empty_cvv_field',
        ]
    )

    def test_required_field(self, browser_driver, card, month,
                            year, holder, cvv):
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
        assert driver.error_displayed()

    @allure.title('Негативная проверка поля "Номер карты"')
    @pytest.mark.parametrize(
    "field, card, month, year, holder, cvc, expected_message", [
            ('card','123', '12', '31', 'Ivan Ivanov', '999', 'Неверный формат'),
            ('month','4444 4444 4444 4444', '01', '26', 'Ivan Ivanov', '999', 'Неверно указан срок действия карты' ),
            ('year', '4444 4444 4444 4444', '12', '20', 'Ivan Ivanov', '999', 'Истёк срок действия карты'),
            ('holder', '4444 4444 4444 4444', '12', '31', '123456789', '999','Некорректное имя владельца карты'),
            ('cvc', '4444 4444 4444 4444', '12', '31', 'Ivan Ivanov', '99', 'Неверный формат'),
        ],
        ids=[
            'Некорректный номер карты',
            'Некорректный месяц',
            'Истекший срок действия карты',
            'Цифры в поле "Владелец"',
            'Короткий cvv'
        ]
    )
    def test_incorrect_field_data(self,
                                  browser_driver,
                                  field,
                                  card,
                                  month,
                                  year,
                                  holder,
                                  cvc,
                                  expected_message):
        driver = PaymentPage(browser_driver)
        driver.login_page()
        driver.send_form(
            'card',
            card,
            month,
            year,
            holder,
            cvc
        )
        notification = driver.find_field_error(field)
        assert_ui(expected_message, notification)
