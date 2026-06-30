from language.languages import TRANSLATIONS

def translate(key, lang="en"):
    return TRANSLATIONS.get(lang, {}).get(key, key)