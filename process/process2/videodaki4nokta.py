import cv2
import numpy as np
from ultralytics import YOLO
import torch

# CUDA kontrolü
device = 'cuda' if torch.cuda.is_available() else 'cpu'

# Modeli yükle
def load_model(model_path):
    model = YOLO(model_path)  # ultralytics kütüphanesi ile model yükleme
    model.to(device)  # CUDA veya CPU'ya yerleştir
    return model

# Model dosya yolunu belirt
model_path = 'yolov8x.pt'
model = load_model(model_path)

# Video dosyasını aç
video_path = 'input_media/videobu2.mp4'
cap = cv2.VideoCapture(video_path)

# İlk kareyi oku
ret, frame = cap.read()

if not ret:
    print("Video okunamadı.")
    cap.release()
    cv2.destroyAllWindows()
    exit()

# Kullanıcıdan 4 tane nokta seçmesini iste
cv2.namedWindow('Frame', cv2.WINDOW_NORMAL)
cv2.imshow('Frame', frame)

# Nokta seçimi için global değişkenler
points = []
def select_point(event, x, y, flags, param):
    global points
    if event == cv2.EVENT_LBUTTONDOWN:
        if len(points) < 4:
            points.append((x, y))
            cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)
            cv2.imshow('Frame', frame)
        if len(points) == 4:
            cv2.destroyAllWindows()

cv2.setMouseCallback('Frame', select_point)

# Kullanıcıdan 4 tane nokta seçmesini bekle
cv2.waitKey(0)

if len(points) != 4:
    print("4 nokta seçilmedi. Program sonlandırılıyor.")
    cap.release()
    cv2.destroyAllWindows()
    exit()

# Seçilen noktaları yazdır
print("Seçilen noktalar:")
for i, point in enumerate(points):
    print(f"Nokta {i+1}: {point}")

# Koordinatları bir dosyaya yaz
with open('outputs/txt_outputs/video_selected_points.txt', 'w') as f:
    for point in points:
        f.write(f"{point[0]},{point[1]}\n")

cap.release()
cv2.destroyAllWindows()
