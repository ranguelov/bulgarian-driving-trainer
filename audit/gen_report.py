#!/usr/bin/env python3
"""HTML-отчёт аудита: скриншот из PDF + текущее состояние приложения + дифф."""
import fitz, json, os, re, html, difflib
from collections import defaultdict

HERE = os.path.dirname(__file__)
CROPS = os.path.join(HERE, "crops")
os.makedirs(CROPS, exist_ok=True)

TYPE_LABEL = {
    "question_text": "Текст вопроса не совпадает с PDF",
    "answer_text": "Текст ответа не совпадает с PDF",
    "answers_count": "Не совпадает число ответов",
    "correct_flag": "Не совпадает правильный ответ",
    "missing_in_app": "Вопрос отсутствует в приложении",
    "extra_in_app": "Лишний вопрос в приложении",
}

issues = json.load(open(os.path.join(HERE, "diff_report.json"), encoding="utf-8"))
gt = []
for i in range(1, 20):
    gt += json.load(open(os.path.join(HERE, f"gt_t{i}.json"), encoding="utf-8"))
gt_by_id = {f"{q['topic']}_{q['n1']}_{q['n2']}": q for q in gt}

src = open(os.path.join(HERE, "..", "questions.js"), encoding="utf-8").read()
app = json.loads(src[src.index("["):].rstrip().rstrip(";"))
app_by_id = {q["id"]: q for q in app}

by_q = defaultdict(list)
for it in issues:
    by_q[it["id"]].append(it)

def sort_key(qid):
    t, a, b = qid.split("_")
    return (int(t[1:]), int(a), int(b))
qids = sorted(by_q, key=sort_key)

# --- кропы
docs = {}
for qid in qids:
    g = gt_by_id.get(qid)
    if not g or os.path.exists(os.path.join(CROPS, f"{qid}.png")):
        continue
    tnum = g["topic"][1:]
    if tnum not in docs:
        docs[tnum] = fitz.open(os.path.join(HERE, "..", "tickets", f"тема {tnum}.pdf"))
    page = docs[tnum][g["page"] - 1]
    r = fitz.Rect(g["rect"])
    r = fitz.Rect(r.x0 - 2, r.y0 - 2, r.x1 + 2, r.y1 + 2)
    pix = page.get_pixmap(clip=r, dpi=140)
    pix.save(os.path.join(CROPS, f"{qid}.png"))

def wdiff(ref, cur, mark_cls):
    """Подсветка отличий cur относительно ref (по словам)."""
    a, b = (ref or "").split(), (cur or "").split()
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    out = []
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        seg = html.escape(" ".join(b[j1:j2]))
        if op in ("replace", "insert") and seg:
            out.append(f'<mark class="{mark_cls}">{seg}</mark>')
        elif seg:
            out.append(seg)
    return " ".join(out)

def render_q(qid):
    g, a = gt_by_id[qid], app_by_id.get(qid)
    its = by_q[qid]
    types = {i["type"] for i in its}
    tnum = g["topic"][1:]
    badges = " ".join(f'<span class="badge">{TYPE_LABEL[t]}</span>' for t in sorted(types))
    # PDF-эталон
    pdf_answers = ""
    if g["img_answers"]:
        pdf_answers = f'<li class="img">{g["n_checkboxes"]} вариантов-картинок</li>'
    else:
        for i, ans in enumerate(g["answers"]):
            chk = " ✓" if g.get("correct_idx") and i in g["correct_idx"] else ""
            pdf_answers += f'<li>{html.escape(ans)}<b>{chk}</b></li>'
    # приложение, дифф против эталона
    app_q = wdiff(g["question"], a["question"], "bad") if a else "—"
    app_answers = ""
    if a:
        for i, ans in enumerate(a.get("answers", [])):
            ref = "" if g["img_answers"] else (g["answers"][i] if i < len(g["answers"]) else "")
            t = wdiff(ref, ans["text"], "bad") if not g["img_answers"] else html.escape(ans["text"])
            cor = ' class="cor"' if ans.get("correct") else ""
            app_answers += f"<li{cor}>{t}</li>"
    return f"""
<section id="{qid}">
<h3>Тема {tnum} — вопрос {g['num']} <span class="qid">({qid}, PDF стр. {g['page']})</span></h3>
<div class="badges">{badges}</div>
<div class="cols">
 <figure><figcaption>Оригинал (PDF, тема {tnum}, стр. {g['page']})</figcaption>
  <img loading="lazy" src="crops/{qid}.png"></figure>
 <div>
  <div class="panel pdf"><h4>Эталон из PDF (текстовый слой)</h4>
   <p class="q">{html.escape(g['question'])}</p><ol>{pdf_answers}</ol></div>
  <div class="panel app"><h4>Сейчас в приложении <span class="hint">(красным — отличия от PDF; зелёная рамка — помечен правильным)</span></h4>
   <p class="q">{app_q}</p><ol>{app_answers}</ol></div>
 </div>
</div>
</section>"""

