import sys

from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import *
from pyowm.commons.exceptions import APIRequestError
from pyowm.commons.exceptions import NotFoundError

from HistoryWidget import HistoryWidget
from data.weather_api import WeatherApi


class App(QWidget):
	def __init__(self):
		super(App, self).__init__()
		loader = QUiLoader()
		self.ui = loader.load("weather.ui")
		self.ui.show()
		self.states = ['search', 'success', 'OWM_error', 'back']

		self.weather_api = WeatherApi()
		self.history = HistoryWidget(self.ui.tableWidget)
		self.history.restore_history()

		self.send_city()

		self.ui.pushButton.clicked.connect(self.send_city)
		self.ui.tableWidget.itemClicked.connect(self.item_click)

	def item_click(self):
		city = self.ui.tableWidget.currentItem().text()
		self.ui.lineEdit.setText(city)
		self.send_city(city)

	def send_city(self, city=False):
		is_need_add = not city
		city = self.ui.lineEdit.text() if not city else city

		try:
			weather = self.weather_api.get_weather(city)
			if is_need_add:
				self.history.add(city)
			self.ui.label.setText(weather.to_string())
		except (NotFoundError, APIRequestError):
			self.ui.label.setText(
				f"Возможные ошибки:\n "
				f"1. Вы допустили ошибку в написании города {city}\n "
				f"2. Города/страны {city} не существует\n "
				f"3. Вы отправили пустой запрос.\n "
				"4. Проблема с интернетом 🚫")


if __name__ == "__main__":
	app = QApplication([])
	widget = App()
	sys.exit(app.exec_())
