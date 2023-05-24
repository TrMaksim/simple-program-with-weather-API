from datetime import datetime
from typing import Union, Dict, List, Tuple, Any
import requests
from config import API_KEY


class WeatherAPI:
    def __init__(self):
        """
        Конструктор класса WeatherAPI.

        Инициализирует параметры для доступа к API сервису погоды.
        """
        self.url = "https://api.openweathermap.org/data/2.5/weather"
        self.api_key = API_KEY

    def _sending_request(self, city: str) -> Dict[str, Any]:
        """
        Метод отправляет запрос на сервер для получения данных о погоде
        в указанном городе и возвращает JSON-ответ в виде словаря.

        :param city: город, для которого запрашиваются данные
        :type city: str

        :return: словарь с данными о погоде, содержащий температуру, влажность и скорость ветра
        :rtype: Dict[str, Union[int, float, Dict[str, Union[int, float]]]]
        """
        params = {"appid": self.api_key, "q": city, "units": "metric"}
        response = requests.get(self.url, params=params)
        return response.json()

    def _processing_response(self, data: Dict[str, Any]) -> Tuple[float, int, float]:
        """
        Частный метод, обрабатывающий данные о погоде, полученные из API.

        :param data: Данные о погоде, полученные из API.
        :type data: Dict[str]

        :return: Tuple с данными о температуре, влажности и скорости ветра.
        :rtype: Tuple[float, int, float].
        """
        temp_c = data.get("main").get("temp")
        humidity = data.get("main").get("humidity")
        wind_mps = data.get("wind").get("speed")
        return temp_c, humidity, wind_mps

    def _get_weather(self, city: str) -> Dict[str, Union[int, float]]:
        """
        Метод для получения данных о погоде в указанном городе.

        :param city: город, для которого запрашиваются данные
        :type city: str

        :return: словарь с данными о температуре, влажности и скорости ветра
        :rtype: Dict[str, Union[int, float]]
        """
        data = self._sending_request(city)
        temp_c, humidity, wind_mps = self._processing_response(data)

        return {
            "temperature": float(temp_c),
            "humidity": int(humidity),
            "wind_speed": float(wind_mps),
        }

    def show_weather(self, city: str) -> None:
        """
        Метод для вывода данных о погоде в указанном городе на экран.

        :param city: город, для которого запрашиваются данные
        :type city: str

        :return: None
        :rtype: None
        """
        weather_data = self._get_weather(city)
        print(
            f"Температура в {city}: {weather_data.get('temperature')}>°C, влажность: "
            f"{weather_data.get('humidity')}>%, скорость ветра: {weather_data.get('wind_speed')}> м/с."
        )


class WeatherForecast(WeatherAPI):
    def __init__(self):
        super().__init__()
        self.url = "https://api.openweathermap.org/data/2.5/forecast"

    def _send_request(self, city: str) -> Dict[str, Any]:
        """
        Метод отправляет запрос на сервер для получения данных о погоде
        в указанном городе и возвращает JSON-ответ в виде словаря.

        :param city: город, для которого запрашиваются данные
        :type city: str

        :return: словарь с данными о погоде
        :rtype: Dict[str, Any]
        """

        url = f"{self.url}?q={city}&appid={self.api_key}&units=metric"
        response = requests.get(url)
        return response.json()

    def get_forecast(self, city: str) -> List[Dict[str, Union[str, int, float]]]:
        """
        Метод для получения прогноза погоды на ближайшие 5 дней в указанном городе.

        :param city: город, для которого запрашивается прогноз
        :type city: str

        :return: список словарей с данными о дате, температуре, влажности и скорости ветра
        :rtype: List[Dict[str, Union[str, int, float]]]
        """

        data = self._send_request(city)
        forecasts = data["list"][:5]

        result = []
        for forecast in forecasts:
            date = datetime.fromtimestamp(forecast["dt"])
            temp = forecast["main"]["temp"]
            humidity = forecast["main"]["humidity"]
            wind_speed = forecast["wind"]["speed"]

            result.append(
                {
                    "date": date.strftime("%Y-%m-%d"),
                    "temp": temp,
                    "humidity": humidity,
                    "wind_speed": wind_speed,
                }
            )

        return result


def main():
    output = WeatherAPI()
    output.show_weather("Одесса")
    forecast = WeatherForecast()
    for day in forecast.get_forecast("Одесса"):
        print(day)


if __name__ == "__main__":
    main()
