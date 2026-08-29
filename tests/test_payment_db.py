import pytest
from factories.card_data_factory import CardDataFactory
from pages.payment_page import PaymentPage
from tests.conftest import browser_driver
from utils.db_queries import Database


class TestPayment:
    @pytest.mark.parametrize(
        'payment_method, card, month, year, owner, cvv, message, payment_table, order_table, query_payment, query_order, status, amount ',[
            (
                'card',
                CardDataFactory().card_approved(),
                CardDataFactory().month_valid(),
                CardDataFactory().year_valid(),
                CardDataFactory().holder_valid(),
                CardDataFactory().cvv_valid(),
                "Операция одобрена Банком.",
                'payment_entity',
                'order_entity',
                'SELECT amount, status, transaction_id FROM payment_entity WHERE id = %s',
                'SELECT payment_id FROM order_entity WHERE id = %s',
                'APPROVED',
                45000
            ),
            (
                    'card',
                    CardDataFactory().card_declined(),
                    CardDataFactory().month_valid(),
                    CardDataFactory().year_valid(),
                    CardDataFactory().holder_valid(),
                    CardDataFactory().cvv_valid(),
                    "Банк отказал в проведении операции.",
                    'payment_entity',
                    'order_entity',
                    'SELECT amount, status, transaction_id FROM payment_entity WHERE id = %s',
                    'SELECT payment_id FROM order_entity WHERE id = %s',
                    'DECLINED',
                    45000
            )
        ],
        ids=[
            'card_approved',
            'card_declined',
        ]
    )

    def test_payment_card(self,
                                     browser_driver,
                                     db_driver,
                                     clean_db,
                                     payment_method,
                                     card,
                                     month,
                                     year,
                                     owner,
                                     cvv,
                                     message,
                                     payment_table,
                                     order_table,
                                     query_payment,
                                     query_order,
                                     status,
                                     amount):
        driver = PaymentPage(browser_driver)
        # data = CardDataFactory()
        cursor, connection = db_driver

        driver.login_page()
        driver.send_form(
            payment_method,
            card,
            month,
            year,
            owner,
            cvv
        )
        driver.find_notification()
        try:
            assert message in driver.find_notification()
        except AssertionError:
            print(f'Проверка UI не пройдена')

        db = Database()
        payment_id = db.get_id(
            cursor,
            payment_table
        )

        order_id = db.get_id(
            cursor,
             order_table
        )

        payment_data = db.get_table_data(
            cursor,
            query_payment,
            payment_id
        )

        order_data = db.get_table_data(
            cursor,
            query_order,
            order_id
        )

        ids = clean_db
        ids[payment_table] = payment_id
        ids[order_table] = order_id

        try:
            assert order_data[0] == payment_data[2]
            assert status == payment_data[1]
            assert amount == payment_data[0]
        except AssertionError:
            print(f"Проверка базы данных не пройдена")

class TestCredit:

    @pytest.mark.parametrize(
        'payment_method, card, month, year, owner, cvv, message, credit_table, order_table, query_credit, query_order, status',[
            (
                    'credit',
                    CardDataFactory().card_approved(),
                    CardDataFactory().month_valid(),
                    CardDataFactory().year_valid(),
                    CardDataFactory().holder_valid(),
                    CardDataFactory().cvv_valid(),
                    "Операция одобрена Банком.",
                    'credit_request_entity',
                    'order_entity',
                    'SELECT bank_id, status FROM credit_request_entity WHERE id = %s',
                    'SELECT credit_id FROM order_entity WHERE id = %s',
                    'APPROVED'
            ),
            (
                    'credit',
                    CardDataFactory().card_declined(),
                    CardDataFactory().month_valid(),
                    CardDataFactory().year_valid(),
                    CardDataFactory().holder_valid(),
                    CardDataFactory().cvv_valid(),
                    "Банк отказал в проведении операции.",
                    'credit_request_entity',
                    'order_entity',
                    'SELECT bank_id, status FROM credit_request_entity WHERE id = %s',
                    'SELECT credit_id FROM order_entity WHERE id = %s',
                    'DECLINED'
            )
        ],
        ids=[
            'credit_approved',
            'credit_declined',
        ]
    )
    def test_buy_on_credit(self,
                           browser_driver,
                           db_driver,
                           clean_db,
                           payment_method,
                           card,
                           month,
                           year,
                           owner,
                           cvv,
                           message,
                           credit_table,
                           order_table,
                           query_credit,
                           query_order,
                           status):
        driver = PaymentPage(browser_driver)
        # data = CardDataFactory()
        cursor, connection = db_driver

        driver.login_page()
        driver.send_form(
            payment_method,
            card,
            month,
            year,
            owner,
            cvv
        )
        driver.find_notification()
        try:
            assert message in driver.find_notification()
        except AssertionError:
            print('Проверка UI не пройдена')

        db = Database()
        credit_id = db.get_id(
            cursor,
            credit_table
        )

        order_id = db.get_id(
            cursor,
             order_table
        )

        credit_data = db.get_table_data(
            cursor,
            query_credit,
            credit_id
        )

        order_data = db.get_table_data(
            cursor,
            query_order,
            order_id
        )

        ids = clean_db
        ids[credit_table] = credit_id
        ids[order_table] = order_id

        try:
            assert status == credit_data[1]
            assert order_data[0] == credit_data[0]
        except AssertionError:
            print('Проверка DB не пройдена')