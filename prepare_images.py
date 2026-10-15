
import zipfile
from pathlib import Path
import pandas as pd

zip_path = Path.home() / "Downloads" / "Indian-Road-Damage-Infrastructure-Dataset-main.zip"
output_dir = Path("data") / "processed" / "images"
csv_path = Path("data") / "processed" / "verified_images.csv"

df = pd.read_csv(csv_path)

if not zip_path.exists():
    raise FileNotFoundError(f"ZIP file nahi mili: {zip_path}")

saved = 0
missing = 0

with zipfile.ZipFile(zip_path, "r") as z:
    available_files = set(z.namelist())

    for _, row in df.iterrows():
        source = row["image_path_in_zip"]
        label = row["label"]

        if source not in available_files:
            missing += 1
            continue

        destination_dir = output_dir / label
        destination_dir.mkdir(parents=True, exist_ok=True)

        filename = Path(source).name
        destination = destination_dir / filename

        with z.open(source) as src, open(destination, "wb") as dst:
            dst.write(src.read())

        saved += 1

print("Images extracted:", saved)
print("Missing images:", missing)
print("Images folder:", output_dir.resolve())
