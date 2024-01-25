from PySide2.QtGui import QIcon, QCursor
from PySide2.QtWidgets import QPushButton


def delete_btn(on_click):
	button = QPushButton()
	button.setFixedSize(40, 40)
	button.clicked.connect(on_click)
	button.setIcon(QIcon('screen/resources/delete.svg'))
	button.setCursor(QCursor.shape(QCursor()).PointingHandCursor)

	return button
