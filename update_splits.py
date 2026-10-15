
from pathlib import Path
import pandas as pd

base_dir = Path("data/processed")
image_dir = base_dir / "images"

for split in ["train", "val", "test"]:
    csv_path = base_dir / f"{split}.csv"
    df = pd.read_csv(csv_path)

    df["image_path"] = df.apply(
        lambda row: str(
            image_dir / row["label"] / Path(row["image_path_in_zip"]).name
        ),
        axis=1
    )

    # Verify that every image exists
    missing = df[~df["image_path"].apply(
        lambda path: Path(path).is_file()
    )]

    if not missing.empty:
        print(f"{split}: Missing images = {len(missing)}")
        raise FileNotFoundError("Kuch image paths nahi mile.")

    df.to_csv(csv_path, index=False)
    print(f"{split}: {len(df)} images verified and saved.")

print("\nAll splits are ready for training!")

