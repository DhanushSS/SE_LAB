import pygame
import random
import math
import time

WIDTH, HEIGHT = 800, 560
FPS = 60
BG = (30, 35, 25)


# ============================================================
# BASE ZOMBIE
# ============================================================

class Zombie:
    SPEED = 1.5
    HP = 3
    SIZE = 30
    COLOR = (60, 140, 60)

    def __init__(self, x, y):
        self.rect = pygame.Rect(
            x, y,
            self.SIZE,
            self.SIZE
        )
        self.color = self.COLOR
        self.hp = self.HP
        self.frame = 0

    def update(self, player_pos):
        px, py = player_pos
        cx, cy = self.rect.center

        dx = px - cx
        dy = py - cy

        dist = (dx ** 2 + dy ** 2) ** 0.5

        if dist:
            self.rect.x += int(dx / dist * self.SPEED)
            self.rect.y += int(dy / dist * self.SPEED)

        self.frame += 1

    def hit(self):
        self.hp -= 1
        return self.hp <= 0

    def draw(self, screen):
        wobble_y = int(
            math.sin(self.frame * 0.2) * 3
        )

        draw_rect = self.rect.move(
            0,
            wobble_y
        )

        pygame.draw.rect(
            screen,
            self.color,
            draw_rect,
            border_radius=5
        )

        eye_offset = max(
            5,
            self.SIZE // 5
        )

        eye_size = max(
            3,
            self.SIZE // 8
        )

        pygame.draw.circle(
            screen,
            (200, 40, 40),
            (
                draw_rect.x + eye_offset,
                draw_rect.y + eye_offset
            ),
            eye_size
        )

        pygame.draw.circle(
            screen,
            (200, 40, 40),
            (
                draw_rect.right - eye_offset,
                draw_rect.y + eye_offset
            ),
            eye_size
        )


# ============================================================
# TASK 4: FAST ZOMBIE
# ============================================================

class FastZombie(Zombie):
    SPEED = 3.5
    HP = 1
    SIZE = 20
    COLOR = (220, 200, 50)

    def draw(self, screen):
        wobble_y = int(
            math.sin(self.frame * 0.3) * 2
        )

        draw_rect = self.rect.move(
            0,
            wobble_y
        )

        pygame.draw.rect(
            screen,
            self.color,
            draw_rect,
            border_radius=5
        )

        # Fast zombie eyes
        pygame.draw.circle(
            screen,
            (180, 30, 30),
            (
                draw_rect.x + 5,
                draw_rect.y + 6
            ),
            3
        )

        pygame.draw.circle(
            screen,
            (180, 30, 30),
            (
                draw_rect.right - 5,
                draw_rect.y + 6
            ),
            3
        )


# ============================================================
# TASK 4: TANK ZOMBIE
# ============================================================

class TankZombie(Zombie):
    SPEED = 0.8
    HP = 6
    SIZE = 45
    COLOR = (110, 60, 150)

    def draw(self, screen):
        wobble_y = int(
            math.sin(self.frame * 0.12) * 2
        )

        draw_rect = self.rect.move(
            0,
            wobble_y
        )

        pygame.draw.rect(
            screen,
            self.color,
            draw_rect,
            border_radius=7
        )

        # Tank eyes
        pygame.draw.circle(
            screen,
            (255, 70, 70),
            (
                draw_rect.x + 10,
                draw_rect.y + 12
            ),
            5
        )

        pygame.draw.circle(
            screen,
            (255, 70, 70),
            (
                draw_rect.right - 10,
                draw_rect.y + 12
            ),
            5
        )

        # HP indicator
        hp_width = int(
            draw_rect.width
            * self.hp
            / self.HP
        )

        pygame.draw.rect(
            screen,
            (40, 40, 40),
            (
                draw_rect.x,
                draw_rect.y - 7,
                draw_rect.width,
                4
            )
        )

        pygame.draw.rect(
            screen,
            (220, 70, 70),
            (
                draw_rect.x,
                draw_rect.y - 7,
                hp_width,
                4
            )
        )


# ============================================================
# ZOMBIE SPAWNING
# ============================================================

def spawn_zombie(
    width,
    height,
    player_rect,
    margin=120,
    zombie_type=None
):
    while True:

        x = random.randint(
            0,
            width - 45
        )

        y = random.randint(
            0,
            height - 45
        )

        # Select zombie type
        if zombie_type == "fast":
            zombie_class = FastZombie

        elif zombie_type == "tank":
            zombie_class = TankZombie

        else:
            zombie_class = Zombie

        rect = pygame.Rect(
            x,
            y,
            zombie_class.SIZE,
            zombie_class.SIZE
        )

        if not rect.colliderect(
            player_rect.inflate(
                margin,
                margin
            )
        ):
            return zombie_class(
                x,
                y
            )


