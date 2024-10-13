from typing import List, Tuple, Literal
import pygame
import time

class Laser:
    def __init__(self, orientation: Literal["Horizontal", "Vertical"], position: float, timer: float = 0.5, persistent: bool = False) -> None:
        self.orientation = orientation
        self.position = position
        self.timer = timer
        self.animprogress = 0.0
        self.start_time = None
        self.done = False
        self.persistent = persistent

    def activate(self):
        self.start_time = time.time()

    def update(self):
        if self.start_time is not None:
            elapsed_time = time.time() - self.start_time
            self.animprogress = min(elapsed_time, self.timer + 0.8)
            if not self.persistent and self.animprogress >= self.timer + 0.75:
                self.done = True

    def render(self, display: pygame.Surface):
        if self.animprogress >= self.timer:
            if self.start_time is None:
                return
            
            # Create the rectangle for rendering
            if self.orientation == "Vertical":
                x_pos = self.position * display.get_rect().width
                rect = pygame.Rect(
                    x_pos,
                    0,
                    10,
                    (self.animprogress / self.timer) * display.get_rect().height
                )
                rect.centerx = x_pos
            else:  # Horizontal
                y_pos = self.position * display.get_rect().height
                rect = pygame.Rect(
                    0,
                    y_pos,
                    (self.animprogress / self.timer) * display.get_rect().width,
                    10
                )
                rect.centery = y_pos

            color = pygame.Color("#FF2071")
            pygame.draw.rect(display, color, rect)

            # Store the rectangle for collision checks
            self.rect = rect

    def render_bg(self, display: pygame.Surface):
        if self.animprogress < self.timer:
            if self.start_time is None:
                return
            
            # Create the rectangle for rendering
            if self.orientation == "Vertical":
                x_pos = self.position * display.get_rect().width
                rect = pygame.Rect(
                    x_pos,
                    0,
                    (self.animprogress / self.timer) * 10,
                    display.get_rect().height
                )
                rect.centerx = x_pos
            else:  # Horizontal
                y_pos = self.position * display.get_rect().height
                rect = pygame.Rect(
                    0,
                    y_pos,
                    display.get_rect().width,
                    (self.animprogress / self.timer) * 10
                )
                rect.centery = y_pos

            color = pygame.Color("#690f2f")
            pygame.draw.rect(display, color, rect)

            # Store the rectangle for collision checks
            self.rect = rect

    def check_collision(self, other_rect: pygame.Rect) -> bool:
        """Check for collision with another rectangle."""
        if self.animprogress >= self.timer:
            if hasattr(self, 'rect'):
                return self.rect.colliderect(other_rect)
        return False

