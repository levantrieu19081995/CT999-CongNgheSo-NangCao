"""Bài 3: dữ liệu World Bank Việt Nam 2014–2023.
Chạy: python bai3_phan_tich.py
Mặc định đọc JSON đã lưu; thêm --tai-lai để cập nhật từ World Bank.
"""
from pathlib import Path
from urllib.request import urlopen
import json
import sys
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

THU_MUC = Path(__file__).resolve().parent
DU_LIEU = THU_MUC / 'du_lieu'
KET_QUA = THU_MUC / 'ket_qua'
DU_LIEU.mkdir(exist_ok=True)
KET_QUA.mkdir(exist_ok=True)

# 1. Lấy và lưu nguyên phản hồi JSON, không nhập số liệu bằng tay.
def lay_chi_tieu(ma, ten_cot):
    url = (f'https://api.worldbank.org/v2/country/VNM/indicator/{ma}'
           '?date=2014:2023&format=json&per_page=100')
    tep = DU_LIEU / f'{ma}.json'
    if not tep.exists() or '--tai-lai' in sys.argv:
        with urlopen(url, timeout=40) as phan_hoi:
            tep.write_bytes(phan_hoi.read())
    noi_dung = json.loads(tep.read_text(encoding='utf-8-sig'))
    bang = pd.DataFrame([
        {'nam': dong['date'], ten_cot: dong['value']}
        for dong in noi_dung[1]
    ])
    return bang, noi_dung[0], url

gdp, meta_gdp, url_gdp = lay_chi_tieu('NY.GDP.MKTP.KD', 'gdp_usd_2015')
tang_truong, meta_tt, url_tt = lay_chi_tieu('NY.GDP.MKTP.KD.ZG', 'tang_truong_pct')

# 2. Ghép theo năm, kiểm tra và chuyển dữ liệu sang kiểu số.
df = gdp.merge(tang_truong, on='nam', how='outer', validate='one_to_one')
df.to_csv(DU_LIEU / 'vietnam_gdp_goc.csv', index=False, encoding='utf-8-sig')
so_dong_goc = len(df)
for cot in df.columns:
    df[cot] = pd.to_numeric(df[cot], errors='coerce')
so_dong_thieu = int(df.isna().any(axis=1).sum())
so_dong_trung = int(df.duplicated().sum())
df = df.dropna().drop_duplicates().copy()
df = df[df['nam'].between(2014, 2023)].sort_values('nam').reset_index(drop=True)
df['nam'] = df['nam'].astype(int)
df['gdp_ty_usd_2015'] = df['gdp_usd_2015'] / 1_000_000_000
df = df[['nam', 'gdp_ty_usd_2015', 'tang_truong_pct']]
if df['nam'].tolist() != list(range(2014, 2024)):
    raise ValueError('Không đủ đúng 10 năm; cần kiểm tra nguồn trước khi phân tích.')
df.to_csv(KET_QUA / 'vietnam_gdp_2014_2023.csv', index=False, encoding='utf-8-sig')

# 3. Tính số liệu để nhận diện hai mẫu, không suy luận nguyên nhân từ biểu đồ.
dau = float(df.iloc[0]['gdp_ty_usd_2015'])
cuoi = float(df.iloc[-1]['gdp_ty_usd_2015'])
theo_nam = df.set_index('nam')
so_lan_tang = int((df['gdp_ty_usd_2015'].diff().dropna() > 0).sum())
tom_tat = {
    'gdp_2014': dau, 'gdp_2023': cuoi,
    'chenh_lech_ty_usd': cuoi - dau,
    'tang_ca_ky_pct': (cuoi / dau - 1) * 100,
    'so_lan_tang_lien_nam': so_lan_tang,
    'tb_2014_2019': float(df.loc[df['nam'].between(2014, 2019), 'tang_truong_pct'].mean()),
    'tb_2020_2021': float(df.loc[df['nam'].between(2020, 2021), 'tang_truong_pct'].mean()),
    'nam_thap_nhat': int(df.loc[df['tang_truong_pct'].idxmin(), 'nam']),
    'nam_cao_nhat': int(df.loc[df['tang_truong_pct'].idxmax(), 'nam']),
    'tang_2021_2022_diem_pct': float(theo_nam.loc[2022, 'tang_truong_pct'] - theo_nam.loc[2021, 'tang_truong_pct']),
    'tang_truong_theo_nam': {str(n): float(v) for n, v in theo_nam['tang_truong_pct'].items()},
    'so_dong_goc': so_dong_goc, 'so_dong_thieu': so_dong_thieu,
    'so_dong_trung': so_dong_trung, 'so_dong_sau_xu_ly': len(df),
    'worldbank_lastupdated': meta_gdp['lastupdated'],
    'nguon_gdp': url_gdp, 'nguon_tang_truong': url_tt
}
(KET_QUA / 'tom_tat_phan_tich.json').write_text(
    json.dumps(tom_tat, ensure_ascii=False, indent=2), encoding='utf-8')

