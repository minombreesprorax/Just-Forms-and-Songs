import os
import time
from typing import Tuple
import pygame
import math

if __name__ == "__main__":
    resources = os.path.abspath("./resources/")
else:
    resources = os.path.abspath("./vanilla/resources/")

class square2D:
    def __init__(self, squareString: str): # "(widthxheight);(x,y);(velocityx,velocityy)"
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

class circle2D:
    def __init__(self, squareString: str): # "(radius);(x,y);(velocityx,velocityy)"
        values = squareString.split(";")
        dims = values[0]
        self.radius = int(dims.strip("()"))
        pos = values[1]
        self.x, self.y = map(int, pos.strip("()").split(","))
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.radius*2, self.radius*2)

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
        self.duration = duration + appear_time + 0.2
        self.animprogress = 0.0
        self.start_time = None
        self.done = False
        self.shrink_started = False
        self.rotation_angle, self.rotation_speed = rotation_settings.split(";")
        self.rotation_angle = int(self.rotation_angle)
        self.rotation_speed = int(self.rotation_speed)
        self.chkimg = None
        self.chkrct = None

    def activate(self):
        self.start_time = time.time()

    def update(self):
        if self.start_time is not None:
            elapsed_time = time.time() - self.start_time
            self.animprogress = min(elapsed_time, self.duration)
            
            shrink_duration = 0.2
            shrink_start_time = self.duration - shrink_duration
            
            if not self.shrink_started and self.animprogress >= shrink_start_time and not self.manual_done:
                self.shrink_started = True
                self.rect.width = self.original_size[0]
                self.rect.height = self.original_size[1]
            
            if self.shrink_started and not self.manual_done:
                shrink_factor = 1 - (self.animprogress - shrink_start_time) / shrink_duration
                shrink_factor = max(shrink_factor, 0)
                self.rect.width = int(self.original_size[0] * shrink_factor)
                self.rect.height = int(self.original_size[1] * shrink_factor)
                self.rect.center = self.center
            
            if self.animprogress >= self.duration and not self.manual_done:
                self.done = True

            if not self.shrink_started and self.moving and self.animprogress >= self.appear_time and not self.manual_done:
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
            self.chkimg = rotated_surface

            # Get the new rect for the rotated surface, center it on the original rect
            rotated_rect = rotated_surface.get_rect(center=self.rect.center)
            self.chkrct = rotated_rect

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
        if self.shrink_started or self.animprogress < self.appear_time or self.chkimg is None:
            return False
        
        my_mask = pygame.mask.from_surface(self.chkimg)
        evil_mask = pygame.mask.Mask(other_rect.size, True)
        
        return my_mask.overlap(evil_mask, (other_rect.x - self.chkrct.x, other_rect.y - self.chkrct.y))

