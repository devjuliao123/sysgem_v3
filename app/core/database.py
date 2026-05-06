import psycopg2
from psycopg2.extras import RealDictCursor
import logging
import os
import sys

class Database:
    def __init__(self, db_config):
        self.config = db_config
        self.db_name = db_config.get("database", "db_gem")
        try:
            self._ensure_db_exists()
            self._run_migrations()
        except psycopg2.OperationalError as e:
            logging.error("="*50)
            logging.error("ERRO DE CONEXÃO COM O BANCO DE DADOS")
            logging.error(f"Detalhes: {e}")
            logging.error("Verifique se o PostgreSQL está rodando e se a senha em DB_PASSWORD está correta.")
            logging.error("="*50)
            # Do not exit immediately to allow Flask to potentially show error or for testing
            # but in this case, we'll raise it so the user sees the clear message above
            raise e

    def _get_connection(self, dbname=None):
        config = self.config.copy()
        if dbname:
            config["database"] = dbname

        # If password is empty and not provided in env, some PG setups fail
        return psycopg2.connect(**config)

    def _ensure_db_exists(self):
        conn = self._get_connection("postgres")
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (self.db_name,))
        if not cur.fetchone():
            cur.execute(f"CREATE DATABASE {self.db_name}")
        cur.close()
        conn.close()

    def _run_migrations(self):
        conn = self.get_connection()
        cur = conn.cursor()
        try:
            # Create table if not exists
            cur.execute("""
                CREATE TABLE IF NOT EXISTS public.tb_organizacao (
                    id SERIAL PRIMARY KEY,
                    numero INT UNIQUE NOT NULL,
                    nome TEXT NOT NULL,
                    schema TEXT NOT NULL,
                    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Ensure UNIQUE constraint on nome
            cur.execute("""
                DO $$
                BEGIN
                    IF NOT EXISTS (
                        SELECT 1 FROM pg_constraint WHERE conname = 'tb_organizacao_nome_key'
                    ) THEN
                        ALTER TABLE public.tb_organizacao ADD CONSTRAINT tb_organizacao_nome_key UNIQUE (nome);
                    END IF;
                END $$;
            """)

            # Ensure indexes
            cur.execute("CREATE INDEX IF NOT EXISTS idx_org_numero ON public.tb_organizacao(numero)")
            cur.execute("CREATE INDEX IF NOT EXISTS idx_org_schema ON public.tb_organizacao(schema)")

            conn.commit()
        except Exception as e:
            conn.rollback()
            logging.error(f"Migration error: {e}")
            raise e
        finally:
            cur.close()
            conn.close()

    def get_connection(self, schema=None):
        conn = self._get_connection(self.db_name)
        if schema:
            cur = conn.cursor()
            # search_path is used to point to the correct tenant schema
            cur.execute(f"SET search_path TO {schema}, public")
            cur.close()
        return conn

    def get_cursor(self, conn):
        return conn.cursor(cursor_factory=RealDictCursor)

    def get_table_columns(self, table_name, schema):
        """Fetches metadata from information_schema.columns."""
        conn = self.get_connection()
        cur = self.get_cursor(conn)
        try:
            cur.execute("""
                SELECT column_name, data_type, is_nullable, column_default
                FROM information_schema.columns
                WHERE table_name = %s AND table_schema = %s
                ORDER BY ordinal_position
            """, (table_name, schema))
            return cur.fetchall()
        finally:
            cur.close()
            conn.close()

    def select_dynamic(self, table, schema, filters=None):
        conn = self.get_connection(schema=schema)
        cur = self.get_cursor(conn)
        try:
            query = f"SELECT * FROM {table}"
            params = []
            if filters:
                conditions = []
                for key, value in filters.items():
                    conditions.append(f"{key} = %s")
                    params.append(value)
                query += " WHERE " + " AND ".join(conditions)

            cur.execute(query, params)
            return cur.fetchall()
        finally:
            cur.close()
            conn.close()

    def insert_dynamic(self, table, data, schema):
        conn = self.get_connection(schema=schema)
        cur = self.get_cursor(conn)
        try:
            columns = data.keys()
            values = [data[col] for col in columns]
            placeholders = ["%s"] * len(values)

            query = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({', '.join(placeholders)}) RETURNING *"
            cur.execute(query, values)
            result = cur.fetchone()
            conn.commit()
            return result
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cur.close()
            conn.close()

    def update_dynamic(self, table, id, data, schema):
        conn = self.get_connection(schema=schema)
        cur = self.get_cursor(conn)
        try:
            columns = data.keys()
            params = [data[col] for col in columns]
            set_clause = ", ".join([f"{col} = %s" for col in columns])

            query = f"UPDATE {table} SET {set_clause} WHERE id = %s RETURNING *"
            params.append(id)

            cur.execute(query, params)
            result = cur.fetchone()
            conn.commit()
            return result
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cur.close()
            conn.close()

    def delete_dynamic(self, table, id, schema):
        conn = self.get_connection(schema=schema)
        cur = self.get_cursor(conn)
        try:
            cur.execute(f"DELETE FROM {table} WHERE id = %s", (id,))
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cur.close()
            conn.close()
