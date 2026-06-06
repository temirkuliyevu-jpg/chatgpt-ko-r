# 🤖 UstaTop Bot — Gemini AI Integratsiyali Versiya

## ✨ Yangi Xususiyatlar

- 🤖 **Gemini AI Yordamchi** — foydalanuvchilar AI dan savollariga javob olishi mumkin
- 🧠 **Intelligent Service Detection** — AI muammoni batafsil tahlil qiladi
- 📊 **Smart Categorization** — AI muammoning kategoriyasini avtomatik aniqlaydi
- 💬 **Conversational AI** — tabiiy tilni qayta ishlash

## 🚀 Ishga tushirish

### 1️⃣ Paketlarni o'rnatish

```bash
pip install -r requirements.txt
```

### 2️⃣ Environment Variables sozlash

```bash
export BOT_TOKEN="8966706827:AAGO9hAyC4JPxxvigsab1cmii2iIjIWOG-8"
export GEMINI_API_KEY="AIzaSyBwdV5xOX7kGMKK9fKMUNkRJ7U2MbgFkG8"
export ADMIN_ID="123456789"  # o'zingizning ID-ingiz
```

Yoki `.env` faylida:

```
BOT_TOKEN=8966706827:AAGO9hAyC4JPxxvigsab1cmii2iIjIWOG-8
GEMINI_API_KEY=AIzaSyBwdV5xOX7kGMKK9fKMUNkRJ7U2MbgFkG8
ADMIN_ID=123456789
```

### 3️⃣ Botni ishga tushirish

```bash
python bot_ai.py
```

## 📋 Yangi Buyruqlar va Tugmalar

| Tugma | Tavsif |
|-------|--------|
| 📋 Buyurtma berish | Yangi buyurtma berish (eskisi kabi) |
| 📊 Mening buyurtmalarim | O'z buyurtmalarni ko'rish |
| **🤖 AI Yordam** | **YANGI**: AI yordamchiga savol berish |
| ℹ️ Ma'lumot | Platforma haqida |
| 📞 Aloqa | Kontakt ma'lumotlar |

## 🤖 AI Yordamchi Qanday Ishlaydi?

### Savol berish

Foydalanuvchi "🤖 AI Yordam" tugmasini bosadi va savolini yozadi:

```
💬 Foydalanuvchi: "Suv oqyapti, birinchi nima qilishim kerak?"
🤖 AI: "Birinchi, suvni ochib qo'ymang. Kran ostidagi qo'ziqni yopib qo'ying...
        Keyin santexnikni chaqiring. Muammongiz uchun eng yaxshi xizmat - 
        Santexnik bo'lib, kran ta'miri bo'ladi."
```

### Auto-Detect Service

Foydalanuvchi matn yozsachi, AI avtomatik xizmat turini aniqlaydi:

```
💬 Foydalanuvchi: "Elektr rozetkasi buzildi, o'rnatish kerak"
🤖 Bot: "AI muammongizni tushunadim! ⚡ Elektrik xizmati kerak ko'rinadi. 
         ✅ Tasdiqlaysizmi yoki boshqa xizmat tanlaysizmi?"
```

### Smart Categorization

Buyurtma berishda muammoni kategoriyalash:

```
Xizmat: 🔧 Santexnik
Muammo: "Vanna xonasidagi kran buzildi, oqyapti"
AI Kategorizatsiya: ✅ "Kran ta'miri" (Eski: "Santexnik — Umumiy muammo")
```

## 🔄 API Integratsiyasi

Bot quyidagi AI funksiyalaridan foydalanadi:

### 1. `get_ai_response(user_message, context_info)`
Foydalanuvchining savollariga AI javob beradi.

```python
response = get_ai_response("Kran ta'miri qancha turadi?")
# Natija: "Kran ta'miri odatda 30-60 daqiqada bajariladi..."
```

### 2. `detect_service_with_ai(text)`
Matndan xizmat turini aniqlaydi.

```python
service = detect_service_with_ai("Elektr rozetkasi buzildi")
# Natija: "elektrik"
```

### 3. `categorize_with_ai(description, service_id)`
Muammoni kategoriyalaydi.

```python
cat = categorize_with_ai("Kran oqyapti", "santexnik")
# Natija: "Kran ta'miri"
```

## 📊 Database Schema

Buyurtmalar bazasiga yangi maydoni yo'q. Mavjud struktura:

```sql
orders (
  id INTEGER,
  name TEXT,
  phone TEXT,
  address TEXT,
  service_type TEXT,
  category TEXT,           -- AI yordamida to'ldiriladi
  description TEXT,
  status TEXT,
  price TEXT,
  note TEXT,
  created_at TEXT
)
```

## ⚙️ Sozlamalar

### Gemini API Kaliti
- Kalitni `.env` yoki kodda `GEMINI_API_KEY` o'zgaruvchida saqlang
- Kalitni publicda chop etmang!
- API cheklovlari: 60 so'rov/minut (free tier)

### Admin Notifikatsiyalari
Yangi buyurtmada admin notification mavjud:
```python
ADMIN_ID = 123456789  # o'zingizning ID-ingiz
```

### Bot Token
```python
TOKEN = "8966706827:AAGO9hAyC4JPxxvigsab1cmii2iIjIWOG-8"
```

## 🛡️ Xavfsizlik Maslahatlar

1. **API Kalitlarni Muhofaza Qiling**
   ```bash
   # .gitignore da qo'shing
   .env
   bot_config.py
   ```

2. **Rate Limiting**
   - Gemini API 60 so'rov/minutga cheklangan
   - Juda ko'p so'rovlar uchun backup keyword-based method
   
3. **Error Handling**
   - AI javob berish uchun timeout: 10 sekund
   - Agar API fail bo'lsa, keyword-based detect ishlatiladi

## 🧪 Testing

### AI Response sinashi
```bash
python -c "
from bot_ai import get_ai_response
response = get_ai_response('Kran qancha turadi?')
print(response)
"
```

### Service Detection sinashi
```bash
python -c "
from bot_ai import detect_service_with_ai
service = detect_service_with_ai('Elektr rozetkasi buzildi')
print(f'Detected: {service}')
"
```

## 📈 Performance Tips

1. **Caching** - Tez javoblar uchun cache qo'shish mumkin
2. **Batch Processing** - Ko'p buyurtmalar uchun API batch call
3. **Fallback** - AI failed bo'lsa, keyword method ishlatiladi

## 🐛 Muammolarni Hal Qilish

### "GEMINI_API_KEY not found"
```bash
# Kalitni environment'ga qo'shing
export GEMINI_API_KEY="your_api_key_here"
python bot_ai.py
```

### Gemini API timeout
- Network tekshiring
- Rate limit check qiling
- Keyword-based fallback avtomatik ishlaydi

### Sqlite3 xatosi
```bash
# Database file o'chirib, qayta ishga tushiring
rm usta_booking.db
python bot_ai.py
```

## 📝 Logs

Bot chiqomlari:
```
INFO:root:🤖 UstaTop bot (Gemini AI integratsiyali) ishga tushdi!
DEBUG:telegram.ext:Polling started
```

## 🔗 Foydali Linklar

- [Gemini AI Docs](https://ai.google.dev)
- [python-telegram-bot Docs](https://python-telegram-bot.readthedocs.io)
- [UstaTop.uz](https://usatop.uz)

## 📧 Qo'llab-quvvatlash

Muammolar uchun:
- Email: info@usatop.uz
- Telegram: @usatop_support

---

**Version**: 2.0 (Gemini AI)
**Last Updated**: 2024-12-20
