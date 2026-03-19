import os
import re
import logging
import yt_dlp
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Logging sozlash
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot tokenini environment variable dan olish
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")

# Instagram URL ni tekshirish
def is_instagram_url(url: str) -> bool:
    pattern = r'(https?://)?(www\.)?instagram\.com/(p|reel|tv)/[\w-]+'
    return bool(re.search(pattern, url))

# /start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Salom! Men Instagram video yuklovchi botman.\n\n"
        "📥 Ishlash tartibi:\n"
        "Instagram post yoki reel havolasini yuboring, men videoni yuklab beraman!\n\n"
        "📌 Misol:\n"
        "https://www.instagram.com/reel/ABC123/\n\n"
        "⚠️ Faqat ochiq (public) akkauntlar ishlaydi."
    )

# /help komandasi
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "ℹ️ Yordam:\n\n"
        "1. Instagram dan video/reel havolasini nusxalab oling\n"
        "2. Shu havolani menga yuboring\n"
        "3. Video yuklab beriladi\n\n"
        "📌 Qo'llab-quvvatlanadigan formatlar:\n"
        "• Instagram Reels\n"
        "• Instagram Posts (video)\n"
        "• Instagram TV (IGTV)\n\n"
        "⚠️ Eslatma: Faqat ochiq akkauntlar ishlaydi!"
    )

# Video yuklab olish funksiyasi
def download_video(url: str) -> tuple[str | None, str | None]:
    """
    Videoni yuklab oladi.
    Returns: (fayl_nomi, xato_xabari)
    """
    output_path = f"/tmp/instagram_video_%(id)s.%(ext)s"
    
    ydl_opts = {
        'outtmpl': output_path,
        'format': 'best[ext=mp4]/best',
        'cookiefile': 'www.instagram.com_cookies.txt',
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            
            # .mp4 kengaytmasini tekshirish
            if not filename.endswith('.mp4'):
                base = filename.rsplit('.', 1)[0]
                mp4_file = base + '.mp4'
                if os.path.exists(mp4_file):
                    filename = mp4_file
            
            return filename, None
    except yt_dlp.utils.DownloadError as e:
        error_msg = str(e)
        if "Private" in error_msg or "login" in error_msg.lower():
            return None, "🔒 Bu akkaunt yopiq (private). Faqat ochiq akkauntlar ishlaydi."
        elif "404" in error_msg:
            return None, "❌ Video topilmadi. Havola noto'g'ri yoki o'chirilgan bo'lishi mumkin."
        else:
            return None, f"❌ Yuklab olishda xato: {error_msg[:200]}"
    except Exception as e:
        return None, f"❌ Kutilmagan xato: {str(e)[:200]}"

# Xabarlarni qayta ishlash
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    
    # Instagram URL emasligini tekshirish
    if not is_instagram_url(text):
        await update.message.reply_text(
            "⚠️ Bu Instagram havolasi emas.\n\n"
            "Iltimos, Instagram post yoki reel havolasini yuboring.\n"
            "Misol: https://www.instagram.com/reel/ABC123/"
        )
        return
    
    # Yuklanayotganligi haqida xabar
    status_msg = await update.message.reply_text("⏳ Video yuklanmoqda, iltimos kuting...")
    
    # Videoni yuklab olish
    filename, error = download_video(text)
    
    if error:
        await status_msg.edit_text(error)
        return
    
    if not filename or not os.path.exists(filename):
        await status_msg.edit_text("❌ Video fayli topilmadi. Qayta urinib ko'ring.")
        return
    
    # Fayl hajmini tekshirish (Telegram 50MB limit)
    file_size = os.path.getsize(filename)
    if file_size > 50 * 1024 * 1024:  # 50MB
        os.remove(filename)
        await status_msg.edit_text(
            "❌ Video hajmi juda katta (50MB dan oshiq).\n"
            "Telegram 50MB gacha fayllarni qabul qiladi."
        )
        return
    
    # Videoni yuborish
    try:
        await status_msg.edit_text("📤 Video yuborilmoqda...")
        with open(filename, 'rb') as video_file:
            await update.message.reply_video(
                video=video_file,
                caption="✅ Mana sizning videongiz!\n\n🤖 @YourBotUsername",
                supports_streaming=True
            )
        await status_msg.delete()
    except Exception as e:
        await status_msg.edit_text(f"❌ Video yuborishda xato: {str(e)[:200]}")
    finally:
        # Vaqtinchalik faylni o'chirish
        if os.path.exists(filename):
            os.remove(filename)

# Botni ishga tushirish
def main():
    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("❌ Xato: BOT_TOKEN o'rnatilmagan!")
        print("export BOT_TOKEN='your_token_here' buyrug'ini ishlatib token o'rnating.")
        return
    
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Handlerlarni qo'shish
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("🤖 Bot ishga tushdi...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
