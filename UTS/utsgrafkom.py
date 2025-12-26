import tkinter as tk
import math
import random
from PIL import Image, ImageTk

# ==========================================
# 1. KELAS ENGINE GRAFIKA MANUAL
# ==========================================
class GraphicsEngine:
    def __init__(self, canvas):
        self.canvas = canvas
        self.width = int(canvas['width'])
        self.height = int(canvas['height'])

    def put_pixel(self, x, y, color):
        """Implementasi dasar manipulasi titik"""
        x, y = int(x), int(y)
        if 0 <= x < self.width and 0 <= y < self.height:
            self.canvas.create_line(x, y, x + 1, y + 1, fill=color, width=1)

    def draw_line(self, x0, y0, x1, y1, color="black"):
        """POIN 1: Algoritma Garis Bresenham"""
        x0, y0, x1, y1 = int(x0), int(y0), int(x1), int(y1)
        dx, dy = abs(x1 - x0), abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        while True:
            self.put_pixel(x0, y0, color)
            if x0 == x1 and y0 == y1: break
            e2 = 2 * err
            if e2 > -dy: err -= dy; x0 += sx
            if e2 < dx: err += dx; y0 += sy

    def draw_circle_midpoint(self, xc, yc, r, color="red"):
        """POIN 2: Algoritma Lingkaran Midpoint"""
        xc, yc, r = int(xc), int(yc), int(r)
        if r <= 0: return
        x, y, d = 0, r, 1 - r
        self._plot_circle_points(xc, yc, x, y, color)
        while x < y:
            x += 1
            if d < 0: d = d + 2 * x + 1
            else: y -= 1; d = d + 2 * (x - y) + 1
            self._plot_circle_points(xc, yc, x, y, color)

    def _plot_circle_points(self, xc, yc, x, y, color):
        points = [(xc+x, yc+y), (xc-x, yc+y), (xc+x, yc-y), (xc-x, yc-y),
                  (xc+y, yc+x), (xc-y, yc+x), (xc+y, yc-x), (xc-y, yc-x)]
        for p in points: self.put_pixel(p[0], p[1], color)

    def draw_rectangle(self, xc, yc, r, color="green"):
        """POIN 3: Algoritma Poligon (Persegi)"""
        x0, y0 = xc - r, yc - r
        x1, y1 = xc + r, yc + r
        self.draw_line(x0, y0, x1, y0, color)
        self.draw_line(x1, y0, x1, y1, color)
        self.draw_line(x1, y1, x0, y1, color)
        self.draw_line(x0, y1, x0, y0, color)

