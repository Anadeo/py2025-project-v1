from typing import Optional, Dict, Iterator, List
import json
import os
import time
import csv
from datetime import datetime
class Logger:
    def __init__(self, config_path: str):
        """
        Inicjalizuje logger na podstawie pliku JSON.
        :param config_path: Ścieżka do pliku konfiguracyjnego (.json)
        """
        with open(config_path, 'r') as config:
            data = json.load(config)
            self.log_dir = data['log_dir']
            self.hours_to_rotate = data['rotate_every_hours']
            self.max_size_mb = data['max_size_mb']
            self.retention_days = data['retention_days']
            self.filename_pattern = data["filename_pattern"]
            self.buffer_size = data['buffer_size']
        self.lastRotation = datetime.now()
        self.rotation_counter = 0
        os.makedirs(os.path.join(self.log_dir, 'archive'), exist_ok=True)
        self.buffer: List[List[str]] =[]
    def start(self) -> None:
        """
        Otwiera nowy plik CSV do logowania. Jeśli plik jest nowy, zapisuje nagłówek.
        """
        today = datetime.now()
        self.filename = today.strftime(self.filename_pattern)
        self.filePath = os.path.join(self.log_dir, self.filename)
        # Nagłówki, które chcemy zapisać, jeśli plik nie istnieje
        nagłówki = ['sensor_id', 'timestamp', 'value', 'unit']
        # Sprawdzamy, czy plik istnieje
        if not os.path.exists(self.filePath):
            # Tworzymy nowy plik i zapisujemy nagłówki
            self.log_file = open(self.filePath, 'w', newline='', encoding='utf-8')
            self.writer = csv.writer(self.log_file)
            self.writer.writerow(nagłówki)
        else:
            self.log_file = open(self.filePath, 'a', newline='', encoding='utf-8')
    def stop(self) -> None:
        """
        Wymusza zapis bufora i zamyka bieżący plik.
        """
        self.log_file.flush()
        self.log_file.close()
    def log_reading(
        self,
        sensor_id: str,
        timestamp: datetime,
        value: float,
        unit: str
    ) -> None:
        """
        Dodaje wpis do bufora i ewentualnie wykonuje rotację pliku.
        """
        row = [sensor_id, timestamp.isoformat(), value, unit]
        self.buffer.append(row)
        if len(self.buffer) >= self.buffer_size:
            self.writer.writerows(self.buffer)
            self.buffer = []
            if (datetime.now() - self.lastRotation).total_seconds() > self.hours_to_rotate or os.path.getsize(self.filename) > self.max_size_mb * 1048576:
                self.stop()
                currentTime = datetime.now()
                if currentTime.date() != self.lastRotation.date():
                    self.rotation_counter = 0
                    self.lastRotation = currentTime
                os.rename(self.filePath, os.path.join(self.log_dir, 'archive', str(self.rotation_counter)+"_"+self.filename))
                self.rotation_counter += 1
                for nazwa_pliku in os.listdir(os.path.join(self.log_dir, 'archive')):
                    pelna_sciezka = os.path.join(self.log_dir, 'archive', nazwa_pliku)
                    if os.path.getctime(pelna_sciezka) < time.time() - self.retention_days * 86400:
                        os.remove(pelna_sciezka)
                self.start()
    def read_logs(
        self,
        start: datetime,
        end: datetime,
        sensor_id: Optional[str] = None
    ) -> Iterator[Dict]:
        """
        Pobiera wpisy z logów zadanego zakresu i opcjonalnie konkretnego czujnika.
        """
        logs = []
        for folder in [self.log_dir, os.path.join(self.log_dir, "archive")]:
            if os.path.exists(folder):
                for filename in os.listdir(folder):
                    filePath = os.path.join(folder, filename)
                    with open(filePath, "r", newline='', encoding='utf-8') as file:
                        reader = csv.DictReader(file)
                        for row in reader:
                            timestamp = datetime.fromisoformat(row['timestamp'])
                            if start <= timestamp <= end:
                                if sensor_id is None or row['sensor_id'] == sensor_id:
                                    logs.append({
                                        "timestamp": timestamp,
                                        "sensor_id": row['sensor_id'],
                                        "value": row['value'],
                                        "unit": row['unit']
                                    })
        return logs