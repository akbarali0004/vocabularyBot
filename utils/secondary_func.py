def kb_to_mb(size_kb):
    return round(float(size_kb / 1024**2), 1)

def convert_lang(lang):
    lang = lang.lower()
    languages = {
        'uz': "O'zbekcha",
        'en': "Inglizcha",
        'ru': "Ruscha",
        'ar': "Arabcha",
        'de': "Nemischa",
        'fr': "Fransuzcha",
        'es': "Ispancha",
        'it': "Italyancha",
        'tr': "Turkcha",
        'cn': "Xitoycha",
        'jp': "Yaponcha",
        'kr': "Koreyscha",
        'hi': "Hindcha",
        'tj': "Tojikcha",
        'kg': "Qirgʻizcha",
        'kz': "Qozoqcha"
    }

    return languages[lang]