import streamlit as st
import pandas as pd
import plotly.express as px
import time

st.set_page_config(page_title='Dashboard Khảo sát L8', layout='wide')
st.title('Hiệu quả Khảo sát CSAT / NPS (Luồng L8)')

# TRẠNG THÁI 1: ĐANG TẢI
with st.spinner('Đang truy vấn kho dữ liệu khảo sát...'):
    time.sleep(1) # Giả lập độ trễ mạng để thấy rõ trạng thái loading
    try:
        # Đọc dữ liệu từ file sample (sau này sẽ kết nối DB thực tế)
        df = pd.read_csv('data/sample/survey_sample.csv')
        df['score'] = pd.to_numeric(df['score'], errors='coerce')
        df['nps_score'] = pd.to_numeric(df['nps_score'], errors='coerce')
        df = df.dropna(subset=['score', 'nps_score'])

    except Exception as e:
        # TRẠNG THÁI 3: LỖI KẾT NỐI (Tuyệt đối không in SQL hay đường dẫn nội bộ)
        st.error("Mất kết nối tới hệ thống kho dữ liệu. Vui lòng kiểm tra mạng và bấm tải lại.")
        st.caption(f"Mã lỗi kỹ thuật: {type(e).__name__}")
        st.stop()

# TRẠNG THÁI 2: RỖNG (Không có dữ liệu khớp bộ lọc)
if df.empty:
    st.info('Không có dữ liệu khảo sát nào. Thử chọn khoảng thời gian rộng hơn hoặc kiểm tra lại luồng nạp dữ liệu.')
    st.stop()

# --- HIỂN THỊ BIỂU ĐỒ (KÈM MỐC SO SÁNH) ---

st.subheader("1. Phân bố điểm CSAT (Thang 1-5)")
tb_csat = df['score'].mean()
fig_csat = px.histogram(df, x='score', nbins=5, labels={'score': 'Điểm CSAT'}, text_auto=True)
# Thêm đường tham chiếu (Mốc so sánh bắt buộc)
fig_csat.add_vline(x=4.0, line_dash='dash', line_color='orange', annotation_text='Mục tiêu SLA (4.0)')
fig_csat.add_vline(x=tb_csat, line_dash='solid', line_color='green', annotation_text=f'Trung bình ({tb_csat:.1f})')
st.plotly_chart(fig_csat, use_container_width=True)

st.subheader("2. Phân tán điểm NPS (Thang 0-10)")
tb_nps = df['nps_score'].mean()
fig_nps = px.box(df, y='nps_score', labels={'nps_score': 'Điểm NPS'})
# Thêm đường tham chiếu
fig_nps.add_hline(y=tb_nps, line_dash='dash', line_color='red', annotation_text=f'Trung bình hệ thống ({tb_nps:.1f})')
st.plotly_chart(fig_nps, use_container_width=True)

# Ghi chú nguồn dữ liệu
st.caption(f"Nguồn: Bảng fact_survey_csat - Số liệu tính tới {pd.Timestamp.now().strftime('%d/%m/%Y %H:%M')}")