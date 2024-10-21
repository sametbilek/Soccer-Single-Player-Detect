import numpy as np
import matplotlib.pyplot as plt

# Koordinatları dosyadan okuma fonksiyonu
def read_coordinates_from_file(file_path):
    coordinates = []
    with open(file_path, 'r') as file:
        for line in file:
            x, y = map(float, line.strip().split(','))
            coordinates.append([x, y])
    return np.array(coordinates, dtype="float32")

# Mesafeleri dosyaya yazma fonksiyonu
def write_distances_to_file(file_path, distances):
    with open(file_path, 'w') as file:
        for distance in distances:
            file.write(f"{distance:.2f}\n")

# Hız verilerini dosyaya yazma fonksiyonu
def write_velocities_to_file(file_path, velocities):
    with open(file_path, 'w') as file:
        for velocity in velocities:
            file.write(f"{velocity:.2f}\n")

# İki nokta arasındaki Euclidean mesafeyi hesaplayan fonksiyon
def calculate_distances(points):
    distances = []
    for i in range(len(points) - 1):
        distance = np.linalg.norm(points[i + 1] - points[i])
        distances.append(distance)
    return distances

# Hız verilerini hesaplayan fonksiyon
def calculate_velocities(distances, fps):
    velocities = [distance / (1 / fps) for distance in distances]
    return velocities

# Hız verilerini dosyadan okuma fonksiyonu
def read_velocities_from_file(file_path):
    velocities = []
    with open(file_path, 'r') as file:
        for line in file:
            velocity = float(line.strip())
            velocities.append(velocity)
    return velocities

# Oyuncu pozisyonlarını txt dosyasından okuma
transformed_positions = read_coordinates_from_file('outputs/txt_outputs/homographic_positions.txt')

# İki ardışık koordinat arasındaki mesafeleri hesaplama
distances = calculate_distances(transformed_positions)

# Mesafeleri dosyaya yazma
write_distances_to_file('outputs/txt_outputs/distances.txt', distances)



with open('outputs/txt_outputs/distances.txt', 'r') as file:
    data = [float(line.strip()) for line in file]


# Verilerin standart sapmasını hesapla
mean = np.mean(data)
std_dev = np.std(data)

print(f"Standart Sapma: {std_dev}")


threshold = 3
for i in range(1, len(data)):
    if abs(data[i] - mean) > threshold * std_dev:
        data[i] = data[i-1]

total_distance = 0.00

for i in range(1, len(data)):
    total_distance += data[i]

total_distance = total_distance / 1000

# Toplamı yazdır
print(f"Toplam kosma: {total_distance} km")


# FPS değerini belirleme
fps = 30  # Örnek FPS değeri, gerektiğinde değiştirilebilir

# Hız verilerini hesaplama
velocities = calculate_velocities(data, fps)
velocities = [x * 3.6 for x in velocities]

# Hız verilerini dosyaya yazma
write_velocities_to_file('outputs/txt_outputs/velocities.txt', velocities)

# Hız verilerini dosyadan okuma
velocities = read_velocities_from_file('outputs/txt_outputs/velocities.txt')

# Zaman eksenini oluşturma
time_intervals = np.arange(len(velocities)) / fps

# Her 30 satırda bir hız verisi seçme
interval = 10
selected_indices = np.arange(0, len(velocities), interval)
selected_velocities = np.array(velocities)[selected_indices]
selected_times = time_intervals[selected_indices]

# Grafiği oluşturma
plt.figure(figsize=(10, 6))
plt.plot(selected_times, selected_velocities, linestyle='-', color='b')
plt.title('Player Velocity Over Time')
plt.xlabel('Time (seconds)')
plt.ylabel('Velocity (km/h)')
plt.grid(True)
plt.savefig('outputs/img_outputs/velocity_graph.png')
