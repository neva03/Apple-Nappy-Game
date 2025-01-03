import pygame
import random
import sys
pygame.init()

screenWidth =800
screenHeight=600
#screen
gameDisplay = pygame.display.set_mode((screenWidth,screenHeight)) 
#name of the game
pygame.display.set_caption('fruit nappy') 

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
yellow =(255,255,0)
pink=(255,0,255)
light_blue = (0, 200, 255)

# FPS
clock = pygame.time.Clock()
FPS = 60

#Plate
plate_width=100
plate_height = 20
plate_x = (screenWidth - plate_width) // 2
plate_y = screenHeight- plate_height - 10
plate_speed = 8

is_failed = False 
score = 0

circle_radius = 20
circle_speed = 5
circles = [] 

# Font
font = pygame.font.Font(None, 36)

def draw_plate():
    pygame.draw.rect(gameDisplay, light_blue, (plate_x, plate_y,plate_width,plate_height))
def draw_circles():
    for c in circles:
        x, y, color, _ = c
        pygame.draw.circle(gameDisplay, color, (x, y), circle_radius)

def show_score():
    text = font.render(f"Score: {score}", True, black)
    gameDisplay.blit(text, (10, 10))
def game_over():
    text = font.render("Game Over!", True, red)
    gameDisplay.blit(text, (screenWidth // 2 - 100, screenHeight// 2 - 50))
running = True
while running:
    #Fills the screen white
    gameDisplay.fill(white)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Kullanıcı pencereyi kapatmak isterse
            running = False
    #moves the plate
    keys = pygame.key.get_pressed()
    if not is_failed:
        if keys[pygame.K_LEFT] and plate_x > 0:
            plate_x -= plate_speed
        if keys[pygame.K_RIGHT] and plate_x < screenWidth - plate_width:
            plate_x += plate_speed
        #gökten eşya yağması 
        #rastgele sayı 1 ise meyve oluştur
        if random.randint(1, 100) == 1: #oyunu zorlaştırmak için 100'ü azaltabiliriz daha çok meyve akar
            is_fruit = random.choice([True, False])
            if is_fruit: #meyve renkleri şimdilik yeşil ve pembe
                color =random.choice([green,pink])
            else: #kurukafanın rengi kırmızı
                color=red
            x = random.randint(0, screenWidth - circle_radius)
            y = -circle_radius
            circles.append((x, y, color, is_fruit))
        for i, obj in enumerate(circles):
            x, y, color, is_fruit = obj
            y += circle_speed
            circles[i] = (x, y, color, is_fruit)
            #tabak meyveyi yakalarsa
            if plate_y <= y <= plate_y + plate_height and plate_x <= x <= plate_x + plate_width:
                if is_fruit:
                    score += 1
                else: #kurukafayı yakalarsa yan
                    is_failed = True
                circles.pop(i) #obje ekrandan çıktığı için sil objeyi
                break
            # meyve yere düşerse
            elif y > screenHeight:
                if is_fruit:
                    is_failed = True
                circles.pop(i)
                break
    else:
        game_over()
    draw_plate()
    draw_circles()
    show_score()

    #update the screen
    pygame.display.update()
    clock.tick(FPS)
# Pygame'den çık
pygame.quit()
sys.exit()
