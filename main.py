##### Abdominal Tensing Task #####
# This script is used to run the abdominal tensing task experiment
# Created by: Sigrid Bom
# Date: 2025-04-01

# comments
#-
#-
#-

#------------------------- CODE -------------------------#

# importing packages
import pandas as pd
import pygame
import pygame_gui

# import all modules from locals for easier access to key coordinates
from pygame.locals import * # can also just import K_ESCAPE and QUIT fx
## ------------------USER INPUT ------------------ ##

user_input_ID =input("Participant ID:")
user_input_tutorial = input("Tutorial (1 = yes /0 = no)?:")

## --------------- TEXT ------------------- ##

instruction1 = "        Velkommen til MAVE-SPÆNDINGS-OPGAVEN! \n\n\n " \
" I denne opgave vil du blive bedt om at spænde dine mavemuskler \n eller knytte dine hænder og " \
"svare på nogle spørgsmål om, hvordan det føles." \

#instruction1 = "Velkommen til MAVE-SPÆNDINGS-OPGAVEN! "
#instruction2 = "\n\n\n I denne opgave vil du blive bedt om at spænde dine mavemuskler \n eller knytte dine hænder og " \
#"svare på nogle spørgsmål om, hvordan det føles."\

# make functions?? 

if user_input_tutorial == "1":

    # Initialize pygame
    pygame.init()

    # # Set screen dimensions
    info = pygame.display.Info()  # Get the current display information
    WIDTH, HEIGHT = info.current_w, info.current_h  # Use the current screen dimensions
    # Set up the display
    # screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Windowed mode
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)  # Fullscreen mode
    pygame.display.set_caption("Abdominal Tensing Task")
    pygame.event.get() # Clear the event queue

    # Define colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GREY= (169, 169, 169)

    # Set up font
    font_size = 46#HEIGHT // 10
    font = pygame.font.Font(None, font_size)  # None means use the default font, 36 is the font size

    # Create a clock object to control the frame rate
    clock = pygame.time.Clock()


    # main loop
    running = True
    while running:
        
        screen.fill(GREY)
        #print(f"screen size: {info}")

        # to see what is actually visible on the screen 
        pygame.draw.rect(screen, WHITE, (0, 0, WIDTH, HEIGHT), 10) 

        for event in pygame.event.get():
            if event.type == KEYDOWN:  # Detect key press
                if event.key == K_ESCAPE:  # Check if the pressed key is the Escape key
                    running = False  # Stop the program or exit the loop
            elif event.type == QUIT:
                running = False
        
        text = font.render(instruction1, True, WHITE)

        # Get the rectangle around the text surface
        text_rect = text.get_rect()

        # Center the text horizontally and vertically
        text_rect.center = (WIDTH // 2, HEIGHT // 2)

        # Blit (copy) the text to the screen at the centered position
        screen.blit(text, text_rect)

        # text = font.render(instruction2, True, WHITE)

        #  # Get the rectangle around the text surface
        # text_rect = text.get_rect()

        # # Center the text horizontally and vertically
        # text_rect.center = (WIDTH // 2, HEIGHT // 2)

        # # Blit (copy) the text to the screen at the centered position
        # screen.blit(text, text_rect)
        # # text_surface = font.render(instruction1, True, WHITE)

        # # Blit (copy) the text surface to the screen at a specific position
        # text_x = WIDTH // 2 - text_surface.get_width() // 2  # Center horizontally
        # text_y = HEIGHT // 2 - text_surface.get_height() // 2  # Center vertically
        # screen.blit(text_surface, (text_x, text_y))
    
        # Update the display
        pygame.display.flip()

        # Control frame rate
        clock.tick(60)

    pygame.quit()

# WIDTH, HEIGHT = 800, 600
# screen = pygame.display.set_mode((WIDTH, HEIGHT))
# pygame.display.set_caption("Experiment Setup")

# # Colors
# WHITE = (255, 255, 255)
# BLACK = (0, 0, 0)

# # Set up font
# font = pygame.font.Font(None, 36)

# # GUI Manager
# manager = pygame_gui.UIManager((WIDTH, HEIGHT))

# # Input Box & Submit Button
# input_box = pygame_gui.elements.UITextEntryLine(
#     relative_rect=pygame.Rect((250, 250), (300, 50)), manager=manager
# )
# submit_button = pygame_gui.elements.UIButton(
#     relative_rect=pygame.Rect((350, 320), (100, 40)),
#     text="Submit",
#     manager=manager,
# )

# clock = pygame.time.Clock()
# running = True
# show_intro = False  # Flag to control when to show the intro text
# show_second_screen = False  # Flag to control when to show the second screen
# participant_info = ""  # Stores participant input

# # Main loop
# while running:
#     time_delta = clock.tick(30) / 1000.0  # Controls frame rate

#     # Event handling
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
        
#         # GUI event handling
#         if event.type == pygame_gui.UI_BUTTON_PRESSED:
#             if event.ui_element == submit_button:
#                 participant_info = input_box.get_text()
#                 show_intro = True  # Switch to intro screen

#         manager.process_events(event)

#     # Clear screen
#     screen.fill(WHITE)

#     if not show_intro:
#         # Draw GUI elements (input box and button)
#         manager.update(time_delta)
#         manager.draw_ui(screen)
#     elif show_intro and not show_second_screen:
#         # Display introduction text
#         intro_text = [
#             "Welcome to the experiment!",
#             "In this study, you will be asked to complete various tasks.",
#             "Press any key to begin.",
#         ]
        
#         y_offset = 200
#         for line in intro_text:
#             text_surface = font.render(line, True, BLACK)
#             screen.blit(text_surface, (WIDTH // 2 - text_surface.get_width() // 2, y_offset))
#             y_offset += 50

#         # Wait for any key press to proceed to the second screen
#         keys = pygame.key.get_pressed()
#         if any(keys):
#             show_second_screen = True
#             show_intro = False  # Stop showing the intro screen

#     elif show_second_screen:
#         # Display second screen with additional information
#         second_screen_text = [
#             "Thank you for your participation!",
#             "We are now ready to begin the main task.",
#             "Press space to continue."
#         ]
        
#         y_offset = 200
#         for line in second_screen_text:
#             text_surface = font.render(line, True, BLACK)
#             screen.blit(text_surface, (WIDTH // 2 - text_surface.get_width() // 2, y_offset))
#             y_offset += 50
        
#         # Wait for space key press to exit
#         keys = pygame.key.get_pressed()
#         if keys[pygame.K_SPACE]:
#             running = False  # Exit the loop and close the window

#     pygame.display.flip()

# pygame.quit()

# # Print participant info (you can save this to a file instead)
# print("Participant Info:", participant_info)
