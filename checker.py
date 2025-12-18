import re
import os
from datetime import datetime
import winreg  # Windows registry'den masaüstü yolunu almak için


def get_desktop_path():
    """Windows'ta gerçek masaüstü yolunu registry'den alır"""
    with winreg.OpenKey(
        winreg.HKEY_CURRENT_USER,
        r"Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders"
    ) as key:
        return winreg.QueryValueEx(key, "Desktop")[0]


# ==============================
# ŞİFRE KURALLARI
# ==============================

def check_length(password):
    return len(password) >= 12

def check_uppercase(password):
    return any(c.isupper() for c in password)

def check_lowercase(password):
    return any(c.islower() for c in password)

def check_digit(password):
    return any(c.isdigit() for c in password)

def check_special(password):
    return re.search(r"[!@#$%^&*(),.?\":{}|<>]", password) is not None

# ANALİZ

def analyze_password(password):
    checks = {
        "Uzunluk (12+)": check_length(password),
        "Büyük harf": check_uppercase(password),
        "Küçük harf": check_lowercase(password),
        "Rakam": check_digit(password),
        "Özel karakter": check_special(password)
    }

    score = sum(checks.values())

    if score <= 2:
        strength = "ZAYIF"
    elif score <= 4:
        strength = "ORTA"
    else:
        strength = "GÜÇLÜ"

    return strength, checks


def recommendations(checks):
    advice = []

    if not checks["Uzunluk (12+)"]:
        advice.append("Şifreyi en az 12 karakter yap")
    if not checks["Büyük harf"]:
        advice.append("En az 1 büyük harf ekle")
    if not checks["Küçük harf"]:
        advice.append("En az 1 küçük harf ekle")
    if not checks["Rakam"]:
        advice.append("En az 1 rakam ekle")
    if not checks["Özel karakter"]:
        advice.append("En az 1 özel karakter ekle")

    return advice


# RAPORU MASAÜSTÜNE KAYDET

def save_report(strength, checks):
    desktop = get_desktop_path()
    file_path = os.path.join(desktop, "password_analysis_log.txt")

    with open(file_path, "a", encoding="utf-8") as f:
        f.write("====================================\n")
        f.write("ŞİFRE ANALİZ RAPORU\n")
        f.write(f"Tarih: {datetime.now()}\n")
        f.write(f"Genel Güç Seviyesi: {strength}\n\n")

        for rule, result in checks.items():
            f.write(f"{rule}: {'EVET' if result else 'HAYIR'}\n")

        f.write("\n")


# ANA AKIŞ


if __name__ == "__main__":
    print("=== ŞİFRE GÜÇ ANALİZİ ===")
    print("Şifre kaydedilmez, sadece analiz raporu tutulur.\n")

    password = input("Şifreni gir: ")

    strength, checks = analyze_password(password)
    advice = recommendations(checks)

    print(f"\nŞifre Gücü: {strength}\n")

    for k, v in checks.items():
        print(f"- {k}: {'✔' if v else '✘'}")

    if advice:
        print("\nGüçlendirme Önerileri:")
        for a in advice:
            print(f"* {a}")
    else:
        print("\nŞifre güvenlik standartlarını karşılıyor.")

    save_report(strength, checks)

    print("\n✔ Analiz raporu GERÇEK masaüstüne kaydedildi.")

