import streamlit as st
import pandas as pd
from utils import make_receipt_pdf_bytes

st.set_page_config(page_title="管理費查詢（公開版）", page_icon="📄", layout="wide")
st.title("管理費查詢（公開版）")

@st.cache_data
def load_data():
    return pd.read_excel("data/fee_data_normalized.xlsx")

df = load_data()

st.markdown("此版本開放所有人查詢，僅供檢視與下載收據（單筆）。")

with st.expander("查詢條件", expanded=True):
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        addr_kw = st.text_input("住址包含關鍵字")
    with c2:
        month_kw = st.text_input("月份（YYYY-MM）")
    with c3:
        only_paid = st.checkbox("只看已繳", value=True)
    with c4:
        only_unpaid = st.checkbox("只看未繳", value=False)

qry = df.copy()
if addr_kw:
    qry = qry[qry['address'].astype(str).str.contains(addr_kw, case=False, na=False)]
if month_kw:
    qry = qry[qry['fee_month'].astype(str) == month_kw]
if only_paid and not only_unpaid:
    qry = qry[qry['paid'].astype(bool)]
elif only_unpaid and not only_paid:
    qry = qry[~qry['paid'].astype(bool)]

st.dataframe(qry, use_container_width=True, height=480)

st.download_button(
    "下載上表（Excel）",
    data=(lambda d: (lambda io, pd: (pd.ExcelWriter(io, engine='openpyxl'), io))[1])(io:=__import__('io').BytesIO(), __import__('pandas')).to_excel if False else None,
    disabled=True,
    help="公開版不提供整表下載，如需請改用管理版。"
)

st.subheader("下載單筆 PDF 收據")
if qry.empty:
    st.info("目前沒有可下載的資料。調整上方篩選條件試試。")
else:
    sel_idx = st.number_input("輸入上表索引（index）", min_value=int(qry.index.min()), max_value=int(qry.index.max()), step=1)
    if sel_idx in qry.index:
        row = qry.loc[sel_idx]
        if bool(row.get("paid", False)) and pd.notnull(row.get("paid_at")):
            pdf_bytes = make_receipt_pdf_bytes(
                address=row.get("address"),
                owner=row.get("owner"),
                fee_month=row.get("fee_month"),
                amount=row.get("amount"),
                paid_at=row.get("paid_at"),
                cashier=row.get("cashier"),
                note=row.get("note"),
            )
            st.download_button(
                "下載該筆 PDF 收據",
                data=pdf_bytes,
                file_name=f"receipt_{row.get('address','na')}_{row.get('fee_month','na')}.pdf",
                mime="application/pdf"
            )
        else:
            st.warning("此筆尚未繳款，沒有收據可下載。")
