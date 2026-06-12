#!/usr/bin/env python3
"""Извлечение эталона вопросов из официальных PDF (19 тем).

Два макета:
  A (Ubuntu): темы 1-5,9,11,12,14-17,19 — без отметок правильных ответов
  B (Times):  темы 6,7,8,10,13,18 — правильный ответ отмечен ✓
Структура определяется по заголовку таблицы (Точки/Номер/Въпрос) и
геометрии: ряды-прямоугольники + чекбоксы-якоря ответов.
"""
import fitz, json, re, os, sys

TICKETS = os.path.join(os.path.dirname(__file__), "..", "tickets")

CHECK_CHARS = {"✓", "✔", ""}

def get_spans(page):
    """Строки страницы: спаны одной строки объединены (текст в порядке x)."""
    tp = page.get_textpage(flags=0)
    lines = []
    for b in page.get_text("dict", textpage=tp)["blocks"]:
        if b["type"] != 0:
            continue
        for l in b["lines"]:
            sp = [s for s in l["spans"] if s["text"].strip()]
            if not sp:
                continue
            sp.sort(key=lambda s: s["bbox"][0])
            txt = sp[0]["text"]
            for prev, cur in zip(sp, sp[1:]):
                gap = cur["bbox"][0] - prev["bbox"][2]
                txt += cur["text"] if gap < 1.0 and not txt.endswith(" ") \
                    and not cur["text"].startswith(" ") else " " + cur["text"].strip()
            lines.append({"x": sp[0]["bbox"][0], "y": l["bbox"][1],
                          "y1": l["bbox"][3], "text": txt.strip()})
    return lines

