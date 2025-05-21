import json
import socket
class NetworkServer:
    def __init__(self):
        """Inicjalizuje serwer na wskazanym porcie."""
        with open("server\\server.json", 'r') as config:
            data = json.load(config)
            self.port = data["port"]
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def start(self) -> None:
        """Uruchamia nasłuchiwanie połączeń i obsługę klientów."""
        try:
            self.server_socket.bind(('0.0.0.0', self.port))
            self.server_socket.listen(2)
            print("[INFO] Serwer nadsłuchuje na porcie: "+str(self.port))
            while True:
                client_socket, client_address = self.server_socket.accept()
                print("[INFO] "+str(client_address[0])+":"+str(client_address[1])+" połączył się z serwerem")
                self._handle_client(client_socket)
        except Exception as e:
            print("[ERROR] Bład serwera: "+str(e))

    def _handle_client(self, client_socket) -> None:
        """Odbiera dane, wysyła ACK i wypisuje je na konsolę."""
        try:
            data = client_socket.recv(4096)
