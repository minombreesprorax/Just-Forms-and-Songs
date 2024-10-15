import csv
import os
import sys
import pygame
import random
from typing import Tuple, List, Any
from modules.Keyhole import Kh
from modules.player import Player
from vanilla.obstacles.Lasers import *
from vanilla.obstacles.Statics import *

# Function to show escape message
def show_escape_prompt():
    """Display 'Tho you'll have to restart the launcher :/' after beat message."""
    font = pygame.font.SysFont("Impact", 24)
    text = font.render("Tho you'll have to restart the launcher :/", True, "#00FFFF", "#000000")
    rect = text.get_rect()
    screen = pygame.display.get_surface()  # Assume screen is initialized
    rect.center = (screen.get_width()/2, screen.get_height()/4)
    screen.blit(text, rect)  # Adjust position as needed
    pygame.display.flip()

def load_icon():
    try:
        icon_path = os.path.abspath("./icon2.png")  # Ensure this is correct
        icon = pygame.image.load(icon_path)
        pygame.display.set_icon(icon)
    except Exception as e:
        print(f"Error loading icon: {e}")

lvl = ("", "", "")
haswon = False

activeObjects: List[Laser | BigLaser | Square] = []
persistentObjects: List[Tuple[float, Laser]] = []
screen: pygame.surface.Surface = None

