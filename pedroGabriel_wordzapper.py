import pygame
import sys

pygame.init()

largura = 1280
altura = 720

window = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("WordZapper")


while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
