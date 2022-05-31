import sys

import numpy as np

from zadanie_1.gui.gui import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from zadanie_1.signal import Signal
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import json

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

    def create_hist(signal_value):
        plt.figure()

        if signal_value == results:
            signal_value.MATH[ui.comboBox_3.currentText()](signal_1, signal_2)

        if ui.comboBox_4.currentText() == '':
            plt.hist(signal_value.y_values)
        else:
            plt.hist(signal_value.y_values, bins=int(ui.comboBox_4.currentText()))

        if signal_value == signal_1:
            plt.savefig("hist_1.png", dpi=300)
            ui.label_15.setPixmap(QtGui.QPixmap("hist_1.png"))
        elif signal_value == signal_2:
            plt.savefig("hist_2.png", dpi=300)
            ui.label_16.setPixmap(QtGui.QPixmap("hist_2.png"))
        else:
            plt.savefig("hist_result.png", dpi=300)
            ui.label_17.setPixmap(QtGui.QPixmap("hist_result.png"))

    def print_statistic(signal_value):
        signal_value.calculate_all_statistics()
        signal_label = {signal_1: ui.label_19, signal_2: ui.label_20, results: ui.label_21}
        text = f"Wartość średnia: {signal_value.average}\n" \
               f"Wartość średnia bezwzględna: {signal_value.absolut_average}\n" \
               f"Wartość skuteczna: {signal_value.effective_value}\n" \
               f"Wariancja: {signal_value.variance}\n" \
               f"Moc średnia: {signal_value.power_average}"

        signal_label[signal_value].setText(text)
        signal_label[signal_value].setText(text)

    def _():
        return ""

    def update_values():
        signals = {signal_1: ui.comboBox.currentText, signal_2: ui.comboBox_2.currentText, results: _}

        for sig in signals.keys():
            if signals[sig]() != "FROM_FILE":
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
                    sig.name = ui.comboBox.currentText()
                elif sig == signal_2:
                    sig.generate(ui.comboBox_2.currentText())
                    sig.name = ui.comboBox_2.currentText()
            else:
                q_file = QtWidgets.QFileDialog()
                q_file.setFileMode(QtWidgets.QFileDialog.AnyFile)
                file = q_file.getOpenFileName()
                sig.load(file[0])
                ui.lineEdit.setText(str(sig.A))
                ui.lineEdit_2.setText(str(sig.t1))
                ui.lineEdit_3.setText(str(sig.d))
                ui.lineEdit_4.setText(str(sig.T))
                ui.lineEdit_5.setText(str(sig.kw))
                ui.lineEdit_6.setText(str(sig.jump_time))
                ui.lineEdit_7.setText(str(sig.possibility))
                ui.lineEdit_8.setText(str(sig.freq))

            # plots & statistics
            create_chart(sig)
            create_hist(sig)
            print_statistic(sig)

    def save():
        signals = {"signal_1": signal_1, "signal_2": signal_2, "results": results}
        signal_value = signals[ui.comboBox_5.currentText()]
        save_list = {
            "signal name": signal_value.name,
            "t1": signal_value.t1,
            "freq": signal_value.freq,
            "real": True,
            "size": len(signal_value.x_values),
            "x_values": list(signal_value.x_values),
            "y_values": list(signal_value.y_values),
            "A": signal_value.A,
            "d": signal_value.d,
            "T": signal_value.T,
            "kw": signal_value.kw,
            "jump_time": signal_value.jump_time,
            "possibility": signal_value.possibility
        }

        with open(f'{ui.comboBox_5.currentText()}.json', 'w') as file:
            json.dump(save_list, file)


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
    ui.comboBox_4.addItems(['', '5', '10', '15', '20'])
    ui.comboBox_5.addItems(["signal_1", "signal_2", "results"])
    ui.pushButton.clicked.connect(update_values)
    ui.pushButton_2.clicked.connect(save)

    MainWindow.show()
    sys.exit(app.exec_())
