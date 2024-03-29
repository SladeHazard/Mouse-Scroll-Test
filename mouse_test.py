import pygame
import sys
import time

# Initialize Pygame and font
pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Arial', 20)

# Screen dimensions
width, height = 300, 300
screen = pygame.display.set_mode((width, height))

# Tick attributes
x, y = 150, 150
prevx, prevy = 150, 150
tick_height = 10
color = (255, 255, 255)  # Initial color of the tick

# For mouse click test
last_click_time = 0
double_click_threshold = 0.08  # Seconds
click_count = 0  # Number of clicks within a potential double click window
total_clicks = 0  # Total number of clicks
double_clicks_detected = 0  # Total double clicks detected
double_click_message_display_time = 0  # Timer to display double click message

# Clock to control frame rate
clock = pygame.time.Clock()

# Mode selection message in green
print("\033[92mSelect mode (1 for Scroll Wheel Test, 2 for Mouse Click Test): \033[0m", end='')
mode = input()

running = True
while running:
    screen.fill((0, 0, 0))  # Always clear screen (needed for both modes)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if mode == '1':  # Scroll Wheel Test
            if event.type == pygame.MOUSEWHEEL:
                if event.y > 0:
                    color = (0, 255, 0)  # Scroll up, paint tick green
                    print("Scroll up detected")  # Print message on scroll up
                else:
                    color = (255, 0, 0)  # Scroll down, paint tick red
                # Move the tick in the direction of scroll
                prevy = y
                y += event.y * tick_height
                if y > height:
                    y = 0
                    prevy = y
                elif y < 0:
                    y = height
                    prevy = y
                    

        elif mode == '2':  # Mouse Click Test
            if event.type == pygame.MOUSEBUTTONDOWN:
                total_clicks += 1  # Increment total clicks for every mouse button down event
                current_time = time.time()
                
                if click_count == 0:
                    click_count = 1
                    last_click_time = current_time
                elif click_count == 1:
                    if (current_time - last_click_time) <= double_click_threshold:
                        double_clicks_detected += 1
                        double_click_message_display_time = pygame.time.get_ticks()  # Mark the time of detection
                        click_count = 0  # Reset click count after a double click
                    else:
                        # This was a slow second click; treat it as the first click of a new potential double click
                        last_click_time = current_time

    # Display double click detection message for a limited time
    if mode == '2' and (pygame.time.get_ticks() - double_click_message_display_time) < 2000:  # 2 seconds visibility
        text_surface = myfont.render('Double Click Detected', False, (0, 255, 0))
        screen.blit(text_surface, (50, height // 2))

    # Display click and double click counters at the top right
    if mode == '2':
        clicks_surface = myfont.render(f'Clicks: {total_clicks}', False, (255, 255, 255))
        double_clicks_surface = myfont.render(f'Double Clicks: {double_clicks_detected}', False, (255, 255, 255))
        screen.blit(clicks_surface, (width - 200, 10))
        screen.blit(double_clicks_surface, (width - 200, 35))  # Adjust positioning as needed

    if mode == '1':
        # Draw a semi-transparent background
        screen.fill((0, 0, 0, 5))
        
        # Draw the tick
        pygame.draw.line(screen, color, (prevx, prevy), (x, y), 2)
        
        # Move the tick to the right
        prevx = x
        x += 1
        if x > width:
            x = 0
            prevx = x

    pygame.display.flip()
    clock.tick(60)  # Limit to 60 frames per second

pygame.quit()
