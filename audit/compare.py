#!/usr/bin/env python3
"""Сверка questions.js с эталоном из PDF. Результат: audit/diff_report.json"""
import json, re, os, unicodedata

HERE = os.path.dirname(__file__)

def norm(s):
    if s is None: return ""
    s = unicodedata.normalize("NFC", s)
    s = s.replace(" ", " ").replace("’", "'").replace("‘", "'")
    s = re.sub(r"([а-яА-Я])- ([а-я])", r"\1-\2", s)
    s = s.replace("km /h", "km/h").replace("кkm/h", "km/h")
    s = re.sub(r"\s+", " ", s)
    # унификация дефисов/тире внутри слов не делаем — сравниваем как есть
    return s.strip()

# --- приложение
src = open(os.path.join(HERE, "..", "questions.js"), encoding="utf-8").read()
src = src[src.index("["):]
src = src.rstrip().rstrip(";")
app = json.loads(src)
app_by_id = {q["id"]: q for q in app}

# --- эталон
gt = []
for i in range(1, 20):
    gt += json.load(open(os.path.join(HERE, f"gt_t{i}.json"), encoding="utf-8"))
gt_by_id = {f"{q['topic']}_{q['n1']}_{q['n2']}": q for q in gt}

issues = []
def add(qid, typ, severity, field, pdf_val, app_val, note=""):
    issues.append({"id": qid, "type": typ, "severity": severity, "field": field,
                   "pdf": pdf_val, "app": app_val, "note": note})

# 1. полнота
missing_in_app = sorted(set(gt_by_id) - set(app_by_id))
extra_in_app = sorted(set(app_by_id) - set(gt_by_id))
for qid in missing_in_app:
    add(qid, "missing_in_app", "critical", "-", gt_by_id[qid]["question"], None)
for qid in extra_in_app:
    add(qid, "extra_in_app", "critical", "-", None, app_by_id[qid]["question"])

# 2. посимвольная сверка
stats = {"q_mismatch": 0, "ans_count": 0, "ans_mismatch": 0, "correct_mismatch": 0, "points": 0, "ok": 0}
for qid in sorted(set(gt_by_id) & set(app_by_id)):
    g, a = gt_by_id[qid], app_by_id[qid]
    bad = False
    if norm(g["question"]) != norm(a["question"]):
        add(qid, "question_text", "critical", "question", g["question"], a["question"])
        stats["q_mismatch"] += 1; bad = True
    if g.get("points") and g["points"] != a.get("points"):
        # информационно: баллы намеренно по схеме категории B (сайт ИААА), не по общим PDF
        stats["points"] += 1
    app_answers = a.get("answers", [])
    if g["img_answers"]:
        # ответы-картинки: сверяем только количество чекбоксов
        n_img = g["n_checkboxes"]
        if n_img and len(app_answers) != n_img:
            add(qid, "answers_count", "critical", "answers",
                f"{n_img} вариантов (картинки)", f"{len(app_answers)} вариантов")
            stats["ans_count"] += 1; bad = True
    else:
        if len(g["answers"]) != len(app_answers):
            add(qid, "answers_count", "critical", "answers",
                " | ".join(g["answers"]), " | ".join(x["text"] for x in app_answers))
            stats["ans_count"] += 1; bad = True
        else:
            for i, (ga, aa) in enumerate(zip(g["answers"], app_answers)):
                if norm(ga) != norm(aa["text"]):
                    add(qid, "answer_text", "critical", f"answer_{i+1}", ga, aa["text"])
                    stats["ans_mismatch"] += 1; bad = True
    # правильный ответ (✓ в макете B, залитый квадрат в макете A)
    if g.get("correct_idx") and g["img_answers"] and \
       g["n_checkboxes"] == len(app_answers):
        app_correct = [i for i, x in enumerate(app_answers) if x.get("correct")]
        if app_correct != g["correct_idx"]:
            add(qid, "correct_flag", "critical", "correct",
                "правильные №" + ", ".join(str(i+1) for i in g["correct_idx"]),
                "в приложении №" + ", ".join(str(i+1) for i in app_correct))
            stats["correct_mismatch"] += 1; bad = True
    if g.get("correct_idx") and not g["img_answers"] and app_answers:
        # сверка по СОДЕРЖАНИЮ правильного ответа (устойчиво к перестановкам)
        pdf_cor = {norm(g["answers"][i]) for i in g["correct_idx"] if i < len(g["answers"])}
        app_cor = {norm(x["text"]) for x in app_answers if x.get("correct")}
        if pdf_cor != app_cor:
            add(qid, "correct_flag", "critical", "correct",
                "правильно: " + " | ".join(sorted(pdf_cor)),
                "в приложении правильным помечено: " + " | ".join(sorted(app_cor)))
            stats["correct_mismatch"] += 1; bad = True
    if not bad:
        stats["ok"] += 1

print(f"эталон: {len(gt_by_id)}, приложение: {len(app_by_id)}")
print(f"нет в приложении: {len(missing_in_app)}, лишние: {len(extra_in_app)}")
print("статистика:", json.dumps(stats, ensure_ascii=False))
print("всего проблем:", len(issues))
json.dump(issues, open(os.path.join(HERE, "diff_report.json"), "w"),
          ensure_ascii=False, indent=1)