def loadLevel(level: Tuple[str, str, str]):
    global lvl, activeObjects, screen, haswon
    # Initialize pygame
    lvl = level
    
    pygame.init()
    load_icon()
        
    screen = pygame.display.set_mode((800, 600))  # Set the screen size
    clock = pygame.time.Clock()

    # Set the window caption
    pygame.display.set_caption("Just Forms and Songs")
    pygame.mouse.set_visible(False)

    # Read events from CSV file
    events = []
    with open(level[0]) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            # Append the command and its arguments
            events.append((row['Command'], row['Arg1'], row['Arg2'], row['Arg3'], row['Arg4'], row['Arg5'], row['Arg6'], row['Arg7'], row['Arg8'], float(row['Beat'])))  # Use float for beat
    # Sort events by beat
    events.sort(key=lambda x: x[9])  # Sort by the beat value

    # Create a keyhole object
    keyhole = Kh()
    
    # Wait for begin
    while True:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            keyhole.event(event)
        begin_text = pygame.font.SysFont("Impact", 72).render("Press enter to begin!", True, "#FFFFFF", "#000000")
        begin_text_rect = begin_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 36))
        screen.blit(begin_text, begin_text_rect)
        
        pygame.display.flip()
        
        if keyhole.is_pressed(pygame.K_RETURN):
            break

    # Create a player object
    player = Player(screen.get_width() // 4, screen.get_height() // 4, 3, keyhole)

    # Initialize variables for beat tracking
    current_beat = 0.0  # Change to float for offbeat handling
    next_event_index = 0
    running = True

    # Get the BPM from the first StartMusic command
    bpm = 120  # Default BPM
    for event in events:
        if event[0] == "StartMusic":
            bpm = int(event[1])  # Assuming the BPM is passed as the first argument in StartMusic
            break

    # Calculate the interval for beats
    beat_interval = 60000 / bpm  # Interval in milliseconds
    last_beat_time = pygame.time.get_ticks()  # Get the current ticks to track elapsed time
    game_over_pause = False

    # Start music for beat 0
    if events:  # Check if there are events to process
        execute_command(events, next_event_index, player)  # Change the index to start at 0

    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            keyhole.event(event)

        # Update game logic
        keyhole.update()
        
        if not haswon:
            # Modify how you handle game over restart logic
            if game_over_pause and keyhole.is_pressed(pygame.K_RETURN):
                game_over_pause = False
                # Call reset_level to restart the game
                events, bpm, beat_interval, last_beat_time = reset_level(level, keyhole, screen, player)
                current_beat = 0.0  # Reset beat tracking
                next_event_index = 0  # Reset event tracking
                if events:
                    execute_command(events, next_event_index, player)  # Restart at beat 0
            
            if not game_over_pause:
                player.update(screen.get_rect().size)  # Pass the screen size here

                # Check for beat-based events based on the elapsed time
                current_time = pygame.time.get_ticks()
                time_since_last_beat = current_time - last_beat_time

                # Update current beat based on elapsed time
                current_beat += time_since_last_beat / beat_interval
                last_beat_time = current_time  # Reset the timer for the next calculation

                # Check for events that should be executed at the current beat
                while next_event_index < len(events) and events[next_event_index][9] <= current_beat:
                    execute_command(events, next_event_index, player)
                    next_event_index += 1
                
                # Check persistent lasers for despawning
                for despawn_beat, obstacle in persistentObjects[:]:
                    if current_beat >= despawn_beat:
                        # Remove the obstacle from list
                        persistentObjects.remove((despawn_beat, obstacle))
                        obstacle.done = True

            # Render everything
            screen.fill((0, 0, 0))  # Fill the screen with black

            if not game_over_pause:
                # Render and update lasers
                for obstacle in activeObjects[:]:
                    obstacle.update()
                    if obstacle.done:
                        activeObjects.remove(obstacle)
                    else:
                        obstacle.render_bg(screen)  # Render the obstacle background

                for obstacle in activeObjects[:]:
                    obstacle.render(screen)  # Render the obstacle
                    if obstacle.check_collision(player.rect):
                        player.take_damage()  # Call the new method for damage handling
                        if player.hp <= 0:
                            pygame.mixer.music.stop()
                            game_over_pause = True
                            
                player.render(screen)
            else:
                text = pygame.font.SysFont("Impact", 72).render("GAME OVER!", True, "#FF2071")
                rect = text.get_rect()
                rect.center = (screen.get_width() // 2, screen.get_height() // 2 - 36)
                screen.blit(text, rect)
                player.rect = player.original_image.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
                player.image = player.original_image.copy()
                text = pygame.font.SysFont("Impact", 48).render("Press Enter to start over.", True, "#FF2071")
                rect = text.get_rect()
                rect.center = (screen.get_width() // 2, screen.get_height() // 2 + 36)
                screen.blit(text, rect)

            pygame.display.flip()
        clock.tick(60)  # Maintain a frame rate of 60 FPS

    pygame.quit()

def execute_command(events: List[str], index: int, player: Player):
    global haswon
    command, arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, _ = events[index]  # Get the event at the current index

    if command == "StartMusic":
        # Load and play the music
        pygame.mixer.music.load(lvl[2])  # Load the music file
        pygame.mixer.music.play(-1, 0, 1000)  # Play indefinitely

    elif command == "Laser":
        # Create the laser
        p = float(arg2) if arg2 != "rand" else round(random.random(), 2)
        laser = Laser(arg1, p, float(arg3), arg4 == "True")  # Create the laser first
        activeObjects.append(laser)
        laser.activate()

        if arg4 == "True":  # If it's persistent
            despawn_beat = float(arg5)  # When it should despawn
            persistentObjects.append((despawn_beat, laser))
        
    elif command == "BigLaser":
        p = float(arg2) if arg2 != "rand" else round(random.random(), 2)
        laser = BigLaser(arg1, p, float(arg3), int(arg4))
        activeObjects.append(laser)
        laser.activate()
        
    elif command == "Square":
        square = Square(square2D(arg1), float(arg2), float(arg3), arg4 == "True", arg5 == "True", arg6)
        activeObjects.append(square)
        square.activate()
        
        if arg5 == "True":
            despawn_beat = float(arg7)
            persistentObjects.append((despawn_beat, square))
    
    elif command == "Circle":
        circle = Circle(circle2D(arg1), float(arg2), float(arg3), arg4 == "True")
        activeObjects.append(circle)
        circle.activate()
        
        if arg4 == "True":
            despawn_beat = float(arg5)
            persistentObjects.append((despawn_beat, circle))
    
    elif command == "BeatLevel":
        # Fade out the music over 1 second
        pygame.mixer.music.fadeout(1000)
        
        # Rank system based on player's health
        if player.hp == 5:
            rank = "S"
        elif player.hp == 4:
            rank = "A"
        elif player.hp == 3:
            rank = "B"
        elif player.hp == 2:
            rank = "C"
        else:
            rank = "D"

        # Display "LEVEL BEAT!" message with rank
        screen.fill((0, 0, 0))  # Clear the screen
        
        haswon = True
        
        # Display "LEVEL BEAT!" message
        level_beat_text = pygame.font.SysFont("Impact", 72).render("LEVEL BEAT!", True, "#00FFFF")
        level_beat_rect = level_beat_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 36))
        screen.blit(level_beat_text, level_beat_rect)
        
        # Display rank message
        rank_text = pygame.font.SysFont("Impact", 48).render(f"Rank: {rank}", True, "#00FFFF")
        rank_rect = rank_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 36))
        screen.blit(rank_text, rank_rect)

        pygame.display.flip()  # Update the screen
 
        # Pause for 2 seconds to display the message before showing ESCAPE prompt
        pygame.time.delay(2000)

        # Show the escape prompt
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            show_escape_prompt()
            pygame.time.delay(100)
        

# Add a new function to reset level
def reset_level(level: Tuple[str, str, str], keyhole: Kh, screen, player: Player):
    global activeObjects, persistentObjects
    activeObjects = []
    persistentObjects = []
    
    # Reinitialize player
    player.hp = 5
    player.in_dash = False
    player.i_count = 0
    player.dash_cooldown = 0
    player.dash_timer = 0
    player.rect.topleft = (screen.get_width() // 4, screen.get_height() // 4)

    # Re-read the level events
    events = []
    with open(level[0]) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            # Append the command and its arguments
            events.append((row['Command'], row['Arg1'], row['Arg2'], row['Arg3'], row['Arg4'], row['Arg5'], row['Arg6'], row['Arg7'], row['Arg8'], float(row['Beat'])))  # Use float for beat
    
    # Sort events by beat
    events.sort(key=lambda x: x[9])  # Sort by the beat value

    # Get the BPM from the first StartMusic command
    bpm = 120  # Default BPM
    for event in events:
        if event[0] == "StartMusic":
            bpm = int(event[1])  # Assuming the BPM is passed as the first argument in StartMusic
            break

    beat_interval = 60000 / bpm  # Interval in milliseconds
    last_beat_time = pygame.time.get_ticks()

    return events, bpm, beat_interval, last_beat_time