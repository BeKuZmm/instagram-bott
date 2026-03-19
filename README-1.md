# 📱 Instagram Video Yuklovchi Telegram Bot

## 🚀 O'rnatish va Ishga Tushirish

### 1. Telegram Bot yaratish
1. Telegramda **@BotFather** ni oching
2. `/newbot` buyrug'ini yuboring
3. Bot nomini kiriting (masalan: `Instagram Downloader`)
4. Username kiriting (masalan: `my_insta_dl_bot`)
5. **API tokenini** nusxalab oling (ko'rinishi: `123456:ABC-DEF...`)

### 2. Kutubxonalarni o'rnatish
```bash
pip install -r requirements.txt
```

### 3. Bot tokenini o'rnatish
```bash
# Linux/Mac
export BOT_TOKEN="your_token_here"

# Windows (CMD)
set BOT_TOKEN=your_token_here

# Windows (PowerShell)
$env:BOT_TOKEN="your_token_here"
```

### 4. Botni ishga tushirish
```bash
python instagram_bot.py
```

---

## 📋 Bot Imkoniyatlari

| Buyruq | Tavsif |
|--------|--------|
| `/start` | Botni boshlash |
| `/help` | Yordam |
| Instagram URL | Videoni yuklab beradi |

---

## ✅ Qo'llab-quvvatlanadigan Formatlar
- Instagram Reels
- Instagram Posts (video)
- Instagram TV (IGTV)

## ⚠️ Cheklovlar
- Faqat **ochiq (public)** akkauntlar ishlaydi
- Maksimal video hajmi: **50MB** (Telegram cheklovi)

---

## 🛠️ Server (VPS) ga Deploy Qilish

### Systemd service (Linux)
```bash
# /etc/systemd/system/instagram-bot.service faylini yarating
[Unit]
Description=Instagram Telegram Bot
After=network.target

[Service]
ExecStart=/usr/bin/python3 /path/to/instagram_bot.py
Environment=BOT_TOKEN=your_token_here
Restart=always
User=ubuntu

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable instagram-bot
sudo systemctl start instagram-bot
```

### Screen orqali
```bash
screen -S instagram-bot
export BOT_TOKEN="your_token"
python instagram_bot.py
# Ctrl+A, D - screen dan chiqish
```
