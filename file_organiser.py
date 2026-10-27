from pathlib import Path
import shutil

downloads = Path.home() / "Downloads"

types = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".webp"],
    "Documents": [".pdf",".txt", ".pptx", ".xlsx"],
    "Words Documents ": [".docx"],
    "Videos": [".mp4", ".mkv", ".avi"],
    "Audio": [".mp3", ".wav"],
    "Archives": [".zip", ".rar", ".7z"],
    "Python": [".py", ".ipynb"],
    "Exe File ": [".exe"],
    "Programming": [".js", ".ts", ".html", ".css", ".json"],
}

for file in downloads.iterdir():
    if not file.is_file() or file.name == Path(__file__).name:
        continue

    folder = next(
        (name for name, exts in types.items()
         if file.suffix.lower() in exts),
        "Others"
    )

    destination = downloads / folder
    destination.mkdir(exist_ok=True)
    target = destination / file.name

    i = 1
    while target.exists():
        target = destination / f"{file.stem}_{i}{file.suffix}"
        i += 1

    shutil.move(str(file), str(target))
    print(f"Moved: {file.name} -> {folder}")

print("Downloads organized successfully!")
