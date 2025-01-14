Cài đặt Python nếu chưa có:
sudo apt update
sudo apt install python3 python3-pip

Tạo virtual environment để install các lib mà không làm ảnh hưởng đến hệ thống:
python3 -m venv venv
source venv/bin/activate

PyQt5 cần một số công cụ xây dựng như qtbase5-dev, qt5-qmake, và build-essential :
sudo apt install python3-dev qtbase5-dev qt5-qmake build-essential -y

(neu k the cai dat qt5 hay upgrade pip): python -m pip install --upgrade pip

sau do cai dat:
pip install PyQt5

(PyQt5 phù hợp với Python 3.6.9 trên Ubuntu 18.04) :
pip install PyQt5==5.15.4

(Xem cac thu vien can cai dat nhu sau)
pip list
-> ket qua hien ra
Package       Version
------------- -------
pip           24.3.1
pkg_resources 0.0.0
PyQt5         5.15.11
PyQt5-Qt5     5.15.16
PyQt5_sip     12.15.0
setuptools    44.0.0


chạy chương trình:
python ten_ch_trinh.py
