# 🎮 2048 Hand Gesture Control 🖐️

Một phiên bản làm lại của tựa game 2048 kinh điển, tích hợp công nghệ Computer Vision để điều khiển bằng cử chỉ tay thay vì bàn phím truyền thống. Dự án ứng dụng **MediaPipe** để tracking khớp tay và **OpenCV** để xử lý hình ảnh realtime.

![Video Project 2](https://github.com/user-attachments/assets/989e6e7d-1240-4434-acf0-56dc445a6ddc)



## ✨ Tính năng nổi bật
* **Chế độ chơi linh hoạt:** Hỗ trợ cả điều khiển bằng bàn phím vật lý lẫn nhận diện cử chỉ tay qua Webcam.
* **Hand Tracking Realtime:** Theo dõi chính xác chuyển động tay với độ trễ thấp bằng Google MediaPipe.
* **Giao diện trực quan:** Xây dựng giao diện game mượt mà bằng Pygame.

## 🛠️ Công nghệ sử dụng
* **Ngôn ngữ:** Python 3.x
* **Thư viện:** * `opencv-python` (Xử lý ảnh/video)
  * `mediapipe` (Nhận diện & trích xuất đặc trưng bàn tay)
  * `pygame` (Xây dựng UI Game)
  * `pyautogui` (Giả lập phím bấm)

## 🚀 Hướng dẫn cài đặt

Dự án này có thể chạy tốt trên môi trường Windows. Để chạy thử trên máy của bạn, vui lòng làm theo các bước sau:

**1. Clone repository về máy:**
```bash
git clone [https://github.com/baonguyenmh2021-cpu/2048-hand-gesture.git]
cd 2048-hand-gesture
2. Tạo môi trường ảo (Virtual Environment):

Bash
python -m venv venv
venv\Scripts\activate
3. Cài đặt các thư viện cần thiết:

Bash
pip install -r requirements.txt
4. Khởi chạy game:

Bash
python game2048OpenCVMediapipe.py
🕹️ Cách điều khiển
Sau khi chạy script, bạn có thể chọn 1 trong 2 chế độ ở Menu chính:

Phím 1 (Bàn phím): Dùng các phím Mũi tên (Lên, Xuống, Trái, Phải) để gộp số.

Phím 2 (Webcam): * Đưa tay lên trước Camera.

Vuốt tay nhanh sang Trái/Phải/Lên/Xuống để điều khiển game.

Giữ khoảng cách vừa đủ để Camera nhận diện rõ các khớp tay.

Phím R: Chơi lại (Restart).

Phím Q / Đóng cửa sổ: Thoát game.

Dự án được phát triển bởi [Trần Thị Bảo Nguyên] - Cập nhật lần cuối: 2026
