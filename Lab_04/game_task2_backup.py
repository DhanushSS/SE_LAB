import pygame
import random
import math
import time

WIDTH, HEIGHT = 800, 560
FPS = 60
BG = (30, 35, 25)


class Zombie:
    SPEED = 1.5

    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 30, 30)
        self.color = (60, 140, 60)
        self.hp = 3
        self.wobble = random.uniform(0, 6.28)
        self.frame = 0

    def update(self, player_pos):
        px, py = player_pos
        cx, cy = self.rect.center
        dx, dy = px - cx, py - cy
        dist = (dx ** 2 + dy ** 2) ** 0.5

        if dist:
            self.rect.x += int(dx / dist * self.SPEED)
            self.rect.y += int(dy / dist * self.SPEED)

        self.frame += 1

    def hit(self):
        self.hp -= 1
        return self.hp <= 0

    def draw(self, screen):
        wobble_y = int(math.sin(self.frame * 0.2) * 3)
        draw_rect = self.rect.move(0, wobble_y)

        pygame.draw.rect(
            screen,
            self.color,
            draw_rect,
            border_radius=5
        )

        for ex in [draw_rect.x + 6, draw_rect.x + 18]:
            pygame.draw.circle(
                screen,
                (200, 40, 40),
                (ex, draw_rect.y + 10),
                4
            )


def spawn_zombie(width, height, player_rect, margin=120):
    while True:
        x = random.randint(0, width - 30)
        y = random.randint(0, height - 30)

        rect = pygame.Rect(x, y, 30, 30)

        if not rect.colliderect(
            player_rect.inflate(margin, margin)
        ):
            return Zombie(x, y)


SPEED = 4


class Player:
    # =========================
    # TASK 1: HEALTH
    # =========================
    MAX_HP = 100
    DAMAGE_PER_HIT = 10

    # =========================
    # TASK 2: AMMO
    # =========================
    MAX_AMMO = 12
    RELOAD_TIME = 2.0

    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 32, 32)
        self.color = (60, 160, 220)

        # Bullets
        self.bullets = []

        # Shooting cooldown
        self.shoot_cooldown = 0

        # =========================
        # TASK 1: HEALTH SYSTEM
        # =========================
        self.hp = self.MAX_HP
        self.damage_cooldown = 0

        # =========================
        # TASK 2: AMMO SYSTEM
        # =========================
        self.ammo = self.MAX_AMMO
        self.reloading = False
        self.reload_start_time = 0

    # =========================
    # TASK 1: TAKE DAMAGE
    # =========================
    def take_damage(self, damage):
        if self.damage_cooldown > 0:
            return False

        self.hp = max(0, self.hp - damage)

        # 0.5 second damage cooldown
        self.damage_cooldown = FPS // 2

        return self.hp <= 0

    # =========================
    # TASK 2: START RELOAD
    # =========================
    def start_reload(self):
        if self.reloading:
            return

        if self.ammo >= self.MAX_AMMO:
            return

        self.reloading = True
        self.reload_start_time = time.time()

    # =========================
    # TASK 2: UPDATE RELOAD
    # =========================
    def update_reload(self):
        if not self.reloading:
            return

        elapsed = time.time() - self.reload_start_time

        if elapsed >= self.RELOAD_TIME:
            self.ammo = self.MAX_AMMO
            self.reloading = False

    def move(self, keys, width, height):
        dx = dy = 0

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy = -SPEED

        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy = SPEED

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx = -SPEED

        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx = SPEED

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

    # =========================
    # TASK 2: SHOOT
    # =========================
    def shoot(self, target_pos):

        # Cannot shoot while reloading
        if self.reloading:
            return

        # Cannot shoot with no ammo
        if self.ammo <= 0:
            self.start_reload()
            return

        # Shooting cooldown
        if self.shoot_cooldown > 0:
            return

        cx, cy = self.rect.center
        tx, ty = target_pos

        dx, dy = tx - cx, ty - cy
        dist = (dx ** 2 + dy ** 2) ** 0.5

        if dist == 0:
            return

        vx, vy = dx / dist * 10, dy / dist * 10

        self.bullets.append(
            [cx - 4, cy - 4, vx, vy]
        )

        # =========================
        # TASK 2: CONSUME AMMO
        # =========================
        self.ammo -= 1

        self.shoot_cooldown = 15

        # Automatically reload at 0
        if self.ammo == 0:
            self.start_reload()

    def update_bullets(self, width, height):
        live = []

        for b in self.bullets:
            b[0] += b[2]
            b[1] += b[3]

            if (
                0 <= b[0] <= width
                and 0 <= b[1] <= height
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
                (int(b[0]), int(b[1])),
                5
            )