class BigLaser:
    def __init__(self, orientation: Literal["Up-Down", "Left-Right", "Down-Up", "Right-Left"] | int, position: float, timer: float = 1, size: int = 100) -> None:
        self.orientation = 0 if orientation == "Up-Down" else 1 if orientation == "Left-Right" else 2 if orientation == "Down-Up" else 3 if orientation == "Right-Left" else orientation if isinstance(orientation, int) and orientation in range(0, 4) else 0
        self.position = position
        self.timer = timer
        self.size = size
        self.animprogress = 0.0
        self.start_time = None
        self.done = False

    def activate(self):
        self.start_time = time.time()

    def update(self):
        if self.start_time is not None:
            elapsed_time = time.time() - self.start_time
            self.animprogress = min(elapsed_time, self.timer + 0.6)
            if self.animprogress >= self.timer + 0.5:
                self.done = True

    def render(self, display: pygame.Surface):
        if self.start_time is None:
            return
        
        # Calculate the position based on the orientation
        if self.orientation == 0:  # Up-Down
            x_pos = self.position * display.get_rect().width
            rect_height = (self.animprogress / self.timer) * display.get_rect().height / 50 + 5 if self.animprogress < self.timer else (self.animprogress / self.timer) * display.get_rect().height * 2
            rect = pygame.Rect(x_pos, 0, self.size, rect_height)
            rect.centerx = x_pos
        
        elif self.orientation == 1:  # Left-Right
            y_pos = self.position * display.get_rect().height
            rect_width = (self.animprogress / self.timer) * display.get_rect().width / 50 + 5 if self.animprogress < self.timer else (self.animprogress / self.timer) * display.get_rect().width * 2
            rect = pygame.Rect(0, y_pos, rect_width, self.size)
            rect.centery = y_pos
        
        elif self.orientation == 2:  # Down-Up
            x_pos = self.position * display.get_rect().width
            rect_height = (self.animprogress / self.timer) * display.get_rect().height / 50 + 5 if self.animprogress < self.timer else (self.animprogress / self.timer) * display.get_rect().height * 2
            rect = pygame.Rect(x_pos, display.get_rect().height - rect_height, self.size, rect_height)
            rect.centerx = x_pos

        elif self.orientation == 3:  # Right-Left
            y_pos = self.position * display.get_rect().height
            rect_width = (self.animprogress / self.timer) * display.get_rect().width / 50 + 5 if self.animprogress < self.timer else (self.animprogress / self.timer) * display.get_rect().width * 2
            rect = pygame.Rect(display.get_rect().width - rect_width, y_pos, rect_width, self.size)
            rect.centery = y_pos
        
        color = pygame.Color("#FFFFFF") if self.animprogress > self.timer and self.animprogress < self.timer + 0.1 else pygame.Color("#FF2071")
        pygame.draw.rect(display, color, rect)    # Animated rectangle

        # Store the rectangle for collision checks
        self.rect = rect
    
    def render_bg(self, display: pygame.Surface):
        if self.start_time is None:
            return
        
        # Calculate the position based on the orientation
        if self.orientation == 0:  # Up-Down
            x_pos = self.position * display.get_rect().width
            brect = pygame.Rect(x_pos, 0, self.size, display.get_rect().height)
            brect.centerx = x_pos
        
        elif self.orientation == 1:  # Left-Right
            y_pos = self.position * display.get_rect().height
            brect = pygame.Rect(0, y_pos, display.get_rect().width, self.size)
            brect.centery = y_pos
        
        elif self.orientation == 2:  # Down-Up
            x_pos = self.position * display.get_rect().width
            brect = pygame.Rect(x_pos, 0, self.size, display.get_rect().height)
            brect.centerx = x_pos

        elif self.orientation == 3:  # Right-Left
            y_pos = self.position * display.get_rect().height
            brect = pygame.Rect(0, y_pos, display.get_rect().width, self.size)
            brect.centery = y_pos
        
        bcolor = pygame.Color("#690f2f")
        pygame.draw.rect(display, bcolor, brect)  # Background rectangle

    def check_collision(self, other_rect: pygame.Rect) -> bool:
        """Check for collision with another rectangle."""
        if self.animprogress >= self.timer:
            if hasattr(self, 'rect'):
                return self.rect.colliderect(other_rect)
        return False

if __name__ == "__main__":
    # Example usage
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    lasers: List[Tuple[float, Laser]] = [
        (0, Laser('Horizontal', 0.1)),
        (0.9, BigLaser('Left-Right', 0.1)),
        (0.1, Laser('Horizontal', 0.2)),
        (0.2, Laser('Horizontal', 0.3)),
        (1.1, BigLaser('Left-Right', 0.3)),
        (0.3, Laser('Horizontal', 0.4)),
        (0.4, Laser('Horizontal', 0.5)),
        (1.3, BigLaser('Left-Right', 0.5)),
        (0.5, Laser('Horizontal', 0.6)),
        (0.6, Laser('Horizontal', 0.7)),
        (1.5, BigLaser('Left-Right', 0.7)),
        (0.7, Laser('Horizontal', 0.8)),
        (0.8, Laser('Horizontal', 0.9)),
        (1.7, BigLaser('Left-Right', 0.9)),
    ]

    activelasers: List[Laser] = []
    start_timer = time.time()

    running = True
    while running:
        clock.tick(60)
        now = time.time() - start_timer

        # Activating the lasers based on the timer
        for time_threshold, laser in lasers[:]:
            if now >= time_threshold and laser:
                activelasers.append(laser)
                laser.activate()
                lasers.remove((time_threshold, laser))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Example collision rect (this could be your player or any other object)
        collision_rect = pygame.Rect(400, 300, 50, 50)  # Example object

        screen.fill((0, 0, 0))  # Clear the screen

        # Update and render active lasers
        for laser in activelasers[:]:
            laser.update()
            if laser.done:
                activelasers.remove(laser)
            else:
                laser.render_bg(screen)  # Render the laser background
        for laser in activelasers[:]:
            laser.render(screen)  # Render the laser
        
        pygame.display.flip()  # Update the display

    pygame.quit()