
from pathlib import Path
import json
import pandas as pd
import tensorflow as tf

from tensorflow.keras import layers, models
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

# 1. Load the dataset CSV files
base_dir = Path("data/processed")

train_df = pd.read_csv(base_dir / "train.csv")
val_df = pd.read_csv(base_dir / "val.csv")
test_df = pd.read_csv(base_dir / "test.csv")

class_names = sorted(train_df["label"].unique())
class_to_id = {name: i for i, name in enumerate(class_names)}

for df in [train_df, val_df, test_df]:
    if not set(df["label"]).issubset(class_to_id):
        raise ValueError("Dataset mein unknown category mili.")

print("Categories:", class_names)

# 2. Prepare images for the model
IMAGE_SIZE = 160
BATCH_SIZE = 16

def create_dataset(df, shuffle=False):
    paths = df["image_path"].tolist()
    labels = [class_to_id[label] for label in df["label"]]

    dataset = tf.data.Dataset.from_tensor_slices((paths, labels))

    def load_image(path, label):
        image = tf.io.read_file(path)
        image = tf.io.decode_jpeg(image, channels=3)
        image = tf.image.resize(image, (IMAGE_SIZE, IMAGE_SIZE))
        image = preprocess_input(image)
        return image, label

    dataset = dataset.map(
        load_image,
        num_parallel_calls=tf.data.AUTOTUNE
    )

    if shuffle:
        dataset = dataset.shuffle(
            buffer_size=len(df),
            seed=42
        )

    return dataset.batch(BATCH_SIZE).prefetch(tf.data.AUTOTUNE)

train_ds = create_dataset(train_df, shuffle=True)
val_ds = create_dataset(val_df)
test_ds = create_dataset(test_df)

# 3. Load the pretrained MobileNetV2 model
base_model = MobileNetV2(
    weights="imagenet",
    include_top=False,
    input_shape=(IMAGE_SIZE, IMAGE_SIZE, 3)
)

# Keep pretrained layers frozen initially
base_model.trainable = False

# 4. Add our six-category classifier
model = models.Sequential([
    layers.Input(shape=(IMAGE_SIZE, IMAGE_SIZE, 3)),
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.Dropout(0.2),
    layers.Dense(len(class_names), activation="softmax")
])

model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

model.summary()

# 5. Train the model
history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=5
)

# 6. Evaluate on the separate test dataset
test_loss, test_accuracy = model.evaluate(test_ds)

print(f"\nTest accuracy: {test_accuracy:.4f}")
print(f"Test loss: {test_loss:.4f}")

# 7. Save the trained model and category names
models_dir = Path("models")
models_dir.mkdir(parents=True, exist_ok=True)

model.save(models_dir / "road_damage_model.keras")

with open(models_dir / "class_names.json", "w") as file:
    json.dump(class_names, file, indent=4)

print("\nModel saved in models/road_damage_model.keras")
print("Category names saved in models/class_names.json")
