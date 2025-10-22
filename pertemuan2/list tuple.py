# 1. Membuat dan Menampilkan List Pasangan Titik
titik_list = [(0, 0), (50, 50), (100, 0)]
print("--- Menampilkan Semua Titik dalam List ---")
for x, y in titik_list:
    print(f"Titik: ({x}, {y})")
    
# 2. Menyimpan dan Menampilkan Nilai Tuple
pusat = (0, 0)
print("\n--- Titik Pusat (Tuple) ---")
print(f"Nilai titik pusat adalah: {pusat}")

# 3. Membuat dan Menampilkan Data Dictionary
objek_attr = {"x": 10, "y": 20, "warna": "biru"}
print("\n--- Atribut Objek (Dictionary) ---")

# Mengambil nilai dari dictionary
x_val = objek_attr["x"]
y_val = objek_attr["y"]
warna_val = objek_attr["warna"]

# Menampilkan dalam format yang diminta
print(f"Titik ({x_val}, {y_val}) berwarna {warna_val}.")