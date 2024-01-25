from PySide2.QtWidgets import QTableWidgetItem, QMessageBox
from pyowm.commons.exceptions import APIRequestError
from pyowm.commons.exceptions import NotFoundError

from screen.views import DeleteButton


class Controller:
	def __init__(self, ui, weather_api, database):
		self.ui = ui
		self.weather_api = weather_api
		self.database = database

		self.table = self.ui.tableWidget

	def item_click(self):
		city = self.ui.tableWidget.currentItem().text()
		self.ui.lineEdit.setText(city)
		self.send_city(city, False)

	def send_city(self, city='', is_need_add=True):
		city = self.ui.lineEdit.text() if city == '' else city

		try:
			weather = self.weather_api.get_weather(city)
			if is_need_add:
				self.add(city)
			self.ui.label.setText(weather.to_string())
		except (NotFoundError, APIRequestError):
			self.ui.label.setText(
				f"Возможные ошибки:\n "
				f"1. Вы допустили ошибку в написании города {city}\n "
				f"2. Города/страны {city} не существует\n "
				f"3. Вы отправили пустой запрос.\n "
				"4. Проблема с интернетом 🚫")

	def restore_history(self):
		cities = self.database.get_history()
		cities.reverse()
		self.table.setRowCount(len(cities))
		self.table.setColumnCount(2)

		for i, city in enumerate(cities):
			btn = DeleteButton.delete_btn(self.delete)

			self.table.setItem(i, 0, QTableWidgetItem(city[0]))
			self.table.setCellWidget(i, 1, btn)

	def add(self, city):
		self.database.add(city)
		self.restore_history()

	def delete(self):
		row_index = self.table.currentIndex().row()
		if row_index > -1:
			messageBox = QMessageBox.warning(
				self.table, "Warning!", "Вы хотите удалить этот город из истории?", QMessageBox.No, QMessageBox.Yes)

			if messageBox == QMessageBox.Yes:
				try:
					self.database.delete(len(self.database.get_history()) - row_index - 1)
					self.restore_history()
				except Exception as e:
					print("error:", e)
		else:
			QMessageBox.warning(self.table, "Error", "Пожалуйста выберите город", QMessageBox.Ok)
