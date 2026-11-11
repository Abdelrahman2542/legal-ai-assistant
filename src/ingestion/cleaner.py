import os
import json
import fitz  # PyMuPDF

# تحديد مسار جذر المشروع بثبات (الوصول لمجلد legal-ai-assistant مباشرة)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DATA_DIR = os.path.join(BASE_DIR, "data")

RAW_DIR = os.path.join(DATA_DIR, "raw", "labor law")
STAGED_DIR = os.path.join(DATA_DIR, "staging")
CORRECTIONS_FILE = os.path.join(DATA_DIR, "corrections.json")

def load_corrections():
    """تحميل قاموس التصحيحات الإملائية لو ملف corrections.json موجود"""
    if os.path.exists(CORRECTIONS_FILE):
        try:
            with open(CORRECTIONS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"تحذير: لم يتم قراءة ملف corrections.json بشكل صحيح: {e}")
    return {}

def clean_text(text: str, corrections: dict) -> str:
    """عمليات التنظيف الأساسية وتطبيق التصحيحات"""
    for wrong, right in corrections.items():
        text = text.replace(wrong, right)
    return text

def extract_and_stage_pdf(pdf_filename="قانون العمل.pdf"):
    pdf_path = os.path.join(RAW_DIR, pdf_filename)
    
    if not os.path.exists(pdf_path):
        print(f"خطأ: ملف الـ PDF غير موجود في المسار: {pdf_path}")
        print(f"تأكد أن الملف موجود في: {pdf_path}")
        return
    
    # التأكد من وجود مجلد staged
    os.makedirs(STAGED_DIR, exist_ok=True)
    
    print(f"جاري فتح واستخراج النص من: {pdf_path} ...")
    doc = fitz.open(pdf_path)
    full_text = ""
    
    for page_num, page in enumerate(doc):
        page_text = page.get_text("text")
        full_text += f"\n--- الصفحة رقم {page_num + 1} ---\n" + page_text

    # تحميل التصحيحات وتطبيقها
    corrections = load_corrections()
    cleaned_full_text = clean_text(full_text, corrections)
    
    # حفظ الناتج في مجلد staged
    output_filename = "extracted_clean.txt"
    output_path = os.path.join(STAGED_DIR,"labor law", output_filename)
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(cleaned_full_text)
        
    print(f"تم بنجاح! إجمالي الحروف المستخرجة: {len(cleaned_full_text)}")
    print(f"تم حفظ النص المنظف في: {output_path}")

if __name__ == "__main__":
    extract_and_stage_pdf()