# -*- coding: utf-8 -*-
"""
Count all helmet classes: With Helmet, Without Helmet, Triple Riding
Save images for each category
"""
import os
import csv
from datetime import datetime
from ultralytics import YOLO
import cv2

# Load the model
model = YOLO("runs/detect/train7/weights/best.pt")

# Detection parameters
CONFIDENCE_THRESHOLD = 0.15  # Lower threshold to detect more

# Create directories
os.makedirs("violations", exist_ok=True)
os.makedirs("violations/with_helmet", exist_ok=True)
os.makedirs("violations/without_helmet", exist_ok=True)
os.makedirs("violations/triple_riding", exist_ok=True)

# CSV file for all detections
csv_file = "violations/all_detections.csv"

# Counters
with_helmet_count = 0
without_helmet_count = 0
triple_riding_count = 0

# Open video
video_file = "triple_riding.mp4"
cap = cv2.VideoCapture(video_file)

frame_count = 0
detection_records = []

print("Processing video to count all helmet classes...")
print("="*60)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    frame_count += 1
    
    # Process every 5th frame for speed
    if frame_count % 5 != 0:
        continue
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Run prediction
    results = model.predict(source=frame, save=False, show=False, conf=CONFIDENCE_THRESHOLD)
    
    # Process results
    frame_has_detection = False
    for result in results:
        for box in result.boxes:
            class_id = int(box.cls.item())
            confidence = box.conf.item()
            bbox = box.xyxy.tolist()[0]  # [x1, y1, x2, y2]
            
            class_name = model.names[class_id]
            
            # Count by class
            if class_id == 0:  # With Helmet
                with_helmet_count += 1
                label = "With Helmet"
                save_dir = "violations/with_helmet"
            elif class_id == 1:  # Without Helmet
                without_helmet_count += 1
                label = "Without Helmet"
                save_dir = "violations/without_helmet"
            elif class_id == 2:  # Triple Riding
                triple_riding_count += 1
                label = "Triple Riding"
                save_dir = "violations/triple_riding"
            
            # Save annotated frame
            annotated_frame = results[0].plot()
            x1, y1, x2, y2 = map(int, bbox)
            cv2.putText(annotated_frame, f"{label}: {confidence:.2f}", (x1, y1 - 10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            save_path = f"{save_dir}/frame_{frame_count}_class_{class_id}.jpg"
            cv2.imwrite(save_path, annotated_frame)
            
            detection_records.append({
                'Frame Number': frame_count,
                'Timestamp': timestamp,
                'Class': class_name,
                'Confidence': confidence,
                'Bounding Box': str(bbox)
            })
            
            frame_has_detection = True
            print(f"Frame {frame_count}: {class_name} (Conf: {confidence:.2f})")

cap.release()
cv2.destroyAllWindows()

# Save CSV
with open(csv_file, mode='w', newline='') as file:
    if detection_records:
        writer = csv.DictWriter(file, fieldnames=detection_records[0].keys())
        writer.writeheader()
        writer.writerows(detection_records)

print("="*60)
print("DETECTION RESULTS:")
print("="*60)
print(f"With Helmet (Compliant):    {with_helmet_count}")
print(f"Without Helmet (Violation):  {without_helmet_count}")
print(f"Triple Riding (Violation):   {triple_riding_count}")
print("="*60)
print(f"Total Detections:           {with_helmet_count + without_helmet_count + triple_riding_count}")
print("="*60)
print(f"\nImages saved in:")
print(f"  - violations/with_helmet/     ({with_helmet_count} images)")
print(f"  - violations/without_helmet/  ({without_helmet_count} images)")
print(f"  - violations/triple_riding/   ({triple_riding_count} images)")
print(f"\nCSV saved: {csv_file}")
