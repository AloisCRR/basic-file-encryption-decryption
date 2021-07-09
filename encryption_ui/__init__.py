import base64
from PyQt5 import QtCore, QtGui, QtWidgets
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class FileList(QtWidgets.QWidget):
    def __init__(self, parent: QtWidgets.QWidget = None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setup_default_drag_label()

    def setup_default_drag_label(self):
        self.file_list = QtWidgets.QVBoxLayout(self)

        self.create_file_list_label(
            "Arrastra los archivos aquí...", "empty_files_label"
        )

    def create_file_list_label(self, label_text: str, object_name: str):
        label = QtWidgets.QLabel(label_text, self)
        label.setFont(self.get_default_button_font())
        label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        label.setObjectName(object_name)

        self.file_list.addWidget(label)

    def get_default_button_font(self):
        font = QtGui.QFont()
        font.setPointSize(16)
        return font

    def dragEnterEvent(self, event: QtGui.QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event: QtGui.QDropEvent):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        for f in files:
            self.create_file_list_label(f, f"object_{f}")


class Ui_MainWindow:
    def setup_ui(self, MainWindow: QtWidgets.QMainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(801, 336)
        self.setup_central_widget(MainWindow)
        MainWindow.setCentralWidget(self.centralwidget)
        self.setup_file_list_frame()
        self.setup_action_buttons()
        self.setup_status_bar(MainWindow)
        MainWindow.setStatusBar(self.status_bar)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def get_default_size_policy(self):
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        return sizePolicy

    def get_default_button_font(self):
        font = QtGui.QFont()
        font.setPointSize(16)
        return font

    def setup_status_bar(self, MainWindow):
        self.status_bar = QtWidgets.QStatusBar(MainWindow)
        self.status_bar.setEnabled(True)
        self.status_bar.setObjectName("status_bar")

    def setup_action_buttons(self):
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 240, 781, 71))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.action_buttons = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.action_buttons.setContentsMargins(0, 0, 0, 0)
        self.action_buttons.setObjectName("action_buttons")
        self.encrypt = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.encrypt.clicked.connect(lambda: self.encrypt_files())
        self.encrypt.setSizePolicy(self.get_default_size_policy())
        self.encrypt.setFont(self.get_default_button_font())
        self.encrypt.setFlat(False)
        self.encrypt.setObjectName("encrypt")
        self.action_buttons.addWidget(self.encrypt)
        self.decrypt = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.decrypt.clicked.connect(lambda: self.decrypt_files())
        self.decrypt.setSizePolicy(self.get_default_size_policy())
        self.decrypt.setFont(self.get_default_button_font())
        self.decrypt.setObjectName("decrypt")
        self.action_buttons.addWidget(self.decrypt)

    def setup_file_list_frame(self):
        self.file_list_widget = FileList(self.centralwidget)

        self.file_list_widget.setGeometry(QtCore.QRect(10, 30, 781, 191))
        self.file_list_widget.setObjectName("file_list")

    def setup_central_widget(self, MainWindow: QtWidgets.QMainWindow):
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

    def encrypt_files(self):
        text, ok = QtWidgets.QInputDialog.getText(
            self.centralwidget,
            "Encriptar archivos",
            "Ingrese una contraseña",
            QtWidgets.QLineEdit.Password,
        )

        files = self.file_list_widget.findChildren(QtWidgets.QLabel)

        if ok:

            salt = b"q\xe3Q5\x8c\x19~\x17\xcb\x88\xc6A\xb8j\xb4\x85"

            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256,
                salt=salt,
                length=32,
                iterations=10,
                backend=default_backend(),
            )

            key = base64.urlsafe_b64encode(kdf.derive(text.encode()))

            print(f"Llave para desbloquear: {key.decode()}")

            cipher = Fernet(key)

            for f in files:
                if f.objectName() == "empty_files_label":
                    continue

                with open(f.text(), "rb") as target_file:
                    e_file = target_file.read()

                encrypted_file = cipher.encrypt(e_file)

                with open(f.text(), "wb") as ef:
                    ef.write(encrypted_file)

    def decrypt_files(self):
        text, ok = QtWidgets.QInputDialog.getText(
            self.centralwidget,
            "Desencriptar archivos",
            "Ingrese su llave para desencriptar",
            QtWidgets.QLineEdit.Password,
        )

        files = self.file_list_widget.findChildren(QtWidgets.QLabel)

        if ok:
            cipher = Fernet(text.encode())

            for f in files:
                if f.objectName() == "empty_files_label":
                    continue

                with open(f.text(), "rb") as target_file:
                    encrypted_data = target_file.read()

                decrypted_file = cipher.decrypt(encrypted_data)

                with open(f.text(), "wb") as ef:
                    ef.write(decrypted_file)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.encrypt.setText(_translate("MainWindow", "Encriptar"))
        self.decrypt.setText(_translate("MainWindow", "Desencriptar"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setup_ui(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
