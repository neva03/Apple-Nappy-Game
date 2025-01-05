import pygame
import random
import sys

# Initialize the pygame library
pygame.init()

# Screen dimensions
screenWidth = 800
screenHeight = 600

# Screen setup
gameDisplay = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption('Fruit Nappy')

# Colors
black = (0, 0, 0)
light_blue = (0, 200, 255)
red=(230,0,0)

# Frames Per Second (FPS) settings
clock = pygame.time.Clock()
FPS = 60

# Plate properties
plate_width = 100
plate_height = 20
plate_x = (screenWidth - plate_width) // 2  # Center the plate horizontally
plate_y = screenHeight - plate_height - 10  # Position plate near the bottom
plate_speed = 8  # Speed of the plate's movement

# Game state variables
is_failed = False  # Whether the game is over
score = 0  # Player's current score
lives = 3  # Player's starting lives
is_paused = False  # Tracks whether the game is paused
max_score = 0  # Player's high score

# Circle properties
circle_radius = 20
circle_speed = 5
circles = []  # List to track falling objects (fruits/skulls)

# Heart image for lives display
heart_image = pygame.image.load("heart.png")
heart_image = pygame.transform.scale(heart_image, (40, 40))


# Fruit images
apple_image = pygame.image.load("apple.png")
apple_image = pygame.transform.scale(apple_image, (60, 60))
grape_image = pygame.image.load("grape.png")
grape_image = pygame.transform.scale(grape_image, (60, 60))

# Skull image
skull_image = pygame.image.load("skull.png")
skull_image = pygame.transform.scale(skull_image, (60, 60))

# Background image
background_image = pygame.image.load("background.png")
background_image = pygame.transform.scale(background_image, (screenWidth, screenHeight))

# Monkey image
monkey_image = pygame.image.load(r"monkey.png")
monkey_image = pygame.transform.scale(monkey_image, (70, 70))  # Plate'in boyutlarına uygun

# Font for rendering text
font = pygame.font.Font(None, 36)

#function to draw the monkey 
def draw_plate():
     plate_y =+510
     gameDisplay.blit(monkey_image, (plate_x, plate_y))

# Function to draw the plate
def draw_plate():
    pygame.draw.rect(gameDisplay, light_blue, (plate_x, plate_y, plate_width, plate_height))

# Function to draw the falling objects (circles)
def draw_circles():
    for c in circles:
        x, y, color, is_fruit = c
        if is_fruit == "apple":  # Draw apple image
            gameDisplay.blit(apple_image, (x - circle_radius, y - circle_radius))
        elif is_fruit == "grape":  # Draw grape image
            gameDisplay.blit(grape_image, (x - circle_radius, y - circle_radius))
        elif is_fruit == "skull":  # Draw skull image
            gameDisplay.blit(skull_image, (x - circle_radius, y - circle_radius))

# Function to display the current score
def show_score():
    text = font.render(f"Score: {score}", True, black)
    gameDisplay.blit(text, (10, 10))

# Function to draw the pause button
def draw_pause_button():
    button_width, button_height = 100, 40
    button_x = screenWidth - 150
    button_y = 60
    draw_button("Pause", button_x, button_y, button_width, button_height, light_blue, black, pause_game)

# Function to show player's remaining lives
def show_lives():
    for i in range(lives):
        gameDisplay.blit(heart_image, (screenWidth - 150 + i * 50, 10))

# Function to draw a button
def draw_button(text, x, y, width, height, inactive_color, active_color, action=None):
    mouse = pygame.mouse.get_pos()  # Get current mouse position
    click = pygame.mouse.get_pressed()  # Check mouse clicks

    # Highlight button if hovered
    if x < mouse[0] < x + width and y < mouse[1] < y + height:
        pygame.draw.rect(gameDisplay, active_color, (x, y, width, height))
        if click[0] == 1 and action is not None:  # If clicked, trigger action
            action()
    else:
        pygame.draw.rect(gameDisplay, inactive_color, (x, y, width, height))

    # Draw button text
    button_font = pygame.font.Font(None, 36)
    text_surface = button_font.render(text, True, black)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    gameDisplay.blit(text_surface, text_rect)

# Function to restart the game
def restart_game():
    global is_failed, score, circles, plate_x, lives
    is_failed = False
    score = 0
    lives = 3
    circles = []
    plate_x = (screenWidth - plate_width) // 2

