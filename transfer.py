import serial, sys
import serial.tools.list_ports

from PyQt5 import QtCore, QtGui, QtWidgets
git 
class MainWindow(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.resize(480, 320)
        ports = serial.tools.list_ports.comports()
        print([(p.device, p.name, p.description, p.hwid, p.vid, p.pid, p.product, p.manufacturer) for p in ports])
        self.show()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())


