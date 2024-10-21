import cv2
import numpy as np

# Görsel dosya yolunu belirt
image_path = 'input_media/sahafoto.png'

# Görseli yükle
image = cv2.imread(image_path)

if image is None:
    print("Görsel yüklenemedi.")
    exit()

# Kullanıcıdan 4 tane nokta seçmesini iste
cv2.namedWindow('Image', cv2.WINDOW_NORMAL)
cv2.imshow('Image', image)

# Nokta seçimi için global değişkenler
points = []
def select_point(event, x, y, flags, param):
    global points
    if event == cv2.EVENT_LBUTTONDOWN:
        if len(points) < 4:
            points.append((x, y))
            cv2.circle(image, (x, y), 5, (0, 255, 0), -1)
            cv2.imshow('Image', image)
        if len(points) == 4:
            cv2.destroyAllWindows()

cv2.setMouseCallback('Image', select_point)

# Kullanıcıdan 4 tane nokta seçmesini bekle
cv2.waitKey(0)

if len(points) != 4:
    print("4 nokta seçilmedi. Program sonlandırılıyor.")
    exit()

# Seçilen noktaları yazdır
print("Seçilen noktalar:")
for i, point in enumerate(points):
    print(f"Nokta {i+1}: {point}")

# Koordinatları bir dosyaya yaz
with open('outputs/txt_outputs/image_selected_points.txt', 'w') as f:
    for point in points:
        f.write(f"{point[0]},{point[1]}\n")

# Görseli kaydedin veya gösterin
cv2.imwrite('outputs/img_outputs/image_selected_points.png', image)
