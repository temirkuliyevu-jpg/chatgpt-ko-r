#!/usr/bin/env bash
# 🤖 UstaTop Telegram Bot — Gemini AI Setup Script
# Botni 1 clickda o'rnatish uchun

set -e

echo "╔═══════════════════════════════════════════════════════════════════╗"
echo "║                                                                   ║"
echo "║     🤖 UstaTop Telegram Bot — Gemini AI Integrated Version        ║"
echo "║                                                                   ║"
echo "╚═══════════════════════════════════════════════════════════════════╝"

echo ""
echo "📋 STEP 1: Python va pip tekshiruvi..."
python --version || { echo "❌ Python not found"; exit 1; }
pip --version || { echo "❌ pip not found"; exit 1; }

echo ""
echo "📦 STEP 2: Dependencies o'rnatish..."
pip install -r requirements.txt

echo ""
echo "⚙️ STEP 3: Environment sozlamalar..."

if [ ! -f ".env" ]; then
    echo "   .env fayl yaratilmoqda..."
    cp .env.example .env
    echo "   ✅ .env yaratildi"
    echo ""
    echo "   ⚠️  MUHIM: .env faylni o'zingizning raqamlaringiz bilan tahrir qiling:"
    echo "   • BOT_TOKEN=... (BotFather dan)"
    echo "   • GEMINI_API_KEY=... (Google AI Studio dan)"
    echo "   • ADMIN_ID=... (O'zingizning Telegram ID)"
    echo ""
    echo "   nano .env  # yoki o'zingiz yoqtagan editor"
else
    echo "   ✅ .env fayli mavjud"
fi

echo ""
echo "🧪 STEP 4: Bot testing..."

echo ""
echo "✅ SETUP TUGADI!"
echo ""
echo "Botni ishga tushirish uchun:"
echo "  python bot_ai.py"
echo ""
echo "Advanced features'ni test qilish uchun:"
echo "  python advanced_features.py"
echo ""
echo "API examples:"
echo "  python gemini_api_examples.py"
echo ""
