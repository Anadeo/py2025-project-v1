import random
import datetime
import time
class Sensor:
    def __init__(self, sensor_id, name, unit, min_value, max_value, frequency=1):
        """
        Inicjalizacja czujnika.

        :param sensor_id: Unikalny identyfikator czujnika
        :param name: Nazwa lub opis czujnika
        :param unit: Jednostka miary (np. '°C', '%', 'hPa', 'lux')
        :param min_value: Minimalna wartość odczytu
        :param max_value: Maksymalna wartość odczytu
        :param frequency: Częstotliwość odczytów (sekundy)
        """
        self.sensor_id = sensor_id
        self.name = name
        self.unit = unit
        self.min_value = min_value
        self.max_value = max_value
        self.frequency = frequency
        self.active = True
        self.last_value = None
        self.last_date = None

    def read_value(self):
        """
        Symuluje pobranie odczytu z czujnika.
        W klasie bazowej zwraca losową wartość z przedziału [min_value, max_value].
        """
        if not self.active:
            raise Exception(f"Czujnik {self.name} jest wyłączony.")
        now = datetime.datetime.now()
        if self.last_date is None:
            self.last_date = now
            value = random.uniform(self.min_value, self.max_value)
            self.last_value = value
            return value
        difference = now - self.last_date
        if difference.total_seconds() > self.frequency:
            self.last_date = now
            value = random.uniform(self.min_value, self.max_value)
            self.last_value = value
            return value
        return self.last_value
    def get_last_value(self):
        """
        Zwraca ostatnią wygenerowaną wartość, jeśli była wygenerowana.
        """
        if self.last_value is None:
            return self.read_value()
        return self.last_value

    def start(self):
        """
        Włącza czujnik.
        """
        self.active = True

    def stop(self):
        """
        Wyłącza czujnik.
        """
        self.active = False

    def __str__(self):
        return f"Sensor(id={self.sensor_id}, name={self.name}, unit={self.unit})"

class TemperatureSensor(Sensor):
    def __init__(self, sensor_id, name="Sensor temperatury", frequency=1):
        super().__init__(sensor_id, name, "°C", -20, 50, frequency)
    def read_value(self):
        return super().read_value()
    def get_last_value(self):
        return super().get_last_value()
    def start(self):
        super().start()
    def stop(self):
        super().stop()
class HumiditySensor(Sensor):
    def __init__(self, sensor_id, name="Sensor wilgotnosci", frequency=1):
        super().__init__(sensor_id, name, "%", 0, 100, frequency)
        self.start_time = time.time()
    def read_value(self):
        SECONDS_PER_DAY = 120
        virtual_day_time = (time.time() - self.start_time) % SECONDS_PER_DAY / SECONDS_PER_DAY
        if 0.25 <= virtual_day_time and virtual_day_time <= 0.75: # dzień
            self.min_value = 30
            self.max_value = 50
            return super().read_value()
        self.min_value = 60
        self.max_value = 90
        return super().read_value()
    def get_last_value(self):
        return super().get_last_value()
    def start(self):
        super().start()
    def stop(self):
        super().stop()
class PressureSensor(Sensor):
    def __init__(self, sensor_id, name="Sensor ciśnienia", frequency=1):
        super().__init__(sensor_id, name, "hPa", 950, 1050, frequency)
    def read_value(self):
        return super().read_value()
    def get_last_value(self):
        return super().get_last_value()
    def start(self):
        super().start()
    def stop(self):
        super().stop()
class AirQualitySensor(Sensor):
    def __init__(self, sensor_id, name="Sensor jakości powietrza", frequency=1):
        super().__init__(sensor_id, name, "AQI", 0, 500, frequency)
    def read_value(self):
        return super().read_value()
    def get_last_value(self):
        return super().get_last_value()
    def start(self):
        super().start()
    def stop(self):
        super().stop()