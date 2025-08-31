import io
import pandas as pd
import matplotlib.pyplot as plt

def make_receipt_pdf_bytes(address, owner, fee_month, amount, paid_at, cashier, note=""):
    fig, ax = plt.subplots(figsize=(8.27, 11.69))  # A4
    ax.axis('off')
    lines = [
        "長億城D區 管理費收據（示範）",
        "",
        f"地址（住戶）: {address}",
        f"戶名（區權人）: {owner or '-'}",
        f"費用月份: {fee_month}",
        f"金額（NTD）: {amount}",
        f"繳款時間: {pd.to_datetime(paid_at).strftime('%Y-%m-%d %H:%M:%S') if pd.notnull(paid_at) else '-'}",
        f"經手人: {cashier or '-'}",
        "",
        f"備註: {note or '-'}",
        "",
        "本收據由系統自動產生。"
    ]
    y = 0.95
    for ln in lines:
        ax.text(0.05, y, ln, transform=ax.transAxes, fontsize=14, va='top')
        y -= 0.05
    bio = io.BytesIO()
    fig.savefig(bio, format="pdf", bbox_inches="tight")
    plt.close(fig)
    bio.seek(0)
    return bio
