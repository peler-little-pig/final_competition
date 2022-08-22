import Window
import sys

import qdarkstyle
from PyQt5 import QtWidgets

from port import Port

if __name__ == '__main__':
    port = Port()

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Window.Ui_MainWindow()

    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))

    ui.setupUi(MainWindow) 

    ui.comboBox.addItems(port.get_port())

    ui.open.clicked.connect(lambda: port.begin(ui.comboBox.currentText(),ui.spinBox.value()))
    ui.load_data.clicked.connect(lambda: port.load_data())

    #禁止拉伸窗口大小
    MainWindow.setFixedSize(MainWindow.width(), MainWindow.height())

    MainWindow.show()
    sys.exit(app.exec_()) 