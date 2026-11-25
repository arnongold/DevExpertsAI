#!/usr/bin/env python3
"""יצירת קובץ דוגמא של פניות לקוחות.

הקובץ כולל שלוש עמודות: שם הלקוח, אופן הפנייה ותוכן הפנייה.
כל השמות והתכנים בדויים ונוצרים אקראית.

שימוש:
    python scripts/generate_sample_contacts.py
    python scripts/generate_sample_contacts.py --rows 10000 --output sample_contacts.csv --seed 42
"""

import argparse
import csv
import random

FIRST_NAMES = [
    "דניאל", "נועה", "יוסי", "מיכל", "אבי", "שירה", "רון", "תמר", "איתי", "יעל",
    "עומר", "מאיה", "גיל", "רותם", "אורי", "הילה", "עידו", "ליאת", "אלון", "שני",
    "משה", "רחל", "דוד", "שרה", "יונתן", "אסתר", "נדב", "ענבל", "אריאל", "קרן",
    "אחמד", "פאטמה", "מוחמד", "לילה", "סמיר", "רנא", "יוליה", "דמיטרי", "אנה", "איגור",
]

LAST_NAMES = [
    "כהן", "לוי", "מזרחי", "פרץ", "ביטון", "דהן", "אברהם", "פרידמן", "אזולאי", "מלכה",
    "שפירא", "גולדברג", "רוזן", "אוחיון", "חדד", "גבאי", "קפלן", "ברק", "נחום", "שלום",
    "סעדה", "חורי", "עבאס", "נסאר", "איבנוב", "פטרוב", "וייס", "קליין", "בן דוד", "אדלר",
]

# שמות חברות (לקוחות עסקיים) – בדויים
COMPANY_PREFIXES = ["טכנו", "דיגי", "אופק", "נתיב", "גלובל", "סמארט", "פרו", "אלפא", "מגה", "נובה"]
COMPANY_SUFFIXES = ["מערכות", "פתרונות", "תעשיות", "שיווק", "לוגיסטיקה", "סחר", "ייעוץ", "תוכנה"]
COMPANY_FORMS = ['בע"מ', "ושות'", "גרופ", ""]

CONTACT_METHODS = {
    "טלפון": 30,
    "דוא\"ל": 25,
    "וואטסאפ": 15,
    "צ'אט באתר": 12,
    "טופס יצירת קשר": 8,
    "פגישה פרונטלית": 5,
    "רשתות חברתיות": 5,
}

PRODUCTS = ["מערכת ה-CRM", "מודול הדיוור", "אפליקציית המובייל", "לוח הבקרה", "ממשק ה-API",
            "מודול החשבוניות", "מערכת ניהול הלידים", "מודול הדוחות"]

TEMPLATES = [
    "מבקש לקבל הצעת מחיר עבור {product} ל-{users} משתמשים.",
    "מתעניין בהדגמה של {product}. זמין ביום {day} בשעה {hour}.",
    "דיווח על תקלה ב{product}: המערכת לא נטענת מאז {day}.",
    "שאלה לגבי חיוב כפול בחשבונית מספר {invoice}.",
    "מבקש לשדרג את החבילה ל-{users} משתמשים ולהוסיף את {product}.",
    "מעוניין לבטל את המנוי בסוף החודש. מבקש שיחזרו אליו.",
    "שאלה האם {product} תומך באינטגרציה עם {integration}.",
    "מבקש הדרכה לצוות של {users} עובדים על {product}.",
    "תלונה על זמן תגובה ארוך של התמיכה. ממתין כבר {days} ימים.",
    "מבקש לעדכן את פרטי החשבון ואת כתובת החיוב.",
    "מחמאה לנציג השירות על טיפול מהיר ומקצועי.",
    "מבקש לייצא את כל נתוני הלקוחות מ{product} לקובץ Excel.",
    "שאלה לגבי אבטחת מידע ועמידה בתקנות הגנת הפרטיות.",
    "מבקש להאריך את תקופת הניסיון של {product} ב-{days} ימים.",
    "לא מצליח להתחבר לחשבון. איפוס הסיסמה לא עובד.",
    "מבקש פגישה עם מנהל הלקוח לגבי חידוש החוזה.",
]

DAYS = ["ראשון", "שני", "שלישי", "רביעי", "חמישי"]
INTEGRATIONS = ["Outlook", "Gmail", "SAP", "Priority", "Salesforce", "Slack", "Zapier", "WhatsApp Business"]


def random_customer_name(rng: random.Random) -> str:
    """70% לקוחות פרטיים, 30% לקוחות עסקיים."""
    if rng.random() < 0.7:
        return f"{rng.choice(FIRST_NAMES)} {rng.choice(LAST_NAMES)}"
    name = f"{rng.choice(COMPANY_PREFIXES)} {rng.choice(COMPANY_SUFFIXES)}"
    form = rng.choice(COMPANY_FORMS)
    return f"{name} {form}".strip()


def random_contact_method(rng: random.Random) -> str:
    methods = list(CONTACT_METHODS)
    weights = list(CONTACT_METHODS.values())
    return rng.choices(methods, weights=weights, k=1)[0]


def random_content(rng: random.Random) -> str:
    return rng.choice(TEMPLATES).format(
        product=rng.choice(PRODUCTS),
        users=rng.choice([5, 10, 25, 50, 100, 250]),
        day=rng.choice(DAYS),
        hour=f"{rng.randint(9, 17)}:{rng.choice(['00', '30'])}",
        invoice=rng.randint(100000, 999999),
        integration=rng.choice(INTEGRATIONS),
        days=rng.randint(2, 14),
    )


def generate(rows: int, output: str, seed: int | None) -> None:
    rng = random.Random(seed)
    # utf-8-sig כדי ש-Excel יציג עברית כראוי
    with open(output, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["שם הלקוח", "אופן הפנייה", "תוכן הפנייה"])
        for _ in range(rows):
            writer.writerow([random_customer_name(rng), random_contact_method(rng), random_content(rng)])


def main() -> None:
    parser = argparse.ArgumentParser(description="יצירת קובץ CSV לדוגמא של פניות לקוחות")
    parser.add_argument("--rows", type=int, default=10_000, help="מספר שורות (ברירת מחדל: 10,000)")
    parser.add_argument("--output", default="sample_contacts.csv", help="נתיב קובץ הפלט")
    parser.add_argument("--seed", type=int, default=None, help="זרע אקראיות לתוצאה קבועה")
    args = parser.parse_args()

    generate(args.rows, args.output, args.seed)
    print(f"נוצר הקובץ {args.output} עם {args.rows:,} שורות.")


if __name__ == "__main__":
    main()
