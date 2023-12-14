#from argostranslate import package
#package.install_from_path('translate-en_es-1_0.argosmodel')
#package.install_from_path('translate-es_en-1_0.argosmodel')
#download packages from https://www.argosopentech.com/argospm/index/

import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QPlainTextEdit, QPushButton, QHBoxLayout
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

# Assuming 'functions' module has the required functions
from package import functions

from_language, to_language = "en", "es"

class TranslatorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Offline Translator')
        self.setGeometry(0, 0, 1400, 800)
        self.center_on_screen()

        # Set window icon
        self.setWindowIcon(QIcon('./icons/icon.png'))
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)

        self.text_input = QPlainTextEdit(self)
        self.text_input.setPlaceholderText('English...')
        self.text_input.setMaximumBlockCount(100)  # Set a maximum of 100 characters per line

        self.translated_output = QPlainTextEdit(self)
        self.translated_output.setReadOnly(True)
        self.translated_output.setPlaceholderText('Spanish...')

        self.translate_button = QPushButton('Translate', self)
        self.listen_button = QPushButton('Listen', self)
        self.switch_button = QPushButton('Switch', self)

        layout = QVBoxLayout(self)

        form_layout = QHBoxLayout()
        form_layout.addWidget(self.text_input)
        form_layout.addWidget(self.translated_output)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.translate_button)
        button_layout.addWidget(self.switch_button)
        button_layout.addWidget(self.listen_button)

        layout.addLayout(form_layout)
        layout.addLayout(button_layout)

        self.translate_button.clicked.connect(self.translate_text)
        self.listen_button.clicked.connect(self.speak_text)
        self.switch_button.clicked.connect(self.switch_language)

        # Disable buttons initially
        self.translate_button.setEnabled(False)
        self.listen_button.setEnabled(False)

        # Connect input validation
        self.text_input.textChanged.connect(self.enable_buttons)
        self.translated_output.textChanged.connect(self.enable_buttons)

        # Apply styles
        self.setStyleSheet('''
            QWidget {
                background-color: #2c3e50; /* Change to your preferred background color */
            }

            QPlainTextEdit {
                border: 2px solid #3498db; /* Change to your preferred border color */
                border-radius: 8px;
                padding: 8px;
                background-color: #ecf0f1; /* Change to your preferred background color */
                font-size: 30px; /* Adjust the font size as needed */
                color: #2c3e50; /* Change to your preferred text color */
            }

            QPushButton {
                border: 2px solid #e74c3c; /* Change to your preferred border color */
                border-radius: 8px;
                padding: 8px 16px;
                background-color: #e74c3c; /* Change to your preferred background color */
                color: white;
                font-size: 40px; /* Adjust the font size as needed */
            }

            QPushButton:hover {
                background-color: #c0392b; /* Change to your preferred hover background color */
                border-color: #c0392b; /* Change to your preferred hover border color */
            }
        ''')

    def enable_buttons(self):
        # Enable buttons only if there is text to translate
        text_to_translate = self.text_input.toPlainText().strip()
        translated_text = self.translated_output.toPlainText().strip()
        self.translate_button.setEnabled(bool(text_to_translate))
        self.listen_button.setEnabled(bool(translated_text))

    def translate_text(self):
        text_to_translate = self.text_input.toPlainText()
        translated_text = functions.translate_text(
            text_to_translate,
            from_language,
            to_language
        )
        self.translated_output.setPlainText(translated_text)

    def speak_text(self):
        text_to_speak = self.translated_output.toPlainText()
        functions.text_to_speech(text_to_speak)

    def switch_language(self):
        global from_language, to_language
        from_language, to_language = to_language, from_language
        text_input_placeholder = self.translated_output.placeholderText()
        translated_output_placeholder = self.text_input.placeholderText()
        self.text_input.setPlaceholderText(text_input_placeholder)
        self.translated_output.setPlaceholderText(translated_output_placeholder)

    def center_on_screen(self):
        screen = QApplication.primaryScreen()
        center_point = screen.availableGeometry().center()
        self.move(center_point - self.rect().center())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    translator_app = TranslatorApp()
    translator_app.show()
    sys.exit(app.exec_())
