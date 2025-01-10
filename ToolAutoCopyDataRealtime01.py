import os
import subprocess
import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QFileDialog, QVBoxLayout, QWidget, QLabel, QLineEdit, QMessageBox
)
from PyQt5.QtCore import QDate
from datetime import datetime

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Copy data tu ssd autera -> ssd gan ngoai")
        self.setGeometry(100, 100, 600, 400)

        # Layout chính
        layout = QVBoxLayout()

        # Nhãn và nút chọn thư mục nguồn
        self.source_label = QLabel("Source Directory:")
        layout.addWidget(self.source_label)

        self.source_input = QLineEdit()
        layout.addWidget(self.source_input)

        self.source_button = QPushButton("Browse Source")
        self.source_button.clicked.connect(self.browse_source)
        layout.addWidget(self.source_button)

        # Nhãn và nút chọn thư mục đích
        self.dest_label = QLabel("Destination Directory:")
        layout.addWidget(self.dest_label)

        self.dest_input = QLineEdit()
        layout.addWidget(self.dest_input)

        self.dest_button = QPushButton("Browse Destination")
        self.dest_button.clicked.connect(self.browse_dest)
        layout.addWidget(self.dest_button)

        # Nút bắt đầu sao chép
        self.copy_button = QPushButton("Start Backup")
        self.copy_button.clicked.connect(self.start_backup)
        layout.addWidget(self.copy_button)

        # Hiển thị trạng thái
        self.status_label = QLabel("")
        layout.addWidget(self.status_label)

        # Thiết lập widget trung tâm
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def browse_source(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Source Directory")
        if directory:
            self.source_input.setText(directory)

    def browse_dest(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Destination Directory")
        if directory:
            self.dest_input.setText(directory)

    def start_backup(self):
        source = self.source_input.text().strip()
        dest = self.dest_input.text().strip()

        # Kiểm tra thư mục nguồn và đích
        if not source or not dest:
            QMessageBox.critical(self, "Error", "Please select both source and destination directories.")
            return
        if not os.path.exists(source):
            QMessageBox.critical(self, "Error", f"Source directory does not exist: {source}")
            return
        if not os.path.exists(dest):
            QMessageBox.critical(self, "Error", f"Destination directory does not exist: {dest}")
            return

        # Chạy lệnh rsync
        self.status_label.setText("Backing up... Please wait.")
        QApplication.processEvents()

        try:
            result = subprocess.run(
                ["rsync", "-av", "--progress", "--partial", "--ignore-errors", source + "/", dest + "/"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

            if result.returncode == 0:
                self.status_label.setText("Backup completed successfully!")
                QMessageBox.information(self, "Success", "Backup completed successfully!")
            else:
                self.status_label.setText("Backup encountered errors!")
                QMessageBox.critical(self, "Error", f"Backup failed:\n{result.stderr}")
        except Exception as e:
            self.status_label.setText("Backup failed!")
            QMessageBox.critical(self, "Error", f"An error occurred:\n{str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
