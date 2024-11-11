#!/usr/bin/env python3

import os
import shutil
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QFileDialog,
    QMessageBox,
    QVBoxLayout,
    QWidget,
    QPushButton,
    QListWidget,
    QHBoxLayout,
    QInputDialog,
)

class FileManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Файловый менеджер")
        self.setGeometry(100, 100, 600, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Основной компоновщик
        self.layout = QHBoxLayout(self.central_widget)

        # Список файлов
        self.file_list = QListWidget()
        self.layout.addWidget(self.file_list)

        # Компоновщик для кнопок
        self.button_layout = QVBoxLayout()

        self.btn_open = QPushButton("Открыть")
        self.btn_open.clicked.connect(self.open_directory)
        self.button_layout.addWidget(self.btn_open)

        self.btn_copy = QPushButton("Копировать")
        self.btn_copy.clicked.connect(self.copy_file)
        self.button_layout.addWidget(self.btn_copy)

        self.btn_move = QPushButton("Переместить")
        self.btn_move.clicked.connect(self.move_file)
        self.button_layout.addWidget(self.btn_move)

        self.btn_delete = QPushButton("Удалить")
        self.btn_delete.clicked.connect(self.delete_file)
        self.button_layout.addWidget(self.btn_delete)

        self.btn_new_folder = QPushButton("Создать папку")
        self.btn_new_folder.clicked.connect(self.create_folder)
        self.button_layout.addWidget(self.btn_new_folder)

        # Кнопка для отображения справки
        self.btn_help = QPushButton("Справка")
        self.btn_help.clicked.connect(self.show_help)
        self.button_layout.addWidget(self.btn_help)

        self.layout.addLayout(self.button_layout)

        self.current_path = ""

    def open_directory(self):
        self.current_path = QFileDialog.getExistingDirectory(self, "Выберите папку")
        if self.current_path:
            self.load_files()

    def load_files(self):
        self.file_list.clear()
        try:
            for file in os.listdir(self.current_path):
                self.file_list.addItem(file)
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", str(e))

    def copy_file(self):
        selected_item = self.file_list.currentItem()
        if not selected_item:
            return
        src = os.path.join(self.current_path, selected_item.text())
        dest = QFileDialog.getExistingDirectory(self, "Выберите папку для копирования")
        if dest:
            try:
                shutil.copy(src, dest)
                QMessageBox.information(self, "Успех", "Файл скопирован успешно!")
            except Exception as e:
                QMessageBox.warning(self, "Ошибка", str(e))

    def move_file(self):
        selected_item = self.file_list.currentItem()
        if not selected_item:
            return
        src = os.path.join(self.current_path, selected_item.text())
        dest = QFileDialog.getExistingDirectory(self, "Выберите папку для перемещения")
        if dest:
            try:
                shutil.move(src, dest)
                QMessageBox.information(self, "Успех", "Файл перемещен успешно!")
                self.load_files()
            except Exception as e:
                QMessageBox.warning(self, "Ошибка", str(e))

    def delete_file(self):
        selected_item = self.file_list.currentItem()
        if not selected_item:
            return
        file_path = os.path.join(self.current_path, selected_item.text())
        reply = QMessageBox.question(self, "Подтверждение", "Вы действительно хотите удалить этот файл?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                os.remove(file_path)
                QMessageBox.information(self, "Успех", "Файл удален успешно!")
                self.load_files()
            except Exception as e:
                QMessageBox.warning(self, "Ошибка", str(e))

    def create_folder(self):
        folder_name, ok = QInputDialog.getText(self, "Создать папку", "Введите имя новой папки:")
        if ok and folder_name:
            new_folder_path = os.path.join(self.current_path, folder_name)
            try:
                os.mkdir(new_folder_path)
                QMessageBox.information(self, "Успех", "Папка создана успешно!")
                self.load_files()
            except Exception as e:
                QMessageBox.warning(self, "Ошибка", str(e))

    def show_help(self):
        help_text = (
            "Файловый менеджер\n\n"
            "Функции программы:\n"
            "1. Открытие папки: Выберите папку для работы с файлами.\n"
            "2. Копирование файлов: Выберите файл и скопируйте его в другую папку.\n"
            "3. Перемещение файлов: Переместите файл в другую папку.\n"
            "4. Удаление файлов: Удалите выбранный файл из текущей папки.\n"
            "5. Создание папки: Создайте новую папку в текущей директории."
        )
        QMessageBox.information(self, "Справка", help_text)

if __name__ == "__main__":
    app = QApplication([])
    file_manager = FileManager()
    file_manager.show()
    app.exec_()
