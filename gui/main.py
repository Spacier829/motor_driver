from PyQt6 import QtWidgets
import sys
from motor_driver_gui import Motor_Driver_GUI

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = Motor_Driver_GUI()
    win.show()
    app.exec()