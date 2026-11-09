import os

output_file = "project_bundle.txt"
# أضف هنا الصيغ أو الفولدرات اللي حابب تستثنيها
exclude_dirs = {".venv", ".git", "__pycache__", "node_modules"}
exclude_extensions = {".png", ".jpg", ".jpeg", ".exe", ".zip", ".pdf"}

with open(output_file, "w", encoding="utf-8") as outfile:
    for root, dirs, files in os.walk("."):
        # استثناء الفولدرات الغير مرغوبة
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        for file in files:
            if any(file.endswith(ext) for ext in exclude_extensions):
                continue
            if file == output_file or file == "bundle.py":
                continue
            
            file_path = os.path.join(root, file)
            outfile.write(f"\n--- FILE: {file_path} ---\n")
            try:
                with open(file_path, "r", encoding="utf-8") as infile:
                    outfile.write(infile.read())
            except Exception as e:
                outfile.write(f"[Could not read file: {e}]\n")

print("Done! Bundle created successfully.")