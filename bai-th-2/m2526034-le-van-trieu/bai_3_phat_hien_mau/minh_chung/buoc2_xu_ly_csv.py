import pandas as pd

df = pd.read_csv('du_lieu/vietnam_gdp_goc.csv')
for cot in df.columns:
    df[cot] = pd.to_numeric(df[cot], errors='coerce')
print('So dong thieu hoac sai kieu:', df.isna().any(axis=1).sum())
print('So dong trung:', df.duplicated().sum())
df = df.dropna().drop_duplicates().copy()
df = df[df['nam'].between(2014, 2023)].sort_values('nam')
df['nam'] = df['nam'].astype(int)
df['gdp_ty_usd_2015'] = df['gdp_usd_2015'] / 1_000_000_000
df = df[['nam', 'gdp_ty_usd_2015', 'tang_truong_pct']]
df.to_csv('ket_qua/vietnam_gdp_2014_2023.csv', index=False, encoding='utf-8-sig')
print('Sau xu ly:', df.shape[0], 'dong,', df.shape[1], 'cot')
print(df.round(2).to_string(index=False))