class GameEngine:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode(
            (WIDTH, HEIGHT)
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

    def reset(self):
        self.player = Player(
            WIDTH // 2,
            HEIGHT // 2
        )

        self.zombies = [
            spawn_zombie(
                WIDTH,
                HEIGHT,
                self.player.rect
            )
            for _ in range(4)
        ]

        self.score = 0
        self.wave = 1
        self.kills = 0
        self.kills_to_next = 8

        self.game_over = False

        self.start_time = time.time()

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
                event.type == pygame.MOUSEBUTTONDOWN
                and not self.game_over
            ):
                self.player.shoot(event.pos)

        return True

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
            time.time() - self.start_time
        )

        # =========================
        # ZOMBIE MOVEMENT + DAMAGE
        # =========================
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

        # =========================
        # BULLET COLLISION
        # =========================
        dead = []

        for z in self.zombies:

            for b in self.player.bullets[:]:

                bx, by = int(b[0]), int(b[1])

                if z.rect.collidepoint(
                    bx,
                    by
                ):

                    if z.hit():
                        dead.append(z)

                    if b in self.player.bullets:
                        self.player.bullets.remove(b)

        # Remove dead zombies
        for z in dead:

            if z in self.zombies:

                self.zombies.remove(z)

                self.kills += 1
                self.score += 10

        # =========================
        # WAVE SYSTEM
        # =========================
        if self.kills >= self.kills_to_next:

            self.kills = 0

            self.wave += 1

            self.kills_to_next = (
                8 + self.wave * 2
            )

            for _ in range(self.wave + 3):

                self.zombies.append(
                    spawn_zombie(
                        WIDTH,
                        HEIGHT,
                        self.player.rect
                    )
                )

    def draw(self):
        self.screen.fill(BG)

        # Background grid
        for x in range(0, WIDTH, 60):
            pygame.draw.line(
                self.screen,
                (40, 45, 35),
                (x, 0),
                (x, HEIGHT),
                1
            )

        for y in range(0, HEIGHT, 60):
            pygame.draw.line(
                self.screen,
                (40, 45, 35),
                (0, y),
                (WIDTH, y),
                1
            )

        # Draw zombies
        for z in self.zombies:
            z.draw(self.screen)

        # Draw player
        self.player.draw(self.screen)

        # =========================
        # HUD
        # =========================
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
            f"HP: {self.player.hp}/{self.player.MAX_HP}  "
            f"Ammo: {self.player.ammo}/{self.player.MAX_AMMO}  "
            f"Wave: {self.wave}  "
            f"Score: {self.score}  "
            f"Kills: {self.kills}/{self.kills_to_next}",
            True,
            (160, 220, 120)
        )

        self.screen.blit(
            hud,
            (8, 8)
        )

        # =========================
        # HEALTH BAR
        # =========================
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

        # =========================
        # RELOADING MESSAGE
        # =========================
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
                    - reload_text.get_width() // 2,
                    HEIGHT - 45
                )
            )

        # =========================
        # GAME OVER
        # =========================
        if self.game_over:

            ov = pygame.Surface(
                (WIDTH, HEIGHT),
                pygame.SRCALPHA
            )

            ov.fill(
                (0, 0, 0, 160)
            )

            self.screen.blit(
                ov,
                (0, 0)
            )

            m = self.big_font.render(
                "DEVOURED!",
                True,
                (180, 40, 40)
            )

            s = self.font.render(
                f"Wave {self.wave} | "
                f"Score {self.score} | "
                f"Press R",
                True,
                (200, 200, 200)
            )

            self.screen.blit(
                m,
                (
                    WIDTH // 2
                    - m.get_width() // 2,
                    HEIGHT // 2 - 40
                )
            )

            self.screen.blit(
                s,
                (
                    WIDTH // 2
                    - s.get_width() // 2,
                    HEIGHT // 2 + 20
                )
            )

        pygame.display.flip()

    def run(self):
        running = True

        while running:

            running = self.handle_events()

            self.update()

            self.draw()

            self.clock.tick(FPS)

        pygame.quit()


if __name__ == "__main__":
    engine = GameEngine()
    engine.run()