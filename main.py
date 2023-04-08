# Relevant modules
import pygame
import time 
# Initializations
pygame.font.init()
pygame.mixer.pre_init(22100,-16,2,0)
pygame.mixer.init()
pygame.init()
# Display Settings
# Display width and height
WIDTH,HEIGHT = 900, 500
# WIN variable assigned to the visible image "surface" on display
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
# Name of the display
pygame.display.set_caption("First Game :D")
# Color of the background plus the modified background
BACKGROUND = pygame.image.load("galaxybackground.webp")
modified_back = pygame.transform.scale(BACKGROUND,(900,500))
# Colors
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)
WHITE = (255,255,255)
# Font
HEALTH_FONT = pygame.font.SysFont("comicsans",40)
# Sounds
GAME_SOUND = pygame.mixer.Sound("gamemusic.mp3")
BLASTER_SOUND = pygame.mixer.Sound("Gun+Silencer.mp3")
ON_HIT_SOUND = pygame.mixer.Sound("Grenade+1.mp3")
WINNER_SOUND = pygame.mixer.Sound("winsound.mp3")
# Game events
RED_HIT = pygame.USEREVENT + 1
YELLOW_HIT = pygame.USEREVENT + 2
# Game settings
# Max fps for the game
FPS = 60
# This is our border
BORDER = pygame.Rect(WIDTH // 2 - 5,0,5,HEIGHT)

# Mouse position
# mouse_pos = pygame.mouse.get_pos

# On screen elements 
WASD = pygame.image.load("wasd.png")
ARROWS = pygame.image.load("arrows.png")
LEFT_CONTROLS = pygame.transform.scale(WASD,(400,400))
RIGHT_CONTROLS = pygame.transform.scale(ARROWS,(400,400))
# Characters
# Spaceship images
YELLOW_SPACESHIP_IMAGE = pygame.image.load("spaceship_yellow.png").convert_alpha()
RED_SPACESHIP_IMAGE = pygame.image.load("spaceship_red.png")

# Desired Width and Height of the ships
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55,40

# Transformed spaceships assigned to new variables that will be used
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE,(SPACESHIP_WIDTH,SPACESHIP_HEIGHT)),90)
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE,(SPACESHIP_WIDTH,SPACESHIP_HEIGHT)),270)

# Velocity of the ships
VEL = 6

# Set the velocity of the bullets
BULLET_VEL = 15
MAX_BULLETS = 3

#-------------------------------------------------------------------#
# This function is still be worked on. New addition to the game
# def draw_main():
#   print(mouse_pos)
    
#   WIN.blit(modified_back,(0,0))
#   Play_Button = HEALTH_FONT.render("PLAY",1,WHITE)
#   WIN.blit(Play_Button,(WIDTH // 2 , HEIGHT // 2))
#   pygame.display.update()
#-------------------------------------------------------------------#

