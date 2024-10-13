import os
import time
import pygame
import math

if __name__ == "__main__":
    resources = os.path.abspath("./resources/")
else:
    resources = os.path.abspath("./vanilla/resources/")

class square2D:
    def __init__(self, squareString: str):
        values = squareString.split(";")
        dims = values[0]
        self.width, self.height = map(int, dims.strip("()").split("x"))
        pos = values[1]
        self.x, self.y = map(int, pos.strip("()").split(","))
        if len(values) > 2:
            speed = values[2]
            self.vx, self.vy = map(int, speed.strip("()").split(","))
        else:
            self.vx, self.vy = 0, 0
        
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class Square:
    def __init__(self, square2D: square2D, appear_time: float = 0.5, duration: float = 1.0, move: bool = False, manual_done: bool = False, rotation_settings: str = "0;0") -> None:
        self.center = (square2D.x, square2D.y)
        rect = square2D.get_rect()
        rect.center = self.center
        self.rect = rect
        self.original_size = (self.rect.width, self.rect.height)
        self.appear_time = appear_time
        self.moving = move
        self.manual_done = manual_done
        self.speed = (square2D.vx, square2D.vy)
        self.duration = duration
        self.animprogress = 0.0
        self.start_time = None
        self.done = False
        self.shrink_started = False
        self.rotation_angle, self.rotation_speed = rotation_settings.split(";")
        self.rotation_angle = int(self.rotation_angle)
        self.rotation_speed = int(self.rotation_speed)

    def activate(self):
        self.start_time = time.time()

    def update(self):
        if self.start_time is not None:
            elapsed_time = time.time() - self.start_time
            self.animprogress = min(elapsed_time, self.duration)
            
            shrink_duration = 0.2
            shrink_start_time = self.duration - shrink_duration
            
            if not self.shrink_started and self.animprogress >= shrink_start_time:
                self.shrink_started = True
                self.rect.width = self.original_size[0]
                self.rect.height = self.original_size[1]
            
            if self.shrink_started:
                shrink_factor = 1 - (self.animprogress - shrink_start_time) / shrink_duration
                shrink_factor = max(shrink_factor, 0)
                self.rect.width = int(self.original_size[0] * shrink_factor)
                self.rect.height = int(self.original_size[1] * shrink_factor)
                self.rect.center = self.center
            
            if self.animprogress >= self.duration and not self.manual_done:
                self.done = True

            if not self.shrink_started and self.moving and self.animprogress >= self.appear_time:
                self.rect.x += self.speed[0]
                self.rect.y += self.speed[1]
                self.center = self.rect.center
            
            # Update rotation angle (rotate 15 degrees per frame)
            if self.animprogress >= self.appear_time:
                self.rotation_angle += self.rotation_speed
                if self.rotation_angle >= 360:
                    self.rotation_angle -= 360

    def render(self, display: pygame.Surface):
        if self.start_time and self.animprogress >= self.appear_time:
            color = pygame.Color("#FF2071" if self.animprogress >= self.appear_time + 0.1 else "#FFFFFF")

            # Create a surface for the square
            square_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
            square_surface.fill(color)

            # Rotate the square surface
            rotated_surface = pygame.transform.rotate(square_surface, self.rotation_angle)

            # Get the new rect for the rotated surface, center it on the original rect
            rotated_rect = rotated_surface.get_rect(center=self.rect.center)

            # Blit the rotated surface onto the display
            display.blit(rotated_surface, rotated_rect.topleft)

    def render_bg(self, display: pygame.Surface):
        if self.start_time:
            elapsed_since_start = time.time() - self.start_time
            if elapsed_since_start < self.appear_time:
                scale_factor = elapsed_since_start / self.appear_time
                current_width = int(self.original_size[0] * scale_factor)
                current_height = int(self.original_size[1] * scale_factor)
                current_rect = pygame.Rect(self.center[0] - current_width // 2, self.center[1] - current_height // 2, current_width, current_height)
                
                color = pygame.Color("#690f2f")
                
                surface = pygame.Surface((current_rect.width, current_rect.height), pygame.SRCALPHA)
                surface.fill(color)
                rotated_surface = pygame.transform.rotate(surface, self.rotation_angle)
                
                rotated_rect = rotated_surface.get_rect(center=self.rect.center)
                
                display.blit(rotated_surface, rotated_rect.topleft)

    def check_collision(self, other_rect: pygame.Rect) -> bool:
        if self.shrink_started:
            return False
        if self.animprogress >= self.appear_time and hasattr(self, 'rect'):
            return self.rect.colliderect(other_rect)
        return False

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    # Define a few example squares to test
    squares = [
        Square(square2D("(50x50);(100,100);(2,1)"), appear_time=0.5, duration=2.0, move=True, rotation_settings="0;5"),
        Square(square2D("(100x100);(300,200)"), appear_time=1.0, duration=3.0, rotation_settings="45;0"),
        Square(square2D("(75x25);(500,400);(-3,2)"), appear_time=0.75, duration=2.5, move=True, rotation_settings="0;-15"),
    ]

    active_squares = []
    start_timer = time.time()

    running = True
    while running:
        clock.tick(60)
        now = time.time() - start_timer

        # Activate squares based on their appear_time
        for square in squares[:]:
            if now >= square.appear_time and square not in active_squares:
                active_squares.append(square)
                square.activate()
                squares.remove(square)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Example collision rect (this could be your player or any other object)
        collision_rect = pygame.Rect(400, 300, 50, 50)  # Example object

        screen.fill((0, 0, 0))  # Clear the screen

        # Update and render active squares
        for square in active_squares[:]:
            square.update()
            if square.done:
                active_squares.remove(square)
            else:
                square.render_bg(screen)  # Render the square background
        for square in active_squares[:]:
            square.render(screen)  # Render the square

        pygame.display.flip()  # Update the display

    pygame.quit()
