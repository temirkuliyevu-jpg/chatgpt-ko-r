#!/usr/bin/env python3
"""
UstaTop Bot — Gemini API Direct Examples
API'ni qanday qo'llashni ko'rsatadi
"""

import google.generativeai as genai
import os
from dotenv import load_dotenv

# Environment variables yuklash
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyBwdV5xOX7kGMKK9fKMUNkRJ7U2MbgFkG8")

# Gemini'ni sozlash
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-pro")

# ═══════════════════════════════════════════════════════════════════════════════
# EXAMPLE 1: Simple Text Generation
# ═══════════════════════════════════════════════════════════════════════════════

def example_1_simple_chat():
    """Sodda chat"""
    print("\n" + "="*70)
    print("EXAMPLE 1: Simple Chat")
    print("="*70)
    
    prompt = "Uzbekistonda santexnik xizmati qancha turadi?"
    print(f"Savol: {prompt}\n")
    
    response = model.generate_content(prompt)
    print(f"Javob: {response.text}")
    
    return response.text

# ═══════════════════════════════════════════════════════════════════════════════
# EXAMPLE 2: Service Detection (XizmatLarni Aniqlash)
# ═══════════════════════════════════════════════════════════════════════════════

def example_2_service_detection(user_text):
    """AI yordamida xizmat turini aniqlash"""
    print("\n" + "="*70)
    print("EXAMPLE 2: Service Detection")
    print("="*70)
    
    prompt = f"""
Foydalanuvchi: "{user_text}"

Quyidagi xizmatlardan qaysi biri:
1. santexnik - kran, quvur, kanalizatsiya
2. elektrik - rozetka, sim, yoritish
3. duradgor - eshik, deraza, mebel
4. rassomchi - bo'yash, suvash, oboi
5. konditsioner - sovutish, isitish
6. plitkakor - plitka, mozaika, granit

FAQAT xizmat nomini yozing (masalan: santexnik)
"""
    
    print(f"Matn: {user_text}\n")
    response = model.generate_content(prompt)
    service = response.text.strip().lower()
    print(f"Aniqlangan xizmat: {service}")
    
    return service

# ═══════════════════════════════════════════════════════════════════════════════
# EXAMPLE 3: Category Assignment (Kategoriyalash)
# ═══════════════════════════════════════════════════════════════════════════════

def example_3_categorization(description, service):
    """Muammoni kategoriyalash"""
    print("\n" + "="*70)
    print("EXAMPLE 3: Categorization")
    print("="*70)
    
    prompt = f"""
Xizmat: {service}
Muammo: {description}

Muammoning kategoriyasini qisqacha nomla.
FAQAT kategoriya nomini yozing.
"""
    
    print(f"Xizmat: {service}")
    print(f"Muammo: {description}\n")
    
    response = model.generate_content(prompt)
    category = response.text.strip()
    print(f"Kategoriya: {category}")
    
    return category

# ═══════════════════════════════════════════════════════════════════════════════
# EXAMPLE 4: Price Estimation (Narx Tahmini)
# ═══════════════════════════════════════════════════════════════════════════════

def example_4_price_estimation(description, service):
    """Narx tahmini"""
    print("\n" + "="*70)
    print("EXAMPLE 4: Price Estimation")
    print("="*70)
    
    prompt = f"""
Xizmat: {service}
Muammo: {description}

Ushbu muammo uchun Uzbekistonda taxminan qancha narx?
FAQAT raqam va so'm qo'shing.
Masalan: "150000 so'm" yoki "200000-300000 so'm"
"""
    
    print(f"Xizmat: {service}")
    print(f"Muammo: {description}\n")
    
    response = model.generate_content(prompt)
    price = response.text.strip()
    print(f"Tahmini narx: {price}")
    
    return price

# ═══════════════════════════════════════════════════════════════════════════════
# EXAMPLE 5: Duration Estimation (Vaqt Tahmini)
# ═══════════════════════════════════════════════════════════════════════════════

def example_5_duration_estimation(description, service):
    """Vaqt tahmini"""
    print("\n" + "="*70)
    print("EXAMPLE 5: Duration Estimation")
    print("="*70)
    
    prompt = f"""
Xizmat: {service}
Muammo: {description}

Bu ish taxminan qancha vaqtda bajariladi?
Masalan: "30 daqiqa", "1-2 soat", "1 kun"

FAQAT vaqt yozing.
"""
    
    print(f"Xizmat: {service}")
    print(f"Muammo: {description}\n")
    
    response = model.generate_content(prompt)
    duration = response.text.strip()
    print(f"Tahmini vaqt: {duration}")
    
    return duration

# ═══════════════════════════════════════════════════════════════════════════════
# EXAMPLE 6: Customer Support (Foydalanuvchi Yordam)
# ═══════════════════════════════════════════════════════════════════════════════

def example_6_customer_support(question):
    """FAQ javoblari"""
    print("\n" + "="*70)
    print("EXAMPLE 6: Customer Support")
    print("="*70)
    
    prompt = f"""
Savol: {question}

UstaTop platformasi haqida qisqa javob ber (100 ta belgigacha).
Agar savol platformasi bilan bog'liq bo'lmasa, "Shu haqida bilmayman" deb jawob ber.
"""
    
    print(f"Savol: {question}\n")
    response = model.generate_content(prompt)
    answer = response.text.strip()[:200]
    print(f"Javob: {answer}")
    
    return answer

