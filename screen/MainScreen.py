import sys

from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import *

from screen.Controller import Controller
from screen.data.Database import Database
from screen.views import HistoryWidget
from screen.data.WeatherApi import WeatherApi


class App(QApplication):
	def __init__(self):
		super(App, self).__init__()
		loader = QUiLoader()
		self.ui = loader.load("screen/weather.ui")
		self.ui.show()

		self.weather_api = WeatherApi()
		self.database = Database()

		self.controller = Controller(self.ui, self.weather_api, self.database)
		self.controller.send_city()

		HistoryWidget.setup_table(self.ui.tableWidget, self.controller)

		self.ui.pushButton.clicked.connect(self.controller.send_city)
		self.ui.tableWidget.itemClicked.connect(self.controller.item_click)


if __name__ == "__main__":
	app = App()
	sys.exit(app.exec_())
