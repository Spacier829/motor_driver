import time
from PyQt6 import QtWidgets, QtCore
from connection import Connection
import serial.tools.list_ports
from threading import Thread


class Motor_Control_Panel(QtWidgets.QWidget):
    def __init__(self):
        # super().__init__()
        super().__init__()
        self.connection = Connection('')
        self.setup_ui()

    def setup_ui(self):
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        content_layout = QtWidgets.QHBoxLayout()
        content_layout.setContentsMargins(5, 5, 5, 0)
        content_layout.setSpacing(10)
        content_layout.addLayout(self.setup_params())
        separator = QtWidgets.QFrame()
        separator.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        separator.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        content_layout.addWidget(separator)
        content_layout.addLayout(self.setup_rotation())
        main_layout.addLayout(content_layout)
        main_layout.addLayout(self.setup_connection_panel())
        main_layout.addLayout(self.setup_status_bar())

        self.setLayout(main_layout)

    def setup_connection_panel(self):
        connection_panel_layout = QtWidgets.QHBoxLayout()
        self.find_ports_btn = QtWidgets.QPushButton("Поиск")
        self.com_ports = QtWidgets.QComboBox()
        for port in serial.tools.list_ports.comports():
            self.com_ports.addItem(port.description, port)

        self.connect_btn = QtWidgets.QPushButton("Подключиться")
        self.connect_btn.setEnabled(False)
        if self.com_ports.count() > 0:
            self.connect_btn.setEnabled(True)

        self.disconnect_btn = QtWidgets.QPushButton("Отключиться")
        self.disconnect_btn.setEnabled(False)
        self.reconnect_btn = QtWidgets.QPushButton("Переподключиться")
        self.reconnect_btn.setEnabled(False)

        self.find_ports_btn.clicked.connect(self.on_find_ports_btn_clicked)
        self.connect_btn.clicked.connect(self.on_connect_btn_clicked)
        self.disconnect_btn.clicked.connect(self.on_disconnect_btn_clicked)
        self.reconnect_btn.clicked.connect(self.on_reconnect_btn_clicked)

        connection_panel_layout.addWidget(self.find_ports_btn)
        connection_panel_layout.addWidget(self.com_ports)
        connection_panel_layout.addWidget(self.connect_btn)
        connection_panel_layout.addWidget(self.disconnect_btn)
        connection_panel_layout.addWidget(self.reconnect_btn)

        return connection_panel_layout

    def setup_status_bar(self):
        status_bar_layout = QtWidgets.QHBoxLayout()
        self.status_bar = QtWidgets.QStatusBar()

        self.rotation_time_label = QtWidgets.QLabel()
        self.status_bar.addPermanentWidget(self.rotation_time_label)
        self.status_bar.setSizeGripEnabled(False)
        status_bar_layout.addWidget(self.status_bar)

        return status_bar_layout

    def setup_params(self):
        params_layout = QtWidgets.QVBoxLayout()
        params_layout.setSpacing(5)
        speed_layout = QtWidgets.QHBoxLayout()
        speed_label = QtWidgets.QLabel("Скорость")
        speed_layout.addWidget(speed_label)
        self.speed = QtWidgets.QSpinBox()
        self.speed.setMinimum(200)
        self.speed.setMaximum(51200)
        self.speed.setValue(6400)
        speed_layout.addWidget(self.speed)
        speed_desc_label = QtWidgets.QLabel("шаги/секунда")
        speed_layout.addWidget(speed_desc_label)
        self.speed.valueChanged.connect(self.on_speed_changed)
        params_layout.addLayout(speed_layout)

        speed_slider_layout = QtWidgets.QHBoxLayout()
        speed_slider_min_label = QtWidgets.QLabel("200")
        speed_slider_max_label = QtWidgets.QLabel("51200")
        self.speed_slider = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        self.speed_slider.setMinimum(200)
        self.speed_slider.setMaximum(51200)
        self.speed_slider.valueChanged.connect(self.on_speed_slider_changed)
        self.speed_slider.setEnabled(False)
        self.speed_slider.setSingleStep(1)
        self.speed_slider.setPageStep(1)
        self.speed_slider.setTickInterval(1)
        speed_slider_layout.addWidget(speed_slider_min_label)
        speed_slider_layout.addWidget(self.speed_slider)
        speed_slider_layout.addWidget(speed_slider_max_label)
        params_layout.addLayout(speed_slider_layout)
        separator = QtWidgets.QFrame()
        separator.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        separator.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        params_layout.addWidget(separator)

        time_layout = QtWidgets.QHBoxLayout()
        revolutions_label = QtWidgets.QLabel("Время вращения")
        time_layout.addWidget(revolutions_label)
        self.time_rotation = QtWidgets.QTimeEdit()
        self.time_rotation.setTime(QtCore.QTime(0, 0, 5))
        self.time_rotation.setDisplayFormat("mm:ss")
        time_layout.addWidget(self.time_rotation)
        params_layout.addLayout(time_layout)

        return params_layout

    def on_speed_changed(self):
        self.speed_slider.setValue(self.speed.value())

    def on_speed_slider_changed(self):
        self.speed.setValue(self.speed_slider.value())
        speed_command = 'S' + str(self.speed_slider.value())
        if self.connection.device.is_open:
            self.connection.transmit(speed_command.encode())

    def setup_rotation(self):
        rotation_layout = QtWidgets.QVBoxLayout()
        self.start_btn = QtWidgets.QPushButton("СТАРТ")
        self.start_btn.setEnabled(False)
        rotation_layout.addWidget(self.start_btn)
        self.stop_btn = QtWidgets.QPushButton("СТОП")
        self.stop_btn.setEnabled(False)
        rotation_layout.addWidget(self.stop_btn)
        infinite_layout = QtWidgets.QHBoxLayout()
        inf_label = QtWidgets.QLabel("Бесконечное вращение")
        self.infinite_flag = QtWidgets.QCheckBox()
        self.infinite_flag.setEnabled(False)
        infinite_layout.addWidget(inf_label)
        infinite_layout.addWidget(self.infinite_flag)
        rotation_layout.addLayout(infinite_layout)
        self.direction_btn = QtWidgets.QPushButton("Сменить направление")
        self.direction_btn.setEnabled(False)
        rotation_layout.addWidget(self.direction_btn)

        self.start_btn.clicked.connect(self.on_start_btn_clicked)
        self.stop_btn.clicked.connect(self.on_stop_btn_clicked)
        self.direction_btn.clicked.connect(self.on_direction_btn_clicked)
        self.infinite_flag.stateChanged.connect(self.on_infinite_flag_changed)

        return rotation_layout

    def on_start_btn_clicked(self):
        self.rotation_time = QtCore.QTime.currentTime()
        self.monitoring_motor_status()
        speed_command = 'S' + str(self.speed.value())
        self.connection.transmit(speed_command.encode())
        time.sleep(0.005)
        time_rotation_value = (self.time_rotation.time().minute() * 60 +
                               self.time_rotation.time().second())
        time_command = 'T' + str(time_rotation_value)
        time.sleep(0.005)
        self.connection.transmit(time_command.encode())
        time.sleep(0.005)
        if self.infinite_flag.isChecked():
            self.connection.transmit('I'.encode())
        else:
            self.connection.transmit('R'.encode())
        self.start_btn.setEnabled(False)
        self.status_bar.showMessage("Двигатель вращается")
        self.stop_btn.setEnabled(True)
        self.infinite_flag.setEnabled(False)

    def on_stop_btn_clicked(self):
        self.connection.transmit('P'.encode())
        self.stop_btn.setEnabled(False)
        self.start_btn.setEnabled(True)
        self.infinite_flag.setEnabled(True)

    def on_direction_btn_clicked(self):
        self.connection.transmit('D'.encode())

    def on_infinite_flag_changed(self):
        if self.infinite_flag.isChecked():
            self.direction_btn.setEnabled(True)
            self.speed_slider.setEnabled(True)
        else:
            self.direction_btn.setEnabled(False)
            self.speed_slider.setEnabled(False)

    def on_find_ports_btn_clicked(self):
        self.status_bar.showMessage("Поиск устройств...")
        self.com_ports.clear()
        for port in serial.tools.list_ports.comports():
            self.com_ports.addItem(port.description, port)
        self.status_bar.showMessage("Поиск устройств завершен")
        if self.com_ports.count() == 0:
            self.status_bar.showMessage("Устройства не найдены")

    def on_connect_btn_clicked(self):
        port_name = self.com_ports.itemData(
            self.com_ports.findText(self.com_ports.currentText())).device
        if self.connection.port_name != port_name:
            self.connection = Connection(port_name)
        self.connection.connect()
        if self.connection.device.is_open:
            self.status_bar.showMessage(
                "Подключено к " + self.connection.port_name)
            self.connect_btn.setEnabled(False)
            self.disconnect_btn.setEnabled(True)
            self.reconnect_btn.setEnabled(True)
            self.start_btn.setEnabled(True)
            self.infinite_flag.setEnabled(True)
        else:
            self.status_bar.showMessage("Ошибка подключения")

    def on_disconnect_btn_clicked(self):
        if self.connection.device.is_open:
            self.connection.transmit('P'.encode())
            self.connection.disconnect()
        if not self.connection.device.is_open:
            self.status_bar.showMessage(
                "Отключено от " + self.connection.port_name)
            self.connect_btn.setEnabled(True)
            self.disconnect_btn.setEnabled(False)
            self.reconnect_btn.setEnabled(False)
            self.start_btn.setEnabled(False)
            self.stop_btn.setEnabled(False)
            self.infinite_flag.setEnabled(False)
            self.speed_slider.setEnabled(False)
            self.infinite_flag.setChecked(False)
        else:
            self.status_bar.showMessage("Ошибка отключения")

    def on_reconnect_btn_clicked(self):
        self.on_disconnect_btn_clicked()
        self.on_connect_btn_clicked()

    def update_rotation_time(self):
        if self.rotation_time is not None:
            elapsed = QtCore.QTime.currentTime().secsTo(self.rotation_time)
            elapsed_time = QtCore.QTime(0, 0).addSecs(abs(elapsed))
            self.rotation_time_label.setText(
                f"Время вращения: {elapsed_time.toString('mm:ss')}")

    def monitoring_motor_status(self):
        self.connection.monitoring_stop_event.clear()
        self.connection.monitoring_thread = Thread(
            target=self.process_motor_status)
        self.connection.monitoring_thread.start()

    def process_motor_status(self):
        while not self.connection.monitoring_stop_event.is_set():
            self.update_rotation_time()
            status = self.connection.receive()
            if status == 'Y':
                self.stop_btn.setEnabled(False)
                self.start_btn.setEnabled(True)
                self.infinite_flag.setEnabled(True)
                self.status_bar.showMessage("Двигатель остановлен")
                self.connection.monitoring_stop_event.set()

    def monitoring_motor(self):
        self.connection.monitoring_thread.start()
