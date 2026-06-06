"""
UstaTop Telegram Bot — To'liq versiya
Conversation flow, inline keyboards, SQLite DB, admin panel
"""

import logging
import sqlite3
import os
from datetime import datetime
from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup,
    ReplyKeyboardMarkup, ReplyKeyboardRemove
)
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    ConversationHandler, CallbackQueryHandler,
    ContextTypes, filters
)

TOKEN = "8966706827:AAGO9hAyC4JPxxvigsab1cmii2iIjIWOG-8"
ADMIN_ID = None  # o'zingizning Telegram ID-ingizni qo'ying, masalan: 123456789
DB_PATH = "usta_booking.db"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ── Conversation states ───────────────────────────────────────────────────────
SELECT_SERVICE, GET_DESCRIPTION, GET_NAME, GET_PHONE, GET_ADDRESS, CONFIRM = range(6)

# ── Services ──────────────────────────────────────────────────────────────────
SERVICES = {
    "santexnik":    ("🔧", "Santexnik"),
    "elektrik":     ("⚡", "Elektrik"),
    "duradgor":     ("🪚", "Duradgor"),
    "rassomchi":    ("🎨", "Rassomchi"),
    "konditsioner": ("❄️", "Konditsioner"),
    "plitkakor":    ("🧱", "Plitkakor"),
}

KEYWORDS = {
    "santexnik":    ["kran", "quvur", "unitaz", "suv oqyapti", "lavabo", "kanalizatsiya", "vanna", "dush"],
    "elektrik":     ["tok", "elektr", "rozetka", "chiroq", "sim", "svet", "qisqa tutashuv", "lampa"],
    "duradgor":     ["eshik", "deraza", "mebel", "pol", "shkaf", "parket", "tokcha"],
    "rassomchi":    ["bo'yash", "devor", "suvash", "kraska", "oboi", "gips"],
    "konditsioner": ["konditsioner", "konditsaner", "sovitmayapti", "isitmayapti"],
    "plitkakor":    ["plitka", "mozaika", "granit", "mramor", "keramika"],
}

