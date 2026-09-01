import json
import allure

def assert_ui(expected, actual):
    with allure.step(f'Проверить отображение уведомления'):
        allure.attach(f'Ожидаемый текст: {expected}. Фактический текст: {actual}', name='notification',
                      attachment_type=allure.attachment_type.TEXT)
        assert expected in actual


@allure.step(f'Проверить запись статуса в БД')
def assert_status_in_db(status, table_data):
    allure.attach(f'Фактическая запись: {table_data}', name='status',
                    attachment_type=allure.attachment_type.TEXT)
    assert status == table_data


def assert_record_operation_db(table_1, table_2):
    with allure.step(
            f'Проверить запись id заказа в соответствующих столбцах таблиц.'
            f'Таблица заказов: {table_1}. Таблица способа оплаты: {table_2}'
    ):
        allure.attach(f'{table_1}, {table_2}', name='operations id',
                      attachment_type=allure.attachment_type.TEXT)
        assert table_1 == table_2


@allure.step('Проверить запись стоимости тура в БД')
def assert_amount(amount, expected):

    allure.attach(f'Ожидаемая запись в БД: {expected}. Фактическая запись в БД: {amount}.', name='amount',
                    attachment_type=allure.attachment_type.TEXT)
    assert expected == amount


@allure.step('Проверка статус кода ответа сервера')
def assert_status_code(response, status_code):
    allure.attach(f'Ожидаемый статус код: {response.status_code}. Фактический статус код: {status_code}. ',
                  name='status_code',
                  attachment_type=allure.attachment_type.TEXT)
    assert response.status_code == status_code


@allure.step('Проверка ответа сервера')
def assert_response(response, key, message):
    allure.attach(
        json.dumps(response.json(), indent=4, ensure_ascii=False),
        name='Ответ сервера',
        attachment_type=allure.attachment_type.JSON
    )
    assert response.json()[key] == message
