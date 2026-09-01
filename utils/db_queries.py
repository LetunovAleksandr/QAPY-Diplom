import allure

class Database:

    @allure.step('Получить ID последней записи в БД')
    def get_last_entry(self, cursor, table_name):
        cursor.execute(
            f'SELECT id, created FROM {table_name} ORDER BY created DESC LIMIT 1'
        )
        return cursor.fetchone()[0]

    @allure.step('Получить информацию последней записи в БД')
    def get_data_entry(self, cursor, query, id):
        cursor.execute(query, id)
        return cursor.fetchone()


