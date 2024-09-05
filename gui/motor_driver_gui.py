from PyQt6 import QtWidgets
from motor_control_panel import Motor_Control_Panel


class Motor_Driver_GUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Motor Driver")
        self.setup_ui()

    def setup_ui(self):
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0);

        self.motor_panel_1 = Motor_Control_Panel()
        self.motor_panel_2 = Motor_Control_Panel()

        separator = QtWidgets.QFrame()
        separator.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        separator.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)

        main_layout.addWidget(self.motor_panel_1)
        main_layout.addWidget(separator)
        main_layout.addWidget(self.motor_panel_2)

        self.setLayout(main_layout)
        self.adjustSize()
        self.setFixedSize(self.size())

    def closeEvent(self, event):
        if self.motor_panel_1.connection.device.is_open:
            self.motor_panel_1.connection.transmit('P'.encode())
            self.motor_panel_1.connection.disconnect()
        if self.motor_panel_2.connection.device.is_open:
            self.motor_panel_2.connection.transmit('P'.encode())
            self.motor_panel_2.connection.disconnect()
        event.accept()
