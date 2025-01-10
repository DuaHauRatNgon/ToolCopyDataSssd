Giaỉ nén ra được 4 file sau:
CopyDataSsd.py  Note.txt  README.txt  requirements.txt

Cài đặt Python nếu chưa có:
sudo apt update
sudo apt install python3 python3-pip

Tạo virtual environment để install các lib mà không làm ảnh hưởng đến hệ thống:
python3 -m venv venv
source venv/bin/activate

PyQt5 cần một số công cụ xây dựng như qtbase5-dev, qt5-qmake, và build-essential :
sudo apt install python3-dev qtbase5-dev qt5-qmake build-essential -y
pip install PyQt5


chạy chương trình:
python ten_ch_trinh.py
