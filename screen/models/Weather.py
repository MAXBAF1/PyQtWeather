class Weather:

	def __init__(self, weather, city):
		super(Weather, self).__init__()
		self.weather = weather
		self.city = city

	def to_string(self):
		tg = self.weather.temperature("celsius")
		local_temp = tg['temp']
		f_like = tg['feels_like']
		max_temp = tg['temp_max']
		min_temp = tg['temp_min']
		wind = self.weather.wind()['speed']
		pressure = self.weather.pressure['press']
		moisture = self.weather.humidity
		status = self.weather.detailed_status

		return \
			f"В городе {self.city} температура: {int(local_temp)} °C 🌡 \n" \
			f"Ощущается как: {int(f_like)} °C \n" \
			f"Максимальная температура: {int(max_temp)} °C \n" \
			f"Минимальная температура: {int(min_temp)}°C \n" \
			f"Скорость ветра: {int(wind)} м/c \n" \
			f"Давление: {int(pressure)} мм.рт.ст \n" \
			f"Влага: {int(moisture)} % \n" \
			f"По состоянию: {status} {status_emoji.get(status) or '🌍'}"


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
