# Đồ Án Giao Tiếp Tiếng Anh

Đây là đồ án sử dụng Flask, Google Speech-to-Text và Google AI Studio để xây dựng hệ thống giao tiếp tiếng Anh. Hệ thống có chức năng submit video transcript và gợi ý câu hỏi tiếp theo dựa trên nội dung

## Cài Đặt
1.**Thiết lập môi trường ảo**

    python -m venv venv
    source venv/bin/activate  (#Trên Windows: venv\Scripts\activate)


2.**Cài đặt các gói cần thiết**

    pip install -r requirements.txt


3.**Cấu hình API key**

    Tải file JSON chứa thông tin tài khoản dịch vụ Google Speech-to-Text và đặt vào đường dẫn `.\Doan_TKPM\Doan_TKPM\speech-to-text.json`.
    Đặt API key của Google AI Studio trong biến môi trường `GEMINI_API_KEY`.
    Ở đây đã cài đặt sẵn file json cũng như api key, có thể vào 	https://console.cloud.google.com/
        menu -> APIs and Services để tải file JSON cũng như thiết lập API key riêng

4. **Chạy ứng dụng**
   python app.py

5.**Mở trình duyệt và truy cập địa chỉ**
   http://127.0.0.1:5000

6.**Transcribe Audio**
  Chọn file audio và nhấn nút "Transcribe".
  Hệ thống sẽ hiển thị transcript của audio.
  Hệ thống sẽ trả về câu trả lời và gợi ý các câu hỏi tiếp theo

7. **submit text
  Nhập văn bản vào ô input và nhấn nút "Submit"
  Hệ thống sẽ trả về câu trả lời và gợi ý các câu hỏi tiếp theo dựa trên nội dung

Cấu trúc thư mục:
  main.py: Tập tin chính của ứng dụng
  main.js: Tập tin JavaScript để xử lý các yêu cầu từ giao diện người dùng
  templates/index.html: Tập tin HTML để hiển thị giao diện người dùng.