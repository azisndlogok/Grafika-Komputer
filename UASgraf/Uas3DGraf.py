from ursina import *
import random

app = Ursina()

# --- 1. SETTING DUNIA ---
window.color = color.black
sky = Sky() 
AmbientLight(color=color.rgba(180, 180, 180, 255))
sun = DirectionalLight(y=20, rotation=(45, -45, 45), shadows=True)

# --- 2. DARATAN ---
ground = Entity(model='plane', texture='grass', scale=2000, color=color.green, y=0, collider='box')

# --- 3. UI (SKOR & HP) ---
score = 0
ui_score = Text(text=f'Score: {score}', position=(-0.85, 0.45), scale=1.5, color=color.yellow)
ui_hp = Text(text='', position=(-0.85, 0.40), scale=1.5, color=color.red)

# Indikator Lock Aim (Kotak Target)
lock_cursor = Entity(model='quad', color=color.rgba(0, 255, 0, 150), scale=0.2, add_to_scene_entities=False)
lock_cursor.texture = 'circle_outline' # Menggunakan tekstur bawaan yang mirip target

def update_ui():
    ui_score.text = f'Score: {score}'
    ui_hp.text = "HP: " + "X " * player.health

def restart_game():
    global score
    score = 0
    player.health = 3
    player.position = (0, 25, -100)
    player.rotation = (0,0,0)
    player.enabled = True
    for e in enemies:
        e.position = (random.uniform(-50, 50), 25, player.z + random.uniform(300, 500))
        e.health = 3
        e.enabled = True
    restart_button.enabled = False
    update_ui()

restart_button = Button(text='Restart', color=color.red, scale=(0.12, 0.05), position=(0.75, 0.45), on_click=restart_game, enabled=False)

# --- 4. EFEK LEDAKAN ---
def explode(pos):
    explosion = Entity(model='sphere', color=color.orange, position=pos, scale=1)
    explosion.animate_scale(5, duration=0.2, curve=curve.out_expo)
    explosion.animate_color(color.rgba(255,165,0,0), duration=0.3)
    destroy(explosion, delay=0.3)

# --- 5. MODEL PESAWAT ---
def create_jet_model(c):
    parent = Entity(model=None)
    Entity(parent=parent, model='cube', scale=(1, 0.8, 5), color=c)
    Entity(parent=parent, model='sphere', scale=(0.6, 0.5, 1.5), position=(0, 0.4, 1), color=color.black66)
    Entity(parent=parent, model='cube', scale=(7, 0.1, 2), position=(0, 0, -0.5), color=c)
    Entity(parent=parent, model='cube', scale=(0.1, 1.5, 1), position=(0, 0.7, -2.2), color=c)
    return parent

# --- 6. PEMAIN ---
player = create_jet_model(color.azure)
player.position = (0, 25, -100)
player.collider = 'box'
player.health = 3

# --- 7. SISTEM TEMBAK ---
bullets = []
enemy_bullets = []

def create_bullet(spacer, is_player=True):
    if not spacer or not spacer.enabled: return
    b = Entity(model='sphere', color=color.yellow if is_player else color.red, 
               scale=0.6, world_position=spacer.world_position + spacer.forward * 6, 
               world_rotation=spacer.world_rotation, collider='sphere')
    if is_player: bullets.append(b)
    else: enemy_bullets.append(b)
    destroy(b, delay=1.2)

# --- 8. MUSUH ---
enemies = []
def spawn_enemy():
    e = create_jet_model(color.red)
    e.position = (random.uniform(-100, 100), random.uniform(20, 40), player.z + random.uniform(400, 800))
    e.collider = 'box'
    e.health = 3
    e.shoot_timer = 0
    enemies.append(e)

for i in range(6): spawn_enemy()

camera.parent = player
camera.position = (0, 7, -20)
camera.rotation_x = 10

# --- 9. LOGIKA UPDATE ---
def update():
    global score
    if not player.enabled: return

    update_ui()
    
    # Gerak Dasar
    player.position += player.forward * 18 * time.dt
    player.rotation_x += (held_keys['s'] - held_keys['w']) * 60 * time.dt
    player.rotation_y += (held_keys['d'] - held_keys['a']) * 60 * time.dt

    # --- FITUR AUTO AIM & LOCK ---
    target = None
    closest_dist = 150 # Jarak deteksi radar
    
    for e in enemies:
        dist = distance(player, e)
        if dist < closest_dist:
            # Cek apakah musuh ada di depan pesawat (FOV)
            dot_product = Vec3.dot(player.forward, (e.world_position - player.world_position).normalized())
            if dot_product > 0.7: # Sekitar 45 derajat di depan
                target = e
                closest_dist = dist

    if target:
        # Visual Lock (Kotak Hijau di musuh)
        lock_cursor.enabled = True
        lock_cursor.world_position = target.world_position
        lock_cursor.look_at(camera) # Selalu menghadap kamera
        
        # Auto Aim (Mengarahkan perlahan ke target saat menembak atau dekat)
        if held_keys['space']:
            # Secara bertahap memutar player ke arah target
            player.look_at(target, 'forward')
            player.rotation_x = lerp(player.rotation_x, player.rotation_x, 0.1)
    else:
        lock_cursor.enabled = False

    # Tembak
    if held_keys['space']:
        if not hasattr(player, 'gun_timer'): player.gun_timer = 0
        player.gun_timer += time.dt
        if player.gun_timer > 0.15: # Tembakan sedikit lebih cepat
            create_bullet(player)
            player.gun_timer = 0

    # Logika Peluru & Kerusakan (Sama seperti sebelumnya)
    for b in bullets[:]:
        if b and b.enabled:
            b.position += b.forward * 120 * time.dt
            hit = b.intersects()
            if hit.hit and hit.entity in enemies:
                hit.entity.health -= 1
                bullets.remove(b)
                destroy(b)
                if hit.entity.health <= 0:
                    explode(hit.entity.position)
                    score += 100
                    hit.entity.position = (player.x + random.uniform(-100,100), 30, player.z + 600)
                    hit.entity.health = 3

    for e in enemies:
        e.look_at(player)
        e.position += e.forward * 9 * time.dt
        e.shoot_timer += time.dt
        if e.shoot_timer > 3.0:
            create_bullet(e, is_player=False)
            e.shoot_timer = 0

    for eb in enemy_bullets[:]:
        if eb and eb.enabled:
            eb.position += eb.forward * 50 * time.dt
            if eb.intersects().hit and eb.intersects().entity == player:
                player.health -= 1
                enemy_bullets.remove(eb)
                destroy(eb)
                if player.health <= 0:
                    explode(player.position)
                    player.enabled = False
                    restart_button.enabled = True

    if player.y < 2: player.y = 2

app.run() 