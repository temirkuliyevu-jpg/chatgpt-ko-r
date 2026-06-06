# 🤖 UstaTop Telegram Bot

UstaTop platformasi uchun professional Telegram bot. Foydalanuvchilar botdan to'g'ridan-to'g'ri usta chaqirish buyurtmasi bera oladi.

## ✨ Xususiyatlar

- 🔄 **Conversation flow** — bosqichma-bosqich buyurtma berish jarayoni
- ⌨️ **Inline keyboards** — qulay tugma orqali xizmat tanlash
- 🗄️ **SQLite DB** — buyurtmalar web-sayt bilan umumiy bazada saqlanadi
- 🤖 **Auto-detect** — matn orqali avtomatik xizmat turi aniqlash
- 📊 **Mening buyurtmalarim** — foydalanuvchi o'z buyurtmalarini ko'rishi
- 🔔 **Admin bildirishnoma** — yangi buyurtmada adminga xabar
- 👥 **Foydalanuvchilar bazasi** — ro'yxatdan o'tgan userlar

## 🚀 Ishga tushirish

```bash
pip install -r requirements.txt
python bot.py
```

## ⚙️ Sozlash

`bot.py` faylida:
- `TOKEN` — BotFather dan olingan token
- `ADMIN_ID` — adminning Telegram ID si (bildirishnomalar uchun)
- `DB_PATH` — usta_booking.db fayl yo'li

## 📋 Buyruqlar

| Buyruq | Tavsif |
|--------|--------|
| `/start` | Botni ishga tushirish |
| `/book` | Yangi buyurtma berish |
| `/cancel` | Jarayonni bekor qilish |
| `/admin` | Statistika (admin uchun) |

## 🔄 Conversation States

```
START → SELECT_SERVICE → GET_DESCRIPTION → GET_NAME → GET_PHONE → GET_ADDRESS → CONFIRM → ✅
```

## 📁 Fayl tuzilishi

```
Master call bot/
├── bot.py              ← Asosiy bot kodi
├── usta_categorize.py  ← Muammoni kategoriyalash
├── requirements.txt    ← Python kutubxonalar
├── README.md           ← Shu fayl
└── usta_booking.db     ← Umumiy SQLite baza (avtomatik)
```
