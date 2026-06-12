#!/usr/bin/env python3
"""Применение PDF-эталона к questions.js (болгарский текст + правильные ответы)."""
import json, os, re, shutil, unicodedata

HERE = os.path.dirname(__file__)
QJS = os.path.join(HERE, "..", "questions.js")

def norm(s):
    s = unicodedata.normalize("NFC", s or "")
    return re.sub(r"\s+", " ", s.replace(" ", " ")).strip()

gt = []
for i in range(1, 20):
    gt += json.load(open(os.path.join(HERE, f"gt_t{i}.json"), encoding="utf-8"))
gt_by_id = {f"{q['topic']}_{q['n1']}_{q['n2']}": q for q in gt}

src = open(QJS, encoding="utf-8").read()
prefix = src[:src.index("[")]
app = json.loads(src[src.index("["):].rstrip().rstrip(";"))

changed_q = changed_a = changed_c = 0
ru_stale = []  # вопросы, где BG изменился — RU перевод устарел
for q in app:
    g = gt_by_id.get(q["id"])
    assert g, f"нет эталона для {q['id']}"
    qn, gn = norm(q["question"]), norm(g["question"])
    if qn != gn:
        q["question"] = gn
        changed_q += 1
        ru_stale.append(q["id"])
    if not g["img_answers"]:
        assert len(g["answers"]) == len(q["answers"]), q["id"]
        for i, ans in enumerate(q["answers"]):
            ga = norm(g["answers"][i])
            if norm(ans["text"]) != ga:
                ans["text"] = ga
                changed_a += 1
                if q["id"] not in ru_stale:
                    ru_stale.append(q["id"])
    # правильные ответы из PDF (есть для всех вопросов)
    if g.get("correct_idx"):
        n = len(q["answers"])
        new_correct = [i in g["correct_idx"] for i in range(n)]
        old_correct = [bool(a.get("correct")) for a in q["answers"]]
        if new_correct != old_correct:
            for i, a in enumerate(q["answers"]):
                a["correct"] = new_correct[i]
            changed_c += 1

shutil.copy(QJS, os.path.join(HERE, "questions.js.bak"))
out = prefix + json.dumps(app, ensure_ascii=False, separators=(",", ":")) + ";\n"
open(QJS, "w", encoding="utf-8").write(out)
json.dump(ru_stale, open(os.path.join(HERE, "ru_stale.json"), "w"))
print(f"вопросов с изменённым текстом вопроса: {changed_q}")
print(f"исправленных текстов ответов: {changed_a}")
print(f"вопросов с исправленными флагами correct: {changed_c}")
print(f"вопросов с устаревшим RU: {len(ru_stale)}")
