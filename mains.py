import pygame
width,height = 500,500
WIN = pygame.display.set_mode((width,height))
pygame.display.set_caption("Testgame")

FPS = 60
Speed = 5

pos_x,pos_y = width / 2, 400
ship_width,ship_height = 50,60
red_space_ship = pygame.image.load("spaceship_red.png")
red_ship = pygame.transform.rotate(pygame.transform.scale(red_space_ship,(ship_width,ship_height)),180)

def draw_shapes(red):
  WIN.fill(255)
  WIN.blit(red_ship,(red.x,red.y,ship_width,ship_height))
  pygame.display.update()

def red_movement(key_pressed,red):
  if key_pressed[pygame.K_LEFT]:
    red.x -= Speed
  if key_pressed[pygame.K_RIGHT]:
    red.x += Speed
    
def main():
  clock = pygame.time.Clock()
  red = pygame.Rect(pos_x,pos_y,ship_width,ship_height)
  run = True
  while run :
    clock.tick(FPS)
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False
        print("hello")
    draw_shapes(red)
    key_pressed = pygame.key.get_pressed()
    red_movement(key_pressed,red)
  pygame.quit()



if __name__ == "__main__" :
  main()