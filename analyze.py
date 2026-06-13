from youtube import get_comments
from predict import predict_batch

import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
from yt_dlp import YoutubeDL
import tempfile


def analyze_youtube(url, progress=None):

    # ==================================================
    # VIDEO INFO
    # ==================================================

    if progress:
        progress(0.05, desc="Đang lấy thông tin video...")

    try:

        with YoutubeDL({"quiet": True}) as ydl:

            info = ydl.extract_info(
                url,
                download=False
            )

        video_title = info.get(
            "title",
            "Unknown Video"
        )

    except Exception as e:

        print("Video title error:", e)

        video_title = "Unknown Video"

    # ==================================================
    # GET COMMENTS
    # ==================================================

    if progress:
        progress(0.2, desc="Đang lấy comment...")

    comments = get_comments(url)

    print(
        f"Đã lấy {len(comments)} comment"
    )

    # ==================================================
    # PREDICT
    # ==================================================

    if progress:
        progress(
            0.5,
            desc=f"Đang dự đoán {len(comments)} comment..."
        )

    predictions = predict_batch(
        comments
    )

    # ==================================================
    # DATAFRAME
    # ==================================================

    df = pd.DataFrame({
        "comment": comments,
        "predicted_labels": [
            ", ".join(labels)
            if labels
            else "none"
            for labels in predictions
        ]
    })

    # ==================================================
    # SAVE CSV
    # ==================================================

    csv_file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".csv"
    )

    df.to_csv(
        csv_file.name,
        index=False,
        encoding="utf-8-sig"
    )

    # ==================================================
    # SAMPLE DATA
    # ==================================================

    sample_df = df.head(20)

    # ==================================================
    # DETAIL COUNTER
    # ==================================================

    detail_counter = Counter()

    for labels in predictions:

        if len(labels) == 0:

            detail_counter["none"] += 1

        else:

            detail_counter.update(
                labels
            )

    # ==================================================
    # OVERVIEW COUNTER
    # ==================================================

    overview_counter = {
        "Positive": 0,
        "Negative": 0,
        "Neutral": 0,
        "Irrelevant": 0
    }

    for labels in predictions:

        for label in labels:

            if label in [
                "design_positive",
                "experience_positive"
            ]:

                overview_counter[
                    "Positive"
                ] += 1

            elif label in [
                "design_negative",
                "experience_negative"
            ]:

                overview_counter[
                    "Negative"
                ] += 1

            elif label in [
                "design_neutral",
                "experience_neutral"
            ]:

                overview_counter[
                    "Neutral"
                ] += 1

            elif label == "irrelevant":

                overview_counter[
                    "Irrelevant"
                ] += 1

    # ==================================================
    # OVERVIEW PIE CHART
    # ==================================================

    fig1, ax1 = plt.subplots(
        figsize=(6, 6)
    )

    overview_values = [
        v
        for v in overview_counter.values()
        if v > 0
    ]

    overview_labels = [
        k
        for k, v in overview_counter.items()
        if v > 0
    ]

    ax1.pie(
        overview_values,
        labels=overview_labels,
        autopct="%1.1f%%"
    )

    ax1.set_title(
        "Sentiment Overview"
    )

    # ==================================================
    # DETAIL PIE CHART
    # ==================================================

    fig2, ax2 = plt.subplots(
        figsize=(7, 7)
    )

    detail_values = list(
        detail_counter.values()
    )

    detail_labels = list(
        detail_counter.keys()
    )

    ax2.pie(
        detail_values,
        labels=detail_labels,
        autopct="%1.1f%%"
    )

    ax2.set_title(
        "Detailed Labels"
    )

    if progress:
        progress(
            1.0,
            desc="Hoàn tất"
        )

    return (
        video_title,     # textbox
        csv_file.name,   # file download
        sample_df,       # dataframe
        fig1,            # chart overview
        fig2             # chart detail
    )