# Function to handle game over
def game_over():
    global max_score

    # Update high score
    if score > max_score:
        max_score = score

    # Display "Game Over" text
    text = font.render("Game Over!", True, black)
    text_rect = text.get_rect(center=(screenWidth // 2, screenHeight // 2 - 50))
    gameDisplay.blit(text, text_rect)

    # Display high score
    high_score_text = font.render(f"High Score: {max_score}", True, black)
    high_score_rect = high_score_text.get_rect(center=(screenWidth // 2, screenHeight // 2))
    gameDisplay.blit(high_score_text, high_score_rect)

    # Restart button
    button_width = 120
    button_height = 50
    button_x = screenWidth // 2 - button_width // 2
    button_y = screenHeight // 2 + 50
    draw_button("Restart", button_x, button_y, button_width, button_height, light_blue, black, restart_game)

#function to countdown 
def countdown():
    
    for i in range(3, 0, -1):  # 3'ten 1'e kadar sayar
        for size in range(50, 150, 5):  # Yazı boyutunu büyütür (50'den 150'ye)
            gameDisplay.blit(background_image, (0, 0))  # Arka planı çiz
            countdown_font = pygame.font.Font(None, size)  # Dinamik yazı boyutu
            text = countdown_font.render(str(i), True, red)
            text_rect = text.get_rect(center=(screenWidth // 2, screenHeight // 2))
            gameDisplay.blit(text, text_rect)
            pygame.display.update()
            pygame.time.delay(10)  # Küçük bir gecikme ile animasyon yaratır
        
        pygame.time.delay(500)  # Sayı ekranda kısa süre kalır

    # "Go!" animasyonu
    for size in range(50, 150, 5):  # "Go!" yazısını büyütür
        gameDisplay.blit(background_image, (0, 0))  # Arka planı çiz
        countdown_font = pygame.font.Font(None, size)  # Dinamik yazı boyutu
        text = countdown_font.render("Go!", True, red)
        text_rect = text.get_rect(center=(screenWidth // 2, screenHeight // 2))
        gameDisplay.blit(text, text_rect)
        pygame.display.update()
        pygame.time.delay(10)  # Küçük bir gecikme ile animasyon yaratır

    pygame.time.delay(500)  # "Go!" ekranda kısa süre kalır


# Function to show high score below the current score
def show_high_score():
    text = font.render(f"High Score: {max_score}", True, black)
    gameDisplay.blit(text, (10, 50))

# Function to display the main menu
def show_menu():
    global menu_running
    menu_running = True
    while menu_running:
        gameDisplay.blit(background_image, (0, 0))  # Display background

        # Display game title
        title_font = pygame.font.Font(None, 72)
        title_surface = title_font.render("Fruit Nappy", True, black)
        title_rect = title_surface.get_rect(center=(screenWidth // 2, screenHeight // 4))
        gameDisplay.blit(title_surface, title_rect)

        # Draw menu buttons
        button_width, button_height = 200, 60
        button_x = screenWidth // 2 - button_width // 2
        start_button_y = screenHeight // 2 - 40
        resume_button_y = screenHeight // 2 + 40
        quit_button_y = screenHeight // 2 + 120

        draw_button("Start Game", button_x, start_button_y, button_width, button_height, light_blue, black, start_game)
        
        # Show "Resume" button only if the game is paused
        if is_paused:
            draw_button("Resume", button_x, resume_button_y, button_width, button_height, light_blue, black, resume_game)
        
        draw_button("Quit", button_x, quit_button_y, button_width, button_height, light_blue, black, quit_game)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Exit game if the close button is pressed
                pygame.quit()
                sys.exit()

        pygame.display.update()
        clock.tick(FPS)

# Function to start the game
def start_game():
    countdown()
    global running, menu_running, max_score, is_paused
    max_score = 0  # Reset high score
    running = True  # Enter game loop
    menu_running = False  # Exit menu loop
    is_paused = False  # Ensure game isn't paused

# Function to resume the game
def resume_game():
    global is_paused
    is_paused = False

# Function to pause the game
def pause_game():
    global is_paused
    is_paused = True

    while is_paused:
        gameDisplay.blit(background_image, (0, 0))  # Draw background

        # Display "Paused" text
        pause_text = font.render("Paused", True, black)
        pause_text_rect = pause_text.get_rect(center=(screenWidth // 2, screenHeight // 2 - 100))
        gameDisplay.blit(pause_text, pause_text_rect)

        # Draw pause menu buttons
        button_width, button_height = 200, 60
        button_x = screenWidth // 2 - button_width // 2
        resume_button_y = screenHeight // 2
        menu_button_y = screenHeight // 2 + 80

        draw_button("Resume", button_x, resume_button_y, button_width, button_height, light_blue, black, resume_game)
        draw_button("Go to Menu", button_x, menu_button_y, button_width, button_height, light_blue, black, show_menu)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Exit game if the close button is pressed
                pygame.quit()
                sys.exit()

        pygame.display.update()
        clock.tick(FPS)

# Function to quit the game
def quit_game():
    pygame.quit()
    sys.exit()

# Display the menu at the start
show_menu()

# Main game loop
running = True
while running:
    gameDisplay.blit(background_image, (0, 0))  # Draw background

    # Ekranda en fazla 5 nesne olmasını sağlıyoruz
    if random.randint(1, 180) == 1:
                is_fruit = random.choice(["apple", "grape", "skull"])  
                margin =150
                x = random.randint(margin + circle_radius, screenWidth - margin - circle_radius)
                y = -circle_radius
                circles.append((x, y, "white", is_fruit))

            # Gruplar
    if len(circles) < 5 and random.randint(1, 180) == 1:
               group_x = random.randint(100, screenWidth - 100)  # Grup merkezi
               initial_y = -circle_radius  # İlk meyvenin başlangıç yüksekliği
            
               for i in range(random.randint(1,2)):  # Aynı anda 1-2 meyve düşür
                   while True:  # Uygun bir pozisyon bulana kadar döngü
                       x = random.randint(max(0, group_x - 50), min(screenWidth, group_x + 50))  # Grup içindeki pozisyon
                       y = initial_y - i * (circle_radius + 13)  # Meyve aralarına mesafe koy
                       is_fruit = random.choice(["apple", "grape", "skull"])  # Rastgele bir nesne seç

                    # Çakışmayı kontrol et
                       overlap = False
                       for existing_x, existing_y, _, existing_type in circles:
                           if abs(x - existing_x) < circle_radius * 2 and abs(y - existing_y) < circle_radius * 2:
                               if (is_fruit == "skull" and existing_type in ["apple", "grape"]) or \
                                  (is_fruit in ["apple", "grape"] and existing_type == "skull"):
                                   overlap = True
                                   break
                    
                       if not overlap:
                            break  # Eğer çakışma yoksa döngüden çık ve meyveyi ekle
                   circles.append((x, y, "white", is_fruit))  # Meyveyi listeye ekle
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Exit the game if the close button is pressed
            running = False

    keys = pygame.key.get_pressed()

    if not is_failed and not is_paused:  # Update game state if not paused or game over
        # Move plate left or right
        if keys[pygame.K_LEFT] and plate_x > 0:
            plate_x -= plate_speed
        if keys[pygame.K_RIGHT] and plate_x < screenWidth - plate_width:
            plate_x += plate_speed

        # Generate new falling objects
        if random.randint(1, 100) == 1:
            is_fruit = random.choice(["apple", "grape", "skull"])
            x = random.randint(0, screenWidth - circle_radius)
            y = -circle_radius
            circles.append((x, y, "white", is_fruit))

        # Update position of falling objects
        for i, obj in enumerate(circles):
            x, y, color, is_fruit = obj
            y += circle_speed
            circles[i] = (x, y, color, is_fruit)

            # Check for collisions with the plate
            if plate_y <= y <= plate_y + plate_height and plate_x <= x <= plate_x + plate_width:
                if is_fruit == "apple":
                    score += 1  # Increase score for apple
                elif is_fruit == "grape":
                    score += 2  # Increase score for grape
                else:
                    lives -= 1  # Lose a life for skull
                    if lives == 0:
                        is_failed = True
                circles.pop(i)
                break
            elif y > screenHeight:  # Remove objects that fall off the screen
                if is_fruit in ["apple", "grape"]:
                    lives -= 1
                    if lives == 0:
                        is_failed = True
                circles.pop(i)
                break
    elif is_failed:  # If game is over, display game over screen
        game_over()

    

    # Draw game elements
    draw_plate()
    draw_circles()
    show_score()
    show_high_score()
    show_lives()
    draw_pause_button()

    pygame.display.update()
    clock.tick(FPS)

# Quit pygame
pygame.quit()
sys.exit()
