import os
import xml.etree.ElementTree as ET
from PIL import Image  # to get image size

# Paths
ANNOTATIONS_PATH = "Helmet_Dataset/annotations"
IMAGES_PATH = "Helmet_Dataset/images"
OUTPUT_LABELS = "Helmet_Dataset/labels"

classes = ["With Helmet", "Without Helmet"]

# Make sure output directory exists
os.makedirs(OUTPUT_LABELS, exist_ok=True)

# Process each XML file
for xml_file in os.listdir(ANNOTATIONS_PATH):
    if not xml_file.endswith(".xml"):
        continue

    xml_path = os.path.join(ANNOTATIONS_PATH, xml_file)
    tree = ET.parse(xml_path)
    root = tree.getroot()

    # Get corresponding image path
    image_file = root.find("filename").text
    image_path = os.path.join(IMAGES_PATH, image_file)

    # Open image to get width and height
    with Image.open(image_path) as img:
        img_width, img_height = img.size

    # Prepare YOLO formatted lines
    yolo_lines = []

    for obj in root.findall("object"):
        class_name = obj.find("name").text
        if class_name not in classes:
            continue  # skip unknown classes

        class_id = classes.index(class_name)
        bbox = obj.find("bndbox")
        xmin = float(bbox.find("xmin").text)
        ymin = float(bbox.find("ymin").text)
        xmax = float(bbox.find("xmax").text)
        ymax = float(bbox.find("ymax").text)

        # Convert to YOLO format
        x_center = (xmin + xmax) / 2 / img_width
        y_center = (ymin + ymax) / 2 / img_height
        width = (xmax - xmin) / img_width
        height = (ymax - ymin) / img_height

        yolo_lines.append(f"{class_id} {x_center} {y_center} {width} {height}")

    # Write to output txt file
    label_file = os.path.join(OUTPUT_LABELS, os.path.splitext(xml_file)[0] + ".txt")
    with open(label_file, "w") as f:
        f.write("\n".join(yolo_lines))

print("Conversion complete! Labels saved in:", OUTPUT_LABELS)
