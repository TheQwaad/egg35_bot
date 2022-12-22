import sqlite3
from sqlite3 import Error as SqlError
import os
from extra_commands import *


class SQLiteDatabase:
    def __init__(self, name):
        self.connection = sqlite3.connect(get_path(name, '.db'))
        self.cursor = self.connection.cursor()
        self.name = name
        self.columns = []

    def create_table(self, name, columns):
        self.columns = columns
        columns = ",\n".join([f"{key} {columns[key]}" for key in columns.keys()])
        command = f'CREATE TABLE IF NOT EXISTS {self.name}(\n{columns});'
        self.cursor.execute(command)
        self.connection.commit()

    def get_single(self, requirements):
        pass
