import threading

import serial
import serial.tools.list_ports
from threading import Thread


class Connection:
    port_name: ''
    baudrate = 9600
    device = serial.Serial()
    ports = serial.tools.list_ports.comports()
    monitoring_thread = Thread()
    monitoring_stop_event = threading.Event()

    def __init__(self, port_name):
        self.port_name = port_name

    def connect(self):
        try:
            self.device = serial.Serial(self.port_name, self.baudrate)
        except serial.serialutil.SerialException:
            print("Невозможно подключиться к " + self.port_name)

    def disconnect(self):
        if self.device.is_open:
            self.monitoring_stop_event.set()
            if self.monitoring_thread.is_alive():
                self.monitoring_thread.join()
            self.device.close()

    def reconnect(self):
        self.disconnect()
        self.connect()

    def transmit(self, command):
        self.device.write(command)

    def receive(self):
        return self.device.read_all().decode()
