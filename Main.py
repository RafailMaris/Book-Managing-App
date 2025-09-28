import sys
import multiprocessing

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QStyleFactory
from PyQt6.QtNetwork import QLocalServer, QLocalSocket
from PyQt6.QtCore import QByteArray

import MainWindow
from DB import *

APP_ID = "QuoteManagingApp"
_single_instance_server = None

#if finds running instance, returns true
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
    print(QStyleFactory.keys())
    app = QApplication(sys.argv)
    app.setStyle('fusion')
    db = DB()
    window = MainWindow.MainWindow(db)
    window.setWindowIcon(QIcon("b.ico"))
    window.resize(1000, 700)
    window.show()


    def on_message(message):
        if message == "raise":
            window.showNormal()
            window.raise_()
            window.activateWindow()

    start_single_instance_server(APP_ID, on_message)

    sys.exit(app.exec())
