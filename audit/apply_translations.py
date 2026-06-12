#!/usr/bin/env python3
"""Применение нового RU-перевода: bg_lines.txt[i] -> ru_*.txt[i]."""
import json, os, re, glob, shutil, sys

HERE = os.path.dirname(__file__)
QJS = os.path.join(HERE, "..", "questions.js")

bg = open(os.path.join(HERE, "bg_lines.txt"), encoding="utf-8").read().split("\n")
ru = []
for f in sorted(glob.glob(os.path.join(HERE, "ru", "ru_*.txt"))):
    ru += open(f, encoding="utf-8").read().rstrip("\n").split("\n")
print(f"bg: {len(bg)}, ru: {len(ru)}")
assert len(bg) == len(ru), "число строк не совпадает!"

# --- валидация
bad = 0
for i, (b, r) in enumerate(zip(bg, ru)):
    if not r.strip():
        print(f"ПУСТО @{i+1}: {b[:60]}"); bad += 1
    # числа должны сохраниться (кроме известной опечатки кkm и 'до 2 часа'-подобных)
    nb = re.findall(r"\d+[.,]?\d*", b)
    nr = re.findall(r"\d+[.,]?\d*", r)
    if sorted(nb) != sorted(nr) and "кkm" not in b:
        print(f"ЧИСЛА @{i+1}: {b[:70]} || {r[:70]}"); bad += 1
    # болгарские маркеры в RU
    for w in [" трябва ", " съм ", "ъத", " защото ", " които ", " след ", " при това"]:
        if w in " " + r + " ":
            print(f"BG-СЛЕД @{i+1}: {r[:80]}"); bad += 1; break
print("проблемных строк:", bad)
if "--check" in sys.argv:
    sys.exit(0)

tr = dict(zip(bg, ru))
src = open(QJS, encoding="utf-8").read()
prefix = src[:src.index("[")]
app = json.loads(src[src.index("["):].rstrip().rstrip(";"))

miss = set(); n_q = n_a = 0
for q in app:
    s = q["question"].strip()
    if s in tr:
        q["question_ru"] = tr[s]; n_q += 1
    elif not re.match(r"^Изображение \d+$", s):
        miss.add(s)
    for a in q["answers"]:
        t = a["text"].strip()
        if re.match(r"^Изображение \d+$", t):
            a["text_ru"] = t
            continue
        if t in tr:
            a["text_ru"] = tr[t]; n_a += 1
        else:
            miss.add(t)

print(f"переведено вопросов: {n_q}, ответов: {n_a}, не найдено: {len(miss)}")
for m in list(miss)[:10]: print("MISS:", m[:80])
if miss:
    sys.exit(1)
shutil.copy(QJS, os.path.join(HERE, "questions.js.bak2"))
open(QJS, "w", encoding="utf-8").write(
    prefix + json.dumps(app, ensure_ascii=False, separators=(",", ":")) + ";\n")
print("questions.js обновлён")