# 4. Biểu đồ đường: quy mô GDP theo giá cố định năm 2015.
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 11})
fig, ax = plt.subplots(figsize=(8.4, 3.7))
ax.plot(df['nam'], df['gdp_ty_usd_2015'], marker='o', color='#39729D', linewidth=2)
ax.set(title='Quy mô GDP Việt Nam giai đoạn 2014–2023',
       xlabel='Năm', ylabel='Tỷ USD theo giá cố định 2015')
ax.set_xticks(df['nam'])
ax.set_ylim(0, 430)
ax.grid(axis='y', alpha=0.25)
for nam in [2014, 2023]:
    gia_tri = theo_nam.loc[nam, 'gdp_ty_usd_2015']
    ax.annotate(f'{gia_tri:.2f}', (nam, gia_tri), xytext=(0, 10),
                textcoords='offset points', ha='center')
fig.tight_layout()
fig.savefig(KET_QUA / 'bieu_do_1_quy_mo_gdp.png', dpi=220)
plt.close(fig)

# 5. Biểu đồ cột: tốc độ tăng trưởng từng năm.
fig, ax = plt.subplots(figsize=(8.4, 3.7))
mau = ['#C27A35' if n in [2020, 2021] else '#39729D' for n in df['nam']]
cot = ax.bar(df['nam'].astype(str), df['tang_truong_pct'], color=mau)
ax.bar_label(cot, fmt='%.2f', padding=3, fontsize=9)
ax.set(title='Tăng trưởng GDP Việt Nam giai đoạn 2014–2023',
       xlabel='Năm', ylabel='Tăng trưởng GDP (%)')
ax.set_ylim(0, 10)
ax.grid(axis='y', alpha=0.25)
ax.set_axisbelow(True)
fig.tight_layout()
fig.savefig(KET_QUA / 'bieu_do_2_tang_truong_gdp.png', dpi=220)
plt.close(fig)

# 6. Lưu nhật ký kết quả thực thi.
nhat_ky = (
    f'Nguồn: World Bank WDI; cập nhật: {meta_gdp["lastupdated"]}\n'
    f'Dữ liệu ghép ban đầu: {so_dong_goc} dòng, 3 cột\n'
    f'Dòng thiếu hoặc không chuyển được sang số: {so_dong_thieu}\n'
    f'Dòng trùng hoàn toàn: {so_dong_trung}\n'
    f'Sau xử lý: {len(df)} dòng, {len(df.columns)} cột\n\n'
    + df.round(2).to_string(index=False)
    + f'\n\nGDP tăng qua {so_lan_tang}/9 khoảng liên năm.'
    + f'\nGDP tăng cả kỳ: {tom_tat["tang_ca_ky_pct"]:.2f}%.'
    + f'\nTăng trưởng thấp nhất: {tom_tat["nam_thap_nhat"]}.'
    + f'\nTăng trưởng cao nhất: {tom_tat["nam_cao_nhat"]}.\n'
)
(KET_QUA / 'nhat_ky_chay.txt').write_text(nhat_ky, encoding='utf-8')
print(nhat_ky)
