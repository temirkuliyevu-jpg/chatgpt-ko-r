# 🚀 UstaTop Bot — Tez O'rnatish (Quick Start)

## ⚡ 5 Daqiqada Ishga Tushirish

### 1️⃣ Prerequisites (Avval Kerak)
```bash
✅ Python 3.8+
✅ pip (Python package manager)
✅ Git (ixtiyoriy)
```

**Python Tekshirish:**
```bash
python --version
# Python 3.9.0 yoki undan yuqori
```

---

### 2️⃣ Kod Download Qilish

```bash
# Option A: ZIP fayldan
# -> Downloads ga saqlanadi

# Option B: Git (Agar installed bo'lsa)
git clone https://github.com/usatop/bot.git
cd bot
```

---

### 3️⃣ Dependencies O'rnatish

```bash
pip install -r requirements.txt
```

**Natija:**
```
Collecting python-telegram-bot==20.7
Collecting google-generativeai==0.3.0
Installing collected packages...
Successfully installed python-telegram-bot-20.7
Successfully installed google-generativeai-0.3.0
```

---

### 4️⃣ Environment Sozlamalar

#### A. `.env` Fayl Yaratish

```bash
# Eski faylni nusxa qilish
cp .env.example .env

# Yoki qo'lda yaratish
nano .env  # Linux/Mac
# YA
notepad .env  # Windows
```

#### B. `.env` Ichini Toldiraylik

```
BOT_TOKEN=8966706827:AAGO9hAyC4JPxxvigsab1cmii2iIjIWOG-8
GEMINI_API_KEY=AIzaSyBwdV5xOX7kGMKK9fKMUNkRJ7U2MbgFkG8
ADMIN_ID=123456789
```

**MUHIM:** Raqamlarni o'zingizning raqamlaringiz bilan almashtiring:
- `ADMIN_ID` → O'zingizning Telegram ID
- Topish: @userinfobot'ga /start yozing

---

### 5️⃣ Botni Ishga Tushirish

```bash
python bot_ai.py
```

**Expected Output:**
```
INFO:root:🤖 UstaTop bot (Gemini AI integratsiyali) ishga tushdi!
DEBUG:telegram.ext:Polling started
```

✅ **TAYYOR!** Bot ishga tushdi!

---

## 📱 Bot Tekshirish

1. **Telegramni Oching**
   - O'zingizning botni qidiring (BotFather dan olingan nom)

2. **/start Bosing**
   ```
   👋 Assalomu alaykum!
   🔨 UstaTop Botiga Xush Kelibsiz!
   ```

3. **Menyuni Test Qiling**
   - 📋 Buyurtma berish ✓
   - 📊 Mening buyurtmalarim ✓
   - 🤖 AI Yordam ✓ (YANGI)
   - ℹ️ Ma'lumot ✓
   - 📞 Aloqa ✓

4. **AI Yordam Test Qiling**
   - 🤖 AI Yordam tugmasini bosing
   - "Kran ta'miri qancha turadi?" - yozing
   - 🧠 Gemini AI javob beradi!

---

## 🆘 Muammolar va Yechimlar

### Problem 1: "ModuleNotFoundError: No module named 'telegram'"
```bash
# Yechim: pip install -r requirements.txt qayta ishga tushiring
pip install --upgrade -r requirements.txt
```

### Problem 2: "GEMINI_API_KEY not found"
```bash
# Yechim 1: .env fayli yaratilganmi tekshiring
ls -la .env

# Yechim 2: .env ni tekshiring
cat .env

# Yechim 3: Python ortamini restart qiling
pkill -f "python bot_ai.py"
python bot_ai.py
```

### Problem 3: Bot javob bermiyor
```bash
# Yechim: Network tekshiring
ping api.telegram.org
ping generativelanguage.googleapis.com

# Agar ping ishlamasa, VPN ishlatib ko'ring
```

### Problem 4: "Invalid API Key"
```bash
# Yechim: API Keyni qayta tekshiring
# Google AI Studio: https://aistudio.google.com/apikey
# Yangi key oling va .env ga qo'ying
```

---

## 🔍 Loglarni Ko'rish

```bash
# Hozirgi loglarni ko'rish
# (Bot ishga tushganda terminallda chiqadi)

# Loglarni faylga saqlash
python bot_ai.py > bot.log 2>&1 &

# Loglarni ko'rish
tail -f bot.log  # Real-time
cat bot.log      # Barcha loglar
```

---

## 📊 Advanced Options

### 1. Fonda Ishga Tushirish (Linux/Mac)

```bash
# Bot fonda ishga tushish
python bot_ai.py &

# Processni tekshirish
ps aux | grep bot_ai.py

# Processni to'xtatzish
kill <PID>
```

