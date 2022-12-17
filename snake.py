import pygame
from sys import exit
from random import randint, choice

pygame.init()
pygame.display.set_caption('hungry snake')
body_index = 1

class snake:
    def __init__(self):
        self.length = 0
        self.snake_position = [] 
        self.snake_position.append((300,300))   
        self.player_snake_head = pygame.sprite.GroupSingle()
        self.player_snake_head.add(self.snake_head())
        self.player_snake_body = pygame.sprite.Group()
        self.new_growing_position = ()
                
    def update(self):
        #draw snake
        self.player_snake_head.draw(screen)
        self.player_snake_head.update()
        self.player_snake_body.draw(screen)
        self.player_snake_body.update()
        self.move_body()

    def move_body(self):
        if self.length == 0: return
        index = 0
        for position in self.snake_position[ :len(self.snake_position) - 1]:
            self.player_snake_body.sprites()[index].rect = self.player_snake_body.sprites()[index].image.get_rect(center = position)
            index+=1
        for i in range(len(self.snake_position)-1,0,-1):
            self.snake_position[i] = self.snake_position[i-1]
        self.snake_position[0] = self.player_snake_head.sprite.rect.center        
    class snake_head(pygame.sprite.Sprite) :

        def __init__ (self) :
            #add the position of snake to snake_position list
            #direction of snake
            self.mode = 0
            #defacult
            self.Direction = W

            super().__init__()
            self.image = pygame.Surface((snake_width,snake_hight))
            self.rect = self.image.get_rect(center = (400,400))
            self.image.fill("red")
        def update(self):
            self.control()
            self.keep_walking()
        def control(self):
            if pygame.key.get_pressed()[pygame.K_w] and self.Direction != S:
                self.Direction = W
            if pygame.key.get_pressed()[pygame.K_s] and self.Direction != W:
                self.Direction = S
            if pygame.key.get_pressed()[pygame.K_a] and self.Direction != D:
                self.Direction = A
            if pygame.key.get_pressed()[pygame.K_d] and self.Direction != A:
                self.Direction = D
        def keep_walking(self):  
            self.rect.center = moving(self)
            
    class snake_body(pygame.sprite.Sprite):
        def __init__(self,position,index):
            self.mode = 0
            self.index = index
            super().__init__()
            self.image = pygame.Surface((snake_width,snake_hight))
            self.image.fill(choice(['green', 'pink', 'brown', 'purple','orange','gray','white']))
            self.rect = self.image.get_rect(center = position)
        def update(self):
            pass


class food(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20,20))
        self.image.fill("blue")
        self.get_food_position_randomly()
        self.rect = self.image.get_rect(center = (self.x,self.y))
    def get_food_position_randomly(self):
        self.y = randint(100,700)
        self.x = randint(100,700)
    def update(self):
        pass


class wall(pygame.sprite.Sprite):
    def __init__(self,index):

        super().__init__()
        self.image = pygame.Surface((800,20))
        self.image = pygame.transform.rotate(self.image, 90*index)
        self.image.fill("yellow")
        self.rect = self.image.get_rect(topleft = four_corner[index])
        print(self.rect)
    def update(self):
        pass


# check collision
def check_collision_between_food_and_snake(player_snake, foods):
    global body_index
    global score
    l_player_snake_head = player_snake.player_snake_head
    l_player_snake_body = player_snake.player_snake_body
    if pygame.sprite.spritecollide(l_player_snake_head.sprite, foods, True):
        score += 1
        player_snake.new_growing_position = player_snake.snake_position[-1]

def check_collision_between_other_and_head(player_snake, walls):
    global Game_failure
    l_player_snake_head = player_snake.player_snake_head
    l_player_snake_body = player_snake.player_snake_body
    if pygame.sprite.spritecollide(l_player_snake_head.sprite, walls, False):
        Game_failure = True
    if pygame.sprite.spritecollide(l_player_snake_head.sprite,l_player_snake_body, False):
        Game_failure = True

def growing(snake):
    global body_index
    if snake.new_growing_position:
        snake.snake_position.append(snake.new_growing_position)
        snake.player_snake_body.add(snake.snake_body(snake.new_growing_position, body_index))
        body_index += 1
        snake.length += 1
        snake.new_growing_position = ()
        

