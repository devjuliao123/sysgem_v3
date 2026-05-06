import logging

class BaseService:
    def __init__(self, db, table_name):
        self.db = db
        self.table_name = table_name

    def get_all(self, schema):
        return self.db.select_dynamic(self.table_name, schema)

    def get_by_id(self, id, schema):
        results = self.db.select_dynamic(self.table_name, schema, filters={'id': id})
        return results[0] if results else None

    def create(self, data, schema):
        # Dynamically filter data based on real columns
        columns = self.db.get_table_columns(self.table_name, schema)
        valid_columns = [col['column_name'] for col in columns if col['column_name'] != 'id']

        filtered_data = {k: v for k, v in data.items() if k in valid_columns}

        # Upper case strings if they are names or observations
        for k, v in filtered_data.items():
            if isinstance(v, str) and (k == 'nome' or k == 'observacao' or k == 'descricao'):
                filtered_data[k] = v.upper()

        return self.db.insert_dynamic(self.table_name, filtered_data, schema)

    def update(self, id, data, schema):
        columns = self.db.get_table_columns(self.table_name, schema)
        valid_columns = [col['column_name'] for col in columns if col['column_name'] != 'id']

        filtered_data = {k: v for k, v in data.items() if k in valid_columns}

        for k, v in filtered_data.items():
            if isinstance(v, str) and (k == 'nome' or k == 'observacao' or k == 'descricao'):
                filtered_data[k] = v.upper()

        return self.db.update_dynamic(self.table_name, id, filtered_data, schema)

    def delete(self, id, schema):
        return self.db.delete_dynamic(self.table_name, id, schema)

    def get_columns(self, schema):
        return self.db.get_table_columns(self.table_name, schema)
