import sys

import numpy as np

from zadanie_1.gui.gui import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from zadanie_1.signal import Signal
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt


if __name__ == "__main__":

    def create_chart(signal_value):
        plt.figure()

        if signal_value == results:
            signal_value.MATH[ui.comboBox_3.currentText()](signal_1, signal_2)

        if signal_value == signal_1:
            if ui.comboBox.currentText() == "UNIT_IMPULSE" or ui.comboBox.currentText() == "IMPULSE_NOISE":
                plt.scatter(signal_value.x_values, signal_value.y_values)
            else:
                plt.plot(signal_value.x_values, signal_value.y_values)
            plt.savefig("signal_1.png", dpi=300)
            ui.label_12.setPixmap(QtGui.QPixmap("signal_1.png"))
        elif signal_value == signal_2:
            if ui.comboBox_2.currentText() == "UNIT_IMPULSE" or ui.comboBox.currentText() == "IMPULSE_NOISE":
                plt.scatter(signal_value.x_values, signal_value.y_values)
            else:
                plt.plot(signal_value.x_values, signal_value.y_values)
            plt.savefig("signal_2.png", dpi=300)
            ui.label_13.setPixmap(QtGui.QPixmap("signal_2.png"))
        else:
            # if ui.comboBox.currentText() == "UNIT_IMPULSE" or ui.comboBox.currentText() == "IMPULSE_NOISE":
            #     plt.scatter(signal_value.x_values, signal_value.y_values)
            # else:
            plt.plot(signal_value.x_values, signal_value.y_values)
            plt.savefig("signal_result.png", dpi=300)
            ui.label_14.setPixmap(QtGui.QPixmap("signal_result.png"))

    def update_values():
        signals = [signal_1, signal_2, results]
        for sig in signals:
            sig.A = float(ui.lineEdit.text())
            sig.t1 = float(ui.lineEdit_2.text())
            sig.d = float(ui.lineEdit_3.text())
            sig.T = float(ui.lineEdit_4.text())
            sig.kw = float(ui.lineEdit_5.text())
            sig.jump_time = float(ui.lineEdit_6.text())
            sig.possibility = float(ui.lineEdit_7.text())
            sig.freq = float(ui.lineEdit_8.text())
            if sig == signal_1:
                sig.generate(ui.comboBox.currentText())
            elif sig == signal_2:
                sig.generate(ui.comboBox_2.currentText())
            # plot
            create_chart(sig)
            # save
            # sig.save_to_file(signal_1, ui.comboBox.currentText())

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    signal_1 = Signal()
    signal_2 = Signal()
    results = Signal()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    ui.comboBox.addItems(signal_1.all_signals.keys())
    ui.comboBox_2.addItems(signal_1.all_signals.keys())
    ui.comboBox_3.addItems(["Dodawanie", "Odejmowanie", "Mnożenie", "Dzielenie"])
    ui.pushButton.clicked.connect(update_values)


    MainWindow.show()
    sys.exit(app.exec_())
