import configparser

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from pyowm import OWM
from pyowm.commons.exceptions import APIRequestError
from pyowm.commons.exceptions import NotFoundError
from pyowm.utils import config as cfg


owm = OWM("15be1aebc67c9dbf5d58ab9302f4d8a0")
owm_config = cfg.get_default_config()
owm_config['language'] = 'ru'

Form, Window = uic.loadUiType('weather.ui')
app = QApplication([])
window = Window()
form = Form()
form.setupUi(window)
window.show()
log = configparser.ConfigParser()
states = ['search', 'success', 'OWM_error', 'back']


def create_weather_ui():
	city = form.lineEdit.text()
	try:
		print(f"{states[0]} -> {city}")
		mgr = owm.weather_manager()
		observation = mgr.weather_at_place(city)
		weather = observation.weather
		tg = weather.temperature("celsius")
		local_temp = tg['temp']
		f_like = tg['feels_like']
		max_temp = tg['temp_max']
		min_temp = tg['temp_min']
		e_temp = "🌡"
		wind = weather.wind()['speed']
		pressure = weather.pressure['press']
		moisture = weather.humidity
		status = weather.detailed_status

		status_emoji = {
			"ясно": "☀️",
			"переменная облачность": "🌤",
			"облачно с прояснениями": "🌥",
			"небольшой дождь": "🌦",
			"пасмурно": "☁️",
			"небольшая облачность": "☁️",
			"дождь": "🌧",
			"мгла": "💨"
		}

		print(f"{states[1]} -> {city}")
		return form.label.setText(
			f"В городе {city} температура: {int(local_temp)} °C {e_temp} \n"
			f"Максимальная температура: {int(max_temp)} °C \n"
			f"Минимальная температура: {int(min_temp)}°C \n"
			f"Ощущается как: {int(f_like)} °C \n"
			f"Скорость ветра: {int(wind)} м/c \n"
			f"Давление: {int(pressure)} мм.рт.ст \n"
			f"Влага: {int(moisture)} % \n"
			f"По состоянию: {status} {status_emoji.get(status) or '🌍'}")
	except (NotFoundError, APIRequestError):
		print(states[2])
		error = \
			f"Возможные ошибки:\n " \
			f"1. Вы допустили ошибку в написании города {city}\n " \
			f"2. Города/страны {city} не существует\n " \
			f"3. Вы отправили пустой запрос.\n " \
			"4. Проблема с интернетом 🚫"
		return form.label.setText(error)


def on_back_btn():
	print(states[3])
	return form.label.setText("")


form.pushButton.clicked.connect(create_weather_ui)
form.pushButton_2.clicked.connect(on_back_btn)
app.exec_()
