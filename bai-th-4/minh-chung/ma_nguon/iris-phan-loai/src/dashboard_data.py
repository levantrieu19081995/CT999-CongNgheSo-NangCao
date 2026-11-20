"""Đọc kết quả Iris, lọc dữ liệu và tạo PDF theo lựa chọn trên dashboard."""
from io import BytesIO
from pathlib import Path
import hashlib
import json
import xml.sax.saxutils as xml

import pandas as pd
from matplotlib.figure import Figure
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak

FEATURES = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']
CLASSES = ['Iris-setosa', 'Iris-versicolor', 'Iris-virginica']
LABELS = {
    'sepal_length': 'Chiều dài đài hoa (cm)',
    'sepal_width': 'Chiều rộng đài hoa (cm)',
    'petal_length': 'Chiều dài cánh hoa (cm)',
    'petal_width': 'Chiều rộng cánh hoa (cm)',
    'species': 'Loài hoa', 'source_id': 'Mẫu',
}
COLORS = {'Iris-setosa': '#286b9a', 'Iris-versicolor': '#d48238', 'Iris-virginica': '#549467'}


def load_snapshot(project):
    project = Path(project)
    source = project / 'data/iris.csv'
    raw = pd.read_csv(source)
    if not {'source_id', 'species', *FEATURES}.issubset(raw.columns):
        raise ValueError('CSV thiếu cột Iris bắt buộc.')
    if raw[['source_id', 'species', *FEATURES]].isna().any().any():
        raise ValueError('CSV còn ô thiếu. Cần kiểm tra trước khi mở dashboard.')
    clean = raw.drop_duplicates(subset=FEATURES + ['species']).copy()
    results = project / 'results'
    summary = json.loads((results / 'summary.json').read_text(encoding='utf-8'))
    metrics = pd.read_csv(results / 'metrics.csv')
    predictions = pd.read_csv(results / 'predictions.csv')
    if hashlib.sha256(source.read_bytes()).hexdigest() != summary['data_sha256']:
        raise ValueError('CSV đã thay đổi. Chạy lại src/phan_tich.py trước khi mở dashboard.')
    if len(clean) != summary['clean_rows'] or len(predictions) != summary['test_rows']:
        raise ValueError('Số mẫu không khớp với kết quả phân tích đã lưu.')
    for _, row in metrics.iterrows():
        if row['model'] not in predictions:
            raise ValueError('Thiếu cột dự đoán của mô hình: ' + row['model'])
        correct = int((predictions['species'] == predictions[row['model']]).sum())
        if correct != int(row['correct']):
            raise ValueError('Số dự đoán đúng không khớp với metrics.csv.')
    return raw, clean, metrics, summary


def filter_species(clean, selected):
    if not set(selected).issubset(CLASSES):
        raise ValueError('Loài hoa không thuộc dữ liệu Iris.')
    return clean.loc[clean['species'].isin(selected)].copy()


