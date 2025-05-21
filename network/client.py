import json
import socket
from http.client import responses
import time

class NetworkClient:
    def __init__(
        self
    ):
        """Inicjalizuje klienta sieciowego."""
        with open("network\\config.json", 'r') as config:
            data = json.load(config)
            self.adres = data["host"]
            self.port = data["port"]
            self.retry_count = data["retries"]
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(data["timeout"])
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def connect(self) -> None:
        """Nawiazuje połączenie z serwerem."""
        for i in range(self.retry_count):
            try:
                print("[INFO] Łączenie z serwerem...")
                self.socket.connect((self.adres, self.port))
                print("[INFO] Połączono z serwerem")
                return
            except socket.error as e:
                print("[WARN] Nie udało się połączyć z serwerem ("+str(i)+"):"+e)
                print("[WARN]Ponowna próba za 5s")
                time.sleep(5)
        print("[ERROR] Wyczerpano wszystkie próby łączenia z serwerem")

    def send(self, data: dict) -> bool:
        """Wysyła dane i czeka na potwierdzenie zwrotne."""
        try:
            # Wysyłanie danych
            self.socket.sendall(self._serialize(data))
            print("[INFO] Dane wysłane, oczekiwanie na potwierdzenie...")
            try:
                response = self._deserialize(self.socket.recv(4096))
                if response != "ACK\n":
                    print("[ERROR] Błędna odpowiedź serwera: " + response)
                    return False
                return True
            except socket.timeout:
                print("[ERROR] Nie otrzymano potwierdzenia zwrotnego w wymaganym czasie")
                return False
            except Exception as e:
                print("[ERROR] Wystąpił problem z odbiorem danych: "+str(e))
                return False
        except Exception as e:
            print("[ERROR] Nie udało się wysłać danych: "+str(e))

    def close(self) -> None:
        """Zamyka połączenie."""
        self.socket.close()
        print("[INFO] Zamnięto połączenie z serwerem")

    # Metody pomocnicze:
    def _serialize(self, data: dict) -> bytes:
        return json.dumps(data).encode('utf-8')

    def _deserialize(self, raw: bytes) -> dict:
        return json.loads(raw.decode('utf-8'))