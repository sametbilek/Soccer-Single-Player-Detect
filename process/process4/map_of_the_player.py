import cv2
import numpy as np


def read_coordinates_from_file(file_path):
    coordinates = []
    with open(file_path, 'r') as file:
        for line in file:
            x, y = map(float, line.strip().split(','))
            coordinates.append([x, y])
    return np.array(coordinates, dtype="float32")


video_points = read_coordinates_from_file("outputs/txt_outputs/video_selected_points.txt")

image_points = read_coordinates_from_file("outputs/txt_outputs/image_selected_points.txt")

H, status = cv2.findHomography(video_points, image_points)


def apply_homography(x, y, H):
    point = np.array([[x, y]], dtype="float32")
    point = np.array([point])
    transformed_point = cv2.perspectiveTransform(point, H)
    return transformed_point[0][0]


# Görseli yükle
image_path = 'input_media/sahafoto.png'
image = cv2.imread(image_path)

if image is None:
    print("Görsel yüklenemedi.")
    exit()

# Koordinatları içeren txt dosyasını okuyun
coordinates = []
with open('outputs/txt_outputs/player_positions.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        x, y = map(float, line.strip().split(','))
        coordinates.append((x, y))

# Marker görselini yükle ve yeniden boyutlandır
marker_path = 'input_media/marker.png'
marker = cv2.imread(marker_path, cv2.IMREAD_UNCHANGED)

if marker is None:
    print("Marker görseli yüklenemedi.")
    exit()

marker_size = (5, 5)  # Marker boyutu (genişlik, yükseklik)
marker = cv2.resize(marker, marker_size, interpolation=cv2.INTER_AREA)


# Marker'ı görsele eklemek için fonksiyon
def add_marker(image, point, marker):
    x, y = point
    mh, mw = marker.shape[0], marker.shape[1]

    # Marker'ı merkeze hizalamak için sol üst köşe koordinatları
    top_left_x = int(x - mw / 2)
    top_left_y = int(y - mh / 2)

    # Görüntünün boyutlarını alın
    img_h, img_w = image.shape[0], image.shape[1]

    # Marker'ın sınırlar içinde kalması için kontroller
    if top_left_x < 0:
        top_left_x = 0
    if top_left_y < 0:
        top_left_y = 0
    if top_left_x + mw > img_w:
        mw = img_w - top_left_x
        marker = marker[:, :mw]
    if top_left_y + mh > img_h:
        mh = img_h - top_left_y
        marker = marker[:mh, :]

    # Marker'ın dört kanalını ayrıştır
    if marker.shape[2] == 4:
        alpha_mask = marker[:, :, 3] / 255.0
        alpha_image = 1.0 - alpha_mask

        for c in range(0, 3):
            # Marker'ı mevcut görüntüyle karıştırarak koyulaştırma
            image[top_left_y:top_left_y + mh, top_left_x:top_left_x + mw, c] = (
                    alpha_mask * marker[:, :, c] +
                    alpha_image * image[top_left_y:top_left_y + mh, top_left_x:top_left_x + mw, c]
            )

            # Üst üste binen bölgelerde koyulaştırma
            image[top_left_y:top_left_y + mh, top_left_x:top_left_x + mw, c] = np.clip(
                image[top_left_y:top_left_y + mh, top_left_x:top_left_x + mw, c] * (1 + alpha_mask),
                0, 255
            )


# Koordinatları homografi matrisi ile dönüştürün ve marker ile işaretleyin
for coord in coordinates:
    transformed_coord = apply_homography(coord[0], coord[1], H)
    add_marker(image, tuple(map(int, transformed_coord)), marker)

# Görseli %50 boyutta yeniden boyutlandırın
resized_image = cv2.resize(image, (image.shape[1] // 2, image.shape[0] // 2))

# Görseli kaydedin veya gösterin
cv2.namedWindow('Image with Markers', cv2.WINDOW_NORMAL)  # Normal boyutta pencere oluştur
cv2.imshow('Image with Markers', resized_image)
cv2.imwrite('outputs/img_outputs/last_output.png', resized_image)
cv2.waitKey(0)
cv2.destroyAllWindows()