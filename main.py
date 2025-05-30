odp = ""
while odp != "c" and odp != "s":
    odp = input("Moduł ma działać jako client: 'c' czy serwer: 's'?: ")
if odp == "s":
    import global_data
    import threading
    import server.server
    from tkinter import *
    global_data.root.title("Network Server Gui")
    sterowanie_frame = Frame(global_data.root)
    sterowanie_frame.pack(side=TOP, fill=X)

    port = Label(sterowanie_frame, text="Port: ")
    port.pack(side=LEFT, anchor="n")

    entry = Entry(sterowanie_frame)
    entry.pack(side=LEFT, anchor="n")

    def uruchomienie_serwera():
        global serwer
        serwer = server.server.NetworkServer(int(entry.get()))
        sluchanie_portu.config(text="Serwer działa na porcie: " +entry.get())

        def serwerowanie():
            serwer.start()
        threading.Thread(target=serwerowanie, daemon=True).start()

    przycisk_start = Button(sterowanie_frame, text="Start", command=uruchomienie_serwera)
    przycisk_start.pack(side=LEFT, anchor="n")

    def zatrzymaj():
        serwer.stop()
        sluchanie_portu.config(text="Serwer zatrzymany")
    przycisk_stop = Button(sterowanie_frame, text="Stop", command=zatrzymaj)
    przycisk_stop.pack(side=LEFT, anchor="n")

    # Definiuj nagłówki kolumn
    global_data.tree.heading("Sensor", text="Sensor")
    global_data.tree.heading("Wartość", text="Wartość")
    global_data.tree.heading("Jednostka", text="Jednostka")
    global_data.tree.heading("Timestamp", text="Timestamp")
    global_data.tree.heading("Śr.1h", text="Śr.1h")
    global_data.tree.heading("Śr.12h", text="Śr.12h")

    # Umieść tabelę na oknie
    global_data.tree.pack(fill="both", expand=True)

    sluchanie_portu = Label(global_data.root, text="Wprowadź port")
    sluchanie_portu.pack(side=LEFT, anchor="n")

    global_data.root.mainloop()



elif odp == "c":
    import sensors
    import logger
    import time
    import network.client
    import datetime
    wilgotnosc = sensors.HumiditySensor(0, "Sensor_wilgotnosci")
    logowanie = logger.Logger("config.json")
    logowanie.start()
    wilgotnosc.register_callback(logowanie.log_reading)
    temperatura = sensors.TemperatureSensor(1, "Sensor_temperatury")
    temperatura.register_callback(logowanie.log_reading)
    cisnienie = sensors.PressureSensor(2, "Sensor_cisnienia")
    cisnienie.register_callback(logowanie.log_reading)
    jakosc = sensors.AirQualitySensor(3, "Sensor_jakosci powietrza")
    jakosc.register_callback(logowanie.log_reading)
    client = network.client.NetworkClient()
    client.connect()
    while True:
        time.sleep(0.5)
        client.send({"id": wilgotnosc.sensor_id, "timestamp": datetime.datetime.now().isoformat(), "value": wilgotnosc.read_value(), "unit": wilgotnosc.unit})
        client.send({"id": temperatura.sensor_id, "timestamp": datetime.datetime.now().isoformat(), "value": temperatura.read_value(), "unit": temperatura.unit})
        client.send({"id": cisnienie.sensor_id, "timestamp": datetime.datetime.now().isoformat(), "value": cisnienie.read_value(), "unit": cisnienie.unit})
        client.send({"id": jakosc.sensor_id, "timestamp": datetime.datetime.now().isoformat(), "value": jakosc.read_value(), "unit": jakosc.unit})