# ── DB ────────────────────────────────────────────────────────────────────────
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS orders (
        id           INTEGER PRIMARY KEY AUTOINCREMENT,
        name         TEXT NOT NULL,
        phone        TEXT NOT NULL,
        address      TEXT NOT NULL,
        service_type TEXT NOT NULL,
        category     TEXT NOT NULL,
        description  TEXT NOT NULL,
        status       TEXT DEFAULT 'Yangi',
        price        TEXT DEFAULT '',
        note         TEXT DEFAULT '',
        created_at   TEXT DEFAULT (datetime('now','localtime'))
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS bot_users (
        user_id    INTEGER PRIMARY KEY,
        username   TEXT,
        first_name TEXT,
        joined_at  TEXT DEFAULT (datetime('now','localtime'))
    )""")
    conn.commit()
    conn.close()

def save_order(data: dict) -> int:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT INTO orders (name,phone,address,service_type,category,description) VALUES (?,?,?,?,?,?)",
        (data["name"], data["phone"], data["address"],
         data["service_type"], data["category"], data["description"])
    )
    oid = c.lastrowid
    conn.commit()
    conn.close()
    return oid

def register_user(user):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT OR IGNORE INTO bot_users (user_id, username, first_name) VALUES (?,?,?)",
        (user.id, user.username or "", user.first_name or "")
    )
    conn.commit()
    conn.close()

def get_user_orders(user_id: int) -> list:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute(
        "SELECT * FROM orders WHERE note LIKE ? ORDER BY created_at DESC LIMIT 5",
        (f"%tg:{user_id}%",)
    )
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows

def get_stats() -> dict:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM orders")
    total = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM orders WHERE status='Yangi'")
    new = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM orders WHERE status='Jarayonda'")
    inprog = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM orders WHERE status='Bajarildi'")
    done = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM bot_users")
    users = c.fetchone()[0]
    conn.close()
    return {"total": total, "new": new, "inprog": inprog, "done": done, "users": users}

# ── Keyboards ─────────────────────────────────────────────────────────────────
def service_keyboard():
    rows = []
    items = list(SERVICES.items())
    for i in range(0, len(items), 2):
        row = []
        for svc_id, (icon, name) in items[i:i+2]:
            row.append(InlineKeyboardButton(f"{icon} {name}", callback_data=f"svc_{svc_id}"))
        rows.append(row)
    rows.append([InlineKeyboardButton("❌ Bekor qilish", callback_data="cancel")])
    return InlineKeyboardMarkup(rows)

def confirm_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✅ Tasdiqlash", callback_data="confirm_yes"),
            InlineKeyboardButton("✏️ O'zgartirish", callback_data="confirm_edit"),
        ],
        [InlineKeyboardButton("❌ Bekor qilish", callback_data="cancel")],
    ])

def main_menu_keyboard():
    return ReplyKeyboardMarkup(
        [
            ["📋 Buyurtma berish", "📊 Mening buyurtmalarim"],
            ["ℹ️ Ma'lumot", "📞 Aloqa"],
        ],
        resize_keyboard=True,
        input_field_placeholder="Menyu...",
    )

# ── Helpers ───────────────────────────────────────────────────────────────────
def detect_service(text: str) -> str | None:
    t = text.lower()
    for svc, kws in KEYWORDS.items():
        if any(k in t for k in kws):
            return svc
    return None

def auto_suggest_service(text: str) -> InlineKeyboardMarkup | None:
    svc = detect_service(text)
    if not svc:
        return None
    icon, name = SERVICES[svc]
    return InlineKeyboardMarkup([[
        InlineKeyboardButton(f"✅ {icon} {name} — Shu xizmatmi?", callback_data=f"svc_{svc}"),
        InlineKeyboardButton("🔄 Boshqa", callback_data="show_services"),
    ]])

def order_summary(data: dict) -> str:
    icon, name = SERVICES.get(data.get("service_type", ""), ("🔨", "Noma'lum"))
    return (
        f"📋 *Buyurtma ma'lumotlari:*\n\n"
        f"👤 *Ism:* {data.get('name', '—')}\n"
        f"📞 *Telefon:* {data.get('phone', '—')}\n"
        f"📍 *Manzil:* {data.get('address', '—')}\n"
        f"{icon} *Xizmat:* {name}\n"
        f"📝 *Muammo:* {data.get('description', '—')}\n"
        f"🏷️ *Kategoriya:* {data.get('category', '—')}\n"
    )

# ── Handlers ──────────────────────────────────────────────────────────────────
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    register_user(update.effective_user)
    name = update.effective_user.first_name or "do'stim"
    await update.message.reply_text(
        f"👋 Assalomu alaykum, *{name}*!\n\n"
        "🔨 *UstaTop Botiga Xush Kelibsiz!*\n\n"
        "Bu bot orqali tez va oson usta chaqirishingiz mumkin.\n"
        "Santexnik, elektrik, duradgor va boshqa ustalar — barchasi bir joyda!\n\n"
        "Quyidagi menyudan foydalaning 👇",
        parse_mode="Markdown",
        reply_markup=main_menu_keyboard(),
    )
    return ConversationHandler.END

async def book_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Buyurtma berish jarayonini boshlash"""
    context.user_data.clear()
    msg = update.message or (update.callback_query and update.callback_query.message)
    if update.callback_query:
        await update.callback_query.answer()
    await msg.reply_text(
        "🔧 *Qaysi xizmat kerak?*\n\nQuyidagi xizmatlardan birini tanlang:",
        parse_mode="Markdown",
        reply_markup=service_keyboard(),
    )
    return SELECT_SERVICE

async def service_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    if q.data == "show_services":
        await q.edit_message_text(
            "🔧 *Xizmat turini tanlang:*",
            parse_mode="Markdown",
            reply_markup=service_keyboard(),
        )
        return SELECT_SERVICE

    svc_id = q.data.replace("svc_", "")
    if svc_id not in SERVICES:
        return SELECT_SERVICE

    icon, name = SERVICES[svc_id]
    context.user_data["service_type"] = svc_id
    await q.edit_message_text(
        f"{icon} *{name}* tanlandi!\n\n"
        "📝 Muammoni batafsil tasvirlab yozing:\n\n"
        "_Masalan: 'Hammomda kran buzildi, suv oqyapti, tezda kerak'_",
        parse_mode="Markdown",
    )
    return GET_DESCRIPTION

async def get_description(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    if len(text) < 5:
        await update.message.reply_text("❗ Muammoni batafsilroq yozing (kamida 5 ta belgi).")
        return GET_DESCRIPTION

    context.user_data["description"] = text

    # Auto-categorize
    svc_id = context.user_data.get("service_type", "")
    from usta_categorize import categorize_description
    try:
        cat = categorize_description(text, svc_id)
    except Exception:
        cat = f"{SERVICES.get(svc_id, ('','Umumiy'))[1]} — Umumiy muammo"
    context.user_data["category"] = cat

    await update.message.reply_text(
        f"✅ Qabul qilindi!\n🏷️ *Kategoriya:* {cat}\n\n"
        "👤 *Ismingizni* yozing:",
        parse_mode="Markdown",
        reply_markup=ReplyKeyboardRemove(),
    )
    return GET_NAME

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.message.text.strip()
    if len(name) < 2:
        await update.message.reply_text("❗ Iltimos, to'liq ismingizni kiriting.")
        return GET_NAME
    context.user_data["name"] = name
    await update.message.reply_text(
        f"👤 *{name}* — yaxshi ism!\n\n📞 *Telefon raqamingizni* yozing:\n_Masalan: +998 90 123 45 67_",
        parse_mode="Markdown",
    )
    return GET_PHONE

async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    phone = update.message.text.strip()
    digits = "".join(c for c in phone if c.isdigit())
    if len(digits) < 9:
        await update.message.reply_text("❗ To'g'ri telefon raqam kiriting. Masalan: +998901234567")
        return GET_PHONE
    context.user_data["phone"] = phone
    await update.message.reply_text(
        "📍 *Manzilingizni* yozing:\n_Masalan: Navoiy sh., Saidiy ko'chasi, 12-uy_",
        parse_mode="Markdown",
    )
    return GET_ADDRESS

async def get_address(update: Update, context: ContextTypes.DEFAULT_TYPE):
    address = update.message.text.strip()
    if len(address) < 5:
        await update.message.reply_text("❗ Manzilni to'liqroq kiriting.")
        return GET_ADDRESS
    context.user_data["address"] = address

    summary = order_summary(context.user_data)
    await update.message.reply_text(
        summary + "\nMa'lumotlar to'g'rimi?",
        parse_mode="Markdown",
        reply_markup=confirm_keyboard(),
    )
    return CONFIRM

async def confirm_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    if q.data == "confirm_yes":
        data = context.user_data.copy()
        data["note"] = f"tg:{update.effective_user.id}"
        order_id = save_order(data)

        icon, name = SERVICES.get(data["service_type"], ("🔨", "Noma'lum"))
        await q.edit_message_text(
            f"🎉 *Buyurtma qabul qilindi!*\n\n"
            f"📋 Buyurtma raqami: *#{order_id}*\n"
            f"{icon} Xizmat: *{name}*\n"
            f"🏷️ Kategoriya: *{data['category']}*\n\n"
            f"⏰ Tez orada usta siz bilan bog'lanadi.\n"
            f"Rahmat va omad! 🙏",
            parse_mode="Markdown",
        )

        # Notify admin
        if ADMIN_ID:
            try:
                await context.bot.send_message(
                    ADMIN_ID,
                    f"🔔 *Yangi buyurtma #{order_id}*\n\n" + order_summary(data),
                    parse_mode="Markdown",
                )
            except Exception:
                pass

        context.user_data.clear()
        await update.effective_message.reply_text(
            "Bosh sahifaga qaytish uchun /start ni bosing.",
            reply_markup=main_menu_keyboard(),
        )
        return ConversationHandler.END

    elif q.data == "confirm_edit":
        await q.edit_message_text(
            "🔧 *Qaysi xizmat kerak?*\nQaytadan tanlang:",
            parse_mode="Markdown",
            reply_markup=service_keyboard(),
        )
        return SELECT_SERVICE

    return CONFIRM

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text("❌ Buyurtma bekor qilindi.")
    else:
        await update.message.reply_text(
            "❌ Bekor qilindi.",
            reply_markup=main_menu_keyboard(),
        )
    return ConversationHandler.END

async def my_orders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    orders = get_user_orders(uid)
    if not orders:
        await update.message.reply_text(
            "📭 Hali buyurtmalaringiz yo'q.\n\n"
            "«📋 Buyurtma berish» tugmasini bosing!",
            reply_markup=main_menu_keyboard(),
        )
        return

    text = "📊 *Sizning so'nggi buyurtmalaringiz:*\n\n"
    status_icons = {
        "Yangi": "🆕", "Qabul qilindi": "👍",
        "Jarayonda": "⚙️", "Bajarildi": "✅", "Bekor qilindi": "❌"
    }
    for o in orders:
        icon, name = SERVICES.get(o["service_type"], ("🔨", "Noma'lum"))
        st = status_icons.get(o["status"], "📌")
        text += (
            f"#{o['id']} {icon} *{name}*\n"
            f"  {st} Status: {o['status']}\n"
            f"  📅 {o['created_at'][:16]}\n\n"
        )

    await update.message.reply_text(text, parse_mode="Markdown", reply_markup=main_menu_keyboard())

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "ℹ️ *UstaTop haqida*\n\n"
        "🔨 UstaTop — ishonchli ustalar xizmati platformasi.\n\n"
        "📌 *Xizmatlar:*\n"
        "🔧 Santexnik — kran, quvur, kanalizatsiya\n"
        "⚡ Elektrik — rozetka, simlar, yoritish\n"
        "🪚 Duradgor — eshik, deraza, mebel\n"
        "🎨 Rassomchi — bo'yash, suvash, oboi\n"
        "❄️ Konditsioner — o'rnatish, ta'mirlash\n"
        "🧱 Plitkakor — plitka, mozaika, granit\n\n"
        "⭐ 500+ bajarilgan buyurtma | 4.9 reyting\n"
        "🌐 Sayt: usatop.uz",
        parse_mode="Markdown",
        reply_markup=main_menu_keyboard(),
    )

async def contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📞 *Aloqa:*\n\n"
        "📱 Telefon: +998 90 000 00 00\n"
        "💬 Telegram: @usatop_support\n"
        "📧 Email: info@usatop.uz\n\n"
        "⏰ Ish vaqti: 08:00 — 22:00",
        parse_mode="Markdown",
        reply_markup=main_menu_keyboard(),
    )