# ==========================================
# 2. LOGIKA GAME UTAMA
# ==========================================
class CannonGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Manual Graphics Engine - 4 Core Points")
        self.WIDTH, self.HEIGHT = 500, 700
        self.canvas = tk.Canvas(root, width=self.WIDTH, height=self.HEIGHT, bg="black", highlightthickness=0)
        self.canvas.pack()

        self.gfx = GraphicsEngine(self.canvas)
        self.DEADLINE_Y = self.HEIGHT - 50

        # POIN 4: Skala (Transformasi Geometris) dilakukan di sini
        try:
            self.cannon_img = Image.open("cannon.png").convert("RGBA").resize((100, 90))
        except: 
            self.cannon_img = Image.new("RGBA", (60, 50), (34, 139, 34, 255))

        root.bind("<Left>", lambda e: self.move_cannon(-20))
        root.bind("<Right>", lambda e: self.move_cannon(20))
        root.bind("<a>", lambda e: self.change_angle(5))
        root.bind("<d>", lambda e: self.change_angle(-5))
        root.bind("<space>", self.shoot)
        root.bind("<r>", self.restart_game)
        root.bind("<q>", lambda e: self.root.destroy())

        self.init_game_state()
        self.run()

    def init_game_state(self):
        self.cannon_x, self.cannon_y = self.WIDTH / 2, self.HEIGHT - 90
        self.cannon_angle = 90
        self.score = 0
        self.bullets = []
        self.targets = []
        self.spawn_timer = 0
        self.game_over = False
        self.time_left = 60.0

    def restart_game(self, event=None):
        if self.game_over: self.init_game_state()

    def change_angle(self, amt):
        if not self.game_over:
            new_angle = self.cannon_angle + amt
            if 0 <= new_angle <= 180: self.cannon_angle = new_angle

    def move_cannon(self, amt):
        """POIN 4: Translasi Geometris 2D (Perpindahan X)"""
        if not self.game_over:
            new_x = self.cannon_x + amt
            if 50 < new_x < self.WIDTH - 50: self.cannon_x = new_x

    def draw_cannon_manual(self):
        """POIN 4: Rotasi Geometris 2D Manual per Piksel"""
        # Konversi sudut ke radian (ditambah offset 90 agar gambar menghadap atas)
        angle_rad = math.radians(-self.cannon_angle + 90)
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)

        pixels = self.cannon_img.load()
        w, h = self.cannon_img.size
        cx, cy = w / 2, h / 2

        # Step 2 untuk efisiensi performa agar tidak terlalu lag
        for y in range(0, h, 2):
            for x in range(0, w, 2):
                r, g, b, a = pixels[x, y]
                if a > 128: # Hanya gambar jika piksel tidak transparan
                    # 1. Translasi ke pusat (0,0)
                    tx, ty = x - cx, y - cy
                    # 2. Rumus Rotasi Manual
                    nx = tx * cos_a - ty * sin_a
                    ny = tx * sin_a + ty * cos_a
                    # 3. Translasi ke posisi meriam di layar
                    final_x = nx + self.cannon_x
                    final_y = ny + self.cannon_y
                    
                    color = '#%02x%02x%02x' % (r, g, b)
                    self.gfx.put_pixel(final_x, final_y, color)

    def shoot(self, event=None):
        if self.game_over: return
        rad = math.radians(-self.cannon_angle)
        self.bullets.append({
            'x': self.cannon_x, 'y': self.cannon_y, 
            'dx': math.cos(rad) * 15, 'dy': math.sin(rad) * 15
        })

    def explode_green(self, x, y):
        for _ in range(8):
            angle = random.uniform(0, 2 * math.pi)
            speed_exp = random.uniform(2, 4)
            self.targets.append({
                'x': x, 'y': y, 'dx': math.cos(angle)*speed_exp, 'dy': math.sin(angle)*speed_exp,
                'r': 10, 'speed': random.uniform(0.5, 1.5), 'color': "red", 'is_fragment': True
            })

    def update_logic(self):
        if self.game_over: return
        self.time_left -= 0.04
        if self.time_left <= 0: self.game_over = True

        self.spawn_timer += 1
        if self.spawn_timer > 40:
            is_green = random.random() < 0.2
            self.targets.append({
                'x': random.randint(30, self.WIDTH-30), 'y': -30, 
                'dx': 0, 'dy': 0, 'r': 20, 'speed': random.uniform(1.0, 2.5),
                'color': "green" if is_green else "red", 'is_fragment': False
            })
            self.spawn_timer = 0

        for b in self.bullets:
            b['x'] += b['dx']; b['y'] += b['dy']

        for t in self.targets[:]:
            t['x'] += t['dx']
            t['y'] += t['speed']
            
            # POIN 4: Refleksi Geometris (Memantul di dinding)
            if t['x'] <= 0 or t['x'] >= self.WIDTH: t['dx'] *= -1
            if (t['y'] + t['r']) >= self.DEADLINE_Y: self.game_over = True

            for b in self.bullets[:]:
                dist = math.sqrt((b['x']-t['x'])**2 + (b['y']-t['y'])**2)
                if dist < t['r']:
                    if t['color'] == "green": self.explode_green(t['x'], t['y']); self.score += 30
                    else: self.score += 10
                    if t in self.targets: self.targets.remove(t)
                    if b in self.bullets: self.bullets.remove(b)

    def draw_frame(self):
        self.canvas.delete("all")
        self.gfx.draw_line(0, self.DEADLINE_Y, self.WIDTH, self.DEADLINE_Y, "white")

        for b in self.bullets:
            self.gfx.draw_line(b['x'], b['y'], b['x']+b['dx'], b['y']+b['dy'], "yellow")
        
        for t in self.targets:
            if t['color'] == "green":
                self.gfx.draw_rectangle(t['x'], t['y'], t['r'], "green")
            else:
                self.gfx.draw_circle_midpoint(t['x'], t['y'], t['r'], t['color'])

        # GAMBAR MERIAM DENGAN ROTASI MANUAL
        self.draw_cannon_manual()

        self.canvas.create_text(80, 30, text=f"SCORE: {self.score}", font=("Courier", 15, "bold"), fill="white")
        secs = max(0, int(self.time_left))
        self.canvas.create_text(self.WIDTH-80, 30, text=f"TIME: {secs}s", font=("Courier", 13), fill="white")
        
        if self.game_over:
            self.canvas.create_rectangle(50, 250, 450, 450, fill="black", outline="white")
            self.canvas.create_text(self.WIDTH/2, 320, text="GAME OVER", font=("Arial", 30, "bold"), fill="red")
            self.canvas.create_text(self.WIDTH/2, 380, text=f"Score: {self.score} | [R]estart", font=("Courier", 15), fill="white")

    def run(self):
        self.update_logic()
        self.draw_frame()
        self.root.after(40, self.run)

if __name__ == "__main__":
    root = tk.Tk()
    game = CannonGame(root)
    root.resizable(False, False)
    root.mainloop()