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
    QLineEdit, QPushButton, QMessageBox, QTextEdit, QProgressBar, QFileDialog,
    QCalendarWidget, QDialog
)
from PyQt5.QtCore import Qt, QDate
from datetime import datetime

class CalendarDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Chọn ngày")
        self.setGeometry(300, 300, 300, 300)

        self.calendar = QCalendarWidget(self)
        self.calendar.setGridVisible(True)
        self.calendar.clicked.connect(self.select_date)

        layout = QVBoxLayout()
        layout.addWidget(self.calendar)
        self.setLayout(layout)

        self.selected_date = None

    def select_date(self, date):
        self.selected_date = date.toString("yyyyMMdd")
        self.accept()

class CopyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tool copy data ssd realtime")
        self.setGeometry(200, 200, 600, 400)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Input fields
        self.src_label = QLabel("Chon thu muc nguon (Internal SSD):")
        self.src_input = QLineEdit()
        self.src_browse_btn = QPushButton("Select")
        self.src_browse_btn.clicked.connect(self.browse_src)

        self.dest_label = QLabel("Chon thu muc dich (External SSD):")
        self.dest_input = QLineEdit()
        self.dest_browse_btn = QPushButton("Select")
        self.dest_browse_btn.clicked.connect(self.browse_dest)

        # Ngày cần sao chép
        self.date_label = QLabel("Ngay can sao chep (YYYYMMDD):")
        self.date_input = QLineEdit()
        self.date_calendar_btn = QPushButton("Chọn ngày")
        self.date_calendar_btn.clicked.connect(self.open_calendar)

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

        layout.addWidget(self.date_label)
        layout.addWidget(self.date_input)
        layout.addWidget(self.date_calendar_btn)

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

    def open_calendar(self):
        dialog = CalendarDialog(self)
        if dialog.exec_():
            selected_date = dialog.selected_date
            if selected_date:
                self.date_input.setText(selected_date)

    def log(self, message):
        self.log_area.append(message)
        self.log_area.ensureCursorVisible()

    # c1 Chờ 7p và kiểm tra nếu kích thước file trong folder ko thay đổi
    # def is_folder_complete(self, folder_path, wait_time=420):
    #     self.log(f"Checking folder: {folder_path}, waiting {wait_time} sec...")
    #     initial_sizes = {f: os.path.getsize(os.path.join(folder_path, f)) for f in os.listdir(folder_path)}
        
    #     QTimer.singleShot(wait_time * 1000, lambda: None)  # Chờ 7 phút
        
    #     current_sizes = {f: os.path.getsize(os.path.join(folder_path, f)) for f in os.listdir(folder_path)}
    #     if initial_sizes == current_sizes:
    #         self.log(f"Folder {folder_path} is complete.")
    #         return True
    #     else:
    #         self.log(f"Folder {folder_path} is still being written. Skipping...")
    #         return False

    # c2 Sử dụng lsof để kiểm tra xem folder có đang được ghi dữ liệu hay ko
    def is_folder_complete(self, folder_path):
        try:
            # Kiểm tra xem folder có file nào đang mở không
            result = subprocess.check_output(['lsof', '+D', folder_path], stderr=subprocess.DEVNULL)
            return not result.strip()  # Nếu không có file nào đang mở, trả về True
        except subprocess.CalledProcessError:
            return True  # Không có file nào đang mở


    def start_copy(self):
        src_dir = self.src_input.text()
        dest_dir = self.dest_input.text()
        filter_date = self.date_input.text().strip()

        if not src_dir or not dest_dir or not filter_date:
            QMessageBox.warning(self, "Error", "Vui long chon source, des, date.")
            return

        if not os.path.exists(src_dir) or not os.path.isdir(src_dir):
            QMessageBox.warning(self, "Error", "Source khong ton tai")
            return

        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)

        # Kiểm tra ngày hợp lệ
        try:
            datetime.strptime(filter_date, "%Y%m%d")
        except ValueError:
            QMessageBox.warning(self, "Error", "Sai dinh dang date ! VD: YYYYMMDD.")
            return

        self.log("Starting copy process...")
        folders = sorted(os.listdir(src_dir))

        for i, folder in enumerate(folders):
            if filter_date not in folder:  # Lọc theo ngày
                continue

            src_folder_path = os.path.join(src_dir, folder)
            dest_folder_path = os.path.join(dest_dir, folder)

            if not os.path.isdir(src_folder_path) or os.path.exists(dest_folder_path):
                continue

            self.log(f"Checking folder: {folder}")
            if self.is_folder_complete(src_folder_path):
                self.log(f"Copying folder: {folder}")
                self.run_rsync(src_folder_path, dest_folder_path)
            else:
                self.log(f"Folder {folder} van dang duoc recording. Skipping...")

            # Update progress bar
            progress = int((i + 1) / len(folders) * 100)
            self.progress_bar.setValue(progress)

        self.log("Da Copy xong!")


    def run_rsync(self, src_folder, dest_folder):
        try:
            rsync_command = [
                "rsync",
                "-a",
                "--info=progress2",
                "--no-o",
                "--no-g",
                "--exclude=.tmp",
                src_folder + "/",
                dest_folder
            ]
            process = subprocess.Popen(rsync_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
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