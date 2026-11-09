from pathlib import Path
import pandas as pd

THU_MUC = Path(__file__).resolve().parent
df = pd.read_csv(THU_MUC / "du_lieu/taxis_goc.csv")
so_dong_goc = len(df)

# Bỏ dòng có ít nhất một ô thiếu, sau đó bỏ dòng trùng hoàn toàn.
df = df.dropna().copy()
so_dong_sau_dropna = len(df)
df = df.drop_duplicates().copy()
so_dong_sau_bo_trung = len(df)

# Tính thời lượng trước khi bỏ phần giờ trong hai cột ngày.
bat_dau = pd.to_datetime(df["pickup"], errors="coerce")
ket_thuc = pd.to_datetime(df["dropoff"], errors="coerce")
df["thoi_luong_phut"] = ((ket_thuc - bat_dau).dt.total_seconds() / 60).round(2)
# Tổng ba khoản có trong dữ liệu, không gồm phụ phí nằm ngoài ba cột này.
df["tong_phi_co_ban"] = (df["fare"] + df["tip"] + df["tolls"]).round(2)
df["pickup"] = bat_dau.dt.strftime("%Y-%m-%d")
df["dropoff"] = ket_thuc.dt.strftime("%Y-%m-%d")

df.to_csv(THU_MUC / "ket_qua/taxis_da_lam_sach.csv", index=False, encoding="utf-8-sig")
print("BÀI 1 - LÀM SẠCH DỮ LIỆU")
print(f"Ban đầu: {so_dong_goc} dòng")
print(f"Bỏ dòng thiếu: {so_dong_goc - so_dong_sau_dropna} dòng")
print(f"Bỏ dòng trùng: {so_dong_sau_dropna - so_dong_sau_bo_trung} dòng")
print(f"Kết quả: {len(df)} dòng, {len(df.columns)} cột")
print(df[["pickup", "dropoff", "thoi_luong_phut", "fare", "tip", "tolls", "tong_phi_co_ban"]].head().to_string(index=False))
