"""Vẽ sơ đồ đề xuất ETL cho tình huống CSV, API và PDF; không kết nối dữ liệu thật."""
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

THU_MUC = Path(__file__).resolve().parent
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 12.5,
                     'svg.fonttype': 'none'})
fig, ax = plt.subplots(figsize=(9, 8.3))
ax.set_xlim(0, 12)
ax.set_ylim(0.5, 11.25)
ax.axis('off')

def hop(x, y, w, h, text, fill='#F2F5F7', size=12.5, bold=False):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
        boxstyle='round,pad=0.06,rounding_size=0.08',
        edgecolor='#455966', facecolor=fill, linewidth=1.15))
    ax.text(x+w/2, y+h/2, text, ha='center', va='center',
            fontsize=size, weight='bold' if bold else 'normal', color='#17232B')

def mui_ten(a, b, nhan=None, lech=(0,0)):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle='-|>', mutation_scale=12,
                               linewidth=1.15, color='#455966'))
    if nhan:
        ax.text((a[0]+b[0])/2+lech[0], (a[1]+b[1])/2+lech[1], nhan,
                ha='center', va='center', fontsize=9,
                bbox={'facecolor':'white','edgecolor':'none','pad':1})

hop(.35,10.15,3.2,.7,'CSV\nĐiểm sinh viên',bold=True)
hop(4.4,10.15,3.2,.7,'API\nKhảo sát trực tuyến',bold=True)
hop(8.45,10.15,3.2,.7,'PDF\nBáo cáo theo lớp',bold=True)
hop(.35,8.85,3.2,.9,'EXTRACT\nPandas đọc CSV')
hop(4.4,8.85,3.2,.9,'EXTRACT\nHTTP GET → JSON')
hop(8.45,8.85,3.2,.9,'EXTRACT\npypdf → kiểm tra bảng')
for x in [1.95,6,10.05]:
    mui_ten((x,10.15),(x,9.82))
    mui_ten((x,8.8),(x,8.4))
hop(.6,7.65,10.8,.7,'Lưu bản gốc CSV, JSON và PDF theo lần lấy dữ liệu',fill='#FFFFFF')
mui_ten((6,7.6),(6,7.35))
hop(.6,6.45,10.8,.85,'TRANSFORM\nChuẩn hóa mã, học kỳ, kiểu số; xử lý thiếu và trùng',fill='#E8EFF4',bold=True)
mui_ten((2.9,6.4),(2.9,5.95))
mui_ten((9.1,6.4),(9.1,5.95))
hop(.6,5.05,4.6,.85,'Ghép điểm + khảo sát\nKhóa: mã sinh viên, học kỳ')
hop(6.8,5.05,4.6,.85,'Tổng hợp theo lớp, học kỳ\nĐối chiếu bảng từ PDF')
mui_ten((5.28,5.475),(6.72,5.475),'Tổng hợp',lech=(0,.2))
mui_ten((2.9,5.0),(2.9,4.45))
mui_ten((9.1,5.0),(7.2,4.45))
hop(1.7,3.45,6.9,.95,'KIỂM TRA\nKhóa duy nhất, số dòng, khoảng giá trị',fill='#FFFFFF',bold=True)
hop(9.25,3.45,2.4,.95,'Bản ghi lỗi\nvà nhật ký',fill='#FFF3E8',size=11.5)
mui_ten((8.68,3.925),(9.17,3.925),'Lỗi',lech=(0,.28))
mui_ten((5.15,3.4),(5.15,2.65),'Đạt',lech=(.35,0))
hop(1.7,1.55,6.9,1.05,'LOAD\nCSV hoặc SQLite\nBảng sinh viên và bảng tổng hợp lớp',fill='#E8EFF4',bold=True)
ax.text(6,.8,'Sơ đồ đề xuất cho tình huống mô phỏng',ha='center',va='center',
        fontsize=10,color='#455966')
fig.subplots_adjust(left=.01,right=.99,top=.99,bottom=.01)
fig.savefig(THU_MUC/'so_do_pipeline.png',dpi=230,facecolor='white')
fig.savefig(THU_MUC/'so_do_pipeline.svg',facecolor='white')
plt.close(fig)
print('Da tao so_do_pipeline.png va so_do_pipeline.svg')
