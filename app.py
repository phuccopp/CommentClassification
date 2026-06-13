import gradio as gr

from analyze import analyze_youtube


# ==================================================
# SAMPLE URLS
# ==================================================

SAMPLE_1 = "https://www.youtube.com/watch?v=OXxrKwQ3DRM"

SAMPLE_2 = "https://www.youtube.com/watch?v=db1S6-85m4U"

SAMPLE_3 = "https://www.youtube.com/watch?v=MUmqNjtyE2w"


# ==================================================
# MAIN FUNCTION
# ==================================================

def run_analysis(url, progress=gr.Progress()):

    return analyze_youtube(
        url,
        progress
    )


# ==================================================
# UI
# ==================================================

with gr.Blocks(
    title="YouTube Comment Analyzer"
) as demo:

    gr.Markdown(
        """
# 🎯 YouTube Comment Analyzer

Phân tích bình luận YouTube bằng PhoBERT Multi-label Classification

Nhập link video hoặc chọn video mẫu bên dưới.
"""
    )

    with gr.Row():

        sample1 = gr.Button(
            "📱 Video mẫu 1"
        )

        sample2 = gr.Button(
            "🎥 Video mẫu 2"
        )

        sample3 = gr.Button(
            "🔥 Video mẫu 3"
        )

    url_input = gr.Textbox(
        label="YouTube URL",
        placeholder="Dán link YouTube vào đây..."
    )

    analyze_btn = gr.Button(
        "🚀 Phân tích",
        variant="primary"
    )

    gr.Markdown("---")

    video_title = gr.Textbox(
        label="Tên video"
    )

    csv_file = gr.File(
        label="📥 Tải kết quả CSV"
    )

    sample_table = gr.Dataframe(
        label="Ví dụ kết quả dự đoán",
        interactive=False
    )

    with gr.Row():

        overview_chart = gr.Plot(
            label="Tổng quan cảm xúc"
        )

        detail_chart = gr.Plot(
            label="Chi tiết 7 nhãn"
        )

    # =====================================
    # EVENTS
    # =====================================

    sample1.click(
        lambda: SAMPLE_1,
        outputs=url_input
    )

    sample2.click(
        lambda: SAMPLE_2,
        outputs=url_input
    )

    sample3.click(
        lambda: SAMPLE_3,
        outputs=url_input
    )

    analyze_btn.click(
        fn=run_analysis,
        inputs=url_input,
        outputs=[
            video_title,
            csv_file,
            sample_table,
            overview_chart,
            detail_chart
        ]
    )

demo.launch(
    server_name="0.0.0.0",
    server_port=7860
)