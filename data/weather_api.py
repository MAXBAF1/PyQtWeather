from pyowm import OWM
from pyowm.utils import config as cfg

from models.Weather import Weather


class WeatherApi:
	def __init__(self):
		self.owm = OWM("15be1aebc67c9dbf5d58ab9302f4d8a0")
		owm_config = cfg.get_default_config()
		owm_config['language'] = 'ru'

	def get_weather(self, city):
		mgr = self.owm.weather_manager()
		observation = mgr.weather_at_place(city)
		return Weather(observation.weather, city)
