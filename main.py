import sensors
import time
wilgotnosc = sensors.HumiditySensor(0, "Sensor")
for i in range(10):
    time.sleep(1)
    print(wilgotnosc.read_value())
