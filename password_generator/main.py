import sys

from PySide6.QtWidgets import QApplication

from password_generator.core import PasswordGenerator


def main():
    app = QApplication(sys.argv)

    window = PasswordGenerator()
    window.show()

    sys.exit(app.exec())