# This function draws everything to the screen
def draw_function(red,yellow,YELLOW_BULLETS,RED_BULLETS,YELLOW_HEALTH,RED_HEALTH):
  WIN.blit(modified_back,(0,0))
  # Add the left control and right control images to the screen
  WIN.blit(LEFT_CONTROLS,(190, 240))
  WIN.blit(RIGHT_CONTROLS,(WIDTH - 110, HEIGHT - 80))
  # The text for the specific fire buttons
  yellow_fire_text = HEALTH_FONT.render("'space' - To fire",1,WHITE)
  red_fire_text = HEALTH_FONT.render("'.' - To fire",1,WHITE)
  # Creating the string for the health text variables
  yellow_health_text = HEALTH_FONT.render("Health:" + str(YELLOW_HEALTH),1,WHITE)
  red_health_text = HEALTH_FONT.render("Health:" + str(RED_HEALTH),1,WHITE)
  # Drawing the yellow and red health text 
  WIN.blit(yellow_health_text,(WIDTH // 6, 10))
  WIN.blit(red_health_text,(625,10))
  # Drawing the yellow and red "to-fire" text
  WIN.blit(yellow_fire_text,(10,450))
  WIN.blit(red_fire_text,(BORDER.x + BORDER.width + 10, 450))
  # Draw the spaceships on the screen at the position of the red and yellow rectangles passed in
  WIN.blit(YELLOW_SPACESHIP,(yellow.x,yellow.y))
  WIN.blit(RED_SPACESHIP,(red.x,red.y))
  # Draw our border
  pygame.draw.rect(WIN,BLACK,BORDER)
  # Draw the bullets
  for bullet in YELLOW_BULLETS:
    pygame.draw.rect(WIN,YELLOW,bullet)
  for bullet in RED_BULLETS:
    pygame.draw.rect(WIN,RED,bullet)
  # Update the display 
  pygame.display.update()

# This function is used to handle the winning event
def call_winner(text):
  # Play the winner music
  WINNER_SOUND.play()
  # Create the text itself
  winner_text = HEALTH_FONT.render(text,1,WHITE)
  # Add the background to the display
  WIN.blit(modified_back,(0,0))
  # Put the winner text in the middle of the screen
  WIN.blit(winner_text,(WIDTH // 2 - 100 ,HEIGHT // 2 ))
  # Update the display
  pygame.display.update()
  # Stop the game for 3 seconds
  pygame.time.delay(3000)

# This function controls the bullets
def handle_bullets(YELLOW_BULLETS,RED_BULLETS,yellow,red):
  # For every yellow bullet
  for yellow_bullet in YELLOW_BULLETS:
    # Move to the right
    yellow_bullet.x += BULLET_VEL
    # If yellow bullet goes off the screen
    if yellow_bullet.x > WIDTH :
      # Remove it from the yellow bullet list
      YELLOW_BULLETS.remove(yellow_bullet)
    # If the yellow bullet collides with the red player
    if red.colliderect(yellow_bullet) :
      # Remove it from the yellow bullet list
      YELLOW_BULLETS.remove(yellow_bullet)
      # Call the Red_Hit event
      pygame.event.post(pygame.event.Event(RED_HIT)) 
  # For every red bullet
  for red_bullet in RED_BULLETS:
    # Move the the left
    red_bullet.x -= BULLET_VEL
    # If red bullet goes of the screen
    if red_bullet.x < 0 :
      # Remove it from the red bullet list
      RED_BULLETS.remove(red_bullet)
    # If the red bullet collides with the yellow player
    if yellow.colliderect(red_bullet) :
      # Remove it from the yellow bullet list
      RED_BULLETS.remove(red_bullet)
      # Call the Yellow_Hit event
      pygame.event.post(pygame.event.Event(YELLOW_HIT))
  
# This function controls the movement of the yellow ship
def yellow_movement(keys_pressed,yellow):
  # If w is pressed and off the screen
  if keys_pressed[pygame.K_w] and yellow.y - 5 > 0:
    yellow.y -= VEL
  # If s pressed and off the screen
  if keys_pressed[pygame.K_s] and yellow.y + yellow.height + 20 < HEIGHT:
    yellow.y += VEL
  # If a pressed and off the screen
  if keys_pressed[pygame.K_a] and yellow.x - 5 > 0:
    yellow.x -= VEL
  # If d pressed and is passed the borders x plus yellow width
  if keys_pressed[pygame.K_d] and yellow.x + yellow.width - 15 < BORDER.x:
    yellow.x += VEL
    
# This function controls the movement of the red ship
def red_movement(keys_pressed,red):
  # If arrow_up pressed and off the screen
  if keys_pressed[pygame.K_UP] and red.y  - 5 > 0:
    red.y -= VEL
  # If arrow_down pressed and off the screen
  if keys_pressed[pygame.K_DOWN] and red.y + red.height + 20 < HEIGHT:
    red.y += VEL
  # If arrow_left pressed and at borders x plus the borders width
  if keys_pressed[pygame.K_LEFT] and red.x > BORDER.x + BORDER.width:
     red.x-= VEL
  # If arrow_right pressed and off the screen
  if keys_pressed[pygame.K_RIGHT] and red.x + red.width - 10 < WIDTH:
    red.x += VEL

# This function controls what happens when the specified fire keys are pressed
def key_down(event,YELLOW_BULLETS,RED_BULLETS,yellow,red):
  # If the event is keydown
  if event.type == pygame.KEYDOWN:
    # If the key is a period and we haven't reached the max red bullets
    if event.key == pygame.K_PERIOD and len(RED_BULLETS) < MAX_BULLETS:
      # Play the blaster sound
      BLASTER_SOUND.play()
      # Create the red bullet
      bullet = pygame.Rect(red.x - 15,red.y + red.height // 2 + 5 ,10,5)
      # Add it to the red bullets list
      RED_BULLETS.append(bullet)
      print("Period button is down")
    # If the key is a space and we haven't reached the max yellow bullets
    if event.key == pygame.K_SPACE and len(YELLOW_BULLETS) < MAX_BULLETS:
      # Play the blaster sound
      BLASTER_SOUND.play()
      # Create the yellow bullet
      bullet = pygame.Rect(yellow.x + yellow.width - 5,yellow.y + yellow.height // 2 + 3 , 10, 5)
      # Add it to the yellow bullets list
      YELLOW_BULLETS.append(bullet)
      print("Space button is down")


# Main game function
def main():
  # Variable to log the time the main function was started
  start_time = time.time()
  
  # The hit_boxes or actual positions of the players
  yellow = pygame.Rect(225,250,SPACESHIP_WIDTH,SPACESHIP_HEIGHT)
  red = pygame.Rect(675,250,SPACESHIP_WIDTH,SPACESHIP_HEIGHT)
  # Lists for the each players bullets
  YELLOW_BULLETS = []
  RED_BULLETS = []
  # Clock for the FPS
  clock = pygame.time.Clock()
  # Character Health variables
  YELLOW_HEALTH = 10
  RED_HEALTH = 10
  # The delay to prevent players from shooting temporarily 
  shoot_delay = 2
  # Our while loop variable that keeps it running
  run = True
  #-------------------------------------------------------------------#
  #Function and variable I want to add later, currently testing this
  # main = False
  # while main: 
  #   draw_main()
  #-------------------------------------------------------------------#
  # Start the game music
  GAME_SOUND.play()
  # This loop will run until run is False
  while run:
    clock.tick(FPS)
    current_time = time.time() - start_time
    # loop through the events of pygame 
    for event in pygame.event.get():
      # If the event is equal to quit event
      if event.type == pygame.QUIT:
        # Exit the run loop for the game
        run = False
        # Close the app after game stops running
        pygame.quit()
        print("Application has quit")
     # If the event is equal to the red_hit event
      if event.type == RED_HIT :
        ON_HIT_SOUND.play()
        RED_HEALTH -= 1
        print("RED HAS BEEN HIT")
    # If the event is equal to the yellow_hit event
      if event.type == YELLOW_HIT :
        ON_HIT_SOUND.play()
        YELLOW_HEALTH -= 1
        print("YELLOW HAS BEEN HIT")
     # If the current time is > then the shoot delay 
      if current_time > shoot_delay :
         # This function handles what happend when the key_down event is fired
        key_down(event,YELLOW_BULLETS,RED_BULLETS,yellow,red)
    # New variable assigned to the key pressed
    keys_pressed = pygame.key.get_pressed()
    # This function handles the yellow players movement
    yellow_movement(keys_pressed,yellow)
    # This function handles the red player movement
    red_movement(keys_pressed,red)
    # This function udpates the screen with the elements that are passed in 
    draw_function(red,yellow,YELLOW_BULLETS,RED_BULLETS,YELLOW_HEALTH,RED_HEALTH)
    # This function controls the bullets created by the key down function 
    handle_bullets(YELLOW_BULLETS,RED_BULLETS,yellow,red)
    # A variable assigned to an empty string, our winner text
    winner_text = ''
    # When yellow health reaches 0 or lower
    if YELLOW_HEALTH <= 0 :
      winner_text = "Red Wins"
    # When red health reaches 0 or lower
    if RED_HEALTH <= 0 :
      winner_text = "Yellow Wins"
    # If the winner_text is not an empty string
    if winner_text != '':
    # Stop the music
      GAME_SOUND.stop()
      # This function put the text winner text in the middle of the screen and pauses the game for a specific delay
      call_winner(winner_text)
      # Exit the while loop
      break
  
  # Once the pause is over restart the game
  main()
  
# If the file name is main then call the main function. This is useful so if any other files import this file. It will not automatically run
if __name__ == "__main__":
  main()

