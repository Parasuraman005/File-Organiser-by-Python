from pathlib import Path
import shutil

DOWNLOADS = Path.home() / "Downloads"

FILE_TYPES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".pptx", ".xlsx", ".csv"],
    "Videos": [".mp4", ".mkv", ".avi", ".mov", ".webm"],
    "Audio": [".mp3", ".wav", ".aac", ".flac", ".m4a"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Python": [".py", ".ipynb", ".pyw"],
    "Programming": [".js", ".ts", ".jsx", ".tsx", ".html", ".css", ".json"],
    "Executables": [".exe", ".msi"],
}

CATEGORIES = set(FILE_TYPES) | {"Others"}


def category(file):
    for name, extensions in FILE_TYPES.items():
        if file.suffix.lower() in extensions:
            return name
    return "Others"


def unique_path(path):
    count = 1
    while path.exists():
        path = path.with_name(
            f"{path.stem}_{count}{path.suffix}"
        )
        count += 1
    return path


def organize():
    if not DOWNLOADS.is_dir():
        print("Downloads folder not found.")
        return

    files = [
        f for f in DOWNLOADS.rglob("*")
        if f.is_file()
        and f.parent.name not in CATEGORIES
        and f.name != Path(__file__).name
    ]

    print(f"Found {len(files)} files in Downloads and subfolders.")

    if not files:
        print("Nothing to organize.")
        return

    for file in files:
        print(f"{file.relative_to(DOWNLOADS)} -> {category(file)}/")

    if input("\nType YES to reorganize: ").strip() != "YES":
        print("Cancelled.")
        return

    moved = 0

    for file in files:
        try:
            folder = DOWNLOADS / category(file)
            folder.mkdir(exist_ok=True)

            destination = unique_path(folder / file.name)
            shutil.move(str(file), str(destination))
            print(f"Moved: {file.name}")
            moved += 1

        except OSError as error:
            print(f"Failed: {file} - {error}")

    # Remove empty subfolders, but never remove Downloads itself.
    for folder in sorted(
        (p for p in DOWNLOADS.rglob("*") if p.is_dir()),
        key=lambda p: len(p.parts),
        reverse=True,
    ):
        if folder.name not in CATEGORIES:
            try:
                folder.rmdir()
            except OSError:
                pass

    print(f"\nCompleted! Files moved: {moved}")


if __name__ == "__main__":
    organize()
