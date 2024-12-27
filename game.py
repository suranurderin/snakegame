import pygame, sys, random

# Ekran boyutlari
screen_width = 600
screen_height = 600

pygame.display.set_caption("Yılan Oyunu")

# Oyunun izgarasinin hucre boyutunu (20x20) ve ekrani kac hucreye bolecegini belirleme
gridsize = 20 
grid_width = screen_width // gridsize 
grid_height = screen_height // gridsize

#İzgarayi , yilani ve yiyecegi temsil eden renkleri tanimlama
light_green = (144,238,144)
dark_green = (124,205,124)
food_color = (255, 255, 0)
snake_color = (139, 69, 0)

# Yilanin hareket edecegi yonlerin koordinatlarini belirtme
up = (0,-1)
down = (0, 1)
right = (1,0)
left = (-1,0)

# Yilanin hareketini, cizimini ve kntrolunu saglama
class SNAKE: 
   def __init__(self): # __init__ metodu yilanin baslangic durumunu tanimlar
      self.positions = [((screen_width/2), (screen_height/2))] # Yilanin her bir parcasinin koordinatlarini tutar
      self.length = 1 # Yilanin uzunlugunu takip eder
      self.direction = random.choice([up,down,left,right]) # Yilanin mevcut hareket yonu 
      self.color = snake_color # Yilanin rengi tanimalama
      self.score = 0 # Oyuncunun puani

   def draw(self, surface): # Bu metot yilanin pozisyonlarini cizer
        for p in self.positions:
            rect = pygame.Rect(p,(gridsize, gridsize))
            pygame.draw.rect(surface,self.color,rect)
   def move(self): # Yilani belirtilen yönde hareket ettirir. Duvara ya da kuyruguna değerse score'u sifirlar
      current = self.positions[0]
      x,y = self.direction
      new = ((current[0] + (x * gridsize)), (current[1] + (y * gridsize)))

      if new[0] in range(0, screen_width) and new[1] in range(0, screen_height) and not new in self.positions[2:]:
         self.positions.insert(0,new)
         if len(self.positions) > self.length:
            self.positions.pop()
      else:
         self.reset()

   def reset(self): # Yilani baslangic durumuna dondurur.
      self.length = 1
      self.positions = [((screen_width/2), (screen_height/2))]
      self.direction = random.choice([up,down,left,right])
      self.score = 0

   def handle_keys(self): # Ok tuslarini dinler ve yon degisikliklerini uygular
      for event in pygame.event.get():
            if event.type == pygame.QUIT:
             pygame.quit()
             sys.exit()
            elif event.type == pygame.KEYDOWN: # Yilanin yon degistirme kontrolu
               if event.key == pygame.K_UP:
                  self.turn(up)
               elif event.key == pygame.K_DOWN:
                  self.turn(down)
               elif event.key == pygame.K_RIGHT:
                  self.turn(right)
               elif event.key == pygame.K_LEFT:
                  self.turn(left)

   def turn(self, direction): # Yilanin yeni degistirir ancak ters yone donmesini engeller
      if (direction[0] * -1, direction[1] * -1) == self.direction:
         return
      else:
         self.direction = direction

      
class FOOD: 
    def __init__(self): # Bu sefer __init__ metodu, yemin baslangic durumunu tanimliyor ve rastgele bir pozisyona atiyor
      self.position = (0,0) # Yemin ekrandaki koordinatlarini tutar
      self.color = food_color # Yemin rengini tanimlama
      self.random_position() 
    def random_position(self): # Yemi ekrandaki rastgele bir konuma yerlestirir.
      self.position = (random.randint(0,grid_width-1)*gridsize,random.randint(0, grid_height-1)*gridsize)
    def draw(self, surface): # Yemi ekranda cizer
      rect = pygame.Rect((self.position[0], self.position[1]), (gridsize,gridsize))
      pygame.draw.rect(surface, self.color,rect)


