from PySide2.QtWidgets import *


def setup_table(table, controller):
	table.horizontalHeader().setStyleSheet(
		"QHeaderView { color: white; }"
		"QHeaderView::section { background-color: #262626; }"
	)

	table.setSelectionBehavior(QAbstractItemView.SelectRows)

	controller.restore_history()
