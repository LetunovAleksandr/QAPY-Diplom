import pytest
from  selenium import webdriver
import pymysql
import allure


@pytest.fixture
def browser_driver(request):
    with allure.step('Подключить браузер'):
        browser = request.config.getoption("--browser")
        if browser == "chrome":
            driver = webdriver.Chrome()
        elif browser == "firefox":
            driver = webdriver.Firefox()
        elif browser == "safari":
            driver = webdriver.Safari()
        elif browser == "edge":
            driver = webdriver.Edge()
        else:
            raise ValueError(f"Браузер не поддерживается: {browser}")

    yield driver
    driver.quit()

def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Browser: chrome, firefox, safari, edge"
    )
@pytest.fixture
def db_driver():
    with allure.step('Подключиться к базе данных'):
        connection = pymysql.connect(
            host="localhost",
            port=3306,
            user="app",
            password="pass",
            db="app",
            charset="utf8"
        )
        cursor = connection.cursor()
    yield cursor, connection
    cursor.close()
    connection.close()

@pytest.fixture
def card_data():
    with allure.step('Подготовка валидных тестовых данных'):
        card_data = {
            'card' : '',
            'month' : '12',
            'year' : '31',
            'holder' : 'Ivan Ivanov',
            'cvc' : '999'
        }
    return card_data

@pytest.fixture
def clean_db(db_driver):
    with allure.step('Удалить тестовые данные из БД'):
        cursor, connection = db_driver
        ids = {
            'payment_entity': None,
            'order_entity': None,
            'credit_request_entity': None,
        }
    yield ids
    if ids['payment_entity']:
        cursor.execute(
            'DELETE FROM payment_entity WHERE id = %s',
            (ids['payment_entity'],)
        )

    if ids['order_entity']:
        cursor.execute(
            'DELETE FROM order_entity WHERE id = %s',
            (ids['order_entity'],)
        )

    if ids['credit_request_entity']:
        cursor.execute(
            'DELETE FROM credit_request_entity WHERE id = %s',
            (ids['credit_request_entity'],)
        )

    connection.commit()
