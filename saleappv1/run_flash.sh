echo "--- Cài thư viện ---"
pip install -r requirements.txt

echo "-- Tạo dữ liệu ---"
#python eapp/models.py

echo "-- Chạy ứng dụng ---"
python -m flash run eapp/index.py