def parse_topic(pdf_path, topic_id):
    doc = fitz.open(pdf_path)
    # --- колонки из заголовка на стр.1
    px = nx = qx = None
    for s in get_spans(doc[0]):
        t = s["text"].strip()
        if t == "Точки": px = s["x"]
        elif t == "Номер": nx = s["x"]
        elif t.startswith("Въпрос"): qx = s["x"]
    if px is None or nx is None or qx is None:
        raise RuntimeError(f"{topic_id}: не найден заголовок таблицы")
    questions = []
    for pno, page in enumerate(doc):
        rows, cboxes, vstrips, acells, filled_boxes = [], [], [], [], []
        for d in page.get_cdrawings():
            if not d.get("rect"):
                continue
            r = fitz.Rect(d["rect"])
            if r.x0 < 46 and 470 < r.width < 580 and 25 < r.height < 700:
                rows.append(r)
            if 10 < r.width < 18 and 10 < r.height < 18 and \
               abs(r.width - r.height) < 3 and len(d.get("items", [])) >= 8:
                cboxes.append(r)
                f = d.get("fill")
                if f and sum(f[:3]) < 2.7:  # цветная заливка = отмечен правильный
                    filled_boxes.append(r)
            # вертикальная кромка чекбокса (квадрат иногда не отрисован)
            if r.width < 3.5 and 11 < r.height < 17:
                vstrips.append(r)
            # ячейка чекбокс-колонки: точные границы каждого ответа по y
            if abs(r.x0 - qx) < 9 and 14 <= r.width <= 32 and 14 < r.height < 90:
                acells.append(r)
        # восстановить чекбоксы из пар вертикальных кромок
        vstrips.sort(key=lambda r: (round(r.y0), r.x0))
        for i, a in enumerate(vstrips):
            for b in vstrips[i+1:]:
                if abs(b.y0 - a.y0) < 2.5 and 10 < b.x0 - a.x0 < 17:
                    cand = fitz.Rect(a.x0, a.y0 - 0.7, b.x1, a.y0 + 14)
                    if not any(abs(c.x0 - cand.x0) < 5 and abs(c.y0 - cand.y0) < 5 for c in cboxes):
                        cboxes.append(cand)
                    break
        rows.sort(key=lambda r: r.y0)
        uniq = []
        for r in rows:
            if not uniq or r.y0 - uniq[-1].y0 > 5:
                uniq.append(r)
        rows = uniq
        spans = get_spans(page)
        # split: правая граница чекбоксов колонки вопроса
        qcol_cbs_all = [c for c in cboxes if abs(c.x0 - qx) < 8]
        split = (max(c.x1 for c in qcol_cbs_all) + 1.5) if qcol_cbs_all else qx + 18
        for row in rows:
            in_row = lambda y: row.y0 - 1 <= y <= row.y1 + 1
            rs = [s for s in spans if in_row((s["y"] + s["y1"]) / 2)]
            if not rs:
                continue
            num = points = None
            qlines, alines, checks = [], [], []
            for s in rs:
                t = s["text"].strip()
                if t in CHECK_CHARS:
                    checks.append(s); continue
                x = s["x"]
                if nx - 10 <= x < qx - 8:
                    m = re.match(r"^(\d+)\s*/\s*(\d+)$", t)
                    if m: num = (int(m.group(1)), int(m.group(2)))
                elif px - 12 <= x < nx - 10:
                    if re.match(r"^\d+$", t): points = int(t)
                elif qx - 8 <= x < split:
                    qlines.append(s)
                elif split <= x <= split + 30:
                    alines.append(s)
                # x > split+30 — текст внутри иллюстраций (таймкоды видео и т.п.)
            if num is None:
                continue
            cbs0 = sorted([c for c in cboxes if in_row((c.y0 + c.y1) / 2)],
                          key=lambda c: (-c.width, c.y0, c.x0))
            cbs = []
            for c in cbs0:  # dedup перекрывающихся (квадрат + ячейка)
                if not any(min(c.y1, k.y1) - max(c.y0, k.y0) > 0.5 * min(c.height, k.height)
                           and min(c.x1, k.x1) - max(c.x0, k.x0) > 0.5 * min(c.width, k.width)
                           for k in cbs):
                    cbs.append(c)
            cbs.sort(key=lambda c: (c.y0, c.x0))
            text_cbs = [c for c in cbs if abs(c.x0 - qx) < 9]
            far_cbs = [c for c in cbs if abs(c.x0 - qx) >= 9]
            # картиночные чекбоксы: максимальная группа на одной горизонтали
            img_row_cbs = []
            for c in far_cbs:
                grp = [k for k in far_cbs if abs(k.y0 - c.y0) < 6]
                if len(grp) > len(img_row_cbs):
                    img_row_cbs = grp
            # ячейки ответов в этом ряду (dedup по y)
            cand = [c for c in acells if in_row((c.y0 + c.y1) / 2)]
            cand.sort(key=lambda c: (-c.width, c.y0))  # ячейки шире чекбоксов — приоритет
            cells = []
            for c in cand:
                if not any(min(c.y1, k.y1) - max(c.y0, k.y0) > 0.5 * min(c.height, k.height)
                           for k in cells):
                    cells.append(c)
            cells.sort(key=lambda c: c.y0)
            qtext = " ".join(s["text"] for s in sorted(qlines, key=lambda s: (round(s["y"]), s["x"])))
            qtext = re.sub(r"\s+", " ", qtext).strip()
            answers, correct_set = [], set()
            if cells and alines:
                def bin_of(yc):
                    for i, c in enumerate(cells):
                        if c.y0 - 2.5 <= yc <= c.y1 + 2.5:
                            return i
                    return min(range(len(cells)),
                               key=lambda i: min(abs(yc - cells[i].y0), abs(yc - cells[i].y1)))
                segs = [[] for _ in cells]
                for s in alines:
                    segs[bin_of((s["y"] + s["y1"]) / 2)].append(s)
                for seg in segs:
                    at = " ".join(s["text"] for s in sorted(seg, key=lambda s: (round(s["y"]), s["x"])))
                    answers.append(re.sub(r"\s+", " ", at).strip())
                for ch in checks:
                    correct_set.add(bin_of((ch["y"] + ch["y1"]) / 2))
                for fb in filled_boxes:  # залитый квадрат = правильный (макет A)
                    if in_row((fb.y0 + fb.y1) / 2) and abs(fb.x0 - qx) < 9:
                        correct_set.add(bin_of((fb.y0 + fb.y1) / 2))
            img_answers = not cells and len(img_row_cbs) >= 2
            # отметки у имидж-ответов: по близости к чекбоксу варианта
            if img_answers:
                img_cbs = sorted(img_row_cbs, key=lambda c: c.x0)
                for ch in checks:
                    for i, c in enumerate(img_cbs):
                        if abs((ch["x"]) - c.x0) < 12 and abs(ch["y"] - c.y0) < 12:
                            correct_set.add(i)
                for fb in filled_boxes:
                    for i, c in enumerate(img_cbs):
                        if abs(fb.x0 - c.x0) < 6 and abs(fb.y0 - c.y0) < 6:
                            correct_set.add(i)
            questions.append({
                "topic": topic_id, "num": f"{num[0]}/{num[1]}", "n1": num[0], "n2": num[1],
                "points": points, "question": qtext, "answers": answers,
                "n_checkboxes": len(img_row_cbs) if img_answers else len(cells), "img_answers": img_answers,
                "correct_idx": sorted(correct_set) if correct_set else None,
                "page": pno + 1, "rect": [row.x0, row.y0, row.x1, row.y1],
            })
    doc.close()
    return questions

if __name__ == "__main__":
    a, b = int(sys.argv[1]), int(sys.argv[2])
    for i in range(a, b + 1):
        qs = parse_topic(os.path.join(TICKETS, f"тема {i}.pdf"), f"t{i}")
        out = os.path.join(os.path.dirname(__file__), f"gt_t{i}.json")
        json.dump(qs, open(out, "w"), ensure_ascii=False, indent=1)
        nc = sum(1 for q in qs if q["correct_idx"] is not None)
        print(f"t{i}: {len(qs)} вопросов, с отметкой ✓: {nc}", flush=True)
