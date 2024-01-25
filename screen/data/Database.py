import sqlite3


class Database:
	def __init__(self):
		super(Database, self).__init__()
		self.connection = sqlite3.connect('history.db')
		self.cursor = self.connection.cursor()
		self.cursor.execute("CREATE TABLE IF NOT EXISTS history (name TEXT PRIMARY KEY, deleted INTEGER)")
		self.connection.commit()

	def get_history(self):
		self.cursor.execute('SELECT name FROM history WHERE deleted = 0')
		return self.cursor.fetchall()

	def add(self, city):
		self.cursor.execute(f"INSERT OR REPLACE INTO history (name, deleted) VALUES(?, ?)", (city, 0))
		self.connection.commit()

	def delete(self, row_index):
		sql = 'DELETE FROM history WHERE name=?'
		history = self.get_history()
		self.cursor.execute(sql, (history[row_index][0],))
		self.connection.commit()
