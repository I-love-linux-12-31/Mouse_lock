import sys

from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import QCoreApplication, Qt, QTimer

from PyQt6.QtWidgets import (
    QApplication,
    QSystemTrayIcon,
    QWidget,
    QPushButton,
    QComboBox,
    QLabel,
    QMenu,
    QSpinBox,
    QCheckBox

)
from PyQt6.uic import loadUi

import backend


class MainWindow(QWidget):
    btn_exit: QPushButton
    btn_help: QPushButton
    btn_lock: QPushButton
    btn_unlock: QPushButton

    display_selection: QComboBox
    # label: QLabel
    update_interval_input: QSpinBox
    border_collisions_politic: QCheckBox

    def __init__(self):
        super().__init__()
        loadUi('main.ui', self)

        self.mouse_grab_on = False

        displays = backend.get_display_info()
        for disp in displays:
            self.display_selection.addItem(disp)
        self.display_selection.setCurrentText(backend.current_display["name"])

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.work_function)
        self.timer.start(1000 // 64) #  64 calls peer sec


        self.btn_exit.clicked.connect(lambda: sys.exit(0))

        self.btn_unlock.clicked.connect(self.free_mouse)
        self.btn_lock.clicked.connect(self.grab_mouse)

        self.display_selection.currentTextChanged.connect(self.change_display_selection)
        self.update_interval_input.valueChanged.connect(self.update_work_function_timer)
        self.border_collisions_politic.checkStateChanged.connect(self.change_border_collisions_politic)

    def update_work_function_timer(self):
        self.timer.setInterval(1000 // self.update_interval_input.value())

    def change_border_collisions_politic(self):
        backend.restrict_border_collisions = self.border_collisions_politic.isChecked()

    def work_function(self):
        if self.mouse_grab_on:
            backend.work_func()

    def change_display_selection(self):
        backend.select_display(self.display_selection.currentText())

    def closeEvent(self, event):
        event.ignore()
        self.hide()

    def grab_mouse(self):
        self.mouse_grab_on = True
        self.btn_lock.setEnabled(False)
        self.btn_unlock.setEnabled(True)

    def free_mouse(self):
        self.mouse_grab_on = False
        self.btn_lock.setEnabled(True)
        self.btn_unlock.setEnabled(False)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.free_mouse()
        else:
            super().keyPressEvent(event)

class SystemTrayIcon(QSystemTrayIcon):
    def __init__(self, icon: QIcon, window: MainWindow, parent=None):
        super().__init__(icon, parent)

        self.window = window

        self.setToolTip("Mouse lock")
        menu = QMenu(parent)

        grab_action = QAction("Grab mouse", self)
        grab_action.triggered.connect(self.window.grab_mouse)
        menu.addAction(grab_action)

        unlock_action = QAction("Unlock mouse", self)
        unlock_action.triggered.connect(self.window.free_mouse)
        menu.addAction(unlock_action)

        show_window_action = QAction("Show window", self)
        show_window_action.triggered.connect(lambda: window.show())
        menu.addAction(show_window_action)

        exit_action = QAction("Exit", self)
        exit_action.setIcon(QIcon.fromTheme("application-exit"))
        exit_action.triggered.connect(QCoreApplication.instance().quit)
        menu.addAction(exit_action)

        self.setContextMenu(menu)


def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    window = MainWindow()
    window.show()

    tray_icon = SystemTrayIcon(QIcon.fromTheme("input-mouse"), window)
    tray_icon.show()

    # app.setWindowIcon(QIcon.fromTheme("input-mouse"))
    # window.setWindowIcon(QIcon.fromTheme("input-mouse"))
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
