"""
UstaTop Bot — Advanced Features
AI-powered analytics, suggestions, at risk management
"""

import sqlite3
from datetime import datetime, timedelta
from typing import List, Dict
import google.generativeai as genai

GEMINI_API_KEY = "AIzaSyBwdV5xOX7kGMKK9fKMUNkRJ7U2MbgFkG8"
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-pro")

# ═══════════════════════════════════════════════════════════════════════════════
# YANGI FEATURE 1: Smart Price Prediction
# ═══════════════════════════════════════════════════════════════════════════════

def predict_price(description: str, service_type: str) -> str:
    """
    AI yordamida narx tahmini
    """
    try:
        prompt = f"""
Xizmat: {service_type}
Muammo: {description}

Ushbu muammo uchun Uzbekistonda taxminan qancha narx bo'ladi?
FAQAT raqam yozing, masalan: "150000" yoki "200000-300000"
"""
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception:
        return "Narx tariflariga bog'langan"

# ═══════════════════════════════════════════════════════════════════════════════
# YANGI FEATURE 2: Risk Assessment
# ═══════════════════════════════════════════════════════════════════════════════

def assess_risk(description: str, service_type: str) -> Dict:
    """
    Muammoning xavflarini baholash
    """
    try:
        prompt = f"""
Xizmat: {service_type}
Muammo: {description}

Bu muammoning xavf darajasini baholang (Yuqori/Oʻrta/Past).
Qisqacha sababini yozing.

Format:
RISK_LEVEL: [Yuqori/Oʻrta/Past]
REASON: [Sababi]
RECOMMENDATION: [Tavsiya]
"""
        response = model.generate_content(prompt)
        text = response.text.strip()
        
        risk_level = "O'rta"
        reason = ""
        recommendation = ""
        
        if "RISK_LEVEL:" in text:
            risk_level = text.split("RISK_LEVEL:")[1].split("\n")[0].strip()
        if "REASON:" in text:
            reason = text.split("REASON:")[1].split("\n")[0].strip()
        if "RECOMMENDATION:" in text:
            recommendation = text.split("RECOMMENDATION:")[1].strip()
        
        return {
            "level": risk_level,
            "reason": reason,
            "recommendation": recommendation
        }
    except Exception:
        return {
            "level": "O'rta",
            "reason": "Xavf baholashda xatolik",
            "recommendation": "Tez usta chaqiring"
        }

# ═══════════════════════════════════════════════════════════════════════════════
# YANGI FEATURE 3: Estimated Completion Time
# ═══════════════════════════════════════════════════════════════════════════════

def estimate_duration(description: str, service_type: str) -> str:
    """
    Isni bajarish vaqtini tahmini
    """
    try:
        prompt = f"""
Xizmat: {service_type}
Muammo: {description}

Bu ish taxminan qancha vaqtda bajariladi?
Masalan: "30 daqiqa", "1-2 soat", "1 kun"

FAQAT vaqt yozing.
"""
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception:
        return "1-2 soat"

# ═══════════════════════════════════════════════════════════════════════════════
# YANGI FEATURE 4: Customer Support Bot
# ═══════════════════════════════════════════════════════════════════════════════

def faq_response(question: str) -> str:
    """
    FAQ savollarga javob berish
    """
    try:
        prompt = f"""
Savol: {question}

UstaTop platformasi haqida javob ber. 
Qisqa va tushunarli javob ber (100 ta belgigacha).

Agar savol platformasi bilan bog'liq bo'lmasa, "Shu haqida bilmayman" deb jawob ber.
"""
        response = model.generate_content(prompt)
        return response.text.strip()[:200]
    except Exception:
        return "Savol uchun rahmat, admin siz bilan bog'lanadi."

# ═══════════════════════════════════════════════════════════════════════════════
# YANGI FEATURE 5: Analytics Dashboard
# ═══════════════════════════════════════════════════════════════════════════════