def spawn_random_zombie(
    width,
    height,
    player_rect
):
    # Mix all zombie types together.
    roll = random.random()

    if roll < 0.20:
        zombie_type = "fast"

    elif roll < 0.35:
        zombie_type = "tank"

    else:
        zombie_type = "normal"

    return spawn_zombie(
        width,
        height,
        player_rect,
        zombie_type=zombie_type
    )


# ============================================================
# TASK 3: EXPLOSIVE BARREL
# ============================================================

class Barrel:

    EXPLOSION_RADIUS = 100

    def __init__(self, x, y):
        self.rect = pygame.Rect(
            x,
            y,
            32,
            40
        )

    def draw(self, screen):

        pygame.draw.rect(
            screen,
            (150, 75, 25),
            self.rect,
            border_radius=5
        )

        pygame.draw.line(
            screen,
            (40, 40, 40),
            (
                self.rect.x,
                self.rect.y + 10
            ),
            (
                self.rect.right,
                self.rect.y + 10
            ),
            4
        )

        pygame.draw.line(
            screen,
            (40, 40, 40),
            (
                self.rect.x,
                self.rect.bottom - 10
            ),
            (
                self.rect.right,
                self.rect.bottom - 10
            ),
            4
        )

        pygame.draw.circle(
            screen,
            (240, 210, 40),
            self.rect.center,
            7
        )


# ============================================================
# PLAYER
# ============================================================

class Player:

    # Task 1
    MAX_HP = 100
    DAMAGE_PER_HIT = 10

    # Task 2
    MAX_AMMO = 12
    RELOAD_TIME = 2.0

    def __init__(self, x, y):

        self.rect = pygame.Rect(
            x,
            y,
            32,
            32
        )

        self.color = (60, 160, 220)

        self.bullets = []

        self.shoot_cooldown = 0

        # Health
        self.hp = self.MAX_HP
        self.damage_cooldown = 0

        # Ammo
        self.ammo = self.MAX_AMMO
        self.reloading = False
        self.reload_start_time = 0

    # --------------------------------------------------------
    # TASK 1
    # --------------------------------------------------------

    def take_damage(self, damage):

        if self.damage_cooldown > 0:
            return False

        self.hp = max(
            0,
            self.hp - damage
        )

        self.damage_cooldown = FPS // 2

        return self.hp <= 0

    # --------------------------------------------------------
    # TASK 2
    # --------------------------------------------------------

    def start_reload(self):

        if self.reloading:
            return

        if self.ammo >= self.MAX_AMMO:
            return

        self.reloading = True
        self.reload_start_time = time.time()

    def update_reload(self):

        if not self.reloading:
            return

        elapsed = (
            time.time()
            - self.reload_start_time
        )

        if elapsed >= self.RELOAD_TIME:

            self.ammo = self.MAX_AMMO
            self.reloading = False

    def move(
        self,
        keys,
        width,
        height
    ):

        dx = 0
        dy = 0

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy = -4

        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy = 4

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx = -4

        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx = 4

        self.rect.x = max(
            0,
            min(
                width - self.rect.width,
                self.rect.x + dx
            )
        )

        self.rect.y = max(
            0,
            min(
                height - self.rect.height,
                self.rect.y + dy
            )
        )

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

        if self.damage_cooldown > 0:
            self.damage_cooldown -= 1

        self.update_reload()

    def shoot(self, target_pos):

        if self.reloading:
            return

        if self.ammo <= 0:

            self.start_reload()
            return

        if self.shoot_cooldown > 0:
            return

        cx, cy = self.rect.center

        tx, ty = target_pos

        dx = tx - cx
        dy = ty - cy

        dist = (
            dx ** 2
            + dy ** 2
        ) ** 0.5

        if dist == 0:
            return

        vx = dx / dist * 10
        vy = dy / dist * 10

        self.bullets.append(
            [
                cx - 4,
                cy - 4,
                vx,
                vy
            ]
        )

        self.ammo -= 1

        self.shoot_cooldown = 15

        if self.ammo == 0:
            self.start_reload()

    def update_bullets(
        self,
        width,
        height
    ):

        live = []

        for b in self.bullets:

            b[0] += b[2]
            b[1] += b[3]

            if (
                0 <= b[0] <= width
                and
                0 <= b[1] <= height
            ):
                live.append(b)

        self.bullets = live

    def draw(self, screen):

        pygame.draw.rect(
            screen,
            self.color,
            self.rect,
            border_radius=6
        )

        for b in self.bullets:

            pygame.draw.circle(
                screen,
                (255, 220, 60),
                (
                    int(b[0]),
                    int(b[1])
                ),
                5
            )


