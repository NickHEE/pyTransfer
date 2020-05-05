import serial, sys, time, json, os, csv
import serial.tools.list_ports

from PyQt5 import QtCore, QtGui, QtWidgets

vid = 1155
pid = 14155

# {
# 	'6843': [{'fName': ..., 'Timestamps': [], 'MagData': []}, {...}, ...}
# 	],
#
# 	'2345': [ ...
# 	]
# }

class MainWindow(QtWidgets.QStackedWidget):

    def __init__(self):
        super().__init__()

        self.resize(480, 320)
        self.port = None
        self.deviceConnected = False

        self.ser = serial.serial_for_url('loop://', timeout=1, baudrate=115200)
        #self.ser.set_buffer_size(rx_size=1000000, tx_size=1000000)
        self.ser.write(bytes('Test', encoding='ascii'))
        time.sleep(0.5)
        print(self.ser.read_all())

        self.waitingLabel = QtWidgets.QLabel('Waiting for EMF monitor...')
        self.waitingLabel.setSizePolicy(QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Expanding)
        self.waitingLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.transferPage = TransferPage(self.ser)

        self.checkSerialTimer = QtCore.QTimer()
        self.checkSerialTimer.timeout.connect(self.checkSerial)
        self.checkSerialTimer.start(500)

        self.addWidget(self.waitingLabel)
        self.addWidget(self.transferPage)
        self.setCurrentWidget(self.waitingLabel)
        self.show()

        ports = serial.tools.list_ports.comports()
        print([(p.device, p.name, p.description, p.hwid, p.vid, p.pid, p.product, p.manufacturer) for p in ports])

    def checkSerial(self):
        validPorts = [p for p in serial.tools.list_ports.comports() if p.vid == vid and p.pid == pid]

        if (validPorts):
            self.port = validPorts[0].device
            self.deviceConnected = True
            self.setCurrentWidget(self.transferPage)
        else:
            self.port = None
            self.deviceConnected = False


class TransferPage(QtWidgets.QWidget):

    def __init__(self, ser):
        super().__init__()

        self.ser = ser  # Parent.ser?

        self.vBox = QtWidgets.QVBoxLayout()
        self.hBox_u = QtWidgets.QHBoxLayout()
        self.hBox_b = QtWidgets.QHBoxLayout()
        self.vBox_list_l = QtWidgets.QVBoxLayout()
        self.vBox_list_r = QtWidgets.QVBoxLayout()
        self.vBox.addLayout(self.hBox_u, 5)
        self.vBox.addLayout(self.hBox_b, 1)
        self.hBox_u.addLayout(self.vBox_list_l, 3)
        self.hBox_u.addLayout(self.vBox_list_r, 1)

        self.fileTree = QtWidgets.QTreeView(self)
        self.employeeList = QtWidgets.QListView()
        self.employeeEdit = QtWidgets.QLineEdit()
        self.downloadButton = QtWidgets.QPushButton('Download')
        self.updateButton = QtWidgets.QPushButton('Update')
        self.deleteButton = QtWidgets.QPushButton('Delete')

        self.vBox_list_l.addWidget(self.fileTree)
        self.vBox_list_r.addWidget(self.employeeList, 4)
        self.vBox_list_r.addWidget(self.employeeEdit, 1)
        self.hBox_b.addWidget(self.downloadButton)
        self.hBox_b.addStretch()
        self.hBox_b.addWidget(self.updateButton)
        self.hBox_b.addWidget(self.deleteButton)

        self.setLayout(self.vBox)
        self.sendTestData()
        time.sleep(0.5)
        test = self.getData()
        print(test)

    def sendTestData(self):

        employeeData = {}

        for folder in os.listdir(r'./csvs'):
            files = []
            for fName in os.listdir(r'./csvs/' + folder):
                with open(os.path.join(r'./csvs/' + folder, fName)) as f:

                    timestamps = []
                    magData = []

                    reader = csv.DictReader(f, fieldnames=["Timestamp", "MagData"])
                    next(reader, None)
                    for row in reader:
                        timestamps.append(row["Timestamp"])
                        magData.append(row["MagData"])

                    data = {"fName": fName, "Timestamps": timestamps, "MagData": magData}
                    files.append(data)

            employeeData[folder] = files

        testData = bytes(str(employeeData), encoding='ascii')
        self.ser.write(testData)

    def getData(self):
        data = self.ser.read_all()
        return json.loads(data.replace(b"'", b'"').decode('ascii'))



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())


