import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from analyze import analyze_youtube

# =========================
# CONFIG
# =========================

st.set_page_config(
    page_title="YouTube Comment Analyzer",
    page_icon="",
    layout="wide"
)

# =========================
# SIDEBAR
# =========================

st.sidebar.title("🎬 Video mẫu")

sample_urls = {
    "iPhone 17 Review":
    "https://www.youtube.com/watch?v=OXxrKwQ3DRM",

    "Bây giờ tôi mới được cầm vào iPhone 17 !":
    "https://www.youtube.com/watch?v=db1S6-85m4U"
}

selected = st.sidebar.selectbox(
    "Chọn video mẫu",
    list(sample_urls.keys())
)

# =========================
# HEADER
# =========================

st.title(" YouTube Comment Analyzer")

url = st.text_input(
    "YouTube URL",
    value=sample_urls[selected]
)

# =========================
# RUN
# =========================

if st.button("🚀 Phân tích", use_container_width=True):

    progress_bar = st.progress(0)
    status_box = st.empty()

    def update_progress(percent, message):
        progress_bar.progress(percent)
        status_box.info(message)

    result = analyze_youtube(
        url,
        progress_callback=update_progress
    )

    progress_bar.empty()
    status_box.empty()

    st.success("🎉 Hoàn tất!")

    # =========================
    # VIDEO INFO
    # =========================

    col1, col2 = st.columns([1, 3])

    with col1:
        if result["thumbnail"]:
            st.image(result["thumbnail"], use_container_width=True)

    with col2:
        st.markdown(f"# **{result['title']}**")
        st.markdown(f"**Channel:** {result['channel']}")
        st.markdown(f"[▶ Xem trên YouTube]({url})")

    # =========================
    # METRICS
    # =========================

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(" Tổng comment", result["total_comments"])


    with c3:
        st.metric(" Số nhãn", len(result["detail_counter"]))

    # =========================
    # CSV DOWNLOAD
    # =========================

    st.info("📁 Tải toàn bộ kết quả CSV")

    with open(result["csv_path"], "rb") as f:
        st.download_button(
            "DOWNLOAD CSV",
            f.read(),
            "youtube_comments.csv",
            "text/csv",
            use_container_width=True
        )

    # =========================
    # 🔥 BẢNG 7 NHÃN (PHẦN BẠN BỊ MẤT)
    # =========================

    st.subheader(" Số lượng theo nhãn")

    label_counts = result["detail_counter"]

    all_labels = [
        "design_negative",
        "design_neutral",
        "design_positive",
        "experience_negative",
        "experience_neutral",
        "experience_positive",
        "irrelevant"
    ]

    row = [label_counts.get(l, 0) for l in all_labels]

    df_summary = pd.DataFrame(
        [row],
        columns=all_labels
    )

    st.dataframe(
        df_summary,
        use_container_width=True
    )

    # =========================
    # SAMPLE TABLE
    # =========================

    st.markdown("---")

    st.subheader("Kết quả mẫu")

    st.dataframe(
        result["sample_df"],
        use_container_width=True,
        height=400
    )

    # =========================
    # CHARTS
    # =========================

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Tổng quan")

        fig, ax = plt.subplots()

        data = result["overview_counter"]

        ax.pie(
            data.values(),
            labels=data.keys(),
            autopct="%1.1f%%"
        )

        st.pyplot(fig)

    with col2:

        st.subheader("Chi tiết 7 nhãn")

        fig2, ax2 = plt.subplots()

        detail = result["detail_counter"]

        ax2.pie(
            detail.values(),
            labels=detail.keys(),
            autopct="%1.1f%%"
        )

        st.pyplot(fig2)