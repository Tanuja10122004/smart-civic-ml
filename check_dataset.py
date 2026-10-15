
from pathlib import Path

# Project ke andar dataset ka path
dataset_path = Path(
    "data/raw/Indian-Road-Damage-Infrastructure-Dataset-main/"
    "Indian-Road-Damage-Infrastructure-Dataset-main"
)

print("Checking dataset...\n")

if dataset_path.exists():
    print("Dataset folder found!")

    for folder in dataset_path.iterdir():
        if folder.is_dir():
            print(f"\nFolder: {folder.name}")

            items = list(folder.iterdir())
            print("Total items:", len(items))

            for item in items[:5]:
                print(" -", item.name)
else:
    print("Dataset folder not found!")
    print("Please check the folder name and location.")
