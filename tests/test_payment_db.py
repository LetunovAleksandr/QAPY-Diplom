import allure
import pytest
from pages.payment_page import PaymentPage
from tests.conftest import browser_driver
from utils.db_queries import Database
from utils.helper import assert_ui, assert_status_in_db, assert_amount, assert_record_operation_db


@allure.feature('Покупка тура банковской картой')
class TestPayment:
    @allure.title('Покупка банковской картой: {status}')
    @pytest.mark.parametrize(
        'card_num, message, query_payment, query_order, status',[
            (
                '4444 4444 4444 4441',
                "Операция одобрена Банком.",
                'SELECT amount, status, transaction_id FROM payment_entity WHERE id = %s',
                'SELECT payment_id FROM order_entity WHERE id = %s',
                'APPROVED'
            ),
            (
                    "4444 4444 4444 4442",
                    "Банк отказал в проведении операции.",
                    'SELECT amount, status, transaction_id FROM payment_entity WHERE id = %s',
                    'SELECT payment_id FROM order_entity WHERE id = %s',
                    'DECLINED',
            )
        ],
        ids=[
            'Успешная покупка банковской картой',
            'Отклонение платежа',
        ]
    )
    def test_payment_card(self, browser_driver, db_driver, clean_db, card_data,
                          card_num, message, query_payment, query_order,
                          status
                          ):
        driver = PaymentPage(browser_driver)
        cursor, connection = db_driver
        card = card_data

        driver.login_page()
        driver.send_form(
            'card',
            card_num,
            card['month'],
            card['year'],
            card['holder'],
            card['cvc'],
        )
        ntf = driver.find_notification()
        try:
            assert_ui(message, ntf)
        except AssertionError:
            print("Проверка UI не пройдена")

        db = Database()
        last_payment = db.get_last_entry(cursor, 'payment_entity')

        last_order = db.get_last_entry(cursor, 'order_entity')

        payment_data = db.get_data_entry(cursor, query_payment, last_payment)

        order_data = db.get_data_entry(cursor, query_order, last_order)

        ids = clean_db
        ids['payment_entity'] = last_payment
        ids['order_entity'] = last_order

        assert_record_operation_db(order_data[0], payment_data[2])
        assert_status_in_db(status, payment_data[1])
        assert_amount(payment_data[0], 45000 )

    @allure.title('Покупка тура с невалидным номером карты')
    def test_invalid_card_number(self, browser_driver, card_data):
        driver = PaymentPage(browser_driver)
        card = card_data

        driver.login_page()
        driver.send_form(
            'card',
            '4444 4444 4444 4444',
            card['month'],
            card['year'],
            card['holder'],
            card['cvc'],
        )
        ntf = driver.find_notification()
        driver.close_notification()

        assert_ui('Банк отказал в проведении операции.', ntf)


@allure.feature('Покупка тура картой в кредит')
class TestCredit:
    @allure.title('Покупка в кредит: {status}')
    @pytest.mark.parametrize(
        'card_num, message, query_credit, query_order, status',[
            (
                    '4444 4444 4444 4441',
                    "Операция одобрена Банком.",
                    'SELECT bank_id, status FROM credit_request_entity WHERE id = %s',
                    'SELECT credit_id FROM order_entity WHERE id = %s',
                    'APPROVED'
            ),
            (
                    '4444 4444 4444 4442',
                    "Банк отказал в проведении операции.",
                    'SELECT bank_id, status FROM credit_request_entity WHERE id = %s',
                    'SELECT credit_id FROM order_entity WHERE id = %s',
                    'DECLINED'
            )
        ],
        ids=[
            'Успешная покупка в кредит',
            'Отклонение заявки на кредит',
        ]
    )
    def test_buy_on_credit(self, browser_driver, db_driver, clean_db, card_data,
                           card_num, message, query_credit, query_order,
                           status
                           ):
        driver = PaymentPage(browser_driver)
        cursor, connection = db_driver
        card = card_data

        driver.login_page()
        driver.send_form(
            'credit',
            card_num,
            card['month'],
            card['year'],
            card['holder'],
            card['cvc']
        )
        ntf = driver.find_notification()
        try:
            assert_ui(message, ntf)
        except AssertionError:
            print("Проверка UI не пройдена")

        db = Database()
        last_credit = db.get_last_entry(cursor, 'credit_request_entity')

        last_order = db.get_last_entry(cursor, 'order_entity')

        credit_data = db.get_data_entry(cursor, query_credit, last_credit)

        order_data = db.get_data_entry(cursor, query_order, last_order)

        ids = clean_db
        ids['credit_request_entity'] = last_credit
        ids['order_entity'] = last_order

        assert_status_in_db(status, credit_data[1])
        assert_record_operation_db(order_data[0], credit_data[0])