import os
import json

# تحديد المسارات حسب هيكل مشروعك
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, "data")

STAGED_DIR = os.path.join(DATA_DIR, "staging", "labor law")
PROCESS_DIR = os.path.join(DATA_DIR, "processed", "labor law")

def chunk_labor_law():
    input_path = os.path.join(STAGED_DIR, "extracted_clean.txt")
    
    print(f"🔍 البحث عن ملف الـ staged في مسار: {input_path}")
    
    if not os.path.exists(input_path):
        print(f"❌ خطأ: ملف الـ staged غير موجود في هذا المسار: {input_path}")
        print("💡 من فضلك شغّل cleaner.py أولاً لاستخراج النص الخام.")
        return

    # التأكد من وجود مجلد processed/labor law
    os.makedirs(PROCESS_DIR, exist_ok=True)

    print("📖 جاري قراءة النص المستخرج وتقسيمه إلى مواد بالطريقة الذكية...")
    with open(input_path, "r", encoding="utf-8") as f:
        full_text = f.read()

    lines = full_text.split('\n')

    chunks = []
    current_article_title = "مقدمة"
    current_article_content = ""
    article_counter = 1

    for line in lines:
        stripped_line = line.strip()

        # شروط بداية المادة بدقة للتأكد من التقسيم السليم
        is_new_article = (
            stripped_line.startswith("مادة") or
            stripped_line.startswith("المادة") or
            stripped_line.startswith("ﻣﺎﺩﺓ") or
            stripped_line.startswith("ﺍﳌﺎﺩﺓ") or
            stripped_line.startswith("مادة)") or
            stripped_line.startswith("ﻣﺎﺩﺓ)")
        )

        if is_new_article:
            # لو فيه مادة قديمة متجمعة، نحفظها كـ Dict منظم
            if current_article_content.strip():
                chunk_data = {
                    "chunk_id": f"labor_art_{article_counter}",
                    "article_title": current_article_title,
                    "section": "issuance" if "إصدار" in current_article_content[:200] else "main_law",
                    "content": current_article_content.strip()
                }
                chunks.append(chunk_data)
                article_counter += 1

            # نبدأ مادة جديدة
            current_article_title = stripped_line
            current_article_content = ""
        else:
            # نجمع محتوى السطور جوه نفس المادة الحالية
            current_article_content += line + "\n"

    # إضافة آخر مادة في الملف
    if current_article_content.strip():
        chunk_data = {
            "chunk_id": f"labor_art_{article_counter}",
            "article_title": current_article_title,
            "section": "issuance" if "إصدار" in current_article_content[:200] else "main_law",
            "content": current_article_content.strip()
        }
        chunks.append(chunk_data)

    # حفظ النتائج في ملف JSON
    output_json_path = os.path.join(PROCESS_DIR, "chunks.json")
    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False, indent=4)

    print(f"✅ تم بنجاح تقسيم القانون إلى {len(chunks)} مادة/تشانك!")
    print(f"💾 تم حفظ التشانكات في: {output_json_path}")

if __name__ == "__main__":
    chunk_labor_law()