class Circle:
    def __init__(self, circle2D: circle2D, appear_time: float = 0.5, duration: float = 1.0, manual_done: bool = False) -> None:
        self.center = (circle2D.x, circle2D.y)
        rect = circle2D.get_rect()
        rect.center = self.center
        self.rect = rect
        self.original_size = (self.rect.width, self.rect.height)
        self.appear_time = appear_time
        self.manual_done = manual_done
        self.duration = duration + appear_time + 0.1
        self.animprogress = 0.0
        self.start_time = None
        self.done = False
        self.shrink_started = False
        self.chkimg = None
        self.chkrct = None
        self.rotclock = 0
        self.color_thingeth = 0.0
        self.add_size = 0

    def activate(self):
        self.start_time = time.time()

    def update(self):
        if self.start_time is not None:
            elapsed_time = time.time() - self.start_time
            self.animprogress = min(elapsed_time, self.duration)

            shrink_duration = 0.1
            shrink_start_time = self.duration - shrink_duration

            self.color_thingeth += 0.5

            # Handle the growth phase
            if self.animprogress >= self.appear_time and not self.shrink_started:
                self.add_size += 2  # Increase the offset size during growth

            self.rotclock -= 5
            if self.rotclock < 0:
                x = self.rotclock
                self.rotclock = 360 - x

            # Start shrinking at the correct time
            if not self.shrink_started and self.animprogress >= shrink_start_time and not self.manual_done:
                self.shrink_started = True
                a = self.original_size[0] + self.add_size  # Include add_size in the initial shrink size
                b = self.original_size[1] + self.add_size  # Include add_size in the initial shrink size
                self.original_size = (a, b)
                self.add_size = 0

            # Shrinking phase
            if self.shrink_started and not self.manual_done:
                shrink_factor = 1 - (self.animprogress - shrink_start_time) / shrink_duration
                shrink_factor = max(shrink_factor, 0)
                self.rect.width = int((self.original_size[0] + self.add_size) * shrink_factor)
                self.rect.height = int((self.original_size[1] + self.add_size) * shrink_factor)
                self.rect.center = self.center  # Keep it centered

            # End the animation when the duration is reached
            if self.animprogress >= self.duration and not self.manual_done:
                self.done = True
    
    def _getColorFade(self, c1: Tuple[int, int, int], c2: Tuple[int, int, int], f: float) -> Tuple[int, int, int]:
        return tuple(int(c1[i] + (c2[i] - c1[i]) * f) for i in range(3))

    def render(self, display: pygame.Surface):
        if self.start_time and self.animprogress >= self.appear_time:
            color = self._getColorFade((255, 32, 113), (255, 255, 255), (math.sin(self.color_thingeth)+1)/2)

            # Draw the circle directly on the display
            render = pygame.Surface((self.rect.width + self.add_size, self.rect.height + self.add_size), pygame.SRCALPHA)
            pygame.draw.circle(render, color, (render.get_rect().centerx, render.get_rect().centery), (self.rect.width + self.add_size) // 2)
            display.blit(render, render.get_rect(center=self.rect.center))
            
            # Update the collision mask to the new circle dimensions
            self.chkimg = pygame.Surface((self.rect.width + self.add_size, self.rect.height + self.add_size), pygame.SRCALPHA)
            pygame.draw.circle(self.chkimg, (255, 255, 255), (self.chkimg.get_rect().width // 2, self.chkimg.get_rect().height // 2), (self.rect.width + self.add_size) // 2)
            self.chkrct = self.chkimg.get_rect(center=self.rect.center)

    def render_bg(self, display: pygame.Surface):
        if self.start_time:
            elapsed_since_start = time.time() - self.start_time
            if elapsed_since_start < self.appear_time:
                # Draw the dotted line (circle) on the display
                self.draw_dotted_circle(display, self.center, self.original_size[0] / 2)

    def draw_dotted_circle(self, display: pygame.Surface, center, radius):
        dot_color = (255, 32, 113)  # Color of the dots
        dot_radius = 2  # Size of each dot
        num_dots = 50  # Number of dots around the circle
        
        # Draw dotted circle
        for i in range(num_dots):
            angle = (2 * math.pi / num_dots) * i + self.rotclock # Calculate the angle for each dot
            # Calculate the x, y position of each dot along the circumference
            x = int(center[0] + radius * math.cos(angle))
            y = int(center[1] + radius * math.sin(angle))
            # Draw a small circle (dot) at this position
            pygame.draw.circle(display, dot_color, (x, y), dot_radius)

    def check_collision(self, other_rect: pygame.Rect) -> bool:
        if self.shrink_started or self.animprogress < self.appear_time or self.chkimg is None:
            return False
        
        my_mask = pygame.mask.from_surface(self.chkimg)
        evil_mask = pygame.mask.Mask(other_rect.size, True)
        
        return my_mask.overlap(evil_mask, (other_rect.x - self.chkrct.x, other_rect.y - self.chkrct.y)) is not None

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    # Define a few example squares to test
    squares = [
        (0, Circle(circle2D("(100);(400,300)"), appear_time=0.5, duration=1.0)),
    ]

    active_squares: list[Square | Circle] = []
    start_timer = time.time()

    running = True
    while running:
        clock.tick(60)
        now = time.time() - start_timer

        # Activate squares based on their appear_time
        for appear_time, square in squares[:]:
            if now >= square.appear_time and square not in active_squares:
                active_squares.append(square)
                square.activate()
                squares.remove((appear_time, square))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Example collision rect (this could be your player or any other object)
        collision_rect = pygame.Rect(200, 100, 50, 50)  # Example object
        
        screen.fill((0, 0, 0))  # Clear the screen
        
        pygame.draw.rect(screen, (255, 0, 0), collision_rect)

        # Update and render active squares
        for square in active_squares[:]:
            square.update()
            if square.done:
                active_squares.remove(square)
            else:
                square.render_bg(screen)  # Render the square background
                print(square.check_collision(collision_rect))
                
        for square in active_squares[:]:
            square.render(screen)  # Render the square

        pygame.display.flip()  # Update the display

    pygame.quit()
