from PySide6.QtWidgets import QApplication, QMainWindow, QLineEdit

from password_generator import password, buttons
from password_generator.ui.ui_main import Ui_MainWindow


class PasswordGenerator(QMainWindow):
    def __init__(self):
        super(PasswordGenerator, self).__init__()
        self.bad_passwords = password.get_bad_passwords()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.connect_slider_to_spinbox()
        self.ui.btn_visibility.clicked.connect(self.change_password_visibility)
        self.ui.btn_copy.clicked.connect(self.copy_to_clipboard)
        self.do_when_password_edit()
        for btn in buttons.GENERATE_PASSWORD:
            getattr(self.ui, btn).clicked.connect(self.set_password)

    def connect_slider_to_spinbox(self) -> None:
        self.ui.slider_length.valueChanged.connect(self.ui.spinbox_length.setValue)
        self.ui.spinbox_length.valueChanged.connect(self.ui.slider_length.setValue)
        self.ui.spinbox_length.valueChanged.connect(self.set_password)

    def get_characters(self) -> str:
        chars = ""

        for btn in buttons.Characters:
            if getattr(self.ui, btn.name).isChecked():
                chars += btn.value

        return chars

    def set_password(self) -> None:
        try:
            self.ui.line_password.setText(
                password.create_new(
                    length=self.ui.slider_length.value(),
                    characters=self.get_characters())
            )
        except IndexError:
            self.ui.line_password.clear()

        self.set_entropy()
        self.set_strength()

    def get_character_number(self) -> int:
        num = 0

        for btn in buttons.CHARACTER_NUMBER.items():
            if getattr(self.ui, btn[0]).isChecked():
                num += btn[1]

        return num

    def set_entropy(self) -> None:
        length = len(self.ui.line_password.text())
        char_num = self.get_character_number()

        self.ui.label_entropy.setText(
            f"Entropy: {password.get_entropy(length, char_num)} bit"
        )

    def set_strength(self) -> None:
        length = len(self.ui.line_password.text())
        char_num = self.get_character_number()

        for strength in password.StrengthToEntropy:
            if self.ui.line_password.text() in self.bad_passwords:
                self.ui.label_strength.setText('Is A BAD PASSWORD')
            if password.get_entropy(length, char_num) >= strength.value:
                self.ui.label_strength.setText(f"Strength: {strength.name}")

    def change_password_visibility(self) -> None:
        if self.ui.btn_visibility.isChecked():
            self.ui.line_password.setEchoMode(QLineEdit.Normal)
        else:
            self.ui.line_password.setEchoMode(QLineEdit.Password)

    def copy_to_clipboard(self) -> None:
        QApplication.clipboard().setText(self.ui.line_password.text())

    def do_when_password_edit(self) -> None:
        self.ui.line_password.textEdited.connect(self.set_entropy)
        self.ui.line_password.textEdited.connect(self.set_strength)
