import pymysql.cursors

from typing import Callable, Iterable, Union, Sized, Sequence

from .logs import Logger
from .sql import SqlTable


# DAO: Database Access Object
class MyConn:
    def __init__(self, host: str, database: str, logger: Logger, verbose: bool):
        self.profile = {
            "host": host,
            "database": database,
            "user": "root",
        }
        self.logger = logger
        self.verbose = verbose

    def wrap(self, func: Callable, **kwargs):
        connection = pymysql.connect(**self.profile)
        try:
            with connection.cursor() as cursor:
                # Execute sql statement
                statement = func(**kwargs)
                cursor.execute(statement)
                connection.commit()
                self.logger.debug(f"execute func {func.__name__} with {kwargs}")

                # Process result
                result = cursor.fetchall()
                if len(result) <= 0:
                    self.logger.debug("func didn't return anything")

                if self.verbose:
                    print("wrapper result:", result)
                return result
        except Exception as e:
            connection.rollback()
            self.logger.error(f"error occurred while executing func {func.__name__}: {e}")
        finally:
            connection.close()

    def wrapmany(self, func: Callable, **kwargs):
        connection = pymysql.connect(**self.profile)
        try:
            with connection.cursor() as cursor:
                # Execute sql statement with many
                statement, data = func(**kwargs)
                cursor.executemany(statement, data)
                connection.commit()
                self.logger.debug(f"execute func {func.__name__} with {kwargs}")
                # Process result
                result = cursor.fetchall()
                if len(result) <= 0:
                    self.logger.debug("func didn't return anything")

                if self.verbose:
                    print("wrapper many result:", result)
                return result
        except Exception as e:
            connection.rollback()
            self.logger.error(f"error occurred while executing func {func.__name__}: {e}")
        finally:
            connection.close()

    def ping(self):
        connection = pymysql.connect(**self.profile)
        try:
            if self.verbose:
                self.logger.debug("Ping sent")
            connection.ping()
        except Exception as e:
            self.logger.error(f"Failed to ping database: {e}")
        finally:
            self.logger.debug("Ping successful")

    @staticmethod
    def test():
        return "TEST"


class SqlStatement:
    def __init__(self, verbose: bool = True):
        self.verbose = verbose

    @staticmethod
    def _name_column(column_name: str):
        return column_name.lower()

    def _process_column(self, columns: dict, key_setup: dict) -> str:
        """
        :param columns: { [key: SQL types]: {value: Column name} }
        :param key_setup: { [key: Column name]: <list of key string> }
            ex) ["AUTO_INCREMENT", "PRIMARY KEY"]
        :return:
        """
        result = list()
        for sql_types, column_name in columns.items():
            script_per_type = list()
            for col in column_name:
                script_per_colname = [f"{self._name_column(col)} {sql_types}"]
                if (key_setup is not None) and (col in key_setup.keys()):
                    script_per_colname.append(
                        " ".join(map(lambda x: str(x), key_setup[col]))
                    )
                script_per_type.append(
                    " ".join(script_per_colname)
                )
            result.append(
                ", ".join(script_per_type)
            )
        return ", ".join(result)

    @staticmethod
    def _auto_generate_index_name(index_col: Sequence):
        return f"idx_{index_col[0]}"

    @staticmethod
    def _auto_generate_placeholder(length: int):
        return ", ".join(["%s" for i in range(length)])

    @staticmethod
    def send_raw(script: str):
        return script

    def create_table(
        self,
        table: SqlTable,
        table_columns: dict,
        table_keys: dict = None
    ) -> str:
        sql_table = """
        create table if not exists {table} (
          {column_settings}
        );
        """
        keyword = {
            "table": table.to_string(),
            "column_settings": self._process_column(table_columns, table_keys)
        }
        if self.verbose:
            print(sql_table.format(**keyword))
        return sql_table.format(**keyword)
    
    def create_table_wid(
        self,
        table: SqlTable,
        table_columns: dict,
    ) -> str:
        sql_table = """
        create table if not exists {table} (
          id AUTO_INCREMENT PRIMARY KEY
          {column_settings}
        );
        """
        keyword = {
            "table": table.to_string(),
            "column_settings": self._process_column(table_columns)
        }
        if self.verbose:
            print(sql_table.format(**keyword))
        return  sql_table.format(**keyword)

    def delete_table(self, table: SqlTable):
        sql_statement = """
        drop tables {table}
        """
        keyword = {
            "table": table.to_string()
        }
        if self.verbose:
            print(sql_statement.format(**keyword))
        return sql_statement.format(**keyword)

    def create_index(
        self,
        table: SqlTable,
        table_columns: Sequence,
    ) -> str:
        sql_statement = """
        create index {index_name} on {table} ({columns})
        """
        keyword = {
            "index_name": self._auto_generate_index_name(table_columns),
            "table": table.to_string(),
            "columns": ", ".join(table_columns)
        }
        if self.verbose:
            print(sql_statement.format(**keyword))
        return sql_statement.format(**keyword)

    def create_data(
        self,
        table: SqlTable,
        table_columns: Union[Iterable, Sized, Sequence],
        data: Sequence[Sequence]
    ) -> tuple:
        """
        :param table: ...
        :param table_columns: Should be [ ... ] - A Sequence.
        :param data: [ [ ... ], [ ... ], ... ] - A nested Sequence.
        :return: SQL insertion statement &
        """
        assert len(table_columns) == len(data[0]), "mismatched column and data"

        sql_statement = """
        insert into {table} ({columns}) values ({placeholders})
        """
        keyword = {
            "table": table.to_string(),
            "columns": ", ".join(table_columns),
            "placeholders": self._auto_generate_placeholder(len(table_columns)),
        }
        if self.verbose:
            print(sql_statement.format(**keyword))
        return sql_statement.format(**keyword), data

    def read_data(self, table: SqlTable):
        sql_statement = """
        select * from {table}
        """
        keyword = {
            "table": table.to_string(),
        }
        if self.verbose:
            print(sql_statement.format(**keyword))
        return sql_statement.format(**keyword)
