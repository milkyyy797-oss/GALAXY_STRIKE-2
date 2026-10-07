import tkinter as tk
import random
import math

# =========================================================
# SPACE INVADERS - PYTHON TKINTER GAME
# =========================================================

WIDTH = 900
HEIGHT = 650

PLAYER_SPEED = 8
BULLET_SPEED = 12

START_ENEMIES = 5
MAX_ENEMIES = 15


class SpaceShooter:

    def __init__(self, root):
        self.root = root
        self.root.title("🚀 GALAXY STRIKE")
        self.root.resizable(False, False)

        self.canvas = tk.Canvas(
            root,
            width=WIDTH,
            height=HEIGHT,
            bg="#050816",
            highlightthickness=0
        )
        self.canvas.pack()

        # Game variables
        self.running = False
        self.game_over = False

        self.score = 0
        self.high_score = 0
        self.level = 1
        self.lives = 3

        self.player_x = WIDTH // 2
        self.player_y = HEIGHT - 80

        self.keys = set()

        self.bullets = []
        self.enemies = []
        self.particles = []
        self.stars = []

        self.last_shot = 0

        self.create_stars()
        self.show_menu()

        self.root.bind("<KeyPress>", self.key_down)
        self.root.bind("<KeyRelease>", self.key_up)

        self.game_loop()

    # =====================================================
    # BACKGROUND STARS
    # =====================================================

    def create_stars(self):

        for _ in range(120):

            star = {
                "x": random.randint(0, WIDTH),
                "y": random.randint(0, HEIGHT),
                "speed": random.uniform(0.5, 2.5),
                "size": random.choice([1, 1, 2, 2, 3])
            }

            self.stars.append(star)

    def draw_stars(self):

        for star in self.stars:

            star["y"] += star["speed"]

            if star["y"] > HEIGHT:
                star["y"] = 0
                star["x"] = random.randint(0, WIDTH)

            color = random.choice([
                "#ffffff",
                "#9bdcff",
                "#6c63ff",
                "#d7b8ff"
            ])

            self.canvas.create_oval(
                star["x"],
                star["y"],
                star["x"] + star["size"],
                star["y"] + star["size"],
                fill=color,
                outline=""
            )

    # =====================================================
    # MENU
    # =====================================================

    def show_menu(self):

        self.canvas.delete("all")

        self.draw_stars()

        self.canvas.create_text(
            WIDTH // 2,
            160,
            text="GALAXY STRIKE",
            fill="#62f5ff",
            font=("Arial", 48, "bold")
        )

        self.canvas.create_text(
            WIDTH // 2,
            215,
            text="🚀 SPACE SHOOTER 🚀",
            fill="#ff4fd8",
            font=("Arial", 20, "bold")
        )

        self.canvas.create_text(
            WIDTH // 2,
            290,
            text="Destroy the enemy fleet!",
            fill="white",
            font=("Arial", 18)
        )

        self.canvas.create_text(
            WIDTH // 2,
            350,
            text="MOVE  :  ← →   or   A D",
            fill="#9bdcff",
            font=("Arial", 16, "bold")
        )

        self.canvas.create_text(
            WIDTH // 2,
            385,
            text="SHOOT :  SPACE",
            fill="#9bdcff",
            font=("Arial", 16, "bold")
        )

        self.canvas.create_text(
            WIDTH // 2,
            465,
            text="PRESS ENTER TO START",
            fill="#ffff00",
            font=("Arial", 20, "bold")
        )

    # =====================================================
    # START GAME
    # =====================================================

    def start_game(self):

        self.running = True
        self.game_over = False

        self.score = 0
        self.level = 1
        self.lives = 3

        self.bullets.clear()
        self.enemies.clear()
        self.particles.clear()

        self.player_x = WIDTH // 2
        self.player_y = HEIGHT - 80

        self.create_enemies(START_ENEMIES)

    # =====================================================
    # ENEMIES
    # =====================================================

    def create_enemies(self, amount):

        for _ in range(amount):

            enemy = {
                "x": random.randint(40, WIDTH - 40),
                "y": random.randint(-400, -50),
                "speed": random.uniform(
                    1.2 + self.level * 0.15,
                    2.2 + self.level * 0.2
                ),
                "size": random.randint(18, 25),
                "color": random.choice([
                    "#ff3864",
                    "#ff7b00",
                    "#b83bff",
                    "#00e5ff",
                    "#ff3cac"
                ])
            }

            self.enemies.append(enemy)

    # =====================================================
    # PLAYER
    # =====================================================

    def draw_player(self):

        x = self.player_x
        y = self.player_y

        # Engine flame
        self.canvas.create_polygon(
            x - 8, y + 25,
            x + 8, y + 25,
            x, y + 45,
            fill="#ff9d00",
            outline=""
        )

        self.canvas.create_polygon(
            x - 5, y + 25,
            x + 5, y + 25,
            x, y + 38,
            fill="#ffff00",
            outline=""
        )

        # Ship
        self.canvas.create_polygon(
            x, y - 30,
            x - 25, y + 25,
            x - 8, y + 18,
            x, y + 28,
            x + 8, y + 18,
            x + 25, y + 25,
            fill="#42e8ff",
            outline="#ffffff",
            width=2
        )

        # Cockpit
        self.canvas.create_oval(
            x - 7,
            y - 12,
            x + 7,
            y + 3,
            fill="#ffffff",
            outline=""
        )

        # Wings
        self.canvas.create_line(
            x - 10, y + 5,
            x - 30, y + 22,
            fill="#ff4fd8",
            width=5
        )

        self.canvas.create_line(
            x + 10, y + 5,
            x + 30, y + 22,
            fill="#ff4fd8",
            width=5
        )

    # =====================================================
    # ENEMY DRAW
    # =====================================================

    def draw_enemy(self, enemy):

        x = enemy["x"]
        y = enemy["y"]
        s = enemy["size"]

        # Body
        self.canvas.create_oval(
            x - s,
            y - s,
            x + s,
            y + s,
            fill=enemy["color"],
            outline="#ffffff",
            width=1
        )

        # Eyes
        self.canvas.create_oval(
            x - 9,
            y - 6,
            x - 3,
            y,
            fill="#ffffff",
            outline=""
        )

        self.canvas.create_oval(
            x + 3,
            y - 6,
            x + 9,
            y,
            fill="#ffffff",
            outline=""
        )

        # Mouth
        self.canvas.create_arc(
            x - 8,
            y - 2,
            x + 8,
            y + 10,
            start=0,
            extent=-180,
            style=tk.ARC,
            outline="#ffffff",
            width=2
        )

        # Wings
        self.canvas.create_polygon(
            x - s,
            y + 5,
            x - s - 12,
            y + 15,
            x - s + 2,
            y - 3,
            fill=enemy["color"],
            outline=""
        )

        self.canvas.create_polygon(
            x + s,
            y + 5,
            x + s + 12,
            y + 15,
            x + s - 2,
            y - 3,
            fill=enemy["color"],
            outline=""
        )

    # =====================================================
    # BULLETS
    # =====================================================

    def shoot(self):

        now = self.root.tk.call("after", "info")

        bullet = {
            "x": self.player_x,
            "y": self.player_y - 35
        }

        self.bullets.append(bullet)

    def draw_bullet(self, bullet):

        x = bullet["x"]
        y = bullet["y"]

        self.canvas.create_rectangle(
            x - 3,
            y - 12,
            x + 3,
            y + 12,
            fill="#ffff00",
            outline=""
        )

        self.canvas.create_oval(
            x - 5,
            y - 5,
            x + 5,
            y + 5,
            fill="#ffffff",
            outline=""
        )

    # =====================================================
    # PARTICLES
    # =====================================================

    def create_explosion(self, x, y):

        for _ in range(18):

            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(1, 5)

            self.particles.append({
                "x": x,
                "y": y,
                "dx": math.cos(angle) * speed,
                "dy": math.sin(angle) * speed,
                "life": random.randint(15, 30),
                "color": random.choice([
                    "#ff3b30",
                    "#ffcc00",
                    "#ff6b00",
                    "#ffffff"
                ])
            })

    def draw_particles(self):

        new_particles = []

        for p in self.particles:

            p["x"] += p["dx"]
            p["y"] += p["dy"]
            p["life"] -= 1

            if p["life"] > 0:

                size = max(1, p["life"] // 5)

                self.canvas.create_oval(
                    p["x"] - size,
                    p["y"] - size,
                    p["x"] + size,
                    p["y"] + size,
                    fill=p["color"],
                    outline=""
                )

                new_particles.append(p)

        self.particles = new_particles

    # =====================================================
    # HUD
    # =====================================================

    def draw_hud(self):

        self.canvas.create_rectangle(
            0,
            0,
            WIDTH,
            55,
            fill="#0b1026",
            outline=""
        )

        self.canvas.create_text(
            25,
            27,
            text=f"SCORE  {self.score}",
            fill="#62f5ff",
            anchor="w",
            font=("Arial", 16, "bold")
        )

        self.canvas.create_text(
            WIDTH // 2,
            27,
            text=f"LEVEL  {self.level}",
            fill="#ffff00",
            font=("Arial", 16, "bold")
        )

        hearts = "❤ " * self.lives

        self.canvas.create_text(
            WIDTH - 25,
            27,
            text=hearts,
            fill="#ff3864",
            anchor="e",
            font=("Arial", 18, "bold")
        )

    # =====================================================
    # KEYBOARD
    # =====================================================

    def key_down(self, event):

        self.keys.add(event.keysym.lower())

        if event.keysym == "Return":

            if not self.running:
                self.start_game()

        if event.keysym == "space":

            if self.running:
                self.shoot()

        if event.keysym == "Escape":

            self.root.destroy()

    def key_up(self, event):

        self.keys.discard(event.keysym.lower())

    # =====================================================
    # UPDATE PLAYER
    # =====================================================

    def update_player(self):

        if "left" in self.keys or "a" in self.keys:
            self.player_x -= PLAYER_SPEED

        if "right" in self.keys or "d" in self.keys:
            self.player_x += PLAYER_SPEED

        self.player_x = max(
            35,
            min(WIDTH - 35, self.player_x)
        )

    # =====================================================
    # UPDATE BULLETS
    # =====================================================

    def update_bullets(self):

        for bullet in self.bullets[:]:

            bullet["y"] -= BULLET_SPEED

            if bullet["y"] < 0:

                self.bullets.remove(bullet)

    # =====================================================
    # UPDATE ENEMIES
    # =====================================================

    def update_enemies(self):

        for enemy in self.enemies[:]:

            enemy["y"] += enemy["speed"]

            # Enemy reaches player area
            if enemy["y"] > HEIGHT + 30:

                self.enemies.remove(enemy)

                self.lives -= 1

                if self.lives <= 0:
                    self.end_game()

    # =====================================================
    # COLLISION
    # =====================================================

    def collision(self, bullet, enemy):

        distance = math.sqrt(
            (bullet["x"] - enemy["x"]) ** 2 +
            (bullet["y"] - enemy["y"]) ** 2
        )

        return distance < enemy["size"] + 10

    def player_collision(self, enemy):

        distance = math.sqrt(
            (self.player_x - enemy["x"]) ** 2 +
            (self.player_y - enemy["y"]) ** 2
        )

        return distance < enemy["size"] + 28

    # =====================================================
    # CHECK COLLISIONS
    # =====================================================

    def check_collisions(self):

        # Bullet vs enemy
        for bullet in self.bullets[:]:

            for enemy in self.enemies[:]:

                if self.collision(bullet, enemy):

                    if bullet in self.bullets:
                        self.bullets.remove(bullet)

                    if enemy in self.enemies:
                        self.enemies.remove(enemy)

                    self.score += 10

                    self.create_explosion(
                        enemy["x"],
                        enemy["y"]
                    )

                    break

        # Player vs enemy
        for enemy in self.enemies[:]:

            if self.player_collision(enemy):

                if enemy in self.enemies:
                    self.enemies.remove(enemy)

                self.lives -= 1

                self.create_explosion(
                    enemy["x"],
                    enemy["y"]
                )

                if self.lives <= 0:
                    self.end_game()

    # =====================================================
    # LEVEL SYSTEM
    # =====================================================

    def update_level(self):

        new_level = min(10, self.score // 100 + 1)

        if new_level > self.level:

            self.level = new_level

            target_enemies = min(
                MAX_ENEMIES,
                START_ENEMIES + self.level
            )

            while len(self.enemies) < target_enemies:

                self.create_enemies(1)

    # =====================================================
    # GAME OVER
    # =====================================================

    def end_game(self):

        self.running = False
        self.game_over = True

        if self.score > self.high_score:
            self.high_score = self.score

    # =====================================================
    # DRAW GAME OVER
    # =====================================================

    def draw_game_over(self):

        self.canvas.create_rectangle(
            150,
            170,
            WIDTH - 150,
            500,
            fill="#090d20",
            outline="#ff3864",
            width=3
        )

        self.canvas.create_text(
            WIDTH // 2,
            240,
            text="GAME OVER",
            fill="#ff3864",
            font=("Arial", 42, "bold")
        )

        self.canvas.create_text(
            WIDTH // 2,
            310,
            text=f"SCORE : {self.score}",
            fill="#62f5ff",
            font=("Arial", 22, "bold")
        )

        self.canvas.create_text(
            WIDTH // 2,
            350,
            text=f"HIGH SCORE : {self.high_score}",
            fill="#ffff00",
            font=("Arial", 18, "bold")
        )

        self.canvas.create_text(
            WIDTH // 2,
            415,
            text="PRESS ENTER TO PLAY AGAIN",
            fill="white",
            font=("Arial", 18, "bold")
        )

        self.canvas.create_text(
            WIDTH // 2,
            450,
            text="ESC = EXIT",
            fill="#8888aa",
            font=("Arial", 13)
        )

    # =====================================================
    # MAIN GAME LOOP
    # =====================================================

    def game_loop(self):

        self.canvas.delete("all")

        self.draw_stars()

        if self.running:

            self.update_player()
            self.update_bullets()
            self.update_enemies()

            self.check_collisions()
            self.update_level()

            # Spawn enemies
            target = min(
                MAX_ENEMIES,
                START_ENEMIES + self.level
            )

            while len(self.enemies) < target:
                self.create_enemies(1)

            self.draw_hud()

            for enemy in self.enemies:
                self.draw_enemy(enemy)

            for bullet in self.bullets:
                self.draw_bullet(bullet)

            self.draw_player()

            self.draw_particles()

        elif self.game_over:

            self.draw_stars()
            self.draw_game_over()

        else:

            self.show_menu()

        self.root.after(30, self.game_loop)


# =========================================================
# START
# =========================================================

root = tk.Tk()

game = SpaceShooter(root)

root.mainloop()
