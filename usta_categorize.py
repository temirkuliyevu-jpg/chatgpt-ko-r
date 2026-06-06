"""
Oddiy kategoriyalash moduli — usta_booking/app.py bilan mos
"""

KEYWORDS = {
    'santexnik': {
        'kran': "Kran ta'miri", 'quvur': "Quvur ta'miri",
        'unitaz': 'Sanitariya qurilmasi', 'suv': "Suv ta'minoti",
        'kanalizatsiya': 'Kanalizatsiya', 'dush': "Dush ta'miri",
        'vanna': 'Vanna xonasi', 'lavabo': "Lavabo ta'miri",
    },
    'elektrik': {
        'rozetka': "Rozetka ta'miri/o'rnatish", 'yoritish': 'Yoritish tizimi',
        'elektr': 'Elektr ishlari', 'sim': 'Kabel/Sim ishlari',
        'qisqa': 'Qisqa tutashuv', 'lampa': 'Lampa almashtirish',
    },
    'duradgor': {
        'eshik': "Eshik ta'miri", 'deraza': "Deraza ta'miri",
        'mebel': "Mebel ta'miri", 'pol': 'Pol ishlari',
        'shkaf': "Shkaf o'rnatish", 'parket': 'Parket ishlari',
    },
    'rassomchi': {
        "bo'yash": "Devor bo'yash", 'devor': "Devor ta'miri",
        'suvash': 'Suvash ishlari', 'kraska': "Bo'yash ishlari",
        'oboi': 'Oboi yopish', 'gips': 'Gips ishlari',
    },
    'konditsioner': {
        'konditsioner': 'Konditsioner xizmati', 'sovutish': 'Sovutish tizimi',
        'isitish': 'Isitish tizimi',
    },
    'plitkakor': {
        'plitka': 'Plitka yotqizish', 'mozaika': 'Mozaika ishlari',
        'granit': 'Granit ishlari', 'mramor': 'Mramor ishlari',
    },
}

SERVICES = {
    'santexnik': 'Santexnik', 'elektrik': 'Elektrik',
    'duradgor': 'Duradgor', 'rassomchi': 'Rassomchi',
    'konditsioner': 'Konditsioner', 'plitkakor': 'Plitkakor',
}

def categorize_description(description: str, service_id: str) -> str:
    desc = description.lower()
    kws = KEYWORDS.get(service_id, {})
    for kw, cat in kws.items():
        if kw in desc:
            return cat
    return f"{SERVICES.get(service_id, 'Usta')} — Umumiy muammo"
