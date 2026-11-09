import pandas as pd

df = pd.read_csv('ket_qua/vietnam_gdp_2014_2023.csv')
dau = df.iloc[0]['gdp_ty_usd_2015']
cuoi = df.iloc[-1]['gdp_ty_usd_2015']
print('GDP dau - cuoi ky:', round(dau, 2), '-', round(cuoi, 2), 'ty USD')
print('Chenh lech:', round(cuoi - dau, 2), 'ty USD')
print('Tang ca ky:', round((cuoi / dau - 1) * 100, 2), '%')
print('So khoang lien nam tang:', (df['gdp_ty_usd_2015'].diff() > 0).sum(), '/ 9')
thap = df.loc[df['tang_truong_pct'].idxmin()]
cao = df.loc[df['tang_truong_pct'].idxmax()]
print('Tang truong thap nhat:', int(thap['nam']), round(thap['tang_truong_pct'], 2), '%')
print('Tang truong cao nhat:', int(cao['nam']), round(cao['tang_truong_pct'], 2), '%')