from collections import Counter
cnt = Counter(i["type"] for i in issues)
total_q = len(qids)
stat_rows = "".join(f"<tr><td>{TYPE_LABEL[k]}</td><td>{v}</td></tr>" for k, v in cnt.most_common())
toc = ""
cur_t = None
for qid in qids:
    t = int(qid.split("_")[0][1:])
    if t != cur_t:
        toc += f'</p><p><b>Тема {t}:</b> '
        cur_t = t
    g = gt_by_id[qid]
    toc += f'<a href="#{qid}">{g["num"]}</a> '

body = "".join(render_q(qid) for qid in qids)
html_doc = f"""<!doctype html><html lang="ru"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Аудит соответствия PDF — ПДД Тренажор</title>
<style>
body{{font:15px/1.45 -apple-system,Segoe UI,sans-serif;margin:24px auto;max-width:1200px;padding:0 16px;color:#1a1a1a}}
h1{{font-size:24px}} h3{{margin:0 0 4px}} .qid{{color:#888;font-weight:400;font-size:13px}}
section{{border-top:2px solid #ddd;padding:18px 0;margin-top:8px}}
.cols{{display:grid;grid-template-columns:1fr 1fr;gap:16px;align-items:start}}
figure{{margin:0}} figcaption{{font-size:12px;color:#666;margin-bottom:4px}}
img{{max-width:100%;border:1px solid #ccc;border-radius:6px;background:#fff}}
.panel{{border:1px solid #ddd;border-radius:8px;padding:10px 14px;margin-bottom:12px}}
.panel.pdf{{background:#f4faf4}} .panel.app{{background:#fbf6f4}}
.panel h4{{margin:0 0 6px;font-size:13px;text-transform:uppercase;letter-spacing:.4px;color:#555}}
.hint{{text-transform:none;font-weight:400;letter-spacing:0;color:#999}}
.q{{font-weight:600;margin:6px 0}}
ol{{margin:4px 0;padding-left:22px}} li{{margin:3px 0}}
li.cor{{outline:2px solid #2e7d32;outline-offset:2px;border-radius:4px}}
li.img{{list-style:none;color:#666;font-style:italic}}
mark.bad{{background:#ffd6d6;color:#a00;border-radius:3px;padding:0 2px}}
.badge{{display:inline-block;background:#fde8c8;border:1px solid #e8b96a;border-radius:12px;padding:2px 10px;font-size:12px;margin-right:6px}}
table{{border-collapse:collapse;margin:12px 0}} td{{border:1px solid #ccc;padding:6px 12px}}
.toc{{background:#f5f5f7;border-radius:8px;padding:10px 16px;font-size:14px}}
.toc a{{margin-right:2px}}
b{{color:#2e7d32}}
</style>
<h1>Аудит: соответствие вопросов оригинальным PDF</h1>
<p>Сверено посимвольно (после нормализации пробелов) <b>1514</b> вопросов в 19 темах.
Без расхождений: <b>{1514 - total_q}</b>. Вопросов с ошибками: <b style="color:#a00">{total_q}</b>, всего расхождений: {len(issues)}.
Отметки правильных ответов извлечены из PDF (залитый квадрат / галочка) для всех 1514 вопросов и сверены по содержанию.</p>
<table>{stat_rows}</table>
<div class="toc"><b>Оглавление (вопросы с ошибками)</b>{toc}</div>
{body}
</html>"""
open(os.path.join(HERE, "report.html"), "w", encoding="utf-8").write(html_doc)
print(f"вопросов с ошибками: {total_q}, кропов: {len(os.listdir(CROPS))}")
