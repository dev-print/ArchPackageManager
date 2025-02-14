import sys
import os
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel, QMessageBox, QInputDialog, QHBoxLayout, QFrame, QTextEdit, QListWidget, QListWidgetItem, QStyledItemDelegate
from PyQt5.QtGui import QFont, QColor, QPalette, QPainter
from PyQt5.QtCore import Qt, QRect

os.environ["QT_QPA_PLATFORM"] = "xcb"

class SpacingDelegate(QStyledItemDelegate):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def sizeHint(self, option, index):
        size = super().sizeHint(option, index)
        size.setHeight(size.height() + 20)  # Add extra space between items
        return size

    def paint(self, painter, option, index):
        painter.save()
        painter.setRenderHint(QPainter.Antialiasing, True)
        super().paint(painter, option, index)
        painter.restore()

class PackageManagerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Simple Arch Package Manager')
        self.setGeometry(100, 100, 600, 400)

        # Set dark theme
        self.setStyleSheet("""
            QWidget {
                background-color: #2E2E2E;
                color: #FFFFFF;
                font-family: Arial, sans-serif;
                font-size: 14px;
            }
            QPushButton {
                background-color: #4B0082;
                color: #FFFFFF;
                border: none;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #6A0DAD;
            }
            QLabel {
                font-size: 18px;
                font-weight: bold;
            }
            QLineEdit {
                background-color: #3E3E3E;
                color: #FFFFFF;
                border: 1px solid #4B0082;
                padding: 5px;
                border-radius: 5px;
            }
            QTextEdit {
                background-color: #3E3E3E;
                color: #FFFFFF;
                border: 1px solid #4B0082;
                padding: 5px;
                border-radius: 5px;
            }
            QListWidget {
                background-color: #3E3E3E;
                color: #FFFFFF;
                border: 1px solid #4B0082;
                padding: 5px;
                border-radius: 5px;
                margin-bottom: 10px;
            }
            QMessageBox {
                background-color: #2E2E2E;
                color: #FFFFFF;
            }
        """)

        layout = QVBoxLayout()

        self.label = QLabel('Welcome to the Simple Arch Package Manager', self)
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        self.search_button = QPushButton('Search for a package', self)
        self.search_button.clicked.connect(self.search_package)
        layout.addWidget(self.search_button)

        self.installed_button = QPushButton('View installed packages', self)
        self.installed_button.clicked.connect(self.view_installed_packages)
        layout.addWidget(self.installed_button)

        self.exit_button = QPushButton('Exit', self)
        self.exit_button.clicked.connect(self.close)
        layout.addWidget(self.exit_button)

        self.setLayout(layout)

    def search_package(self):
        package_name, ok = QInputDialog.getText(self, 'Search for a package', 'Enter package name:')
        if ok and package_name:
            result = os.popen(f"pacman -Ss {package_name}").read()
            self.show_search_results(result)

    def show_search_results(self, result):
        self.result_window = QWidget()
        self.result_window.setWindowTitle('Search Results')
        self.result_window.setGeometry(150, 150, 600, 400)
        self.result_window.setStyleSheet("""
            QWidget {
                background-color: #2E2E2E;
                color: #FFFFFF;
                font-family: Arial, sans-serif;
                font-size: 14px;
            }
            QListWidget {
                background-color: #3E3E3E;
                color: #FFFFFF;
                border: 1px solid #4B0082;
                padding: 5px;
                border-radius: 5px;
                margin-bottom: 10px;
            }
            QPushButton {
                background-color: #4B0082;
                color: #FFFFFF;
                border: none;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #6A0DAD;
            }
        """)

        layout = QVBoxLayout()

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search packages...")
        self.search_bar.textChanged.connect(self.filter_search_results)
        layout.addWidget(self.search_bar)

        self.list_widget = QListWidget()
        self.list_widget.setItemDelegate(SpacingDelegate(self.list_widget))
        layout.addWidget(self.list_widget)

        self.search_results = result.split('\n')
        self.original_search_results = self.search_results.copy()
        self.update_search_results()

        self.download_button = QPushButton('Download Package')
        self.download_button.clicked.connect(self.download_package)
        layout.addWidget(self.download_button)

        self.info_button = QPushButton('Show Info')
        self.info_button.clicked.connect(self.show_info)
        layout.addWidget(self.info_button)

        self.close_button = QPushButton('Close')
        self.close_button.clicked.connect(self.result_window.close)
        layout.addWidget(self.close_button)

        self.result_window.setLayout(layout)
        self.result_window.show()

    def update_search_results(self):
        self.list_widget.clear()
        for line in self.search_results:
            if line.strip() and '/' in line:
                parts = line.split(' ', 1)
                if len(parts[0].split('/')) > 1:
                    package_name = parts[0].split('/')[1]  # Extract the package name correctly
                    description = parts[1] if len(parts) > 1 else ''
                    item = QListWidgetItem(f"{package_name}\n{description}")
                    self.list_widget.addItem(item)

    def filter_search_results(self):
        query = self.search_bar.text().lower()
        if query:
            self.search_results = [line for line in self.original_search_results if query in line.lower()]
        else:
            self.search_results = self.original_search_results
        self.update_search_results()

    def download_package(self):
        selected_item = self.list_widget.currentItem()
        if selected_item:
            package_name = selected_item.text().split('\n')[0]
            reply = QMessageBox.question(self, 'Confirmation', f'Do you really want to install {package_name}?',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                password, ok = QInputDialog.getText(self, 'Password Required', 'Enter your password:', QLineEdit.Password)
                if ok:
                    process = subprocess.Popen(['sudo', '-S', 'pacman', '-S', '--noconfirm', package_name], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    stdout, stderr = process.communicate(input=password + '\n')
                    if process.returncode == 0:
                        QMessageBox.information(self, 'Install Result', f'Installed package: {package_name}')
                    else:
                        QMessageBox.warning(self, 'Install Failed', stderr)

    def show_info(self):
        selected_item = self.list_widget.currentItem()
        if selected_item:
            package_name = selected_item.text().split('\n')[0]
            result = os.popen(f"pacman -Qi {package_name}").read()
            self.result_window.hide()
            self.show_info_page(package_name, result)

    def show_info_page(self, package_name, info):
        self.info_window = QWidget()
        self.info_window.setWindowTitle(f'Info: {package_name}')
        self.info_window.setGeometry(150, 150, 600, 400)
        self.info_window.setStyleSheet("""
            QWidget {
                background-color: #2E2E2E;
                color: #FFFFFF;
                font-family: Arial, sans-serif;
                font-size: 14px;
            }
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #FFFFFF;
                margin-bottom: 10px;
            }
            QPushButton {
                background-color: #4B0082;
                color: #FFFFFF;
                border: none;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #6A0DAD;
            }
            QFrame {
                border: 1px solid #4B0082;
                border-radius: 5px;
                padding: 10px;
                margin-bottom: 10px;
            }
        """)

        layout = QVBoxLayout()

        self.info_label = QLabel(f'Information for {package_name}')
        self.info_label.setAlignment(Qt.AlignCenter)
        self.info_label.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(self.info_label)

        # Extract relevant information
        info_lines = info.split('\n')
        name = version = arch = description = ""
        for line in info_lines:
            if line.startswith("Name"):
                name = line
            elif line.startswith("Version"):
                version = line
            elif line.startswith("Architecture"):
                arch = line
            elif line.startswith("Description"):
                description = line

        info_frame = QFrame()
        info_layout = QVBoxLayout()

        self.name_label = QLabel(name)
        self.name_label.setStyleSheet("font-size: 16px; margin-bottom: 5px;")
        info_layout.addWidget(self.name_label)

        self.version_label = QLabel(version)
        self.version_label.setStyleSheet("font-size: 16px; margin-bottom: 5px;")
        info_layout.addWidget(self.version_label)

        self.arch_label = QLabel(arch)
        self.arch_label.setStyleSheet("font-size: 16px; margin-bottom: 5px;")
        info_layout.addWidget(self.arch_label)

        self.description_label = QLabel(description)
        self.description_label.setAlignment(Qt.AlignCenter)
        self.description_label.setStyleSheet("font-size: 16px; margin-bottom: 10px;")
        info_layout.addWidget(self.description_label)

        info_frame.setLayout(info_layout)
        layout.addWidget(info_frame)

        self.install_button = QPushButton('Install Package')
        self.install_button.clicked.connect(lambda: self.install_package(package_name))
        layout.addWidget(self.install_button)

        self.back_button = QPushButton('Back')
        self.back_button.clicked.connect(self.back_to_search)
        layout.addWidget(self.back_button)

        self.info_window.setLayout(layout)
        self.info_window.show()

    def install_package(self, package_name):
        password, ok = QInputDialog.getText(self, 'Password Required', 'Enter your password:', QLineEdit.Password)
        if ok:
            process = subprocess.Popen(['sudo', '-S', 'pacman', '-S', '--noconfirm', package_name], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate(input=password + '\n')
            if process.returncode == 0:
                QMessageBox.information(self, 'Install Result', f'Installed package: {package_name}')
            else:
                QMessageBox.warning(self, 'Install Failed', stderr)

    def back_to_search(self):
        self.info_window.close()
        self.result_window.show()

    def view_installed_packages(self):
        result = os.popen("pacman -Q").read()
        self.show_installed_packages(result)

    def show_installed_packages(self, result):
        self.installed_window = QWidget()
        self.installed_window.setWindowTitle('Installed Packages')
        self.installed_window.setGeometry(150, 150, 600, 400)
        self.installed_window.setStyleSheet("""
            QWidget {
                background-color: #2E2E2E;
                color: #FFFFFF;
                font-family: Arial, sans-serif;
                font-size: 14px;
            }
            QListWidget {
                background-color: #3E3E3E;
                color: #FFFFFF;
                border: 1px solid #4B0082;
                padding: 5px;
                border-radius: 5px;
                margin-bottom: 10px;
            }
            QPushButton {
                background-color: #4B0082;
                color: #FFFFFF;
                border: none;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #6A0DAD;
            }
        """)

        layout = QVBoxLayout()

        self.search_bar_installed = QLineEdit()
        self.search_bar_installed.setPlaceholderText("Search installed packages...")
        self.search_bar_installed.textChanged.connect(self.filter_installed_packages)
        layout.addWidget(self.search_bar_installed)

        self.installed_list_widget = QListWidget()
        self.installed_list_widget.setItemDelegate(SpacingDelegate(self.installed_list_widget))
        layout.addWidget(self.installed_list_widget)

        self.installed_packages = result.split('\n')
        self.original_installed_packages = self.installed_packages.copy()
        self.update_installed_packages()

        self.uninstall_button = QPushButton('Uninstall Package')
        self.uninstall_button.clicked.connect(self.uninstall_installed_package)
        layout.addWidget(self.uninstall_button)

        self.close_button = QPushButton('Close')
        self.close_button.clicked.connect(self.installed_window.close)
        layout.addWidget(self.close_button)

        self.installed_window.setLayout(layout)
        self.installed_window.show()

    def update_installed_packages(self):
        self.installed_list_widget.clear()
        for line in self.installed_packages:
            if line.strip():
                item = QListWidgetItem(line)
                self.installed_list_widget.addItem(item)

    def filter_installed_packages(self):
        query = self.search_bar_installed.text().lower()
        if query:
            self.installed_packages = [line for line in self.original_installed_packages if query in line.lower()]
        else:
            self.installed_packages = self.original_installed_packages
        self.update_installed_packages()

    def uninstall_installed_package(self):
        selected_item = self.installed_list_widget.currentItem()
        if selected_item:
            package_name = selected_item.text().split()[0]
            reply = QMessageBox.question(self, 'Confirmation', f'Do you really want to uninstall {package_name}?',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                password, ok = QInputDialog.getText(self, 'Password Required', 'Enter your password:', QLineEdit.Password)
                if ok:
                    process = subprocess.Popen(['sudo', '-S', 'pacman', '-R', '--noconfirm', package_name], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    stdout, stderr = process.communicate(input=password + '\n')
                    if process.returncode == 0:
                        QMessageBox.information(self, 'Uninstall Result', f'Uninstalled package: {package_name}')
                    else:
                        QMessageBox.warning(self, 'Uninstall Failed', stderr)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PackageManagerApp()
    ex.show()
    sys.exit(app.exec_())