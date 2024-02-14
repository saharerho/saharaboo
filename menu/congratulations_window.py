import pygame
import os

root_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sound = os.path.join(root_dir, "../puzzle_simple_game/sounds", "win.wav")

# Define the paths to the font and background image
font_path = os.path.join(
    root_dir, "../puzzle_simple_game/fonts", "game_font.ttf")
background_image_path = os.path.join(
    root_dir, "../puzzle_simple_game/images", "background.jpg")


def display_congratulations():
    page_width, page_height = 800, 600
    pygame.init()
    screen = pygame.display.set_mode((page_width, page_height))
    pygame.display.set_caption(
        "Puzzle Simple Game 2024 [Congratulations]"
    )  # Change window title

    # Load the font
    font = pygame.font.Font(font_path, 70)

    # Load the background image
    background_image = pygame.image.load(background_image_path).convert()
    background_image = pygame.transform.scale(
        background_image, (page_width, page_height))

    clock = pygame.time.Clock()  # Create a clock object to control the frame rate
    black_color = (0, 0, 0)
    white_color = (255, 255, 255)
    text_x, text_y = page_width // 2, page_height // 2
    text_direction = 1
    text_alpha = 255  # Initial alpha value for text transparency

    # Load the sound
    pygame.mixer.init()
    win_sound = pygame.mixer.Sound(sound)  # Adjust the filename as needed
    sound_played = False  # Flag to track if the sound has been played

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.blit(background_image, (0, 0))  # Display the background image

        # Animate the color and transparency of the text
        if black_color[0] < 255:
            black_color = (black_color[0] + 1,
                           black_color[1] + 1, black_color[2] + 1)
        else:
            black_color = (0, 0, 0)

        if text_alpha > 0:
            text_alpha -= 1
        else:
            # Reset variables for the next appearance
            text_alpha = 255
            black_color = (0, 0, 0)

        # Check if the sound has not been played yet
        if not sound_played:
            win_sound.play()  # Play the sound
            sound_played = True  # Update the flag to indicate the sound has been played

        # Render the text with the changing color and transparency
        congratulations_text = font.render(
            "Congratulations!", True, white_color)  # Set the color to white
        congratulations_text.set_alpha(text_alpha)  # Set text transparency

        # Draw the text at the center of the screen
        text_rect = congratulations_text.get_rect(center=(text_x, text_y))
        screen.blit(congratulations_text, text_rect)

        # Update the display
        pygame.display.flip()

        # Control the speed of the animation
        clock.tick(60)  # Limit frame rate to 60 FPS

    pygame.quit()


if __name__ == "__main__":
    display_congratulations()
