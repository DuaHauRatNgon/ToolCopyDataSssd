import os
import time
import subprocess
from datetime import datetime


def is_folder_complete(folder_path, wait_time=60):
    """
    Kiểm tra thư mục đã hoàn thành ghi dữ liệu hay chưa.
    Thư mục được coi là hoàn thành nếu không có tệp nào thay đổi kích thước trong thời gian `wait_time`.
    """
    initial_sizes = {f: os.path.getsize(os.path.join(folder_path, f)) for f in os.listdir(folder_path)}
    time.sleep(wait_time)
    current_sizes = {f: os.path.getsize(os.path.join(folder_path, f)) for f in os.listdir(folder_path)}
    return initial_sizes == current_sizes


def copy_completed_folders(src_dir, dest_dir, check_interval=300):
    """
    Sao chép các thư mục hoàn thành từ src_dir sang dest_dir.
    - `check_interval`: Thời gian chờ giữa các lần kiểm tra (tính bằng giây).
    """
    while True:
        try:
            # Lấy danh sách tất cả các thư mục trong thư mục nguồn
            folders = sorted(os.listdir(src_dir))
            
            for folder in folders:
                src_folder_path = os.path.join(src_dir, folder)
                dest_folder_path = os.path.join(dest_dir, folder)

                # Bỏ qua nếu không phải là thư mục hoặc thư mục đã được sao chép
                if not os.path.isdir(src_folder_path) or os.path.exists(dest_folder_path):
                    continue

                # Kiểm tra thư mục đã hoàn thành hay chưa
                print(f"Checking folder: {folder}")
                if is_folder_complete(src_folder_path):
                    print(f"Folder {folder} is complete. Starting copy...")
                    subprocess.run(["rsync", "-a", src_folder_path + "/", dest_folder_path], check=True)
                    print(f"Folder {folder} copied successfully!")
                else:
                    print(f"Folder {folder} is still being written. Skipping...")

            # Chờ trước khi kiểm tra lại
            print(f"Waiting for {check_interval} seconds before next check...")
            time.sleep(check_interval)

        except Exception as e:
            print(f"Error: {str(e)}")
            time.sleep(10)  # Chờ trước khi thử lại nếu có lỗi


if __name__ == "__main__":
    # Thư mục nguồn (SSD nội bộ)
    source_directory = "/mnt/dsu0/VF6_VN"
    # Thư mục đích (SSD ngoài)
    destination_directory = "/mnt/external_ssd"

    # Kiểm tra thư mục đích tồn tại
    if not os.path.exists(destination_directory):
        os.makedirs(destination_directory)

    print(f"Starting backup from {source_directory} to {destination_directory}...")
    copy_completed_folders(source_directory, destination_directory)
