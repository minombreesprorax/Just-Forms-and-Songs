from typing import Tuple
import modules.utils as utils
import modules.Keyhole as keyhole
import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, speed: int, kh: keyhole.Kh) -> None:
        super().__init__()
        self.original_image = pygame.Surface((20, 20))  # Placeholder for player appearance
        self.original_image.fill("#00FFFF")
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = speed
        self.dash_speed = speed * 3
        self.dash_duration = 20
        self.dash_cooldown = 2
        self.dash_timer = 0
        self.cooldown_timer = 0
        self.in_dash = False
        self.keyhole = kh
        self.hp = 5
        self.dash_direction = (0, 0)
        self.i_frames = 60  # Invincibility duration
        self.i_count = 0  # Countdown for invincibility
        self.keyhole.bind_key_down(pygame.K_SPACE, self.start_dash)

    def update(self, screen_size: Tuple[int, int]) -> None:
        """Moves the player and handles dashing."""
        if self.in_dash:
            self.perform_dash()

        self.handle_movement(screen_size)

        # Cooldown logic
        if self.cooldown_timer > 0:
            self.cooldown_timer -= 1

        # Update invincibility countdown
        if self.i_count > 0:
            self.i_count -= 1

    def handle_movement(self, screen_size: Tuple[int, int]) -> None:
        """Handle normal movement logic and update direction for dash."""
        my = 0
        mx = 0
        if self.keyhole.is_pressed(pygame.K_w):
            my -= 1 
        if self.keyhole.is_pressed(pygame.K_a):
            mx -= 1
        if self.keyhole.is_pressed(pygame.K_s):
            my += 1
        if self.keyhole.is_pressed(pygame.K_d):
            mx += 1

        # Normalize and apply speed
        if mx != 0 or my != 0:
            nx, ny = utils.normalize((mx, my))
            if self.in_dash:
                self.dash_direction = (mx, my)  # Update dash direction if dashing
            else:
                self.dash_direction = (mx, my)
                self.rect.x += nx * self.speed
                self.rect.y += ny * self.speed
                self.squish(mx, my)
        else:
            # If no movement keys are pressed and not dashing, reset image
            if not self.in_dash:
                self.dash_direction = (0, 0)
                self.image = self.original_image
                self.rect = self.image.get_rect(center=self.rect.center)

        # Clamp position
        self.rect.topleft = utils.clamp2DBox(self.rect.topleft, self.rect.size, screen_size)
        
    def start_dash(self):
        """Initiates the dash and sets timers."""
        if not self.in_dash and self.cooldown_timer <= 0:
            self.in_dash = True
            self.dash_timer = self.dash_duration
            self.cooldown_timer = self.dash_cooldown + self.dash_duration

            # If no movement direction, default to right
            if self.dash_direction == (0, 0):
                self.dash_direction = (1, 0)  # Default to right

    def perform_dash(self):
        """Moves the player in the current direction during a dash."""
        mx, my = self.dash_direction  # Use stored dash direction
        nx, ny = utils.normalize((mx, my))
        self.rect.x += nx * self.dash_speed
        self.rect.y += ny * self.dash_speed
        
        self.squish(mx, my)  # Change appearance during dash
        
        self.dash_timer -= 1
        if self.dash_timer <= 0:
            self.in_dash = False  # End dash

        # Ensure the player stays within the screen bounds during dash
        screen_size = (pygame.display.get_surface().get_size())
        self.rect.topleft = utils.clamp2DBox(self.rect.topleft, self.rect.size, screen_size)

    def squish(self, mx: int, my: int):
        if mx != 0 or my != 0:
            angle = utils.look0At((mx, my))
            if self.in_dash:
                resized_image = pygame.transform.scale(
                    self.original_image,
                    (int(self.original_image.get_width() * 1.4),
                    int(self.original_image.get_height() * 0.6))
                )
                # Create an outline
                outline_size = (resized_image.get_width() + 4, resized_image.get_height() + 4)  # Adjust outline size
                outline_surface = pygame.Surface(outline_size, pygame.SRCALPHA)
                outline_color = "#ffffff"
                pygame.draw.rect(outline_surface, outline_color, (0, 0, outline_size[0], outline_size[1]), 10)  # Outline thickness of 3
                resized_image.blit(outline_surface, outline_surface.get_rect(center=resized_image.get_rect().center))
            else:
                resized_image = pygame.transform.scale(
                    self.original_image,
                    (int(self.original_image.get_width() * 1.2),
                    int(self.original_image.get_height() * 0.8))
                )
            self.image = pygame.transform.rotate(resized_image.convert_alpha(), -angle)  # Ensure proper rotation direction
            self.rect = self.image.get_rect(center=self.rect.center)
        else:
            self.image = self.original_image
            self.rect = self.image.get_rect(center=self.rect.center)

    def render(self, screen: pygame.Surface) -> None:
        """Renders the player on the given screen."""
        # Flash the player during invincibility
        if self.i_count > 0:
            if (self.i_count // 10) % 2 == 0:  # Flashing every 10 frames
                self.image.set_alpha(128)  # Semi-transparent
            else:
                self.image.set_alpha(255)  # Fully opaque
        else:
            self.image.set_alpha(255)  # Ensure full opacity when not invincible

        screen.blit(self.image, self.rect)
        text = pygame.font.SysFont("Comic Sans MS", 20).render(f"Lives: {self.hp}", True, "#00FFFF")
        rect = text.get_rect()
        rect.center = self.rect.center
        rect.centery = rect.centery - 30
        screen.blit(text, rect)

    def take_damage(self):
        """Handle player taking damage."""
        if self.i_count <= 0 and not self.in_dash:  # Only take damage if not invincible
            self.hp -= 1
            self.i_count = self.i_frames  # Reset invincibility timer
