class Database:
    def get_id(self, cursor, table_name):
        cursor.execute(
            f'SELECT id FROM {table_name} ORDER BY id DESC LIMIT 1'
        )
        return cursor.fetchone()[0]

    def get_table_data(self, cursor, query, id):
        cursor.execute(query, id)
        return cursor.fetchone()


