import json
import socket
import global_data
from datetime import datetime, timedelta
class NetworkServer:
    def __init__(self, port: int):
        """Inicjalizuje serwer na wskazanym porcie."""
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.isClientConnected = None

    def start(self) -> None:
        """Uruchamia nasłuchiwanie połączeń i obsługę klientów."""
        try:
            self.server_socket.bind(('0.0.0.0', self.port))
            self.server_socket.listen(2)
            print("[INFO] Serwer nadsłuchuje na porcie: "+str(self.port))
            while True:
                client_socket, client_address = self.server_socket.accept()
                print("[INFO] " + str(client_address[0]) + ":" + str(client_address[1]) + " połączył się z serwerem")
                self.isClientConnected = True
                while self.isClientConnected:
                    self._handle_client(client_socket)
        except OSError:
            print("[INFO] Serwer został wyłączony")
        except Exception as e:
            print("[ERROR] Bład serwera: "+str(e))

    def _handle_client(self, client_socket) -> None:
        """Odbiera dane, wysyła ACK i wypisuje je na konsolę."""
        try:
            data = client_socket.recv(4096)
            if not data:
                print("[INFO] Klient zakończył połączenie.")
                self.isClientConnected = False
                return
            data_recived = json.loads(data.decode('utf-8'))
            # altualizacja dabeli gui tutaj
            global_data.root.after(0, self.update_tree_with_sensor_data, data_recived)
            print(data_recived)
            client_socket.sendall(b"ACK\n")
        except Exception as e:
            print("[ERROR] błąd przy obsłudze klienta: "+str(e))

    def update_tree_with_sensor_data(self, data: dict):
        sensor_id = data['id']
        timestamp_str = data['timestamp']
        value = data['value']
        unit = data['unit']
        timestamp = datetime.fromisoformat(timestamp_str)

        if sensor_id not in global_data.history:
            global_data.history[sensor_id] = []
        global_data.history[sensor_id].append((timestamp, value))

        now = timestamp
        one_sec_ago = now - timedelta(seconds=1)
        twelve_sec_ago = now - timedelta(seconds=12)

        values_1s = [v for (t, v) in global_data.history[sensor_id] if t >= one_sec_ago]
        values_12s = [v for (t, v) in global_data.history[sensor_id] if t >= twelve_sec_ago]

        global_data.history[sensor_id] = [entry for entry in global_data.history[sensor_id] if entry[0] >= twelve_sec_ago]

        avg_1s = round(sum(values_1s) / len(values_1s), 2) if values_1s else ""
        avg_12s = round(sum(values_12s) / len(values_12s), 2) if values_12s else ""

        values = (sensor_id, value, unit, timestamp, avg_1s, avg_12s)

        if sensor_id in global_data.sensor_items:
            item_id = global_data.sensor_items[sensor_id]
            global_data.tree.item(item_id, values=values)
        else:
            item_id = global_data.tree.insert('', 'end', values=values)
            global_data.sensor_items[sensor_id] = item_id
    def stop(self):
        self.server_socket.close()
        self.isClientConnected = False