async def admin_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if ADMIN_ID and update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ Ruxsat yo'q.")
        return
    stats = get_stats()
    await update.message.reply_text(
        "📊 *Admin statistika:*\n\n"
        f"📋 Jami buyurtmalar: *{stats['total']}*\n"
        f"🆕 Yangi: *{stats['new']}*\n"
        f"⚙️ Jarayonda: *{stats['inprog']}*\n"
        f"✅ Bajarildi: *{stats['done']}*\n"
        f"👥 Bot foydalanuvchilari: *{stats['users']}*",
        parse_mode="Markdown",
    )

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "📋 Buyurtma berish":
        return await book_start(update, context)
    elif text == "📊 Mening buyurtmalarim":
        await my_orders(update, context)
    elif text == "ℹ️ Ma'lumot":
        await info(update, context)
    elif text == "📞 Aloqa":
        await contact(update, context)
    else:
        # Auto-detect service from free text
        suggest = auto_suggest_service(text)
        if suggest:
            context.user_data["description"] = text
            svc = detect_service(text)
            if svc:
                context.user_data["service_type"] = svc
                icon, name = SERVICES[svc]
                await update.message.reply_text(
                    f"🤖 Muammongizni tushunadim!\n{icon} *{name}* xizmati kerak ko'rinadi.",
                    parse_mode="Markdown",
                    reply_markup=suggest,
                )
                return SELECT_SERVICE
        else:
            await update.message.reply_text(
                "Menyudan foydalaning yoki /book buyrug'ini yozing.",
                reply_markup=main_menu_keyboard(),
            )

# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    init_db()

    app = Application.builder().token(TOKEN).build()

    conv = ConversationHandler(
        entry_points=[
            CommandHandler("book", book_start),
            CallbackQueryHandler(service_selected, pattern="^svc_"),
            MessageHandler(filters.Regex("^📋 Buyurtma berish$"), book_start),
        ],
        states={
            SELECT_SERVICE: [
                CallbackQueryHandler(service_selected, pattern="^(svc_|show_services)"),
                CallbackQueryHandler(cancel, pattern="^cancel$"),
            ],
            GET_DESCRIPTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_description)],
            GET_NAME:        [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            GET_PHONE:       [MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)],
            GET_ADDRESS:     [MessageHandler(filters.TEXT & ~filters.COMMAND, get_address)],
            CONFIRM: [
                CallbackQueryHandler(confirm_order, pattern="^confirm_"),
                CallbackQueryHandler(cancel, pattern="^cancel$"),
                CallbackQueryHandler(service_selected, pattern="^svc_"),
            ],
        },
        fallbacks=[
            CommandHandler("cancel", cancel),
            CallbackQueryHandler(cancel, pattern="^cancel$"),
        ],
        allow_reentry=True,
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("admin", admin_stats))
    app.add_handler(conv)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    logger.info("🤖 UstaTop bot ishga tushdi!")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
