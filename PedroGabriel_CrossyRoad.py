import pygame
import sys

pygame.init()

relogio = pygame.time.Clock()

# configs posicao frog
posicao_frog_x = 380  # posicao max 745 - min 12 - - 380
posicao_frog_y = 530

# posicao dos carros primeira parte

# configs carro 1.1
carro1_posicao_x = 800
carro1_posicao_y = 398
velocidade_car1 = 9

# configs carro 2.1
carro2_posicao_x = -120
carro2_posicao_y = 330
velocidade_car2 = 11

# configs carro 3.1
carro3_posicao_x = 930
carro3_posicao_y = 470
velocidade_car3 = 14

# posicao dos carros na segunda parte!!!

# configs carro 1.2
carro1_posicao_x_2 = 800
carro1_posicao_y_2 = 144

# configs carro 2.2
carro2_posicao_x_2 = -190
carro2_posicao_y_2 = 175

# configs carro 3.2
carro3_posicao_x_2 = -100
carro3_posicao_y_2 = 57


posicao_iglu_x = 315
posicao_iglu_y = 530

posicao_core_x = 366
posicao_core_y = 10

largura = 800
altura = 600
# velocidade tartaruga
velocidade = 3.5

window = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Crossy Road")

# load imagens
tamanho_pinguim = (55, 65)

pinguin_direita = pygame.image.load('pinguim_direita.png')
pinguin_direita = pygame.transform.scale(pinguin_direita, tamanho_pinguim)

pinguin_esquerda = pygame.image.load('pinguim_esquerda.png')
pinguin_esquerda = pygame.transform.scale(pinguin_esquerda, tamanho_pinguim)

pinguim_rect = pygame.Rect(posicao_frog_x, posicao_frog_y, pinguin_direita.get_width() - 30, pinguin_direita.get_height() - 30)


background = pygame.image.load('background_frogger.png')
background = pygame.transform.scale(background, (largura, altura))

carro1 = pygame.image.load('carro_azul_direita.png')
carro1 = pygame.transform.scale(carro1, (120, 75))

carro2 = pygame.image.load('carro_azul2_esquerda.png')
carro2 = pygame.transform.scale(carro2, (120, 65))

carro3 = pygame.image.load('caminhao_esquerda.png')
carro3 = pygame.transform.scale(carro3, (120, 65))

carro4 = pygame.image.load('carro_azul_esquerda.png')
carro4 = pygame.transform.scale(carro4, (110, 50))

carro5 = pygame.image.load('carro5.png')
carro5 = pygame.transform.scale(carro5, (120, 135))

carro6 = pygame.image.load('carro6.png')
carro6 = pygame.transform.scale(carro6, (125, 80))

iglu = pygame.image.load('iglu.png')
iglu = pygame.transform.scale(iglu,(74,70))

coracao = pygame.image.load('coracao.png')
coracao = pygame.transform.scale(coracao,(79,52))
coracao_rect = pygame.Rect(posicao_core_x, posicao_core_y, coracao.get_width(), coracao.get_height() - 30)

def personagem_right():
    global pinguin_direita
    pinguin_direita = pygame.image.load('pinguim_direita.png')
    pinguin_direita = pygame.transform.scale(pinguin_direita, tamanho_pinguim)

def personagem_left():
    global pinguin_esquerda
    pinguin_esquerda = pygame.image.load('pinguim_esquerda.png')
    pinguin_esquerda = pygame.transform.scale(pinguin_esquerda, tamanho_pinguim)

personagem_right()  # Inicializa o pinguim virado para a direita

