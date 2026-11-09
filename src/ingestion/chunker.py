import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

LAW = {
    "law_id": "labor_2025",
    "law_name": "قانون العمل",
    "law_number": "14 لسنة 2025",
    "source": "الجريدة الرسمية - قانون العمل 2025",
}

DIGITS = str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789")

ORDINALS = {
    "الأولى": 1, "الاولى": 1, "الثانية": 2, "الثالثة": 3, "الرابعة": 4,
    "الخامسة": 5, "السادسة": 6, "السابعة": 7, "الثامنة": 8,
    "التاسعة": 9, "العاشرة": 10,
}
_ORD = "|".join(sorted(ORDINALS, key=len, reverse=True))
_SEP = r"[\s()\[\]]*"          # مسافات وأقواس بأي اتجاه

HEADER_RE = re.compile(
    rf"^{_SEP}(?:ال)?مادة{_SEP}(\d+|{_ORD}){_SEP}"
    rf"(مكرر(?:[\s()]*[أ-ي][\s()]*)?)?\s*[:\-–.]?\s*(.*)$"
)
# سطر بيبدأ بـ "المادة 45 من هذا القانون..." ده إحالة جوه نص، مش عنوان
REFERENCE_START = re.compile(r"^(من|في|أو|و|فيما|بشأن)\s")


def normalize(text: str) -> str:
    return unicodedata.normalize("NFKC", text).translate(DIGITS)


def parse_header(line: str):
    m = HEADER_RE.match(line)
    if not m:
        return None
    label, suffix, rest = m.group(1), (m.group(2) or "").strip(), m.group(3).strip()
    if REFERENCE_START.match(rest):
        return None
    number = ORDINALS.get(label) or int(label)
    return number, suffix, rest


def chunk_law(text: str, law: dict):
    articles, preamble = [], []
    current, section, last_number = None, 0, None

    for line in text.splitlines():
        h = parse_header(line)
        if h:
            number, suffix, rest = h
            if number == 1 and not suffix and last_number is not None:
                section += 1          # الترقيم بدأ من 1 تاني (إصدار ← القانون نفسه)
            last_number = number
            current = {**law, "section": section, "article_number": number,
                       "article_suffix": suffix, "header": line.strip(),
                       "lines": [rest] if rest else []}
            articles.append(current)
        elif current:
            current["lines"].append(line)
        else:
            preamble.append(line)

    for i, a in enumerate(articles):
        a["text"] = "\n".join(a.pop("lines")).strip()
        suf = "_" + a["article_suffix"].replace(" ", "") if a["article_suffix"] else ""
        a["chunk_id"] = f"{a['law_id']}_s{a['section']}_{a['article_number']}{suf}_{i}"
    return articles, preamble


def validate(articles):
    empty, breaks, prev = [], [], None
    for a in articles:
        if len(a["text"]) < 10:
            empty.append((a["section"], a["article_number"]))
        if not a["article_suffix"]:
            n = a["article_number"]
            if prev is not None and n not in (prev + 1, 1):
                breaks.append((prev, n))
            prev = n
    return {"count": len(articles), "empty_text": empty, "sequence_breaks": breaks}


if __name__ == "__main__":
    src = ROOT / "data/staging/cleaned_labor.txt"
    out = ROOT / "data/processed/labor_2025.json"
    if not src.exists():
        raise SystemExit(f"❌ ملف المصدر مش موجود: {src.resolve()}")

    raw = src.read_text(encoding="utf-8")
    articles, preamble = chunk_law(normalize(raw), LAW)
    report = validate(articles)

    if not articles:
        raise SystemExit("❌ مفيش ولا مادة اتلقطت. راجع شكل العناوين في الملف.")

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(articles, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"حجم الملف: {len(raw)} حرف | عدد المواد: {report['count']}")
    print(f"سطور قبل أول مادة: {len(preamble)}")
    print(f"نص فاضي/قصير: {report['empty_text']}")
    print(f"قفزات الترقيم: {report['sequence_breaks']}")