"""Dashboard khám phá dữ liệu Iris và tải báo cáo theo bộ lọc."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pandas as pd
import plotly.express as px
import streamlit as st
from dashboard_data import FEATURES, CLASSES, LABELS, COLORS, load_snapshot, filter_species, filtered_pdf

PROJECT = Path(__file__).resolve().parents[1]
st.set_page_config(page_title='Khảo sát phân loại hoa Iris', layout='wide')
st.title('Khảo sát phân loại hoa Iris')
st.caption('CT999 · Công nghệ số nâng cao · Dữ liệu UCI Iris')

try:
    raw, clean, metrics, summary = load_snapshot(PROJECT)
except (OSError, ValueError, KeyError) as exc:
    st.error(str(exc))
    st.stop()

with st.sidebar:
    st.header('Chọn dữ liệu')
    species = st.multiselect('Loài hoa', CLASSES, default=CLASSES,
                            format_func=lambda s: s.removeprefix('Iris-'), key='species')
    x = st.selectbox('Trục X', FEATURES, index=2, format_func=LABELS.get, key='x_feature')
    y = st.selectbox('Trục Y', FEATURES, index=3, format_func=LABELS.get, key='y_feature')
    st.divider()
    st.write('CSV gốc: 150 dòng. Sau khi loại ba dòng trùng, còn 147 mẫu.')
    st.markdown('[Nguồn dữ liệu và DOI](https://doi.org/10.24432/C56C76)')

selected = filter_species(clean, species)
columns = st.columns(4)
columns[0].metric('Số mẫu đang chọn', len(selected))
columns[1].metric('Số loài đang chọn', selected['species'].nunique())
columns[2].metric('Ô thiếu trong CSV gốc', summary['missing_cells'])
columns[3].metric('Dòng trùng đã loại', summary['duplicates_removed'])

if selected.empty:
    st.warning('Chưa có dữ liệu để hiển thị. Chọn ít nhất một loài hoa ở bên trái.')
    st.stop()

explore, models, export = st.tabs(['Khám phá dữ liệu', 'Kết quả mô hình', 'Tải báo cáo'])
with explore:
    chart_type = st.radio('Loại biểu đồ', ['Phân tán', 'Phân bố', 'Tương quan'], horizontal=True, key='chart_type')
    if chart_type == 'Phân tán':
        figure = px.scatter(selected, x=x, y=y, color='species', labels=LABELS,
                            color_discrete_map=COLORS, hover_data=['source_id'], opacity=.85)
    elif chart_type == 'Phân bố':
        figure = px.histogram(selected, x=x, color='species', barmode='overlay', opacity=.65,
                              labels=LABELS, color_discrete_map=COLORS, nbins=18)
        figure.update_yaxes(title='Số mẫu')
    else:
        corr = selected[FEATURES].rename(columns=LABELS).corr()
        figure = px.imshow(corr, zmin=-1, zmax=1, color_continuous_scale='RdBu_r', text_auto='.2f', aspect='auto')
    figure.update_layout(template='plotly_white', height=420, margin=dict(t=20, b=35, l=20, r=20), legend_title_text='Loài hoa')
    st.plotly_chart(figure, width='stretch', key='iris_chart')
    st.caption(f'Biểu đồ và bảng bên dưới dùng đúng {len(selected)} mẫu theo bộ lọc. Các kích thước được đo bằng cm.')
    st.subheader('Các mẫu đang chọn')
    st.dataframe(selected.rename(columns=LABELS), hide_index=True, width='stretch')
    st.subheader('Thống kê mô tả')
    st.dataframe(selected[FEATURES].rename(columns=LABELS).describe().round(3), width='stretch')

with models:
    st.subheader('So sánh bốn mô hình')
    st.info(f'Kết quả đã chạy trên toàn bộ {summary["clean_rows"]} mẫu: {summary["train_rows"]} mẫu huấn luyện và {summary["test_rows"]} mẫu kiểm tra. Bộ lọc loài không thay đổi các chỉ số trong phần này.')
    display = metrics.rename(columns={'model':'Mô hình','cv_f1_mean':'F1 macro CV','cv_f1_std':'Độ lệch chuẩn CV',
                                      'test_accuracy':'Accuracy test','test_f1_macro':'F1 macro test','correct':'Số đúng','test_n':'Số mẫu test'})
    st.dataframe(display.round(4), hide_index=True, width='stretch')
    chart = px.bar(metrics, x='model', y='cv_f1_mean', error_y='cv_f1_std', text='cv_f1_mean',
                   labels={'model':'Mô hình','cv_f1_mean':'F1 macro trên 5 fold'}, color_discrete_sequence=['#286b9a'])
    chart.update_traces(texttemplate='%{text:.4f}', textposition='outside')
    chart.update_layout(template='plotly_white', yaxis_range=[0,1.08], height=380, showlegend=False)
    st.plotly_chart(chart, width='stretch', key='model_chart')
    st.write('kNN có F1 macro CV cao nhất trong lần chạy này. Cây quyết định đúng 42/45 mẫu kiểm tra; các mô hình còn lại đúng 41/45. Hai cách đánh giá dùng những mẫu khác nhau.')

@st.cache_data(show_spinner=False)
def build_download(data, x, y, metrics, summary):
    return filtered_pdf(data, x, y, metrics, summary)

with export:
    st.subheader('Tải kết quả đang xem')
    st.write(f'Bộ lọc hiện tại: {len(selected)} mẫu; loài: ' + ', '.join(s.removeprefix('Iris-') for s in species) + '.')
    st.write('Báo cáo theo bộ lọc gồm biểu đồ phân tán theo hai trục đang chọn, thống kê dữ liệu và kết quả mô hình đã lưu. Phần kết quả mô hình được ghi riêng cho toàn bộ dữ liệu.')
    report = build_download(selected, x, y, metrics, summary)
    st.download_button('Tải báo cáo PDF theo bộ lọc', data=report, file_name='Bao_cao_Iris_theo_bo_loc.pdf', mime='application/pdf', key='download_pdf')
    st.download_button('Tải CSV theo bộ lọc', data=selected.to_csv(index=False).encode('utf-8-sig'),
                       file_name='Iris_theo_bo_loc.csv', mime='text/csv', key='download_csv')
    st.download_button('Tải báo cáo tổng hợp ban đầu', data=(PROJECT/'results/Bao_cao_tu_dong.pdf').read_bytes(),
                       file_name='Bao_cao_tu_dong.pdf', mime='application/pdf', key='download_original')
    st.caption('Giấy phép mã nguồn: MIT. Dữ liệu Iris: CC BY 4.0. Mã nguồn, dữ liệu và các chỉ số được lưu kèm bộ bài thực hành.')
