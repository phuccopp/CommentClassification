# YouTube Comment Analyzer for Product Reviews

## Giới thiệu

YouTube Comment Analyzer là ứng dụng hỗ trợ phân tích bình luận từ các video review sản phẩm công nghệ trên YouTube.

Người dùng chỉ cần nhập URL video YouTube, hệ thống sẽ tự động:

- Thu thập bình luận từ video
- Phân loại bình luận bằng mô hình PhoBERT
- Xuất kết quả ra file CSV
- Thống kê và trực quan hóa dữ liệu
- Sinh báo cáo đánh giá sản phẩm bằng Gemini AI

Ứng dụng được xây dựng bằng Python, Streamlit, PhoBERT và Gemini.

---

## Xây dựng mô hình phân loại

Để huấn luyện mô hình, dữ liệu được thu thập từ các bình luận liên quan đến các sản phẩm công nghệ như điện thoại, laptop, tai nghe, đồng hồ thông minh,...

Sau khi thu thập, dữ liệu được làm sạch thủ công:

- Loại bỏ spam và bình luận trùng lặp
- Chỉnh sửa các lỗi chính tả phổ biến
- Loại bỏ bình luận không có ý nghĩa
- Gán nhãn thủ công

Bài toán được xây dựng theo hướng **Multi-label Classification** với 7 nhãn:

| Nhãn                | Ý nghĩa                           |
| ------------------- | --------------------------------- |
| design_negative     | Chê thiết kế                      |
| design_neutral      | Nhận xét trung lập về thiết kế    |
| design_positive     | Khen thiết kế                     |
| experience_negative | Chê trải nghiệm sử dụng           |
| experience_neutral  | Nhận xét trung lập về trải nghiệm |
| experience_positive | Khen trải nghiệm sử dụng          |
| irrelevant          | Bình luận không liên quan         |

Mô hình sử dụng:

```text
PhoBERT Base V2
```

Thông số huấn luyện:

```text
Epochs: 5
Learning Rate: 2e-5
Batch Size: 8
Max Length: 256
GPU: NVIDIA Tesla T4
```

Kết quả đánh giá trên tập Test:

| Metric    | Score  |
| --------- | ------ |
| F1 Micro  | 0.8086 |
| F1 Macro  | 0.7579 |
| Precision | 0.8148 |
| Recall    | 0.8024 |

---

## Chức năng chính

### 1. Thu thập bình luận YouTube

- Nhập URL video YouTube
- Tự động lấy bình luận
- Không yêu cầu YouTube API

### 2. Phân loại bình luận

Mỗi bình luận được đưa qua mô hình PhoBERT để dự đoán một hoặc nhiều nhãn cảm xúc liên quan đến:

- Thiết kế sản phẩm
- Trải nghiệm sử dụng
- Bình luận không liên quan

Ví dụ:

| Comment                   | Prediction          |
| ------------------------- | ------------------- |
| Máy đẹp quá               | design_positive     |
| Pin hơi yếu               | experience_negative |
| Ai xem năm 2026 điểm danh | irrelevant          |

### 3. Xuất kết quả CSV

Kết quả được lưu dưới dạng:

| comment     | predicted_labels    |
| ----------- | ------------------- |
| Máy đẹp quá | design_positive     |
| Pin hơi yếu | experience_negative |

Người dùng có thể tải file CSV trực tiếp trên giao diện.

### 4. Thống kê dữ liệu

Hệ thống hiển thị:

- Tổng số bình luận
- Bảng số lượng theo từng nhãn
- Biểu đồ tổng quan cảm xúc
- Biểu đồ chi tiết 7 nhãn

### 5. Báo cáo bằng Gemini AI

Sau khi hoàn tất phân loại, Gemini AI sẽ tổng hợp:

- Đánh giá tổng quan sản phẩm
- Điểm mạnh
- Điểm yếu
- Đánh giá thiết kế
- Đánh giá trải nghiệm sử dụng
- Kết luận

Dữ liệu đầu vào của Gemini được lấy từ kết quả phân loại của PhoBERT và các bình luận tiêu biểu trong từng nhóm nhãn.

---

## Kiến trúc hệ thống

```text
YouTube URL
      |
      v
Thu thập bình luận
      |
      v
PhoBERT Classification
      |
      +----> CSV Output
      |
      +----> Statistics
      |
      +----> Visualization
      |
      +----> Gemini Analysis
```

---

## Công nghệ sử dụng

### Machine Learning

- PhoBERT Base V2
- PyTorch
- Hugging Face Transformers

### Data Processing

- Pandas
- NumPy

### Visualization

- Matplotlib

### Web Application

- Streamlit

### Generative AI

- Gemini 2.5 Flash

---

## Cấu trúc thư mục

```text
project/
│
├── app.py
├── analyze.py
├── predict.py
├── youtube.py
├── gemini.py
│
├── model_phobert/
│
├── requirements.txt
├── Dockerfile
├── .env
│
└── outputs/
```

---

## Cài đặt

### Clone repository

```bash
git clone <repository_url>

cd project
```

### Cài đặt thư viện

```bash
pip install -r requirements.txt
```

### Tạo file .env

```env
GEMINI_API_KEY=YOUR_API_KEY
```

---

## Chạy ứng dụng

```bash
streamlit run app.py
```

Truy cập:

```text
http://localhost:8501
```

---

## Docker

Build image:

```bash
docker build -t youtube-comment-analyzer .
```

Run container:

```bash
docker run -p 8501:8501 youtube-comment-analyzer
```

---

## Deploy lên Hugging Face Spaces

SDK:

```text
Docker
```

Thêm Secret:

```text
GEMINI_API_KEY
```

---

## Kết quả đầu ra

Sau khi phân tích, hệ thống cung cấp:

- Thumbnail video
- Tên video
- Tên kênh
- Tổng số bình luận
- File CSV kết quả
- Bảng thống kê nhãn
- Biểu đồ trực quan
- Báo cáo đánh giá sản phẩm bằng Gemini AI

---

## Tác giả

Hoàng Phúc Nguyễn

Đề tài ứng dụng PhoBERT trong phân tích cảm xúc và đánh giá sản phẩm công nghệ từ bình luận YouTube.
