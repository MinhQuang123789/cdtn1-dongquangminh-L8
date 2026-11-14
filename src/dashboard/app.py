import os
import pandas as pd
import plotly.express as px
import psycopg2
import streamlit as st

st.set_page_config(page_title="Dashboard Khảo sát CSAT/NPS - Luồng L8", layout="wide")
st.title("Hiệu quả Khảo sát CSAT / NPS (Luồng L8)")


@st.cache_data(ttl=30)
def tai_du_lieu_khao_sat() -> pd.DataFrame:
    dwh_url = os.environ.get("DWH_URL")
    if not dwh_url:
        raise ConnectionError("Chưa cấu hình kết nối kho dữ liệu.")
    conn = psycopg2.connect(dwh_url)
    try:
        query = """
            SELECT response_id, responded_date, store_name, city,
                   customer_pseudo_id, customer_segment,
                   csat_score, nps_score, comment
            FROM v_survey_analytics
            ORDER BY responded_date, response_id;
        """
        return pd.read_sql_query(query, conn)
    finally:
        conn.close()


try:
    with st.spinner("Đang truy vấn kho dữ liệu khảo sát..."):
        df = tai_du_lieu_khao_sat()
except Exception:
    # Trang thai 3: Loi ket noi (An chi tiet ky thuat theo chuan bao mat)
    st.error("Mất kết nối tới hệ thống kho dữ liệu. Vui lòng kiểm tra dịch vụ warehouse và bấm tải lại.")
    st.stop()

# Bo loc theo cua hang
cua_hang = ["Tất cả"] + sorted(df["store_name"].dropna().unique().tolist()) if not df.empty else ["Tất cả"]
chon_ch = st.sidebar.selectbox("Chọn trung tâm / cửa hàng:", cua_hang)
if chon_ch != "Tất cả" and not df.empty:
    df = df[df["store_name"] == chon_ch]

# Trang thai 2: Rong
if df.empty:
    st.info("Không có dữ liệu khảo sát nào. Thử chọn bộ lọc khác hoặc chạy pipeline nạp dữ liệu.")
    st.stop()

# Trang thai 1: Thanh cong
col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Phân bố điểm CSAT (Thang 1–5)")
    tb_csat = df["csat_score"].mean()
    fig_csat = px.histogram(
        df, x="csat_score", nbins=5,
        labels={"csat_score": "Điểm CSAT", "count": "Số phản hồi"},
    )
    fig_csat.add_vline(x=tb_csat, line_dash="solid", line_color="green", annotation_text=f"Trung bình ({tb_csat:.2f})")
    fig_csat.add_vline(x=4.0, line_dash="dash", line_color="orange", annotation_text="Mục tiêu SLA (4.0)")
    st.plotly_chart(fig_csat, use_container_width=True)

with col2:
    st.subheader("2. Phân tán điểm NPS (Thang 0–10)")
    tb_nps = df["nps_score"].mean()
    fig_nps = px.box(df, y="nps_score", points="all", labels={"nps_score": "Điểm NPS"})
    fig_nps.add_hline(y=tb_nps, line_dash="dash", line_color="red", annotation_text=f"Trung bình hệ thống ({tb_nps:.2f})")
    st.plotly_chart(fig_nps, use_container_width=True)

st.caption("Nguồn dữ liệu: View phân tích ẩn danh v_survey_analytics (Vai trò truy cập: nha_phan_tich)")