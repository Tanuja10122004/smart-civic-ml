
from pathlib import Path
import json
import sys
import tensorflow as tf
import numpy as np
from priority_detection import calculate_priority

from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

IMAGE_SIZE = 160

model_path = Path("models/road_damage_model.keras")
class_path = Path("models/class_names.json")

model = tf.keras.models.load_model(model_path)

with open(class_path, "r") as file:
    class_names = json.load(file)

if len(sys.argv) < 2:
    print('Usage: python predict_image.py "image_path"')
    raise SystemExit(1)

image_path = Path(sys.argv[1])

if not image_path.is_file():
    print("Image file nahi mili:", image_path)
    raise SystemExit(1)

image = tf.keras.utils.load_img(
    image_path,
    target_size=(IMAGE_SIZE, IMAGE_SIZE)
)

image = tf.keras.utils.img_to_array(image)
image = preprocess_input(image)
image = np.expand_dims(image, axis=0)

predictions = model.predict(image, verbose=0)[0]
best_index = int(np.argmax(predictions))

print("\nPredicted damage:", class_names[best_index])
print(f"Model score: {predictions[best_index] * 100:.2f}%")


category = class_names[best_index]


# Take actual complaint details from the user
print("\n--- Complaint Details ---")

while True:
    try:
        severity = int(input("Damage severity (1-5): "))
        if 1 <= severity <= 5:
            break
        print("Please enter a number between 1 and 5.")
    except ValueError:
        print("Please enter a valid number.")

def ask_yes_no(question):
    while True:
        answer = input(question + " (yes/no): ").strip().lower()
        if answer in ["yes", "y"]:
            return True
        elif answer in ["no", "n"]:
            return False
        else:
            print("Please enter yes or no.")

blocks_traffic = ask_yes_no("Is traffic blocked?")
injury_risk = ask_yes_no("Is there a possible injury risk?")
near_school_hospital = ask_yes_no(
    "Is the issue near a school or hospital?"
)

complaint_data = {
    "category": category,
    "severity": severity,
    "blocks_traffic": blocks_traffic,
    "injury_risk": injury_risk,
    "near_school_hospital": near_school_hospital
}

result = calculate_priority(complaint_data)

print("\n--- Priority Assessment ---")
print("Priority:", result["priority"])
print("Score:", result["score"])
print("Reasons:")

for reason in result["reasons"]:
    print("-", reason)