def drawGrid(surface):
   for y in range(0, int(grid_height)):
      for x in range(0, int(grid_width)):
         if (x+y) % 2 == 0:
            light = pygame.Rect((x * gridsize, y*gridsize), (gridsize,gridsize))
            pygame.draw.rect(surface, light_green, light)
         else:
            dark = pygame.Rect((x * gridsize, y*gridsize), (gridsize,gridsize))
            pygame.draw.rect(surface, dark_green, dark)

def load_high_score(difficulty):
   filename = f"high_score_{difficulty}.txt"
   try:
        with open(filename, "r") as file:
            return int(file.read())
   except FileNotFoundError:
        return 0

def save_high_score(difficulty, score):
    filename = f"high_score_{difficulty}.txt"
    with open(filename, "w") as file:
        file.write(str(score))

def main():
    pygame.init()

    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 20)
    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()

    difficulties = {"Kolay": 5, "Orta": 10, "Zor": 15}
    state = "menu"

    selected_difficulty = None
    snake_speed = None
    high_score = 0

    while True:
        if state == "menu": # Zorluk seviyesi secme
            screen.fill((255, 255, 255))
            title_text = font.render("Zorluk Seviyesi Seçin", True, (0, 0, 0))
            screen.blit(title_text, (screen_width // 2 - 100, screen_height // 4))

            easy_button = pygame.Rect(screen_width // 2 - 50, screen_height // 2 - 60, 100, 40)
            medium_button = pygame.Rect(screen_width // 2 - 50, screen_height // 2, 100, 40)
            hard_button = pygame.Rect(screen_width // 2 - 50, screen_height // 2 + 60, 100, 40)

            pygame.draw.rect(screen, (0, 255, 0), easy_button)
            pygame.draw.rect(screen, (255, 255, 0), medium_button)
            pygame.draw.rect(screen, (255, 0, 0), hard_button)

            easy_text = font.render("Kolay", True, (0, 0, 0))
            medium_text = font.render("Orta", True, (0, 0, 0))
            hard_text = font.render("Zor", True, (0, 0, 0))

            screen.blit(easy_text, (screen_width // 2 - 25, screen_height // 2 - 50))
            screen.blit(medium_text, (screen_width // 2 - 25, screen_height // 2 + 10))
            screen.blit(hard_text, (screen_width // 2 - 25, screen_height // 2 + 70))

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if easy_button.collidepoint(event.pos):
                        selected_difficulty = "Kolay"
                        state = "game"
                    elif medium_button.collidepoint(event.pos):
                        selected_difficulty = "Orta"
                        state = "game"
                    elif hard_button.collidepoint(event.pos):
                        selected_difficulty = "Zor"
                        state = "game"

            if state == "game": # Yilanin hareketini, yem ile etkileşimini ve skor artişini kontrol etme
                high_score = load_high_score(selected_difficulty)
                snake_speed = difficulties[selected_difficulty]
                snake = SNAKE()
                food = FOOD()

        elif state == "game":
            clock.tick(snake_speed)
            snake.handle_keys()
            snake.move()
            drawGrid(surface)

            if snake.positions[0] == food.position:
                snake.length += 1
                snake.score += 1
                food.random_position()

            snake.draw(surface)
            food.draw(surface)
            screen.blit(surface, (0, 0))

            if snake.score > high_score:
                high_score = snake.score
                save_high_score(selected_difficulty, high_score)

            # Menüye Dön Butonu
            back_button = pygame.Rect(screen_width - 110, 10, 100, 40)
            pygame.draw.rect(screen, (200, 0, 0), back_button)
            back_text = font.render("Menüye Dön", True, (255, 255, 255))
            screen.blit(back_text, (screen_width - 105, 20))

            score_text = font.render(f"Score: {snake.score}", True, (0, 0, 0))
            high_score_text = font.render(f"High Score ({selected_difficulty}): {high_score}", True, (0, 0, 0))
            screen.blit(score_text, (10, 10))
            screen.blit(high_score_text, (10, 50))

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT: # Oyunu kapatma
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:  # Buton tiklamasinin kontrolu
                    if back_button.collidepoint(event.pos):
                        state = "menu"

main()