# ═══════════════════════════════════════════════════════════════════════════════
# EXAMPLE 7: Risk Assessment (Xavf Baholash)
# ═══════════════════════════════════════════════════════════════════════════════

def example_7_risk_assessment(description, service):
    """Xavf baholash"""
    print("\n" + "="*70)
    print("EXAMPLE 7: Risk Assessment")
    print("="*70)
    
    prompt = f"""
Xizmat: {service}
Muammo: {description}

Bu muammoning xavf darajasini baholang.
Qisqacha sababini yozing.

Format:
RISK_LEVEL: [Yuqori/O'rta/Past]
REASON: [Sababi - 1-2 gap]
RECOMMENDATION: [Tavsiya]
"""
    
    print(f"Xizmat: {service}")
    print(f"Muammo: {description}\n")
    
    response = model.generate_content(prompt)
    print(f"Natija:\n{response.text}")
    
    return response.text

# ═══════════════════════════════════════════════════════════════════════════════
# EXAMPLE 8: Multi-turn Conversation (Davomiy Suhbat)
# ═══════════════════════════════════════════════════════════════════════════════

def example_8_multi_turn_chat():
    """Bir nechta savol-javob"""
    print("\n" + "="*70)
    print("EXAMPLE 8: Multi-turn Conversation")
    print("="*70)
    
    # Conversation history
    chat = model.start_chat(history=[])
    
    questions = [
        "Kran ta'miri qancha turadi?",
        "Uskuna kerak bo'ladimi?",
        "Garantiya bormi?"
    ]
    
    for q in questions:
        print(f"Savol: {q}")
        response = chat.send_message(q)
        print(f"Javob: {response.text}\n")

# ═══════════════════════════════════════════════════════════════════════════════
# EXAMPLE 9: Streaming Response (Streaming Javob)
# ═══════════════════════════════════════════════════════════════════════════════

def example_9_streaming():
    """Streaming javob (Real-time)"""
    print("\n" + "="*70)
    print("EXAMPLE 9: Streaming Response")
    print("="*70)
    
    prompt = "Usta professiyasining ishlari nima?"
    
    print(f"Savol: {prompt}\n")
    print("Javob (Real-time):\n")
    
    response = model.generate_content(prompt, stream=True)
    
    for chunk in response:
        print(chunk.text, end="", flush=True)
    print("\n")

# ═══════════════════════════════════════════════════════════════════════════════
# EXAMPLE 10: Error Handling (Xatoliklarni Boshqarish)
# ═══════════════════════════════════════════════════════════════════════════════

def example_10_error_handling():
    """Xatoliklarni qanday boshqarish"""
    print("\n" + "="*70)
    print("EXAMPLE 10: Error Handling")
    print("="*70)
    
    try:
        # Boş prompt
        response = model.generate_content("")
        print("Javob:", response.text)
    except ValueError as e:
        print(f"Input Error: {e}")
    except Exception as e:
        print(f"API Error: {e}")
    
    print("\nError handling - OK ✓")

# ═══════════════════════════════════════════════════════════════════════════════
# Main Function
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    print("\n" + "█"*70)
    print("█" + " "*68 + "█")
    print("█" + "  🤖 UstaTop Bot — Gemini API Examples  ".center(68) + "█")
    print("█" + " "*68 + "█")
    print("█"*70)
    
    # Example 1: Simple Chat
    example_1_simple_chat()
    
    # Example 2: Service Detection
    example_2_service_detection("Kran oqyapti")
    example_2_service_detection("Elektr rozetkasi buzildi")
    
    # Example 3: Categorization
    example_3_categorization(
        "Vanna xonasidagi kran oqyapti, suv tomadi",
        "santexnik"
    )
    
    # Example 4: Price Estimation
    example_4_price_estimation(
        "Kran ta'miri",
        "santexnik"
    )
    
    # Example 5: Duration Estimation
    example_5_duration_estimation(
        "Elektr rozetkasi o'rnatish",
        "elektrik"
    )
    
    # Example 6: Customer Support
    example_6_customer_support(
        "Buyurtma bekor qilish mumkinmi?"
    )
    
    # Example 7: Risk Assessment
    example_7_risk_assessment(
        "Elektr qisqa tutashuvi ehtimoli",
        "elektrik"
    )
    
    # Example 8: Multi-turn Conversation
    example_8_multi_turn_chat()
    
    # Example 9: Streaming
    example_9_streaming()
    
    # Example 10: Error Handling
    example_10_error_handling()
    
    # Final message
    print("\n" + "█"*70)
    print("█" + " "*68 + "█")
    print("█" + "  ✅ BARCHA EXAMPLES TUGADI  ".center(68) + "█")
    print("█" + " "*68 + "█")
    print("█"*70 + "\n")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Xatolik: {e}")
        print("\nMuammolarni hal qiling:")
        print("1. API Key tekshiring")
        print("2. Internet connection tekshiring")
        print("3. python-dotenv o'rnatilganmi tekshiring: pip install python-dotenv")
