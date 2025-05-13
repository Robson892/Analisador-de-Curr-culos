import re

def extract_email(text):
    match = re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)
    return match.group() if match else None

def extract_phone(text):
    match = re.search(r"\(?\d{2}\)?[\s-]?\d{4,5}-?\d{4}", text)
    return match.group() if match else None

def extract_linkedin(text):
    match = re.search(r"(https?://)?(www\.)?linkedin\.com/in/[a-zA-Z0-9_-]+", text)
    return match.group() if match else None

def extract_name(text):
    lines = text.strip().split("\n")
    return lines[0] if lines else "Não identificado"

def extract_skills(text):
    keywords = ['python', 'sql', 'excel', 'power bi', 'tableau', 'java', 'c++', 'git', 'html', 'css', 'javascript']
    text_lower = text.lower()
    return [kw for kw in keywords if kw in text_lower]

def extract_languages(text):
    idiomas = ['inglês', 'espanhol', 'francês', 'alemão', 'português', 'italiano']
    encontrados = []
    for idioma in idiomas:
        if re.search(idioma, text, re.IGNORECASE):
            encontrados.append(idioma.capitalize())
    return encontrados

def extract_experience_years(text):
    match = re.findall(r'(\d{1,2})\s+(anos|ano)\s+(de\s+)?experiência', text.lower())
    return max([int(m[0]) for m in match], default=0)
from transformers import pipeline

