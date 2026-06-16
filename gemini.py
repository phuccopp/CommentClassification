from google import genai
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)


def analyze_product(title, detail_counter, overview_counter, sample_comments):
    # =========================
    # CHECK DATA
    # =========================

    if sample_comments is None or len(sample_comments.strip()) == 0:
        return """
Không đủ dữ liệu
Video có quá ít bình luận để Gemini phân tích.
"""
    prompt = f"""
Bạn là chuyên gia phân tích sản phẩm công nghệ.
Tên video:
{title}

======================
THỐNG KÊ TỔNG QUAN
{overview_counter}

======================
THỐNG KÊ CHI TIẾT
{detail_counter}

======================
BÌNH LUẬN TIÊU BIỂU
{sample_comments}
Hãy phân tích ngắn gọn, súc tích, cô đọng, đi thẳng vào ý chính và tránh viết dài dòng:

1. Đánh giá tổng thể
2. Điểm mạnh
3. Điểm yếu
4. Thiết kế
5. Trải nghiệm sử dụng
6. Điều người dùng thích nhất
7. Điều người dùng phàn nàn nhiều nhất
8. Kết luận
Viết bằng tiếng Việt.
Viết dạng báo cáo rút gọn.
"""
    try:
        
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt,
            config={"max_output_tokens": 1000},
        )

        if response is None:
            return "Gemini không trả về dữ liệu."

        text = getattr(response, "text", None)

        if text is None or len(text.strip()) == 0:
            return "Gemini không sinh được báo cáo."

        return text

    except Exception as e:
        return f"Lỗi Gemini:\n\n{str(e)}"