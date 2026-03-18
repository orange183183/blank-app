import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import asyncio
from telegram import Bot

# ====== Telegram 設定 ======
TOKEN = "8643286375:aahfhqxwpy9ej-pr7vdth43kjd0gokrctf4"       # 換成你的 Bot Token
CHAT_ID = "5684506085"     # 換成抓到的聊天 ID

async def send_telegram(msg):
    bot = Bot(token=TOKEN)
    await bot.send_message(chat_id=CHAT_ID, text=msg)

# ====== Google Sheets ======
scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)
sheet = client.open("AI報價名單").sheet1  # 你的 Google Sheet 名稱

def save_to_sheet(data):
    sheet.append_row(data)

# ====== Streamlit UI ======
st.title("📷 嘉達工程 AI報價系統")

name = st.text_input("姓名")
phone = st.text_input("電話")
st.divider()
camera = st.number_input("攝影機數量", min_value=1, value=4)
floor = st.number_input("樓層數", min_value=1, value=1)
cable = st.selectbox("是否需要重新拉線", ["否", "是"])
remote = st.selectbox("是否需要手機遠端監控", ["否", "是"])

if st.button("📊 送出報價"):
    if name == "" or phone == "":
        st.warning("請填寫姓名與電話")
    else:
        # 計算價格
        price = camera * 3000 + camera * 1500 + 8000
        if cable == "是":
            price += floor * 1000
        if remote == "是":
            price += 3000

        # 顯示價格
        st.subheader("💰 預估價格")
        st.write(f"NT$ {price:,}")

        # 儲存 Google Sheet
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        save_to_sheet([now, name, phone, camera, floor, cable, remote, price])

        # 發送 Telegram
        msg = f"""
📷 新報價
姓名: {name}
電話: {phone}
攝影機: {camera}
樓層: {floor}
拉線: {cable}
遠端: {remote}
💰 {price} 元
"""
        # 非同步發送
        asyncio.run(send_telegram(msg))

        st.success("✅ 已送出！Telegram 已通知！")