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
        os.makedirs(os.path.join(self.log_dir, 'archive'), exist_ok=True)
        os.makedirs(self.log_dir, exist_ok=True)
        self.buffer: List[List[str]] =[]
    def start(self) -> None:
        """
        Otwiera nowy plik CSV do logowania. Jeśli plik jest nowy, zapisuje nagłówek.
        """
        today = datetime.now()
        self.filename = today.strftime(self.filename_pattern)
        # Nagłówki, które chcemy zapisać, jeśli plik nie istnieje
        nagłówki = ['timestamp', 'sensor_id', 'value', 'unit']
        # Sprawdzamy, czy plik istnieje
        if not os.path.exists(self.filename):
            # Tworzymy nowy plik i zapisujemy nagłówki
            self.log_file = open(self.filename, 'w', newline='', encoding='utf-8')
            writer = csv.writer(self.log_file)
            writer.writerow(nagłówki)
            self.lastRotation = today
        else:
            self.log_file = open(filename, 'a', newline='', encoding='utf-8')
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
        row = [timestamp.isoformat(), sensor_id, value, unit]
        self.buffer.append(row)
        if len(self.buffer >= self.buffer_size):
            writer = csv.writer(self.log_file)
            writer.writerows(self.buffer)
            self.buffer: List[List[str]] = []
            if (datetime.now() - self.lastRotation).total_seconds() > self.hours_to_rotate or os.path.getsize(self.filename) > self.max_size_mb * 1048576: """/ 3600"""
                self.stop()
                os.rename(self.filename, os.path.join('archive', self.filename))
                for nazwa_pliku in os.listdir('archive'):
                    pelna_sciezka = os.path.join('archive', nazwa_pliku)
                    if os.path.gettime(pelna_sciezka) < time.time() - self.retention_days * 86400:
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
        ...