"""Tạo báo cáo PDF từ CSV Iris và kết quả phân loại đã lưu."""
from pathlib import Path
import argparse
import json
import hashlib
import xml.sax.saxutils as xml
import pandas as pd
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def register_fonts():
    directory=Path('C:/Windows/Fonts')
    for name,file in [('Report','times.ttf'),('ReportBold','timesbd.ttf'),('ReportItalic','timesi.ttf')]:
        if not (directory/file).exists():raise FileNotFoundError('Cần font Times New Roman hỗ trợ tiếng Việt: '+str(directory/file))
        pdfmetrics.registerFont(TTFont(name,str(directory/file)))

def make_report(csv_path,metrics_path,out):
    register_fonts()
    raw=pd.read_csv(csv_path)
    features=['sepal_length','sepal_width','petal_length','petal_width']
    needed=['source_id',*features,'species']
    if not set(needed).issubset(raw.columns):raise ValueError('CSV thiếu cột Iris')
    if raw[needed].isna().any().any():raise ValueError('CSV còn ô thiếu')
    clean=raw.drop_duplicates(subset=features+['species'])
    metrics=pd.read_csv(metrics_path)
    results=metrics_path.parent
    summary=json.loads((results/'summary.json').read_text(encoding='utf8'))
    if hashlib.sha256(csv_path.read_bytes()).hexdigest()!=summary['data_sha256']:raise ValueError('CSV đã thay đổi, cần chạy lại phan_tich.py')
    predictions=pd.read_csv(results/'predictions.csv')
    if len(clean)!=summary['clean_rows']:raise ValueError('CSV đầu vào không khớp kết quả phân tích')
    if len(predictions)!=summary['test_rows']:raise ValueError('Thiếu dự đoán trên tập kiểm tra')
    for _,row in metrics.iterrows():
        correct=int((predictions['species']==predictions[row['model']]).sum())
        if correct!=int(row['correct']):raise ValueError('Số dự đoán đúng không khớp metrics.csv')
    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle('BodyVN',fontName='Report',fontSize=11,leading=15,spaceAfter=6))
    styles.add(ParagraphStyle('TitleVN',fontName='ReportBold',fontSize=17,leading=21,spaceAfter=8))
    styles.add(ParagraphStyle('HeadVN',fontName='ReportBold',fontSize=13,leading=17,spaceBefore=8,spaceAfter=5))
    styles.add(ParagraphStyle('SmallVN',fontName='Report',fontSize=9,leading=12,spaceAfter=5))
    content=[]
    def p(text,style='BodyVN'):return Paragraph(xml.escape(str(text)),styles[style])
    def table(rows,widths):
        body=[[p(c,'SmallVN') for c in row] for row in rows]
        t=Table(body,colWidths=widths,repeatRows=1,hAlign='LEFT')
        t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e9eef2')),('GRID',(0,0),(-1,-1),.35,colors.HexColor('#c6cbd0')),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),4)]))
        return t
    content += [p('Báo cáo phân tích dữ liệu Iris','TitleVN'),p('Lê Văn Triệu - M2526034 | Học phần CT999','SmallVN')]
    content += [p('1. Dữ liệu và cách thực hiện','HeadVN'),p(f'Chương trình đọc {csv_path.name}, kiểm tra dữ liệu, rồi lập bảng và biểu đồ từ kết quả đã lưu. Tệp gốc có {len(raw)} dòng. Có {int(raw[needed].isna().sum().sum())} ô thiếu và {len(raw)-len(clean)} dòng trùng theo bốn đặc trưng cùng nhãn. Sau khi giữ dòng xuất hiện đầu tiên, còn {len(clean)} mẫu.')]
    content += [p('Nguồn: Fisher, R. (1936), Iris [Dataset], UCI Machine Learning Repository. DOI: 10.24432/C56C76. Dữ liệu dùng giấy phép CC BY 4.0. Bản CSV được chuyển từ iris.data trong gói tải UCI.','SmallVN')]
    content += [p('Bảng 1. Tám dòng đầu của CSV gốc. Bốn kích thước đo bằng cm.','SmallVN')]
    rows=[['Mẫu','Dài đài','Rộng đài','Dài cánh','Rộng cánh','Loài']]
    for _,r in raw.head(8).iterrows():rows.append([str(r.source_id),*[f'{r[c]:.1f}' for c in features],r.species.removeprefix('Iris-')])
    content += [table(rows,[14*mm,25*mm,25*mm,25*mm,25*mm,55*mm]),Spacer(1,5*mm)]
    counts=clean.species.value_counts().sort_index()
    content += [p('Số mẫu sau làm sạch: '+', '.join(f'{key.removeprefix("Iris-")}: {value}' for key,value in counts.items())+'.')]
    content += [Image(str(results/'figures/01_petal_scatter.png'),width=165*mm,height=97*mm),p('Hình 1. Phân bố chiều dài và chiều rộng cánh hoa trên dữ liệu sau làm sạch.','SmallVN')]
    content += [PageBreak(),p('2. So sánh kết quả phân loại','HeadVN')]
    content += [p(f'Tập huấn luyện gồm {summary["train_rows"]} mẫu, tập kiểm tra gồm {summary["test_rows"]} mẫu. Chia phân tầng theo loài với random_state={summary["seed"]}. Đánh giá chéo {summary["cv_folds"]} fold chỉ thực hiện trên tập huấn luyện. kNN và SVM dùng StandardScaler trong Pipeline để tính chuẩn hóa riêng trong từng fold.')]
    rows=[['Mô hình','F1 CV trung bình','Độ lệch chuẩn','Accuracy test','F1 macro test','Đúng/tổng']]
    for _,r in metrics.iterrows():rows.append([r['model'],f'{r.cv_f1_mean:.4f}',f'{r.cv_f1_std:.4f}',f'{r.test_accuracy:.4f}',f'{r.test_f1_macro:.4f}',f'{r.correct}/{r.test_n}'])
    content += [table(rows,[36*mm,29*mm,28*mm,28*mm,27*mm,21*mm]),Spacer(1,4*mm)]
    content += [Image(str(results/'figures/04_cv_f1.png'),width=145*mm,height=98*mm),p('Hình 2. F1 macro trung bình và độ lệch chuẩn mẫu trên 5 fold của tập huấn luyện.','SmallVN')]
    best_cv=metrics.loc[metrics.cv_f1_mean.idxmax()]
    best_test=metrics.loc[metrics.test_f1_macro.idxmax()]
    content += [p('3. Kết luận ngắn','HeadVN'),p(f'Trong lần chạy này, {best_cv["model"]} có F1 macro CV cao nhất ({best_cv.cv_f1_mean:.4f}). Trên tập kiểm tra, {best_test["model"]} dự đoán đúng {int(best_test.correct)}/{int(best_test.test_n)} mẫu và đạt F1 macro {best_test.test_f1_macro:.4f}. Hai kết quả được tính trên hai cách đánh giá khác nhau, nên cần đọc riêng.')]
    content += [p('Tập kiểm tra nhỏ, mỗi mẫu tương ứng khoảng '+f'{100/summary["test_rows"]:.2f}'+' điểm phần trăm Accuracy. Kết quả dùng để đối chiếu cách chạy chương trình trên Iris, chưa đủ để kết luận một thuật toán luôn tốt hơn trên dữ liệu khác.')]
    content += [p('Tệp đối chiếu: metrics.csv, cv_scores.csv, predictions.csv, train.csv, test.csv và summary.json trong cùng thư mục kết quả.','SmallVN')]
    out.parent.mkdir(parents=True,exist_ok=True)
    def footer(canvas,doc):
        canvas.setFont('Report',9);canvas.drawRightString(A4[0]-18*mm,12*mm,str(doc.page))
    SimpleDocTemplate(str(out),pagesize=A4,leftMargin=18*mm,rightMargin=18*mm,topMargin=16*mm,bottomMargin=19*mm,title='Báo cáo phân tích dữ liệu Iris',author='Lê Văn Triệu').build(content,onFirstPage=footer,onLaterPages=footer)
    print('Đã đọc CSV:',csv_path)
    print('Số dòng gốc / sạch:',len(raw),'/',len(clean))
    print('Đã kiểm tra số dự đoán đúng của cả',len(metrics),'mô hình.')
    print('Đã tạo PDF:',out,'-',out.stat().st_size,'byte')

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--csv',type=Path,default=Path('data/iris.csv'))
    parser.add_argument('--metrics',type=Path,default=Path('results/metrics.csv'))
    parser.add_argument('--out',type=Path,default=Path('results/Bao_cao_tu_dong.pdf'))
    args=parser.parse_args();make_report(args.csv,args.metrics,args.out)
