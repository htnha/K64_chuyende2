import os
import logging
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (ApplicationBuilder, CommandHandler, ContextTypes,
                          CallbackQueryHandler, MessageHandler, filters)
from main import get_weather_data, provinces, normalize_name, province_search

# Load biến môi trường
load_dotenv()

# Cấu hình logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "🌤️ *Weather Bot* - Tra cứu thời tiết Việt Nam\n\n"
        "Các lệnh có sẵn:\n"
        "/help - Hiển thị trợ giúp\n"
        "/tracuu [tên tỉnh] - Tra cứu thời tiết tỉnh\n"
        "/danhsach - Xem danh sách tỉnh thành\n\n"
        "Ví dụ:\n"
        "/tracuu Hà Nội\n"
        "/tracuu TP HCM"
    )
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def tracuu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Vui lòng nhập tên tỉnh. Ví dụ: /tracuu Hà Nội")
        return
    
    province_name = ' '.join(context.args)
    search_term = normalize_name(province_name)
    
    if search_term in province_search:
        selected_vn, selected_en = province_search[search_term]
        await send_weather_info(update, selected_vn, selected_en)
        return
    
    matches = [k for k in province_search.keys() if search_term in k]
    if matches:
        buttons = [
            [InlineKeyboardButton(province_search[match][0], callback_data=f"search:{province_search[match][0]}")]
            for match in matches[:3]
        ]
        await update.message.reply_text(
            f"🔍 Tìm thấy {len(matches)} kết quả phù hợp với '{province_name}':",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    else:
        await update.message.reply_text(f"❌ Không tìm thấy tỉnh '{province_name}'")

async def handle_search_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data.startswith("search:"):
        province_name = query.data.split(":")[1]
        found = provinces.get(province_name)
        if found:
            await query.delete_message()
            await send_weather_info(query, province_name, found)
        else:
            await query.edit_message_text("⚠️ Tỉnh thành không tồn tại")

async def send_weather_info(update, vn_name, en_name):
    data = get_weather_data(en_name)
    if 'current' in data:
        current = data['current']
        response = (
            f"🌤 *Thời tiết {vn_name}*\n"
            f"📍 Nhiệt độ: {current['temperature']}°C\n"
            f"🌡 Cảm giác như: {current['feelslike']}°C\n"
            f"💧 Độ ẩm: {current['humidity']}%\n"
            f"🌬 Gió: {current['wind_speed']} km/h\n"
            f"📝 Trạng thái: {current['weather_descriptions'][0]}"
        )
        await update.message.reply_text(response, parse_mode='Markdown')
    else:
        await update.message.reply_text(f"❌ Lỗi: {data.get('error', 'Không thể lấy dữ liệu')}")

async def danhsach(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(province, callback_data=f"province:{province}")]
                for province in provinces.keys()]
    await update.message.reply_text(
        "📋 Danh sách tỉnh thành:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    province_name = query.data.replace("province:", "")
    found = provinces.get(province_name)
    
    if found:
        data = get_weather_data(found)
        if 'current' in data:
            current = data['current']
            response = (
                f"🌤 *Thời tiết {province_name}*\n"
                f"📍 Nhiệt độ: {current['temperature']}°C\n"
                f"🌡 Cảm giác như: {current['feelslike']}°C\n"
                f"💧 Độ ẩm: {current['humidity']}%\n"
                f"🌬 Gió: {current['wind_speed']} km/h\n"
                f"📝 Trạng thái: {current['weather_descriptions'][0]}"
            )
            await query.edit_message_text(response, parse_mode='Markdown')
        else:
            await query.edit_message_text(f"❌ Lỗi: {data.get('error', 'Không thể lấy dữ liệu')}")
    else:
        await query.edit_message_text("⚠️ Tỉnh thành không tồn tại trong hệ thống")

if __name__ == '__main__':
    application = ApplicationBuilder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", start))
    application.add_handler(CommandHandler("tracuu", tracuu))
    application.add_handler(CommandHandler("danhsach", danhsach))
    application.add_handler(CallbackQueryHandler(handle_search_callback, pattern="^search:"))
    application.add_handler(CallbackQueryHandler(button_handler, pattern="^province:"))
    
    application.run_polling()
