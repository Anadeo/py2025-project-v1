import sensors
import time
import network.client
import datetime
wilgotnosc = sensors.HumiditySensor(0, "Sensor")
client = network.client.NetworkClient()
client.connect()
for i in range(10):
    time.sleep(1)
    client.send({"id": 0, "timestamp": datetime.datetime.now().isoformat(), "value": wilgotnosc.read_value(), "unit": "%"})
#import server.server
#server = server.server.NetworkServer(25565)
#server.start()
