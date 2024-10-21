import numpy as np
import cv2


# Homografi matrisini hesaplayan fonksiyon
def calculate_homography(src_points, dst_points):
    h, status = cv2.findHomography(src_points, dst_points)
    return h


# Homografi matrisine göre koordinatları yeniden hesaplayan fonksiyon
def apply_homography(h, points):
    transformed_points = cv2.perspectiveTransform(points.reshape(-1, 1, 2), h)
    return transformed_points.reshape(-1, 2)


# Koordinatları dosyaya yazma fonksiyonu
def write_coordinates_to_file(file_path, coordinates):
    with open(file_path, 'w') as file:
        for coord in coordinates:
            file.write(f"{coord[0]}, {coord[1]}\n")


def read_coordinates_from_file(file_path):
    coordinates = []
    with open(file_path, 'r') as file:
        for line in file:
            x, y = map(float, line.strip().split(','))
            coordinates.append([x, y])
    return np.array(coordinates, dtype="float32")


# Video ve dünya koordinatları
video_points = read_coordinates_from_file("outputs/txt_outputs/video_selected_points.txt")

# world pointsi mecburen sabit yapcaz cunku stadyum olcusune gore hız hesabi lazim
world_points = np.array([
    [0, 0],
    [0, 68],
    [105, 68],
    [105, 0]
], dtype="float32")

# Homografi matrisini hesaplama
h_matrix = calculate_homography(video_points, world_points)

# Oyuncu pozisyonlarını txt dosyasından okuma
player_positions = read_coordinates_from_file('outputs/txt_outputs/player_positions.txt')

# Oyuncu pozisyonlarını homografi matrisine göre yeniden hesaplama
transformed_positions = apply_homography(h_matrix, player_positions)

# Yeniden hesaplanan pozisyonları yeni bir dosyaya yazma
write_coordinates_to_file('outputs/txt_outputs/homographic_positions.txt', transformed_positions)
