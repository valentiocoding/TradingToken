import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="USDT Sell Profit Calculator", layout="centered")
st.title("💵 USDT Sell Profit Calculator")
st.caption("Simulasikan keuntungan jual USDT ke berbagai perusahaan berdasarkan harga beli luar dan rate perusahaan dari BCA E-Rate.")

# --- Input Section ---
with st.expander("📝 Masukkan Data"):
    col1, col2 = st.columns(2)
    with col1:
        erate = st.number_input("BCA E-Rate", value=None, placeholder="Contoh: 16000", step=100)
    with col2:
        total_usdt = st.number_input("Total USDT", value=None, placeholder="Contoh: 100", step=10)

buy_rate = st.number_input("Harga Beli per USDT (dari penjual luar)", value=None, placeholder="Contoh: 15800", step=100)

if erate and total_usdt and buy_rate:
    rates = {
        "R (-20)": erate - 20,
        "DB (-1.3%)": erate / 1.013,
        "CFX (-4%)": erate / 1.04
    }

    sell_df = pd.DataFrame([
        {"Company": name, "Sell Rate": rate, "Total Revenue (IDR)": rate * total_usdt}
        for name, rate in rates.items()
    ])
    sell_df["Buy Rate"] = buy_rate
    sell_df["Total Cost"] = buy_rate * total_usdt
    sell_df["Profit (IDR)"] = sell_df["Total Revenue (IDR)"] - sell_df["Total Cost"]
    sell_df["Formatted Profit"] = sell_df["Profit (IDR)"].apply(lambda x: f"Rp {x:,.0f}".replace(",", "."))

    st.subheader("📈 Simulasi Penjualan USDT")
    st.dataframe(sell_df[["Company", "Sell Rate", "Formatted Profit"]], use_container_width=True)

    # Grafik Profit
    st.subheader("📊 Grafik Profit Penjualan ke Perusahaan")
    st.altair_chart(
        alt.Chart(sell_df).mark_bar().encode(
            x=alt.X("Company", title="Perusahaan"),
            y=alt.Y("Profit (IDR)", title="Profit (Rp)"),
            color="Company"
        ).properties(height=300),
        use_container_width=True
    )

    # Highlight best profit
    best = sell_df.loc[sell_df["Profit (IDR)"].idxmax()]
    st.success(f"💰 Profit Tertinggi: **{best['Company']}** → {best['Formatted Profit']}")

else:
    st.info("Masukkan BCA E-Rate, jumlah USDT, dan harga beli untuk mulai simulasi.")
