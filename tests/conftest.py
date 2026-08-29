import pytest
from  selenium import webdriver
import pymysql


@pytest.fixture
def browser_driver(request):
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
def clean_db(db_driver):
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