"""Derive structured fields from customer_service_surveys.csv for the dashboard.

Each paragraph of the free text is matched against the generator's templates,
which gives: topic, channel, wait minutes, sentiment, a derived 1-5 score,
the main complaint, every complaint mentioned, and the resolution status.
Output: survey_analysis.json as {rows, meta}, with this script's own code in meta.
Run: python3 data/analyze_surveys.py
"""
import csv
import json
import re
from pathlib import Path

import generate_surveys as g

HERE = Path(__file__).parent
SRC = HERE / "customer_service_surveys.csv"
OUT = HERE / "survey_analysis.json"
SENT = {"pos": "חיובית", "mix": "מעורבת", "neg": "שלילית"}

# Complaint named by each (part, sentiment, template index). Positive parts carry none.
COMPLAINT = {
    ("open", "mix", 0): "המתנה ארוכה", ("open", "mix", 1): "צורך לחזור על ההסבר",
    ("open", "mix", 2): "המתנה ארוכה", ("open", "neg", 0): "ניתוק שיחה",
    ("open", "neg", 1): "המתנה ארוכה ללא עדכון", ("open", "neg", 2): "פניות חוזרות",
    ("agent", "mix", 0): "חוסר ידע מקצועי", ("agent", "mix", 1): "תשובות כלליות",
    ("agent", "mix", 2): "העברה בין מחלקות", ("agent", "neg", 0): "יחס לא סבלני",
    ("agent", "neg", 1): "מידע סותר", ("agent", "neg", 2): "סירוב לטפל",
    ("resolve", "mix", 0): "טיפול ממושך", ("resolve", "mix", 1): "פתרון חלקי",
    ("resolve", "mix", 2): "לא חזרו בזמן שהובטח", ("resolve", "neg", 0): "לא חזרו אליי כלל",
    ("resolve", "neg", 1): "אין אישור על טיפול", ("resolve", "neg", 2): "פתרון לא מתאים",
}
RESOLUTION = {"pos": "נפתר במלואו", ("mix", 0): "נפתר באיחור", ("mix", 1): "נפתר חלקית",
              ("mix", 2): "נפתר באיחור", "neg": "לא נפתר"}


def to_regex(template: str) -> re.Pattern:
    out, i = "", 0
    for m in re.finditer(r"\{\w+\}|\[[^\]]*\]|<[^>]*>", template):
        out += re.escape(template[i:m.start()])
        tok = m.group()
        out += ".+?" if tok[0] == "{" else "(?:" + "|".join(map(re.escape, tok[1:-1].split("|"))) + ")"
        i = m.end()
    return re.compile("^" + out + re.escape(template[i:]) + "$")


PATTERNS = [(part, s, i, to_regex(t))
            for part, d in (("open", g.OPEN), ("agent", g.AGENT), ("resolve", g.RESOLVE), ("close", g.CLOSE))
            for s, ts in d.items() for i, t in enumerate(ts)]


def classify(paragraph: str):
    for part, s, i, rx in PATTERNS:
        if rx.match(paragraph):
            return part, s, i
    raise ValueError(f"unmatched paragraph: {paragraph[:60]}")


def main() -> None:
    rows = []
    with SRC.open(encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            text = r["experience"]
            parts = {p: (s, i) for p, s, i in map(classify, text.split("\n\n"))}
            s, ri = parts["resolve"]
            complaints = [COMPLAINT[(p, *parts[p])] for p in ("resolve", "agent", "open") if (p, *parts[p]) in COMPLAINT]
            score = {"pos": 5 if "close" in parts else 4, "mix": 3, "neg": 1 if "close" in parts else 2}[s]
            rows.append({
                "survey_id": r["survey_id"],
                "survey_date": r["survey_date"],
                "month": r["survey_date"][:7],
                "topic": next(t for t in g.TOPICS if t in text),
                "channel": next(c for c in g.CHANNELS if c in text).removeprefix("ב").replace("צ'אט באתר", "צ'אט").replace("מוקד הטלפוני", "מוקד טלפוני"),
                "wait_minutes": int(m.group(1)) if (m := re.search(r"(\d+) דקות", text)) else None,
                "sentiment": SENT[s],
                "score": score,
                "main_complaint": complaints[0] if complaints else "ללא תלונה",
                "all_complaints": "; ".join(complaints),
                "resolution": RESOLUTION.get((s, ri), RESOLUTION.get(s)),
            })
    meta = [{"label": "analyze_surveys.py", "value": Path(__file__).read_text(encoding="utf-8"),
             "type": "code", "lang": "python"},
            {"label": "Input", "value": "customer_service_surveys.csv (1000 שורות לדוגמה)"}]
    OUT.write_text(json.dumps({"rows": rows, "meta": meta}, ensure_ascii=False), encoding="utf-8")
    print(f"wrote {len(rows)} rows to {OUT}")


if __name__ == "__main__":
    main()
