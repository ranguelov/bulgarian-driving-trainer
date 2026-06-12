#!/usr/bin/env python3
"""Аудит v2: автопроверки русского перевода. Результат: audit/ru_qa.json"""
import json, re, os, unicodedata

HERE = os.path.dirname(__file__)
src = open(os.path.join(HERE, "..", "questions.js"), encoding="utf-8").read()
app = json.loads(src[src.index("["):].rstrip().rstrip(";"))

# болгарские маркеры, не встречающиеся в русском
BG_TOKENS = re.compile(
    r"\b(трябва|съм|съответн\w*|защото|които|който|която|преминава\w*|движението|"
    r"скоростта|пътя|пътен|пътна|превозн\w*|водач\w*|задължен\w*|разрешен[оа]? е|"
    r"забранен[оа]? е|непосредствен[оа]|се движ\w+|при тази|върху|изпреварван\w*|"
    r"кръстовище\w*|платното|лентата|ситуаци\w*я та)\b", re.I)
# болгарские буквосочетания/графемы (ъ внутри слов кроме рус. твёрдого знака после согл. перед е/ё/ю/я)
BG_ER = re.compile(r"[а-я]ъ[а-я]", re.I)  # в русском ъ только перед е/ё/ю/я
BG_ER_OK = re.compile(r"[а-я]ъ[еёюя]", re.I)

def numbers(s):
    s = s.replace("cm³", "cm3").replace("кkm", "km")
    return sorted(re.findall(r"\d+(?:[.,]\d+)?", s))

issues = []
stats = {"total_q": 0, "total_a": 0, "empty": 0, "bg_residue": 0,
         "num_mismatch": 0, "untranslated": 0, "img_placeholder_bad": 0}

def check(qid, field, bg, ru):
    if not ru or not ru.strip():
        issues.append({"id": qid, "field": field, "type": "empty", "bg": bg, "ru": ru})
        stats["empty"] += 1
        return
    if re.match(r"^Изображение \d+$", bg.strip()):
        if ru.strip() != bg.strip():
            issues.append({"id": qid, "field": field, "type": "img_placeholder_bad", "bg": bg, "ru": ru})
            stats["img_placeholder_bad"] += 1
        return
    if numbers(bg) != numbers(ru):
        issues.append({"id": qid, "field": field, "type": "num_mismatch", "bg": bg, "ru": ru})
        stats["num_mismatch"] += 1
    hits = BG_TOKENS.findall(ru)
    er = [m.group(0) for m in BG_ER.finditer(ru) if not BG_ER_OK.match(m.group(0))]
    if hits or er:
        issues.append({"id": qid, "field": field, "type": "bg_residue",
                       "bg": bg, "ru": ru, "hits": hits + er})
        stats["bg_residue"] += 1
    # непереведено: RU == BG для содержательной строки (не числа/единицы)
    if ru.strip() == bg.strip() and re.search(r"[а-яА-Я]{4,}", bg) and len(bg) > 12:
        issues.append({"id": qid, "field": field, "type": "untranslated", "bg": bg, "ru": ru})
        stats["untranslated"] += 1

for q in app:
    stats["total_q"] += 1
    check(q["id"], "question", q["question"], q.get("question_ru", ""))
    for i, a in enumerate(q["answers"]):
        stats["total_a"] += 1
        check(q["id"], f"answer_{i+1}", a["text"], a.get("text_ru", ""))
    # структурная согласованность: число правильных в BG-флагах == себе же (тривиально),
    # но проверим что correct есть хотя бы один
    if not any(a.get("correct") for a in q["answers"]):
        issues.append({"id": q["id"], "field": "correct", "type": "no_correct", "bg": "", "ru": ""})

print(json.dumps(stats, ensure_ascii=False))
print("issues:", len(issues))
for it in issues[:30]:
    print(f"- {it['id']} {it['field']} [{it['type']}] RU: {str(it.get('ru'))[:80]} {it.get('hits','')}")
json.dump(issues, open(os.path.join(HERE, "ru_qa.json"), "w"), ensure_ascii=False, indent=1)
