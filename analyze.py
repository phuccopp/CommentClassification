from youtube import get_comments
from predict import predict_batch

import pandas as pd
from collections import Counter
from yt_dlp import YoutubeDL
import tempfile


def analyze_youtube(url, progress_callback=None):

    def update(percent, message):
        if progress_callback:
            progress_callback(percent, message)

    # =====================================
    # VIDEO INFO
    # =====================================

    update(5, "📺 Đang tải thông tin video...")

    try:
        with YoutubeDL({"quiet": True}) as ydl:
            info = ydl.extract_info(url, download=False)

        video_title = info.get("title", "Unknown Video")
        video_thumbnail = info.get("thumbnail", "")
        video_channel = info.get("uploader", "Unknown Channel")

    except Exception:
        video_title = "Unknown Video"
        video_thumbnail = ""
        video_channel = "Unknown Channel"

    update(15, "✅ Đã lấy thông tin video")

    # =====================================
    # COMMENTS
    # =====================================

    update(25, "💬 Đang lấy comment...")

    comments = get_comments(url)

    update(40, f"✅ Đã lấy {len(comments)} comment")

    # =====================================
    # PREDICT
    # =====================================

    update(50, "🤖 Đang dự đoán...")

    def predict_progress(done, total):
        percent = 50 + int(done / total * 30)

        update(
            percent,
            f"🤖 Đang dự đoán... ({done}/{total})"
        )

    predictions = predict_batch(
        comments,
        progress_callback=predict_progress
    )

    update(85, "📊 Đang xử lý thống kê...")

    # =====================================
    # DATAFRAME
    # =====================================

    df = pd.DataFrame({
        "comment": comments,
        "predicted_labels": [
            ", ".join(labels) if labels else "irrelevant"
            for labels in predictions
        ]
    })

    # =====================================
    # CSV
    # =====================================

    update(90, "📥 Đang tạo file CSV...")

    csv_file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".csv"
    )

    df.to_csv(
        csv_file.name,
        index=False,
        encoding="utf-8-sig"
    )

    # =====================================
    # DETAIL COUNTER
    # =====================================

    detail_counter = Counter()

    for labels in predictions:
        if not labels:
            detail_counter["irrelevant"] += 1
        else:
            detail_counter.update(labels)

    # =====================================
    # OVERVIEW COUNTER
    # =====================================

    overview_counter = {
        "Positive": 0,
        "Negative": 0,
        "Neutral": 0,
        "Irrelevant": 0
    }

    for labels in predictions:

        if not labels:
            overview_counter["Irrelevant"] += 1
            continue

        for label in labels:

            if label in ["design_positive", "experience_positive"]:
                overview_counter["Positive"] += 1

            elif label in ["design_negative", "experience_negative"]:
                overview_counter["Negative"] += 1

            elif label in ["design_neutral", "experience_neutral"]:
                overview_counter["Neutral"] += 1

            elif label == "irrelevant":
                overview_counter["Irrelevant"] += 1

    update(100, "🎉 Hoàn tất")

    return {
        "title": video_title,
        "thumbnail": video_thumbnail,
        "channel": video_channel,
        "csv_path": csv_file.name,
        "sample_df": df.head(20),
        "full_df": df,
        "overview_counter": overview_counter,
        "detail_counter": dict(detail_counter),
        "total_comments": len(comments)
    }