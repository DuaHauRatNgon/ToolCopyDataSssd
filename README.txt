Giaỉ nén ra được 4 file sau:
CopyDataSsd.py  Note.txt  README.txt  requirements.txt

Cài đặt Python nếu chưa có:
sudo apt update
sudo apt install python3 python3-pip

Tạo virtual environment để install các lib mà không làm ảnh hưởng đến hệ thống:
python3 -m venv venv
source venv/bin/activate

Cài đặt các lib cần thiết từ file requirements.txt:
pip install -r requirements.txt

chạy chương trình:
python ten_ch_trinh.py
