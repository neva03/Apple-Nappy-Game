import pygame
import random
import sys

pygame.init()

screenWidth = 800
screenHeight = 600

# Screen
gameDisplay = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption('Fruit Nappy')

# Colors
black = (0, 0, 0)
red= (230, 0, 0)
light_blue = (0, 200, 255)

# FPS
clock = pygame.time.Clock()
FPS = 60

# Plate
plate_width = 100
plate_height = 20
plate_x = (screenWidth - plate_width) // 2
plate_y = screenHeight - plate_height - 10
plate_speed = 8

is_failed = False
score = 0
lives = 3  # Starting health point

circle_radius = 20
circle_speed = 6.3
circles = []

# Health points
heart_image = pygame.image.load(r"heart.png")
heart_image = pygame.transform.scale(heart_image, (40, 40))

# Fruits
apple_image = pygame.image.load(r"apple.png")
apple_image = pygame.transform.scale(apple_image, (60, 60))

grape_image = pygame.image.load(r"grape.png")
grape_image = pygame.transform.scale(grape_image, (60, 60))  

# Skull
skull_image = pygame.image.load(r"skull.png")
skull_image = pygame.transform.scale(skull_image, (60, 60)) 

# Background
background_image = pygame.image.load(r"background1.png")
background_image = pygame.transform.scale(background_image, (screenWidth, screenHeight)) 

# Monkey (Plate) Image
monkey_image = pygame.image.load(r"monkey.png")
monkey_image = pygame.transform.scale(monkey_image, (70, 70))  # Plate'in boyutlarına uygun

# Font
font = pygame.font.Font(None, 36)

def draw_plate():
     plate_y =+510
     gameDisplay.blit(monkey_image, (plate_x, plate_y))
    #pygame.draw.rect(gameDisplay, light_blue, (plate_x, plate_y, plate_width, plate_height))

def draw_circles():
    for c in circles:
        x, y, color, is_fruit = c
        if is_fruit == "apple":  
            gameDisplay.blit(apple_image, (x - circle_radius, y - circle_radius))
        elif is_fruit == "grape":  
            gameDisplay.blit(grape_image, (x - circle_radius, y - circle_radius))
        elif is_fruit == "skull":  
            gameDisplay.blit(skull_image, (x - circle_radius, y - circle_radius))

def show_score():
    text = font.render(f"Score: {score}", True, black)
    gameDisplay.blit(text, (10, 10))

def show_lives():
    for i in range(lives):
        gameDisplay.blit(heart_image, (screenWidth - 150 + i * 50, 10))

def draw_button(text, x, y, width, height, inactive_color, active_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    # Buton renklendirme
    if x < mouse[0] < x + width and y < mouse[1] < y + height:
        pygame.draw.rect(gameDisplay, active_color, (x, y, width, height))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(gameDisplay, inactive_color, (x, y, width, height))

    # Buton yazısı
    button_font = pygame.font.Font(None, 36)
    text_surface = button_font.render(text, True, black)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    gameDisplay.blit(text_surface, text_rect)

def restart_game():
    global is_failed, score, circles, plate_x, lives
    is_failed = False
    score = 0
    lives = 3
    circles = []
    plate_x = (screenWidth - plate_width) // 2

def game_over():
    # Game Over yazısını çiz
    text = font.render("Game Over!", True, black)
    text_rect = text.get_rect(center=(screenWidth // 2, screenHeight // 2 - 50))
    gameDisplay.blit(text, text_rect)

    # Restart butonunu çiz
    button_width = 120
    button_height = 50
    button_x = screenWidth // 2 - button_width // 2
    button_y = screenHeight // 2 + 20
    draw_button("Restart", button_x, button_y, button_width, button_height, light_blue, black, restart_game)

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

def start_game():
    countdown()

running = True
started = False
while running:

    gameDisplay.blit(background_image, (0, 0))  # Arka planı çiz

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not started:
        button_width = 120
        button_height = 50
        button_x = screenWidth // 2- button_width // 2
        button_y = screenHeight // 2
        draw_button("Start", button_x, button_y, button_width, button_height, light_blue, black, lambda: start_game())
        if pygame.mouse.get_pressed()[0]:
            started = True
    else:
        keys = pygame.key.get_pressed()
        if not is_failed:
            if keys[pygame.K_LEFT] and plate_x > 0:
                plate_x -= plate_speed
            if keys[pygame.K_RIGHT] and plate_x < screenWidth - plate_width:
                plate_x += plate_speed

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

            for i, obj in enumerate(circles):
                x, y, color, is_fruit = obj
                y += circle_speed
                circles[i] = (x, y, color, is_fruit)

                if plate_y <= y <= plate_y + plate_height and plate_x <= x <= plate_x + plate_width:
                    if is_fruit == "apple":
                        score += 1  # Elma yakalarsa puan ekle
                    elif is_fruit == "grape":
                        score += 2  # Üzüm yakalarsa daha fazla puan ekle
                    else:
                        lives -= 1  # Kafatası yakalarsa can eksilt
                        if lives == 0:  # Eğer can bitmişse oyun sonu
                            is_failed = True
                    circles.pop(i)
                    break
                elif y > screenHeight:
                    if is_fruit == "apple" or is_fruit == "grape":
                        lives -= 1
                        if lives == 0:
                            is_failed = True
                    circles.pop(i)
                    break
        else:
            game_over()

        draw_plate()
        draw_circles()
        show_score()
        show_lives()

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
sys.exit()

