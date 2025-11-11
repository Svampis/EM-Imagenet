import json
from collections import Counter
import os
labels_file = open("./assets/real.json")
labels = json.load(labels_file)
labels_file.close()
labeled_image_paths = []
for image_id in range(0, 50000):
    image_path = "./assets/images/ILSVRC2012_val_"
    image_path += str(image_id + 1).zfill(8)
    image_path += ".JPEG"
    if len(labels[image_id]) != 0:
        labeled_image_paths.append([
            image_path,
            max(labels[image_id], key=labels[image_id].count)
        ])

label_names = []
label_names_file = open("./assets/labels.txt")
for line in label_names_file:
    label_names.append(line.split(';')[1].strip())

for labeled_image_path in labeled_image_paths:
    labeled_image_path[1] = label_names[labeled_image_path[1]]

label_counts = Counter(label for _, label in labeled_image_paths)
top_labels = [label for label, _ in label_counts.most_common(50)]

filtered = [[a, b] for a, b in labeled_image_paths if b in top_labels]

preprocessed_dataset_filename = open("assets/preprocessed_dataset.json", "w")
json.dump(filtered, preprocessed_dataset_filename)
preprocessed_dataset_filename.close()

image_names_file = open("assets/image_names.txt", "w")
for datum in filtered:
    print(os.path.basename(datum[0]), file=image_names_file)
image_names_file.close()