while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # movimentacao do sapo
    comandos = pygame.key.get_pressed()
    if comandos[pygame.K_UP] and posicao_frog_y >= 0:
        posicao_frog_y -= velocidade
    if comandos[pygame.K_DOWN] and posicao_frog_y <= 535:
        posicao_frog_y += velocidade
    if comandos[pygame.K_RIGHT] and posicao_frog_x <= 745:
        personagem_right()
        posicao_frog_x += velocidade
    if comandos[pygame.K_LEFT] and posicao_frog_x >= 12:
        personagem_left()
        posicao_frog_x -= velocidade

    # CONFIGS CARRO 1.1
    if carro1_posicao_x >= 850:
        carro1_posicao_x = -120
    carro1_posicao_x += velocidade_car1

    # CONFIGS CARRO 2.1
    if carro2_posicao_x <= -150:
        carro2_posicao_x = 850
    carro2_posicao_x -= velocidade_car2

    # CONFIGS CARRO 3.1
    if carro3_posicao_x <= -150:
        carro3_posicao_x = 850
    carro3_posicao_x -= velocidade_car3

    # CONFIGS CARRO 1.2
    if carro1_posicao_x_2 <= -190:
        carro1_posicao_x_2 = 900
    carro1_posicao_x_2 -= velocidade_car1

    # CONFIGS CARRO 2.2
    if carro2_posicao_x_2 >= 850:
        carro2_posicao_x_2 = -120
    carro2_posicao_x_2 += velocidade_car2

    # CONFIGS CARRO 3.2
    if carro3_posicao_x_2 >= 850:
        carro3_posicao_x_2 = -120
    carro3_posicao_x_2 += velocidade_car3

    # Criar retângulos dos carros 1
    carro1_rect = pygame.Rect(carro1_posicao_x, carro1_posicao_y, carro1.get_width(), carro1.get_height() - 20)
    carro2_rect = pygame.Rect(carro2_posicao_x, carro2_posicao_y, carro2.get_width(), carro2.get_height() - 20)
    carro3_rect = pygame.Rect(carro3_posicao_x, carro3_posicao_y, carro3.get_width(), carro3.get_height() - 20)

    # Criar retângulos dos carros 2
    carro4_rect = pygame.Rect(carro1_posicao_x_2, carro1_posicao_y_2, carro4.get_width(), carro4.get_height() - 30)
    carro5_rect = pygame.Rect(carro2_posicao_x_2, carro2_posicao_y_2, carro5.get_width(), carro5.get_height() - 50)
    carro6_rect = pygame.Rect(carro3_posicao_x_2, carro3_posicao_y_2, carro6.get_width(), carro6.get_height() - 20)

    # Verificar colisão com os carros
    if pinguim_rect.colliderect(carro1_rect) or pinguim_rect.colliderect(carro2_rect) or pinguim_rect.colliderect(carro3_rect):
        # Houve colisão, volte o pinguim para sua posição inicial
        posicao_frog_x = 380
        posicao_frog_y = 535

    # Verificar colisão com os carros
    if pinguim_rect.colliderect(carro4_rect) or pinguim_rect.colliderect(carro5_rect) or pinguim_rect.colliderect(carro6_rect):
        # Houve colisão, volte o pinguim para sua posição inicial
        posicao_frog_x = 380
        posicao_frog_y = 535

    if pinguim_rect.colliderect(coracao_rect):
        posicao_frog_x = 380
        posicao_frog_y = 535
    # Atualizar retângulo do pinguim
    pinguim_rect.x = posicao_frog_x
    pinguim_rect.y = posicao_frog_y

    # desenhos fundo e sapo e carros
    window.blit(background, (0, 0))
    window.blit(pinguin_direita, (posicao_frog_x, posicao_frog_y))
    window.blit(carro1, (carro1_posicao_x, carro1_posicao_y))
    window.blit(carro2, (carro2_posicao_x, carro2_posicao_y))
    window.blit(carro3, (carro3_posicao_x, carro3_posicao_y))

    window.blit(carro4, (carro1_posicao_x_2, carro1_posicao_y_2))
    window.blit(carro5, (carro2_posicao_x_2, carro2_posicao_y_2))
    window.blit(carro6, (carro3_posicao_x_2, carro3_posicao_y_2))

    window.blit(iglu, (posicao_iglu_x, posicao_iglu_y))

    window.blit(coracao, (posicao_core_x, posicao_core_y))
    # update da tela
    pygame.display.update()

    relogio.tick(60)