### 2. Screen orqali (Persistent)

```bash
# Screen o'rnatish
sudo apt-get install screen

# Bot ishga tushirish
screen -S ustagram
python bot_ai.py

# Screen'dan chiqish: Ctrl+A D
# Qayta kirish: screen -r ustagram
```

### 3. Systemd Service (Automatic Start)

**`/etc/systemd/system/ustagram.service` yaratish:**

```ini
[Unit]
Description=UstaTop Telegram Bot with Gemini AI
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/ustagram
ExecStart=/usr/bin/python3 /home/ubuntu/ustagram/bot_ai.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Ishga tushirish:**
```bash
sudo systemctl start ustagram
sudo systemctl enable ustagram
sudo systemctl status ustagram
```

---

## 📦 Production Setup

### 1. VPS/Server Tayyorlash

```bash
# System yangilash
sudo apt update && sudo apt upgrade -y

# Python o'rnatish
sudo apt install python3 python3-pip

# Loyihani clone qilish
cd /home/ubuntu
git clone <repo-url> ustagram
cd ustagram

# Dependencies
pip3 install -r requirements.txt
```

### 2. Environment Sozlamalar

```bash
# Secure .env fayl
nano /home/ubuntu/ustagram/.env

# Faqat owner o'qiy olsin
chmod 600 /home/ubuntu/ustagram/.env
```

### 3. Database Backup

```bash
# Kunlik backup
0 2 * * * cp /home/ubuntu/ustagram/usta_booking.db \
            /home/ubuntu/backup/usta_booking.$(date +%Y%m%d).db
```

---

## 🔐 Xavfsizlik Maslahatlar

1. **API Kalitlarni Muhofaza Qiling**
   ```bash
   # .gitignore ga qo'shing
   .env
   .env.local
   *.backup
   ```

2. **Git Commit Qilmang**
   ```bash
   # Agar versiyalash ishlatayotgan bo'lsangiz
   git add .
   git commit -m "Add new features (without .env)"
   
   # .env qo'shilgan bo'lsa, remove qiling
   git rm --cached .env
   ```

3. **Ruxsatlarni Sozlang**
   ```bash
   chmod 755 /home/ubuntu/ustagram
   chmod 600 /home/ubuntu/ustagram/.env
   chmod 644 /home/ubuntu/ustagram/*.py
   ```

---

## 📈 Performance Monitoring

### Bot Statusini Tekshirish

```bash
# Memory usage
ps aux | grep bot_ai

# Network connections
netstat -an | grep ESTABLISHED

# CPU load
top -p <PID>
```

### Database Optimization

```bash
# Database hajmi
du -sh usta_booking.db

# Defragmentation
sqlite3 usta_booking.db "VACUUM;"
```

---

## 🐛 Debug Mode

**Bot kodni debug rezhimida ishlatish:**

```python
# bot_ai.py ning birinchi bo'limida
import logging
logging.basicConfig(level=logging.DEBUG)  # INFO o'rniga

# Keyin
python bot_ai.py
```

**Natija:** Barcha debug ma'lumotlar chiqadi

---

## 📞 Qo'llab-quvvatlash

**Agar muammo bo'lsa:**
1. [README_AI.md](README_AI.md) ni o'qing
2. [AI_INTEGRATION_GUIDE.md](AI_INTEGRATION_GUIDE.md) ni tekshiring
3. GitHub Issues ga muammo qo'shing
4. info@usatop.uz ga email yuboring

---

## 🎓 Keying O'rganish Uchun

- [Python Tutorial](https://python.org/tutorials)
- [Telegram Bot API](https://core.telegram.org/bots)
- [Google Gemini API](https://ai.google.dev)
- [SQLite Tutorial](https://sqlite.org/tutorial.html)

---

## ✅ Setup Checklist

- [ ] Python 3.8+ o'rnatilgan
- [ ] `requirements.txt` o'rnatilgan
- [ ] `.env` fayl yaratilgan
- [ ] API Kalitlar to'g'ri
- [ ] Bot ishga tushdi ✅
- [ ] Telegram'da test qilindi
- [ ] Advanced features tekshirilgan
- [ ] Loglar saqlangani

---

## 🎉 Tayyor!

```
🤖 UstaTop Bot (Gemini AI) 
✅ ISHGA TUSHGAN VA ISHLAYAPTI
📱 Telegramda barcha foydalanuvchilarga xizmat beradi
💬 AI yordamchi 24/7 javob beradi
```

**Tabriklaymiz! Botingiz tayyor! 🚀**

---

**Versiya**: 2.0 (Quick Start)
**Yaratilgan**: 2024-12-20
**Status**: ✅ TAQDIRLANGAN

Savollar bo'lsa: @usatop_support
