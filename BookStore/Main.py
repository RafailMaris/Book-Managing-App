
import socket
import subprocess
import sys
import multiprocessing
import os
from google import genai
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QStyleFactory
from PyQt6.QtNetwork import QLocalServer, QLocalSocket
from PyQt6.QtCore import QByteArray
import ctypes
import MainWindow

from DB import *
from LogicLevel import LogicLevel

APP_ID = "QuoteManagingApp"
_single_instance_server = None


def resource_path(relative_path):
    try:

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

def is_server_running(host="127.0.0.1", port=8000):
    try:
        with socket.create_connection((host, port), timeout=0.3):
            return True
    except OSError:
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



    # from groq import Groq
    #
    # client = Groq(api_key="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")
    #
    # completion = client.chat.completions.create(
    #     model="llama-3.3-70b-versatile",
    #     messages=[{"role": "user", "content": "Summarize the book 'La Medeleni' by Ionel Teodoreanu."}]
    # )
    #
    # print(completion.choices[0].message.content)

    django_process = None

    if not is_server_running():
        django_process = subprocess.Popen(
            ['python', '../manage.py', 'runserver', '8000'],
            #stdout=subprocess.DEVNULL,
            #stderr=subprocess.DEVNULL
        )

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
    logicLevel = LogicLevel(db)
    icon_path = resource_path("b.ico")
    print(f"path: {icon_path}")
    print(f"exists: {os.path.exists(icon_path)}")

    icon = QIcon(icon_path)
    print(f"null: {icon.isNull()}")

    app.setWindowIcon(icon)
    window = MainWindow.MainWindow(db,logicLevel)
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