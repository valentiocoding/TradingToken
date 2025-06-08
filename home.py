import streamlit as st
import pandas as pd
import altair as alt

@st.dialog("Cast your vote")
def vote():
     st.warning("Are You sure want to Delete?") 
     if st.button("Delete"):
         st.balloons()
         st.rerun()
     
     
st.set_page_config(page_title="USDT Trade Calculator", layout="centered")
st.title("🪙 USDT Trade Calculator")
st.caption("Bandingkan biaya pembelian USDT dan analisis profit dari berbagai perusahaan.")

# --- Input Section ---
with st.expander("📝 Masukkan Data"):
    col1, col2 = st.columns(2)
    with col1:
        erate = st.number_input("BCA E-Rate", value=None, placeholder="Contoh: 16000", step=100)
    with col2:
        total_usdt = st.number_input("Total USDT", value=None, placeholder="Contoh: 100", step=10)

if erate and total_usdt:
    rates = {
        "R (+20)": erate + 20, # r + 20
        "DB (+1.3%)": erate * 1.013, #db + 1.3%
        "CFX (+4%)": erate * 1.04 #cfx + 4%
    }

    buy_df = pd.DataFrame([
        {"Company": name, "Buy Rate": rate, "Total Cost (IDR)": rate * total_usdt}
        for name, rate in rates.items()
    ])
    buy_df["Formatted Total"] = buy_df["Total Cost (IDR)"].apply(lambda x: f"Rp {x:,.0f}".replace(",", "."))

    st.subheader("💸 Simulasi Pembelian")
    st.dataframe(buy_df[["Company", "Buy Rate", "Formatted Total"]], use_container_width=True)

    # Grafik Total Biaya
    st.subheader("📊 Total Biaya Pembelian per Perusahaan")
    st.altair_chart(
        alt.Chart(buy_df).mark_bar().encode(
            x=alt.X("Company", title="Perusahaan"),
            y=alt.Y("Total Cost (IDR)", title="Total Biaya (Rp)"),
            color="Company"
        ).properties(height=300),
        use_container_width=True
    )

    # --- Analisis Profit ---
    with st.expander("📈 Masukkan Harga Jual & Lihat Profit"):
        sell_rate = st.number_input("Harga Jual per USDT", value=None, placeholder="Contoh: 16500", step=100)

        if sell_rate:
            analysis_df = buy_df.copy()
            analysis_df["Sell Rate"] = sell_rate
            analysis_df["Profit (IDR)"] = (sell_rate - analysis_df["Buy Rate"]) * total_usdt
            analysis_df["Formatted Profit"] = analysis_df["Profit (IDR)"].apply(lambda x: f"Rp {x:,.0f}".replace(",", "."))

            st.subheader("🔍 Analisis Profit")
            st.dataframe(analysis_df[["Company", "Buy Rate", "Sell Rate", "Formatted Total", "Formatted Profit"]], use_container_width=True)

            # Highlight perusahaan dengan profit tertinggi
            best = analysis_df.loc[analysis_df["Profit (IDR)"].idxmax()]
            st.success(f"💰 Profit Tertinggi: **{best['Company']}** → {best['Formatted Profit']}")

            # Grafik Profit
            st.subheader("📊 Grafik Profit per Perusahaan")
            st.altair_chart(
                alt.Chart(analysis_df).mark_bar().encode(
                    x=alt.X("Company", title="Perusahaan"),
                    y=alt.Y("Profit (IDR)", title="Profit (Rp)"),
                    color="Company"
                ).properties(height=300),
                use_container_width=True
            )

            # CTA
            if st.button("🛒 Buat Order Sekarang"):
                vote()

else:
    st.info("Silakan masukkan nilai E-Rate dan jumlah USDT untuk memulai simulasi.")