# ============================================================
# GAME ENGINE
# ============================================================

class GameEngine:

    def __init__(self):

        pygame.init()

        self.screen = pygame.display.set_mode(
            (
                WIDTH,
                HEIGHT
            )
        )

        pygame.display.set_caption(
            "Zombie Escape"
        )

        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont(
            "monospace",
            24
        )

        self.big_font = pygame.font.SysFont(
            "monospace",
            44,
            bold=True
        )

        self.reset()

    # --------------------------------------------------------
    # RESET
    # --------------------------------------------------------

    def reset(self):

        self.player = Player(
            WIDTH // 2,
            HEIGHT // 2
        )

        # Initial mixed zombies
        self.zombies = [
            spawn_random_zombie(
                WIDTH,
                HEIGHT,
                self.player.rect
            )
            for _ in range(4)
        ]

        # Task 3 barrels
        self.barrels = [

            Barrel(100, 100),

            Barrel(650, 100),

            Barrel(100, 420),

            Barrel(650, 420)
        ]

        self.score = 0

        self.wave = 1

        self.kills = 0

        self.kills_to_next = 8

        self.game_over = False

        self.start_time = time.time()

    # --------------------------------------------------------
    # EVENTS
    # --------------------------------------------------------

    def handle_events(self):

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return False

            if (
                event.type == pygame.KEYDOWN
                and event.key == pygame.K_r
            ):
                self.reset()

            if (
                event.type
                == pygame.MOUSEBUTTONDOWN
                and not self.game_over
            ):
                self.player.shoot(
                    event.pos
                )

        return True

    # --------------------------------------------------------
    # TASK 3: BARREL EXPLOSION
    # --------------------------------------------------------

    def explode_barrel(
        self,
        barrel
    ):

        explosion_x, explosion_y = (
            barrel.rect.center
        )

        dead = []

        for z in self.zombies:

            zombie_x, zombie_y = (
                z.rect.center
            )

            distance = math.hypot(
                zombie_x - explosion_x,
                zombie_y - explosion_y
            )

            if (
                distance
                <= Barrel.EXPLOSION_RADIUS
            ):
                dead.append(z)

        for z in dead:

            if z in self.zombies:

                self.zombies.remove(z)

                self.kills += 1

                self.score += 10

        if barrel in self.barrels:

            self.barrels.remove(
                barrel
            )

    # --------------------------------------------------------
    # UPDATE
    # --------------------------------------------------------

    def update(self):

        if self.game_over:
            return

        keys = pygame.key.get_pressed()

        self.player.move(
            keys,
            WIDTH,
            HEIGHT
        )

        self.player.update_bullets(
            WIDTH,
            HEIGHT
        )

        self.score = int(
            time.time()
            - self.start_time
        )

        # ----------------------------------------------------
        # ZOMBIE MOVEMENT
        # ----------------------------------------------------

        for z in self.zombies:

            z.update(
                self.player.rect.center
            )

            if z.rect.colliderect(
                self.player.rect
            ):

                if self.player.take_damage(
                    Player.DAMAGE_PER_HIT
                ):
                    self.game_over = True

        # ----------------------------------------------------
        # TASK 3: BULLET -> BARREL
        # ----------------------------------------------------

        exploded_barrel = None

        for barrel in self.barrels:

            for b in self.player.bullets[:]:

                bx = int(b[0])
                by = int(b[1])

                if barrel.rect.collidepoint(
                    bx,
                    by
                ):

                    self.player.bullets.remove(
                        b
                    )

                    exploded_barrel = barrel

                    break

            if exploded_barrel:
                break

        if exploded_barrel:

            self.explode_barrel(
                exploded_barrel
            )

        # ----------------------------------------------------
        # BULLET -> ZOMBIE
        # ----------------------------------------------------

        dead = []

        for z in self.zombies:

            for b in self.player.bullets[:]:

                bx = int(b[0])
                by = int(b[1])

                if z.rect.collidepoint(
                    bx,
                    by
                ):

                    if z.hit():
                        dead.append(z)

                    if b in self.player.bullets:

                        self.player.bullets.remove(
                            b
                        )

        for z in dead:

            if z in self.zombies:

                self.zombies.remove(z)

                self.kills += 1

                self.score += 10

        # ----------------------------------------------------
        # WAVE SYSTEM
        # ----------------------------------------------------

        if self.kills >= self.kills_to_next:

            self.kills = 0

            self.wave += 1

            self.kills_to_next = (
                8 + self.wave * 2
            )

            # Spawn a mixed group
            for _ in range(
                self.wave + 3
            ):

                self.zombies.append(
                    spawn_random_zombie(
                        WIDTH,
                        HEIGHT,
                        self.player.rect
                    )
                )

    # --------------------------------------------------------
    # DRAW
    # --------------------------------------------------------

    def draw(self):

        self.screen.fill(BG)

        # Background grid
        for x in range(
            0,
            WIDTH,
            60
        ):

            pygame.draw.line(
                self.screen,
                (40, 45, 35),
                (x, 0),
                (x, HEIGHT),
                1
            )

        for y in range(
            0,
            HEIGHT,
            60
        ):

            pygame.draw.line(
                self.screen,
                (40, 45, 35),
                (0, y),
                (WIDTH, y),
                1
            )

        # ----------------------------------------------------
        # BARRELS
        # ----------------------------------------------------

        for barrel in self.barrels:
            barrel.draw(
                self.screen
            )

        # ----------------------------------------------------
        # ZOMBIES
        # ----------------------------------------------------

        for z in self.zombies:
            z.draw(
                self.screen
            )

        # ----------------------------------------------------
        # PLAYER
        # ----------------------------------------------------

        self.player.draw(
            self.screen
        )

        # ----------------------------------------------------
        # HUD
        # ----------------------------------------------------

        hud_bg = pygame.Rect(
            0,
            0,
            WIDTH,
            40
        )

        pygame.draw.rect(
            self.screen,
            (15, 20, 15),
            hud_bg
        )

        hud = self.font.render(
            f"HP: {self.player.hp}/"
            f"{self.player.MAX_HP}  "
            f"Ammo: {self.player.ammo}/"
            f"{self.player.MAX_AMMO}  "
            f"Wave: {self.wave}  "
            f"Score: {self.score}  "
            f"Kills: {self.kills}/"
            f"{self.kills_to_next}",
            True,
            (160, 220, 120)
        )

        self.screen.blit(
            hud,
            (8, 8)
        )

        # ----------------------------------------------------
        # HEALTH BAR
        # ----------------------------------------------------

        bar_x = 8
        bar_y = 44
        bar_width = 220
        bar_height = 18

        pygame.draw.rect(
            self.screen,
            (80, 20, 20),
            (
                bar_x,
                bar_y,
                bar_width,
                bar_height
            )
        )

        health_width = int(
            bar_width
            * self.player.hp
            / self.player.MAX_HP
        )

        pygame.draw.rect(
            self.screen,
            (40, 200, 60),
            (
                bar_x,
                bar_y,
                health_width,
                bar_height
            )
        )

        pygame.draw.rect(
            self.screen,
            (220, 220, 220),
            (
                bar_x,
                bar_y,
                bar_width,
                bar_height
            ),
            2
        )

        # ----------------------------------------------------
        # RELOADING
        # ----------------------------------------------------

        if self.player.reloading:

            reload_text = self.font.render(
                "RELOADING...",
                True,
                (255, 220, 60)
            )

            self.screen.blit(
                reload_text,
                (
                    WIDTH // 2
                    - reload_text.get_width()
                    // 2,
                    HEIGHT - 45
                )
            )

        # ----------------------------------------------------
        # GAME OVER
        # ----------------------------------------------------

        if self.game_over:

            overlay = pygame.Surface(
                (
                    WIDTH,
                    HEIGHT
                ),
                pygame.SRCALPHA
            )

            overlay.fill(
                (0, 0, 0, 160)
            )

            self.screen.blit(
                overlay,
                (0, 0)
            )

            message = (
                self.big_font.render(
                    "DEVOURED!",
                    True,
                    (180, 40, 40)
                )
            )

            score_message = (
                self.font.render(
                    f"Wave {self.wave} | "
                    f"Score {self.score} | "
                    f"Press R",
                    True,
                    (200, 200, 200)
                )
            )

            self.screen.blit(
                message,
                (
                    WIDTH // 2
                    - message.get_width()
                    // 2,
                    HEIGHT // 2 - 40
                )
            )

            self.screen.blit(
                score_message,
                (
                    WIDTH // 2
                    - score_message.get_width()
                    // 2,
                    HEIGHT // 2 + 20
                )
            )

        pygame.display.flip()

    # --------------------------------------------------------
    # RUN
    # --------------------------------------------------------

    def run(self):

        running = True

        while running:

            running = (
                self.handle_events()
            )

            self.update()

            self.draw()

            self.clock.tick(
                FPS
            )

        pygame.quit()


if __name__ == "__main__":

    engine = GameEngine()

    engine.run()