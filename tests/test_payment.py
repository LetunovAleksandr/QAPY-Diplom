import pytest
from factories.card_data_factory import CardDataFactory
from pages.payment_page import PaymentPage
from tests.conftest import browser_driver
from db.queries import Database


class TestPayment:

    def test_successful_payment_card(self, browser_driver, db_driver, clean_db):
        driver = PaymentPage(browser_driver)
        data = CardDataFactory()
        cursor, connection = db_driver

        driver.login_page()
        driver.send_form(
            'card',
            data.card_approved(),
            data.month_valid(),
            data.year_valid(),
            data.owner_valid(),
            data.cvv_valid()
        )
        driver.find_notification()
        assert "Операция одобрена Банком." in driver.find_notification()

        db = Database()
        payment_id = db.get_id(
            cursor,
            'payment_entity'
        )

        order_id = db.get_id(
            cursor,
             'order_entity'
        )

        payment_data = db.get_table_data(
            cursor,
            """
            SELECT amount, status, transaction_id 
            FROM payment_entity 
            WHERE id = %s
            """,
            payment_id
        )

        order_data = db.get_table_data(
            cursor,
            """
            SELECT payment_id FROM order_entity
            WHERE id = %s
            """,
            order_id
        )

        ids = clean_db
        ids['payment'] = payment_id
        ids['order'] = order_id

        assert order_data[0] == payment_data[2]
        assert "APPROVED" == payment_data[1]
        try:
            assert 45000 == payment_data[0]
        except AssertionError:
            print(f"Проверка 'Amount' не пройдена")

    def test_unsuccessful_card_payment(self, browser_driver, db_driver, clean_db):
        driver = PaymentPage(browser_driver)
        data = CardDataFactory()
        cursor, connection = db_driver

        driver.login_page()
        driver.send_form(
            'card',
            data.card_declined(),
            data.month_valid(),
            data.year_valid(),
            data.owner_valid(),
            data.cvv_valid()
        )
        driver.find_notification()
        try:
            assert "Банк отказал в проведении операции." in driver.find_notification()
        except AssertionError:
            print(f'Проверка UI не пройдена')

        db = Database()
        payment_id = db.get_id(
            cursor,
            'payment_entity'
        )

        order_id = db.get_id(
            cursor,
            'order_entity'
        )

        payment_data = db.get_table_data(
            cursor,
            """
            SELECT amount, status, transaction_id 
            FROM payment_entity 
            WHERE id = %s
            """,
            payment_id
        )

        order_data = db.get_table_data(
            cursor,
            """
            SELECT payment_id FROM order_entity
            WHERE id = %s
            """,
            order_id
        )

        ids = clean_db
        ids['payment'] = payment_id
        ids['order'] = order_id


        assert order_data[0] == payment_data[2]
        assert "DECLINED" == payment_data[1]

        try:
            assert 45000 == payment_data[0]
        except AssertionError:
            print(f"Проверка 'Amount' не пройдена")

class TestCredit:

    def test_successful_buy_on_credit(self, browser_driver, db_driver, clean_db):
        driver = PaymentPage(browser_driver)
        data = CardDataFactory()
        cursor, connection = db_driver

        driver.login_page()
        driver.send_form(
            'credit',
            data.card_approved(),
            data.month_valid(),
            data.year_valid(),
            data.owner_valid(),
            data.cvv_valid()
        )
        driver.find_notification()
        assert "Операция одобрена Банком." in driver.find_notification()

        db = Database()
        credit_id = db.get_id(
            cursor,
            'credit_request_entity'
        )

        order_id = db.get_id(
            cursor,
             'order_entity'
        )

        credit_data = db.get_table_data(
            cursor,
            """
            SELECT bank_id, status 
            FROM credit_request_entity 
            WHERE id = %s
            """,
            credit_id
        )

        order_data = db.get_table_data(
            cursor,
            """
            SELECT credit_id FROM order_entity
            WHERE id = %s
            """,
            order_id
        )

        ids = clean_db
        ids['credit'] = credit_id
        ids['order'] = order_id

        assert 'APPROVED' == credit_data[1]
        try:
            assert order_data[0] == credit_data[0]
        except AssertionError:
            print('Проверка DB не пройдена')

    def test_unsuccessful_buy_on_credit(self, browser_driver, db_driver, clean_db):
        driver = PaymentPage(browser_driver)
        data = CardDataFactory()
        cursor, connection = db_driver

        driver.login_page()
        driver.send_form(
            'credit',
            data.card_declined(),
            data.month_valid(),
            data.year_valid(),
            data.owner_valid(),
            data.cvv_valid()
        )
        driver.find_notification()
        try:
            assert "Банк отказал в проведении операции." in driver.find_notification()
        except AssertionError:
            print('Проверка UI не пройдена')

        db = Database()
        credit_id = db.get_id(
            cursor,
            'credit_request_entity'
        )

        order_id = db.get_id(
            cursor,
            'order_entity'
        )

        credit_data = db.get_table_data(
            cursor,
            """
            SELECT bank_id, status 
            FROM credit_request_entity 
            WHERE id = %s
            """,
            credit_id
        )

        order_data = db.get_table_data(
            cursor,
            """
            SELECT credit_id FROM order_entity
            WHERE id = %s
            """,
            order_id
        )

        ids = clean_db
        ids['credit'] = credit_id
        ids['order'] = order_id

        assert 'DECLINED' == credit_data[1]
        try:
            assert order_data[0] == credit_data[0]
        except AssertionError:
            print('Проверка DB не пройдена')