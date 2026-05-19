from pathlib import Path
import random
import shutil

# настройки подвыборки
seed = 42
classes = ["A", "B", "C", "D", "E", "F"]
max_images_per_class = 200

# папка, куда kagglehub скачал полный датасет
source_root = (
    Path.home() / ".cache" / "kagglehub" / "datasets" / "grassknoted" /
    "asl-alphabet" / "versions" / "1" / "asl_alphabet_train" / "asl_alphabet_train"
)

# папка проекта, из которой запускается скрипт
project_dir = Path.cwd()
target_root = project_dir / "data" / "asl_dataset"

# расширения изображений
image_extensions = ["*.jpg", "*.jpeg", "*.png", "*.bmp", "*.webp"]

if not source_root.exists():
    raise FileNotFoundError(f"не найдена папка с полным датасетом: {source_root}")

target_root.mkdir(parents=True, exist_ok=True)

for class_name in classes:
    source_class_dir = source_root / class_name
    target_class_dir = target_root / class_name

    if not source_class_dir.exists():
        raise FileNotFoundError(f"не найдена папка класса: {source_class_dir}")

    target_class_dir.mkdir(parents=True, exist_ok=True)

    # очищаю старые изображения этого класса, чтобы при повторном запуске не было дублей
    for old_file in target_class_dir.iterdir():
        if old_file.is_file():
            old_file.unlink()

    files = []
    for extension in image_extensions:
        files.extend(source_class_dir.glob(extension))

    files = sorted(files)
    random.Random(seed).shuffle(files)
    selected_files = files[:max_images_per_class]

    for file_path in selected_files:
        shutil.copy2(file_path, target_class_dir / file_path.name)

    print(f"{class_name}: скопировано {len(selected_files)} изображений")

print(f"готово, подвыборка сохранена в: {target_root}")
