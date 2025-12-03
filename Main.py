import sys
import multiprocessing
import os

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QStyleFactory
from PyQt6.QtNetwork import QLocalServer, QLocalSocket
from PyQt6.QtCore import QByteArray
import ctypes
import MainWindow

from DB import *

APP_ID = "QuoteManagingApp"
_single_instance_server = None


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def set_app_id(app_id: str):
    try:
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
    except Exception:
        pass


def send_message_to_running_instance(app_id, message: str):
    socket = QLocalSocket()
    socket.connectToServer(app_id)
    if socket.waitForConnected(100):
        socket.write(QByteArray(message.encode("utf-8")))
        socket.flush()
        socket.waitForBytesWritten(100)
        socket.disconnectFromServer()
        return True
    return False


def start_single_instance_server(app_id, on_message):
    global _single_instance_server
    _single_instance_server = QLocalServer()

    # if server exists, clean
    try:
        QLocalServer.removeServer(app_id)
    except Exception:
        pass

    if not _single_instance_server.listen(app_id):
        return False

    def handle_new_connection():
        socket = _single_instance_server.nextPendingConnection()
        if not socket:
            return
        socket.readyRead.connect(lambda: on_message(str(socket.readAll(), "utf-8")))
        socket.disconnected.connect(socket.deleteLater)

    _single_instance_server.newConnection.connect(handle_new_connection)
    return True


if __name__ == "__main__":
    multiprocessing.freeze_support()

    # if instance runs: stop current and raise that instance
    if send_message_to_running_instance(APP_ID, "raise"):
        sys.exit(0)

    print(sys.platform)
    if sys.platform == "win32":
        set_app_id(APP_ID)

    app = QApplication(sys.argv)
    app.setStyle('fusion')
    db = DB()
    icon_path = resource_path("b.ico")
    print(f"path: {icon_path}")
    print(f"exists: {os.path.exists(icon_path)}")

    icon = QIcon(icon_path)
    print(f"null: {icon.isNull()}")

    app.setWindowIcon(icon)
    window = MainWindow.MainWindow(db)
    window.setWindowIcon(icon)

    window.resize(1000, 700)
    window.show()


    def on_message(message):
        if message == "raise":
            window.showNormal()
            window.raise_()
            window.activateWindow()


    start_single_instance_server(APP_ID, on_message)

    sys.exit(app.exec())