#huongnm13@vingroup.net
# v 1.0

# Yêu cầu: 
# -đã cài python3 (môi trường)
# -cài các thư viện PyQt5 shutil os (có thể dùng pip)

# Tóm tắt:
# Tool dung de copy data (asc, idx, jsq, pcap, rex, txt,...) sang ssd externa trong khi ssd internal van dang recording

# Cach hoat dong:
# Chuong trinh theo doi kich thuoc cac thu muc trong 1 khoang time, neu k co thay doi thi thu muc duoc coi la hoan thanh 
# Dung rsync de sao chep nhung thu muc da record hoan thanh tu ssd internal sang ssd external
# Chuong trinh lap lai sau 1 khoang thoi gian de check cac thu muc moi

# Cách dùng: 
# -chọn thư mục nguồn (ssd trong) chứa các video cần sao chép, chọn thư mục đích (ssd ngoài)

# Tinh nang: 
# Tu dong bo qua file dang sao chep 
# Chi sao chep cac thu muc da record vao ssd internal
# Tiep tuc sao chep neu bi gian doan

import os
import subprocess
import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel,
    QLineEdit, QPushButton, QMessageBox, QTextEdit, QProgressBar, QFileDialog
)
from PyQt5.QtCore import Qt, QTimer


class CopyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tool copy data ssd realtime")
        self.setGeometry(200, 200, 600, 400)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Input fields
        self.src_label = QLabel("Source (Internal SSD):")
        self.src_input = QLineEdit()
        self.src_browse_btn = QPushButton("Chon thu muc...")
        self.src_browse_btn.clicked.connect(self.browse_src)

        self.dest_label = QLabel("Destination (External SSD):")
        self.dest_input = QLineEdit()
        self.dest_browse_btn = QPushButton("Chon thu muc...")
        self.dest_browse_btn.clicked.connect(self.browse_dest)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)

        # Log display
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)

        # Start button
        self.start_btn = QPushButton("Start Copy")
        self.start_btn.clicked.connect(self.start_copy)

        # Add widgets to layout
        layout.addWidget(self.src_label)
        layout.addWidget(self.src_input)
        layout.addWidget(self.src_browse_btn)

        layout.addWidget(self.dest_label)
        layout.addWidget(self.dest_input)
        layout.addWidget(self.dest_browse_btn)

        layout.addWidget(self.progress_bar)
        layout.addWidget(self.log_area)
        layout.addWidget(self.start_btn)

        # Central widget
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def browse_src(self):
        directory = QFileDialog.getExistingDirectory(self, "Chon Source")
        if directory:
            self.src_input.setText(directory)

    def browse_dest(self):
        directory = QFileDialog.getExistingDirectory(self, "Chon Destination")
        if directory:
            self.dest_input.setText(directory)

    def log(self, message):
        self.log_area.append(message)
        self.log_area.ensureCursorVisible()

    def is_folder_complete(self, folder_path, wait_time=60):
        """
        Kiểm tra xem thư mục có hoàn thành ghi dữ liệu hay chưa.
        """
        initial_sizes = {f: os.path.getsize(os.path.join(folder_path, f)) for f in os.listdir(folder_path)}
        QTimer.singleShot(wait_time * 1000, lambda: None)  # Wait asynchronously
        current_sizes = {f: os.path.getsize(os.path.join(folder_path, f)) for f in os.listdir(folder_path)}
        return initial_sizes == current_sizes

    def start_copy(self):
        src_dir = self.src_input.text()
        dest_dir = self.dest_input.text()

        if not src_dir or not dest_dir:
            QMessageBox.warning(self, "Error", "Please specify both source and destination directories.")
            return

        if not os.path.exists(src_dir) or not os.path.isdir(src_dir):
            QMessageBox.warning(self, "Error", "Source directory does not exist.")
            return

        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)

        self.log("Starting copy process...")
        folders = sorted(os.listdir(src_dir))

        for i, folder in enumerate(folders):
            src_folder_path = os.path.join(src_dir, folder)
            dest_folder_path = os.path.join(dest_dir, folder)

            if not os.path.isdir(src_folder_path) or os.path.exists(dest_folder_path):
                continue

            self.log(f"Checking folder: {folder}")
            if self.is_folder_complete(src_folder_path):
                self.log(f"Copying folder: {folder}")
                self.run_rsync(src_folder_path, dest_folder_path)
            else:
                self.log(f"Folder {folder} is still being written. Skipping...")

            # Update progress bar
            progress = int((i + 1) / len(folders) * 100)
            self.progress_bar.setValue(progress)

        self.log("Da Copy xong!")

    def run_rsync(self, src_folder, dest_folder):
        """
        Chạy lệnh rsync để sao chép thư mục.
        """
        try:
            rsync_command = [
                "rsync",
                "-a",              # Chế độ lưu trữ, bảo toàn thư mục và file
                "--info=progress2", # Hiển thị thông tin tiến trình
                "--no-o",          # Không sao chép quyền sở hữu
                "--no-g",          # Không sao chép nhóm
                "--exclude=.tmp",  # Loại bỏ file tạm thời
                src_folder + "/",  
                dest_folder        
            ]

            #tham số text=True chỉ hợp lệ trên Python >=3.7
            # process = subprocess.Popen(rsync_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            # treen autera dung:
            process = subprocess.Popen(rsync_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

            for line in process.stdout:
                self.log(line.strip())

            process.wait()
            if process.returncode == 0:
                self.log(f"Folder {src_folder} copy thanh cong.")
            else:
                self.log(f"Da co loi xay ra trong qua trinh sao chep {src_folder}.")
        except Exception as e:
            self.log(f"Error: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CopyApp()
    window.show()
    sys.exit(app.exec_())
