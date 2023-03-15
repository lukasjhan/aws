from typing import List, Any

import pymysql.cursors

class DatabaseProxy:
  def __init__(self, db_name: str):
    self.db_name = db_name

  def execute(self, sql: str, args: List[Any]=None, cursor=pymysql.cursors.DictCursor):
    connection = self._get_connection()
    try:
      with connection.cursor(cursor=cursor) as cursor:
        return cursor.execute(sql, args)
    finally:
      connection.close()

  def _get_connection(self):
    return pymysql.connect(db=self.db_name)