def moving(snack):
    if snack.Direction == W:
        snack.rect.y -= Speed
    elif snack.Direction == S:
        snack.rect.y += Speed
    elif snack.Direction == A:
        snack.rect.x -= Speed
    elif snack.Direction == D:
        snack.rect.x += Speed
    if snack.mode == 0:
        if snack.rect.y > 800:
            snack.rect.y = 0
        elif snack.rect.y < 0:
            snack.rect.y = 800
        if snack.rect.x > 800:
            snack.rect.x = 0
        elif snack.rect.x < 0:
            snack.rect.x = 800 
    return snack.rect.center

def show_score(score):
    text_surface = test_font.render(f'your score is {score}',False, 'red', 'white')
    test_position = text_surface.get_rect(center = (400,400))
    screen.blit(text_surface,test_position)
def show_difficulty():
    text_surface = test_font_2.render(f'the difficulty now is {Difficulty}  (left and right arrow to control its difficulty)', False, 'red', 'white')
    test_position = text_surface.get_rect(bottomleft = (30,750))
    screen.blit(text_surface, test_position)
def show_instruction():
    instruction_surface = test_font.render("click '0' to restart", False,'red')
    instruction_width = instruction_surface.get_width()+10
    instruction_Rect = pygame.Rect(0,0,instruction_width,40)
    #place the rectangle at middle of screen
    instruction_Rect.center = (400,400)
    #draw the rectangle
    pygame.draw.rect(screen,'white',instruction_Rect)
    #draw the text surface
    screen.blit(instruction_surface,(instruction_Rect.x+5,instruction_Rect.y+5)) 

#basic set
food_limitation = 3
clock = pygame.time.Clock()
snake_hight = 20
snake_width = 20
Speed = 21
screen = pygame.display.set_mode((800,800))
test_font = pygame.font.Font(None, 50)
test_font_2 = pygame.font.Font(None, 30)
wall_width = 20
four_corner = [(0,0),(0,0),(0,800 - wall_width),(800 - wall_width,0)]

#set: need 4 walls in group
walls = pygame.sprite.Group()
for i in range(0,4):
    walls.add(wall(i))

#four direction
W = 1
S = 2
A = 3
D = 4
#sprite
foods = pygame.sprite.Group()


#new event to appear food randomly 
food_appear_event = pygame.USEREVENT + 1
pygame.time.set_timer(food_appear_event, 2000)

#map
ground = pygame.Surface((800,800))
ground.fill('black')


def check_user_input(user_text):
    if len(user_text) == 0:
        return ''
    else :
        if user_text == 'c':
            return ''
        return ''
def restart():
    global Stop 
    global Game_failure
    global Difficulty
    global timer
    global user_text
    global score

    Difficulty = 5
    Stop = False
    Game_failure = False
    timer = 0
    user_text = ''
    score = 0

player_snake = snake()
restart()
while True:
    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            pygame.quit()
            exit()
        if event.type == food_appear_event and len(foods) < food_limitation:
            foods.add(food())
        if event.type == pygame.KEYDOWN:
            user_text += event.unicode
            if event.key == pygame.K_SPACE:
                if Stop :
                    Stop = False
                else:
                    Stop = True
            elif event.key == pygame.K_LEFT:
                Difficulty -= 1
                timer = 0
                if Difficulty <= 0: Difficulty = 1
            elif event.key == pygame.K_RIGHT:
                Difficulty += 1
                timer = 0
                if Difficulty > 10: Difficulty = 10
            elif event.key == pygame.K_0:
                restart()
                player_snake.__init__()
    if  not Stop and not Game_failure :
        #growing must place at before of collision between body and head
        # l store position of last body position for placing new body
        growing(player_snake)
        #map
        screen.blit(ground, (0,0))
        #draw wall
        walls.draw(screen)
        walls.update()
        #draw food
        foods.draw(screen)
        foods.update()
        #check collision
        check_collision_between_food_and_snake(player_snake, foods)
        check_collision_between_other_and_head(player_snake, walls)
        #show_score(score)
        show_score(score)
        show_difficulty()
        #show snake
        #user timer to control speed of snake
        timer += 1
        if timer == Difficulty:
            player_snake.update()
            pygame.display.update()  
            timer = -1
        # user input
        user_text = check_user_input(user_text)
        # set
        clock.tick(90)
    elif Game_failure:
        foods.empty()
        screen.blit(ground, (0,0))
        show_instruction()
        pygame.display.update()  
