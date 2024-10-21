import cv2
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

# Pencereyi normal olarak aç
cv2.namedWindow('Frame', cv2.WINDOW_NORMAL)

# Kullanıcıdan ROI (region of interest) seçmesini iste
roi = cv2.selectROI('Frame', frame, fromCenter=False, showCrosshair=True)
cv2.destroyAllWindows()

# Seçilen ROI'yi belirle
x, y, w, h = roi

# CSRT tracker'ı başlat
tracker = cv2.TrackerCSRT_create()
tracker.init(frame, (x, y, w, h))

# Koordinatları kaydedeceğimiz dosya
output_file = 'outputs/txt_outputs/player_positions.txt'

# Video boyunca takip et
with open(output_file, 'w') as f:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Tracker ile nesneyi güncelle
        success, bbox = tracker.update(frame)

        if success:
            x, y, w, h = [int(v) for v in bbox]
            # Nesne merkez koordinatlarını hesapla
            center_x = x + w / 2
            center_y = y + h / 2
            # Koordinatları ekrana yazdır
            print(f"Koordinatlar: x={center_x}, y={center_y}")
            # Koordinatları dosyaya yaz
            f.write(f"{center_x},{center_y}\n")

cap.release()
cv2.destroyAllWindows()
