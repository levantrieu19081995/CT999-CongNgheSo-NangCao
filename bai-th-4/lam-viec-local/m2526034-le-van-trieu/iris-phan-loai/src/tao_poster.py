"""Tạo poster A0 ngang từ các kết quả CSV và hình PDF của thực nghiệm Iris."""
from pathlib import Path
from io import BytesIO
import json
import argparse
import xml.sax.saxutils as xml
import pandas as pd
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph,Spacer,Table,TableStyle,Frame,Flowable
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.graphics.barcode import qr
from reportlab.graphics.shapes import Drawing
from reportlab.graphics import renderPDF
from pypdf import PdfReader,PdfWriter,Transformation

def build(project,output,repo_url):
    for name,file in [('Poster','arial.ttf'),('PosterBold','arialbd.ttf')]:
        pdfmetrics.registerFont(TTFont(name,str(Path('C:/Windows/Fonts')/file)))
    result=project/'results'
    meta=json.loads((result/'summary.json').read_text(encoding='utf8'))
    metrics=pd.read_csv(result/'metrics.csv')
    W,H=1189*mm,841*mm
    margin,gutter=28*mm,18*mm
    col=(W-2*margin-2*gutter)/3
    styles={
        'body':ParagraphStyle('body',fontName='Poster',fontSize=27,leading=37,spaceAfter=18,textColor=colors.HexColor('#203440')),
        'head':ParagraphStyle('head',fontName='PosterBold',fontSize=37,leading=45,spaceBefore=20,spaceAfter=16,textColor=colors.HexColor('#173e53')),
        'caption':ParagraphStyle('caption',fontName='Poster',fontSize=22,leading=29,spaceAfter=18,textColor=colors.HexColor('#3e535e')),
        'table':ParagraphStyle('table',fontName='Poster',fontSize=24,leading=31),
        'small':ParagraphStyle('small',fontName='Poster',fontSize=20,leading=28,spaceAfter=8),
    }
    def P(text,kind='body'):return Paragraph(xml.escape(str(text)).replace('\n','<br/>'),styles[kind])
    def T(rows,widths):
        t=Table([[P(c,'table') for c in row] for row in rows],colWidths=widths,hAlign='LEFT')
        t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e8eff3')),('GRID',(0,0),(-1,-1),.7,colors.HexColor('#bfcbd2')),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('LEFTPADDING',(0,0),(-1,-1),14),('RIGHTPADDING',(0,0),(-1,-1),14),('TOPPADDING',(0,0),(-1,-1),13),('BOTTOMPADDING',(0,0),(-1,-1),13)]))
        return t
    placements=[]
    class Chart(Flowable):
        def __init__(self,name,height):self.name=name;self.width=col;self.height=height
        def draw(self):
            x,y=self.canv.absolutePosition(0,0)
            placements.append((result/'figures'/self.name,x,y,self.width,self.height))
    buf=BytesIO();c=canvas.Canvas(buf,pagesize=(W,H))
    c.setTitle('Phân loại hoa Iris bằng bốn mô hình học máy')
    c.setAuthor('Lê Văn Triệu - M2526034')
    c.setFillColor(colors.HexColor('#173e53'));c.rect(0,H-117*mm,W,117*mm,fill=1,stroke=0)
    c.setFillColor(colors.white);c.setFont('PosterBold',66)
    c.drawString(margin,H-42*mm,'PHÂN LOẠI HOA IRIS BẰNG BỐN MÔ HÌNH HỌC MÁY')
    c.setFont('Poster',31)
    c.drawString(margin,H-65*mm,'Lê Văn Triệu - M2526034 | Trường Đại học Cần Thơ')
    c.drawString(margin,H-84*mm,'Giảng viên hướng dẫn: PGS. TS. Nguyễn Thanh Hải')
    c.setFont('Poster',26)
    c.drawString(margin,H-103*mm,'Học phần CT999 - Công nghệ số nâng cao | Khảo sát trên dữ liệu UCI Iris')
    col1=[P('Vấn đề và mục tiêu','head'),P('Với cùng dữ liệu và cách chia, kNN, SVM, cây quyết định và Random Forest cho kết quả như thế nào? Bài thực hành theo dõi cả kết quả trung bình trên các fold và lỗi trên tập kiểm tra.'),
          P('Dữ liệu sau kiểm tra','head'),T([['Nội dung','Số lượng'],['CSV gốc',str(meta['raw_rows'])],['Dòng trùng đã loại',str(meta['duplicates_removed'])],['Mẫu dùng phân tích',str(meta['clean_rows'])],['Huấn luyện / kiểm tra',f'{meta["train_rows"]} / {meta["test_rows"]}']],[col*.66,col*.34]),
          P('Bốn thuộc tính đo bằng cm: chiều dài và chiều rộng đài hoa, chiều dài và chiều rộng cánh hoa. Nhãn gồm ba loài setosa, versicolor và virginica.'),
          P('Phân bố hai thuộc tính cánh hoa','head'),Chart('01_petal_scatter.pdf',565),P('Mỗi điểm là một mẫu sau làm sạch. Hai loài versicolor và virginica còn vùng chồng lấn.','caption')]
    col2=[P('Phương pháp thực hiện','head'),P('1. Kiểm tra ô thiếu, số đo và dòng trùng.\n2. Chia phân tầng với random_state = 42.\n3. Đánh giá chéo 5 fold trên 102 mẫu huấn luyện.\n4. Huấn luyện lại rồi kiểm tra trên 45 mẫu.'),
          P('Cấu hình mô hình','head'),T([['Mô hình','Thiết lập'],['kNN','k = 5, StandardScaler'],['SVM','RBF, C = 1, StandardScaler'],['Decision Tree','Độ sâu tối đa 3'],['Random Forest','200 cây, seed = 42']],[col*.37,col*.63]),
          P('Kết quả đánh giá chéo','head'),Chart('04_cv_f1.pdf',565),P('Cột là F1 macro trung bình trên 5 fold. Thanh sai số là độ lệch chuẩn mẫu. Chỉ dùng tập huấn luyện.','caption')]
    rows=[['Mô hình','Đúng / tổng','F1 macro']]
    for _,r in metrics.iterrows():rows.append([r['model'],f'{int(r.correct)}/{int(r.test_n)}',f'{r.test_f1_macro:.4f}'])
    col3=[P('Kết quả trên tập kiểm tra','head'),T(rows,[col*.43,col*.28,col*.29]),P('Cây quyết định đúng 42/45 mẫu. Các mô hình còn lại đúng 41/45 mẫu. Một mẫu tương ứng khoảng 2,22 điểm phần trăm Accuracy.'),
          P('Quan sát lỗi của SVM','head'),Chart('05_svm_confusion.pdf',500),P('SVM nhận đúng 15/15 mẫu setosa. Bốn lỗi nằm giữa versicolor và virginica. Hàng là nhãn thực tế, cột là dự đoán.','caption'),
          P('Thảo luận và kết luận','head'),P('kNN có F1 macro CV trung bình cao nhất, còn cây quyết định có F1 macro test cao nhất. Tập kiểm tra nhỏ nên chưa đủ kết luận thuật toán nào luôn tốt hơn.'),P('Bước tiếp theo là thử các lần chia xác định trước và dữ liệu lớn hơn. Mã nguồn, dữ liệu và dự đoán từng mẫu được lưu để chạy lại.')]
    for i,items in enumerate([col1,col2,col3]):
        x=margin+i*(col+gutter)
        f=Frame(x,153*mm,col,H-284*mm,leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0,showBoundary=0)
        f.addFromList(items,c)
        if items:raise ValueError(f'Cột {i+1} còn {len(items)} thành phần chưa vừa trang')
    c.setStrokeColor(colors.HexColor('#bdcbd3'));c.setLineWidth(1)
    c.line(margin,141*mm,W-margin,141*mm)
    refs=[
        '[1] R. A. Fisher, “The use of multiple measurements in taxonomic problems,” Annals of Eugenics, vol. 7, no. 2, pp. 179-188, 1936. DOI: 10.1111/j.1469-1809.1936.tb02137.x.',
        '[2] T. Cover and P. Hart, “Nearest neighbor pattern classification,” IEEE Trans. Inf. Theory, vol. 13, no. 1, pp. 21-27, 1967. DOI: 10.1109/TIT.1967.1053964.',
        '[3] L. Breiman, “Random Forests,” Machine Learning, vol. 45, pp. 5-32, 2001. DOI: 10.1023/A:1010933404324.',
        '[4] R. Fisher, Iris [Dataset], UCI Machine Learning Repository. DOI: 10.24432/C56C76. Dữ liệu CC BY 4.0.',
    ]
    bottom=[P('Tài liệu tham khảo','head'),*[P(s,'small') for s in refs],P('Liên hệ: lvtrieu@ctu.edu.vn | Mã nguồn có giấy phép MIT, dữ liệu giữ giấy phép của UCI.','small')]
    Frame(margin,22*mm,W-margin*2-122*mm,111*mm,leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0).addFromList(bottom,c)
    if bottom:raise ValueError('Tài liệu tham khảo chưa vừa chân poster')
    q=qr.QrCodeWidget(repo_url)
    box=q.getBounds();size=90*mm
    d=Drawing(size,size,transform=[size/(box[2]-box[0]),0,0,size/(box[3]-box[1]),0,0]);d.add(q)
    renderPDF.draw(d,c,W-margin-size,39*mm)
    c.setFillColor(colors.HexColor('#203440'));c.setFont('Poster',20)
    c.drawCentredString(W-margin-size/2,29*mm,'Mã nguồn và kết quả')
    c.showPage();c.save();buf.seek(0)
    page=PdfReader(buf).pages[0]
    for source,x,y,w,h in placements:
        chart=PdfReader(str(source)).pages[0]
        sw,sh=float(chart.mediabox.width),float(chart.mediabox.height)
        scale=min(w/sw,h/sh)
        page.merge_transformed_page(chart,Transformation().scale(scale).translate(x+(w-sw*scale)/2,y+(h-sh*scale)/2),over=True)
    writer=PdfWriter();writer.add_page(page)
    writer.add_metadata({'/Title':'Phân loại hoa Iris bằng bốn mô hình học máy','/Author':'Lê Văn Triệu - M2526034'})
    output.parent.mkdir(parents=True,exist_ok=True)
    with output.open('wb') as f:writer.write(f)
    print('Poster A0 ngang: 1189 x 841 mm')
    print('Giảng viên: PGS. TS. Nguyễn Thanh Hải')
    print('Hình khoa học giữ dạng vector:',len(placements))
    print('Đã tạo:',output)

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--project',type=Path,default=Path('.'))
    p.add_argument('--out',type=Path,default=Path('../yc2_poster/Poster_Iris_A0.pdf'))
    p.add_argument('--repo',default='https://github.com/levantrieu19081995/ct999-iris-phan-loai')
    a=p.parse_args();build(a.project,a.out,a.repo)
