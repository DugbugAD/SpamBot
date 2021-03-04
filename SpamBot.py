'''
Version: 3.8.7
Libraries:
- Os (default with python)
- Sys (default with python)
- Time (default with python)
- PyQt5 (pip3 install pyqt5)
- Pyautogui (pip3 install pyautogui)
Tested on macOS 11.1 Big Sur
'''


import os
import sys
from PyQt5.QtWidgets import QApplication, QGridLayout, QWidget, QLabel, QSpinBox, QMessageBox, QPushButton, QLineEdit, QTextEdit
from PyQt5.QtGui import QFont
from PyQt5.Qt import Qt
import pyautogui
import time


class PopUpWindow(QMessageBox):
    def __init__(self, title, text, informative_text, icon):
        super().__init__()
        self.setWindowTitle(title)
        font = QFont("Futura", 16)
        self.setFont(font)
        self.setText(text)
        self.setInformativeText(informative_text)
        self.setIcon(icon)
        self.exec()


class MainWindow(QWidget):
    message = None
    delay = None
    number = None
    paragraph = None

    def __init__(self):
        super().__init__()
        self.setFixedSize(900, 600)
        self.setWindowTitle("Spam Bot")
        self.layout = QGridLayout(self)

        for lblText in ["Message to Spam:", "Number of Messages:", "Delay (Seconds):"]:
            lbl = QLabel(self, text=lblText)
            lbl.setStyleSheet("""
            QLabel {
            background-color: None;
            border-radius: 10px;
            color: black;
            font: 24pt Futura;
            font-weight: bold;
            }
            """)

            self.layout.addWidget(
                lbl, ["Message to Spam:", "Number of Messages:", "Delay (Seconds):"].index(lblText), 0)

        self.message = QLineEdit(self)
        self.layout.addWidget(self.message, 0, 1)

        self.num = QSpinBox(self)
        self.num.setRange(1, 10000)
        self.num.setValue(100)
        self.num.setAttribute(Qt.WA_MacShowFocusRect, 0)
        self.layout.addWidget(self.num, 1, 1)

        self.delay = QSpinBox(self)
        self.delay.setRange(0, 100)
        self.delay.setValue(0)
        self.delay.setAttribute(Qt.WA_MacShowFocusRect, 0)
        self.layout.addWidget(self.delay, 2, 1)
        self.setLayout(self.layout)

        self.paragraph = QTextEdit(self)
        self.paragraph.setText(
            "Enter a paragraph in this text box, and we will spam it all. Line. By. Line.")
        self.paragraph.setFixedSize(860, 350)
        self.layout.addWidget(self.paragraph, 3, 0, 3, 3)

        self.done = QPushButton(self, text="DONE")
        self.done.setFixedSize(150, 40)
        self.done.setStyleSheet("""
            QPushButton {
            background-color: blue;
            border-radius: 10px;
            color: white;
            font: 24pt Futura;
            }

            QPushButton::pressed {
            background-color: green;
            }
        """)
        self.done.move(725, 550)
        self.done.clicked.connect(self.spam)

    def spam(self):
        if self.paragraph.toPlainText() == "Enter a paragraph in this text box, and we will spam it all. Line. By. Line.":
            MainWindow.message = self.message.text()
            if MainWindow.message == "":
                PopUpWindow("Invalid Value", "Invalid Message",
                            None, QMessageBox.Critical)
                return
            MainWindow.number = self.num.value()
            MainWindow.delay = self.delay.value()
            pyautogui.PAUSE = float(MainWindow.delay)
            self.destroy()
            time.sleep(10)

            start_time = time.perf_counter()
            for i in range(MainWindow.number):
                try:
                    pyautogui.typewrite(f"{MainWindow.message}\n")
                except pyautogui.FailSafeException:
                    os._exit(0)
            end_time = time.perf_counter()

            PopUpWindow("Process Completed",
                        f"Spam Process Completed in {end_time - start_time:0.3f} seconds", None, QMessageBox.Information)
            sys.exit(0)

        else:
            pyautogui.PAUSE = float(self.delay.value())
            MainWindow.paragraph = self.paragraph.toPlainText()
            self.destroy()
            time.sleep(10)
            with open("SpamFile.txt", "w") as file:
                file.writelines(MainWindow.paragraph)
            with open("SpamFile.txt", "r") as file:
                lines = file.readlines()
            os.remove("SpamFile.txt")
            start_time = time.perf_counter()
            for line in lines:
                try:
                    pyautogui.typewrite(line)
                except pyautogui.FailSafeException:
                    os._exit(0)
            end_time = time.perf_counter()
            PopUpWindow("Process Completed",
                        f"Spam Process Completed in {end_time - start_time:0.3f} seconds", None, QMessageBox.Information)
            sys.exit(0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet("""
            QLineEdit {
            background-color: None;
            color: black;
            font: 18pt Futura;
            }

            QSpinBox {
            color: black;
            font: 20pt Futura;
            }

            QTextEdit {
            background-color: None;
            color: black;
            font: 18pt Futura;
            }
        """)

    window = MainWindow()
    PopUpWindow("Spam Bot",
                "Enter in the following information, then switch to the text box you would like to spam. Spamming will start promptly in 10 seconds after you close the information window. To stop the program, move your cursor to the top left corner of your computer/laptop to enable the failsafe and kill the program.",
                None, QMessageBox.Critical)
    window.show()

    sys.exit(app.exec())
