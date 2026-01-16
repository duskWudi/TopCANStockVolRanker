import pandas as pd
import yfinance as yf
import streamlit as st

st.title("CA Top 20 Canada 高量股 (V1)")

df_t = pd.read_csv("tickers_ca.csv", encoding="utf-8-sig")

# normalize column names
df_t.columns = df_t.columns.str.strip().str.lower()

# (optional debug)
# st.write("CSV columns:", df_t.columns.tolist())

tickers = df_t["ticker"].dropna().astype(str).tolist()


rows = []
for t in tickers:
    hist = yf.Ticker(t).history(period="7d", interval="1d")
    if hist.empty:
        continue
    last = hist.iloc[-1]
    close = float(last["Close"])
    vol = float(last["Volume"])
    rows.append({"Ticker": t, "Close": close, "Volume": vol, "DollarVolume": close * vol})

df = pd.DataFrame(rows).sort_values("DollarVolume", ascending=False).head(20)
st.dataframe(df, use_container_width=True)