def filtered_pdf(data, x, y, metrics, summary):
    if data.empty:
        raise ValueError('Cần chọn ít nhất một loài để tạo báo cáo.')
    if x not in FEATURES or y not in FEATURES:
        raise ValueError('Chỉ chọn các thuộc tính đo của hoa Iris.')
    fonts = Path('C:/Windows/Fonts')
    for name, file in [('Iris', 'times.ttf'), ('IrisBold', 'timesbd.ttf')]:
        if name not in pdfmetrics.getRegisteredFontNames():
            pdfmetrics.registerFont(TTFont(name, str(fonts / file)))
    body = ParagraphStyle('IrisBody', fontName='Iris', fontSize=11, leading=15, spaceAfter=7)
    title = ParagraphStyle('IrisTitle', parent=body, fontName='IrisBold', fontSize=17, leading=21)
    head = ParagraphStyle('IrisHead', parent=body, fontName='IrisBold', fontSize=13, leading=17, spaceBefore=7)
    small = ParagraphStyle('IrisSmall', parent=body, fontSize=9, leading=12)
    def p(t, style=body):
        return Paragraph(xml.escape(str(t)), style)
    def table(rows, widths):
        t = Table([[p(c, small) for c in row] for row in rows], colWidths=widths, repeatRows=1)
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e9eef2')),
            ('GRID', (0, 0), (-1, -1), .4, colors.HexColor('#d9d9d9')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 5), ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ]))
        return t
    selected = sorted(data['species'].unique())
    content = [p('Báo cáo dữ liệu Iris theo bộ lọc', title), p('CT999 - Công nghệ số nâng cao', small)]
    content += [p('1 Dữ liệu đang chọn', head),
                p(f'Số mẫu theo bộ lọc: {len(data)}. Số loài: {len(selected)}. Các loài: ' + ', '.join(selected) + '.'),
                p(f'Trục X: {LABELS[x]}. Trục Y: {LABELS[y]}.'),
                p(f'CSV gốc có {summary["raw_rows"]} dòng; loại {summary["duplicates_removed"]} dòng trùng, còn {summary["clean_rows"]} mẫu. Bộ lọc chỉ thay đổi phần dữ liệu đang xem.'),
                p('Nguồn: UCI Iris. DOI: 10.24432/C56C76. Dữ liệu được sử dụng theo CC BY 4.0.', small)]
    counts = data['species'].value_counts().sort_index()
    content.append(table([['Loài hoa', 'Số mẫu']] + [[s, str(n)] for s, n in counts.items()], [110*mm, 55*mm]))
    fig = Figure(figsize=(7.4, 4.0))
    ax = fig.subplots()
    for species in selected:
        part = data.loc[data['species'] == species]
        ax.scatter(part[x], part[y], label=species.removeprefix('Iris-'), color=COLORS[species], s=30, alpha=.85)
    ax.set(xlabel=LABELS[x], ylabel=LABELS[y])
    ax.legend(frameon=False); ax.grid(alpha=.15)
    fig.tight_layout()
    image = BytesIO(); fig.savefig(image, format='png', dpi=160); image.seek(0)
    content += [Spacer(1, 5*mm), Image(image, width=165*mm, height=89*mm),
                p('Hình 1. Biểu đồ phân tán theo loài và hai thuộc tính đang chọn.', small), PageBreak(),
                p('2 Thống kê theo bộ lọc', head)]
    description = data[FEATURES].agg(['mean', 'min', 'max']).T
    rows = [['Thuộc tính', 'Trung bình', 'Nhỏ nhất', 'Lớn nhất']]
    for feature, row in description.iterrows():
        rows.append([LABELS[feature], f'{row["mean"]:.3f}', f'{row["min"]:.1f}', f'{row["max"]:.1f}'])
    content += [table(rows, [75*mm, 30*mm, 30*mm, 30*mm]),
                p('3 Kết quả mô hình trên toàn bộ dữ liệu', head),
                p(f'Các mô hình bên dưới được đánh giá trên toàn bộ {summary["clean_rows"]} mẫu đã làm sạch, chia {summary["train_rows"]} mẫu huấn luyện và {summary["test_rows"]} mẫu kiểm tra. Kết quả này không được tính lại theo bộ lọc loài.'),
                table([['Mô hình', 'F1 macro CV', 'Accuracy test', 'Đúng / tổng']] +
                      [[r['model'], f'{r["cv_f1_mean"]:.4f}', f'{r["test_accuracy"]:.4f}', f'{int(r["correct"])}/{int(r["test_n"])}'] for _, r in metrics.iterrows()],
                      [55*mm, 40*mm, 40*mm, 30*mm]),
                p('4 Nhận xét', head),
                p(f'Bộ lọc hiện có {len(data)} mẫu thuộc {len(selected)} loài. Biểu đồ và bảng thống kê phía trên được tạo lại từ đúng các mẫu này. Kết quả mô hình chỉ mô tả lần chia dữ liệu đã lưu; tập kiểm tra nhỏ nên chưa đủ kết luận một mô hình luôn tốt hơn.'),
                p('Hướng tiếp theo là thử nhiều lần chia dữ liệu và bổ sung dữ liệu để kiểm tra độ ổn định của kết quả.')]
    output = BytesIO()
    def footer(canvas, _):
        canvas.setFont('Iris', 9); canvas.drawRightString(A4[0]-18*mm, 12*mm, str(canvas.getPageNumber()))
    SimpleDocTemplate(output, pagesize=A4, leftMargin=18*mm, rightMargin=18*mm,
                      topMargin=16*mm, bottomMargin=18*mm, title='Báo cáo Iris theo bộ lọc', author='Lê Văn Triệu').build(content, onFirstPage=footer, onLaterPages=footer)
    return output.getvalue()
