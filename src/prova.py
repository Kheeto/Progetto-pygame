import pygame
from characters.elf import Elf
from characters.goblin import Goblin

pygame.init()

FPS = 60

screen = pygame.display.set_mode((1188, 737), pygame.RESIZABLE)
pygame.display.set_caption("Gioco fighissimo")
clock = pygame.time.Clock()

elf = Elf()
goblin = Goblin()

while True:   
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # prova per l'elfo
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                elf.shoot()
            if event.key == pygame.K_b:
                elf.blink()
            if event.key == pygame.K_r:
                elf.run()

        #prova per il goblin
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                goblin.run()

    screen.fill('Black')
    elf.render(screen, (0,0))
    goblin.render(screen, (0,500))

    pygame.display.flip()
    clock.tick(FPS)