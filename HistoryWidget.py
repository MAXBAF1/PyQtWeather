from PySide2.QtCore import Qt
from PySide2.QtGui import QIcon, QCursor
from PySide2.QtWidgets import *
from PySide2.QtWidgets import QMessageBox

from Database import Database


class HistoryWidget:
	def __init__(self, table):
		super(HistoryWidget, self).__init__()

		self.table = table
		self.table.horizontalHeader().setStyleSheet(
			"QHeaderView { color: white; }"
			"QHeaderView::section { background-color: #262626; }"
		)

		self.database = Database()

		self.table.setSelectionBehavior(QAbstractItemView.SelectRows)

	def restore_history(self):
		cities = self.database.get_history()
		cities.reverse()
		self.table.setRowCount(len(cities))
		self.table.setColumnCount(2)

		for i, city in enumerate(cities):
			btn = QPushButton()
			btn.setFixedSize(40, 40)
			btn.clicked.connect(self.delete)
			btn.setIcon(QIcon('resources/delete.svg'))
			btn.setCursor(QCursor.shape(QCursor()).PointingHandCursor)

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