def get_service_statistics(db_path: str) -> Dict:
    """
    Xizmatlar bo'yicha statistika
    """
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    stats = {}
    services = ["santexnik", "elektrik", "duradgor", "rassomchi", "konditsioner", "plitkakor"]
    
    for svc in services:
        c.execute("SELECT COUNT(*) FROM orders WHERE service_type=?", (svc,))
        count = c.fetchone()[0]
        
        c.execute(
            "SELECT AVG(CAST(SUBSTR(price, 1, INSTR(price, '-') - 1) AS INTEGER)) "
            "FROM orders WHERE service_type=? AND price!=''",
            (svc,)
        )
        avg_price = c.fetchone()[0] or 0
        
        stats[svc] = {
            "count": count,
            "avg_price": int(avg_price) if avg_price else 0
        }
    
    conn.close()
    return stats

def get_trending_issues(db_path: str, days: int = 7) -> List[str]:
    """
    Oxirgi kunlardagi ko'p uchraydigan muammolar
    """
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    since = datetime.now() - timedelta(days=days)
    
    c.execute(
        "SELECT category, COUNT(*) as count FROM orders "
        "WHERE created_at > ? GROUP BY category ORDER BY count DESC LIMIT 5",
        (since.isoformat(),)
    )
    
    issues = [row[0] for row in c.fetchall()]
    conn.close()
    return issues

# ═══════════════════════════════════════════════════════════════════════════════
# YANGI FEATURE 6: Usta Matching (Advanced)
# ═══════════════════════════════════════════════════════════════════════════════

def find_best_master(description: str, service_type: str, db_path: str) -> Dict:
    """
    Bugungi muammo uchun eng yaxshi ustani topish (simulyatsiya)
    """
    try:
        # AI yordamida usta talablarini aniqlash
        prompt = f"""
Xizmat: {service_type}
Muammo: {description}

Ushbu muammoni bajarish uchun zarur bo'lgan usta sifatlari:
1. Tajribasi (yil)
2. Mutaxassisliklar
3. Boshqa talablar

Qisqacha yozing.
"""
        response = model.generate_content(prompt)
        
        return {
            "requirements": response.text.strip(),
            "estimated_price": predict_price(description, service_type),
            "duration": estimate_duration(description, service_type),
            "risk": assess_risk(description, service_type)["level"]
        }
    except Exception:
        return {
            "requirements": "Standart usta",
            "estimated_price": "Narif tariflariga bog'langan",
            "duration": "1-2 soat",
            "risk": "O'rta"
        }

# ═══════════════════════════════════════════════════════════════════════════════
# YANGI FEATURE 7: Order Tracking
# ═══════════════════════════════════════════════════════════════════════════════

def generate_order_summary(order_id: int, db_path: str) -> str:
    """
    Buyurtma to'g'risida batafsil ma'lumot
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    c.execute("SELECT * FROM orders WHERE id=?", (order_id,))
    order = dict(c.fetchone() or {})
    conn.close()
    
    if not order:
        return "Buyurtma topilmadi"
    
    summary = f"""
📋 Buyurtma #{order_id}
🕐 {order.get('created_at', 'Unknown')}

👤 {order.get('name')}
📞 {order.get('phone')}
📍 {order.get('address')}

🔧 {order.get('service_type')} — {order.get('category')}
📝 {order.get('description')}

💰 Narx: {order.get('price') or 'Aniqlanmadi'}
{order.get('note')}
"""
    return summary

# ═══════════════════════════════════════════════════════════════════════════════
# Test Functions
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("🤖 Advanced Features Test\n")
    
    # Price Prediction Test
    print("💰 Price Prediction:")
    price = predict_price("Kran oqyapti, suv tomadi", "santexnik")
    print(f"Narx: {price}\n")
    
    # Risk Assessment Test
    print("⚠️ Risk Assessment:")
    risk = assess_risk("Elektr qisqa tutashuviga shubha", "elektrik")
    print(f"Xavf: {risk}\n")
    
    # Duration Estimate Test
    print("⏱️ Duration Estimate:")
    duration = estimate_duration("Eshik o'rnatish kerak", "duradgor")
    print(f"Vaqt: {duration}\n")
    
    # FAQ Test
    print("❓ FAQ Response:")
    faq = faq_response("Buyurtmalarni qanday bekor qilishim mumkin?")
    print(f"Javob: {faq}\n")
