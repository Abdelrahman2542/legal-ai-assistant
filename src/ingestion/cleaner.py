import os
import re

def clean_text(input_path: str, output_path: str):
    if not os.path.exists(input_path):
        print(f"❌ الملف الخام غير موجود في هذا المسار: {input_path}")
        return
    
    # 1. قراءة الملف الأصلي من raw
    with open(input_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # 2. عمليات التنضيف الأساسية
    lines = text.split('\n')
    cleaned_lines = []
    
    for line in lines:
        # استبعاد سطور الترويسة، أرقام الصفحات الوهمية، أو الفواصل المتكررة
        if "الجريدة الرسمية" in line or "--- الصفحة رقم" in line or "======" in line:
            continue  # تخطي السطر ده وما تكتبوش في النص النظيف
        cleaned_lines.append(line)
    
    # تجميع النص بعد استبعاد الزيادات
    cleaned_text = "\n".join(cleaned_lines)
    
    # تنضيف المسافات الفاضية الزيادة والمتفرقة
    cleaned_text = re.sub(r'\n{3,}', '\n\n', cleaned_text)

    # 3. التأكد من وجود فولدر staging وحفظ الملف فيه
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(cleaned_text)
        
    print(f"✅ تم تنضيف النص بنجاح وتم حفظه في: {output_path}")

if __name__ == "__main__":
    # المسارات: بياخد من raw (الملف الخام) ويكتب في staging (النص المؤقت النظيف)
    raw_file = "data/raw/قانون العمل.txt"        
    staging_file = "data/Staging/cleaned_labor.txt"
    
    clean_text(raw_file, staging_file)