import json
import socket
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
            #client_socket.shutdown(socket.SHUT_WR)
            #client_socket.close()

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
            print(json.loads(data.decode('utf-8')))
            client_socket.sendall(b"ACK\n")
        except Exception as e:
            print("[ERROR] błąd przy obsłudze klienta: "+str(e))

