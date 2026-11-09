from pathlib import Path
import pandas as pd

THU_MUC = Path(__file__).resolve().parent

def extract():
    return pd.read_csv(THU_MUC / "du_lieu/taxis_goc.csv")

def transform(df):
    df = df.dropna().drop_duplicates().copy()
    # Chuẩn hóa ba cột: màu xe, cách thanh toán và ngày đón khách.
    df["color"] = df["color"].str.strip().str.lower()
    df["payment"] = df["payment"].str.strip().str.lower()
    df["pickup"] = pd.to_datetime(df["pickup"], errors="coerce").dt.strftime("%Y-%m-%d")
    return df

def load(df):
    df.to_csv(THU_MUC / "ket_qua/taxis_etl.csv", index=False, encoding="utf-8-sig")

if __name__ == "__main__":
    du_lieu = extract()
    print(f"Extract: đọc {len(du_lieu)} dòng từ CSV")
    du_lieu = transform(du_lieu)
    print(f"Transform: còn {len(du_lieu)} dòng; chuẩn hóa color, payment, pickup")
    load(du_lieu)
    print("Load: đã ghi ket_qua/taxis_etl.csv")
    print(du_lieu[["color", "payment", "pickup"]].head().to_string(index=False))
