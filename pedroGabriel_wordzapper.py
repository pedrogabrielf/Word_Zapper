import pygame
import sys
import string
import random
import os
from pathlib import Path

# Classe principal do jogo 
class principal:
    def __init__(self,posicao_x,posicao_y,vel):
        espaconave = pygame.image.load(caminhoRelativo('naveEspacial.png'))
        self.nave = pygame.transform.scale(espaconave, (75,75))
        self.rect = pygame.Rect(posicao_x, posicao_y, self.nave.get_width(), self.nave.get_height())
        self.rect.topleft = posicao_x,posicao_y
        self.vel = vel
        self.disparo_tiro = False

    # Funcao para movimentacao da nave
    def movimentacao(self):
        window.blit(self.nave,self.rect)

        if pygame.key.get_pressed()[pygame.K_LEFT]:
            self.rect.x -= self.vel
            if self.rect.x < -5:
                self.rect.x += self.vel

        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            self.rect.x += self.vel
            if self.rect.x >= 1210:
                self.rect.x -= self.vel

        if pygame.key.get_pressed()[pygame.K_DOWN]:
            self.rect.y += self.vel
            if self.rect.y >= 525:
                self.rect.y -= self.vel

        if pygame.key.get_pressed()[pygame.K_UP]:
            self.rect.y -= self.vel
            if self.rect.y < 150:
                self.rect.y += self.vel


    # Fucao para o tiro 
    def deftiro(self):
        if pygame.key.get_pressed()[pygame.K_SPACE] and not self.disparo_tiro:
            deftiro = disparo(self.rect.center[0],self.rect.top)
            grupoTiros.add(deftiro)

            self.disparo_tiro = True
        elif not pygame.key.get_pressed()[pygame.K_SPACE]:
            self.disparo_tiro = False

 # Funcao coringa para todos os botoes
class botoes():
    def __init__(self,texto,x,y,largura,altura,funcao):

        self.click2 = False

        # Retangulo que sera desenhado
        self.retangulo_Conteiner = pygame.Rect(x,y,largura,altura)
        self.cor_Botao = (100,100,100)

        # Para escrever o texto
        self.texto = fonte_texto.render(texto,True,(255,255,0))
        # pega o tamanho do texto e guarda em ret
        self.retanguloTamanhoTexto = self.texto.get_rect(center=(self.retangulo_Conteiner.centerx, self.retangulo_Conteiner.centery))

        self.funcao = funcao

    def desenha_botoes(self):
        # Desenha o retangulo especificado
        pygame.draw.rect(window,self.cor_Botao,self.retangulo_Conteiner,border_radius=10)
        # Coloca o retangulo na tela
        window.blit(self.texto,self.retanguloTamanhoTexto)

    def clicou(self):

        # Posicao do mouse
        mouse = pygame.mouse.get_pos()

        # Verifica se o mouse esta no botão
        if self.retangulo_Conteiner.collidepoint(mouse):
            
            # Tipo um Hover no css, quando mouse ta em cima muda de cor
            self.cor_Botao = (55,55,55)

            # Verifica o click
            if pygame.mouse.get_pressed()[0]:
                #  Clicou
                self.click2 = True
                
            else:
                if self.click2 == True:
                    self.click2 = False
                    self.funcao()
        else:
            self.cor_Botao = (200,100,0)

class alfabeto():
    def __init__(self,letra, fonte_Letra, Retangulo, vel, larguraFonte, alturaFonte):
        self.letra = letra
        self.fonte_Letra = fonte_Letra
        self.vel = vel
        self.retangulo = Retangulo
        self.cor = (255,255,255)
        self.alturaFonte = alturaFonte
        self.colidiu = False

    def desenha_alfabeto_movendo(self):
        
        letra_Tela = self.fonte_Letra.render(self.letra, True, self.cor)
        window.blit(letra_Tela, self.retangulo)

        self.retangulo.x -= self.vel

        if self.retangulo.x < 0:
            self.retangulo.x = 1700
            self.cor = (255,255,255)
            self.colidiu = False

 # Classe para criar um objeto de disparo que se move para cima na tela e verifica colisões com as opções de letras
class disparo(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        # Carrega a imagem do disparo e redimensiona
        disparo = pygame.image.load(caminhoRelativo('Flame5.png'))
        self.image = pygame.transform.scale(disparo,(20,15))
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]

    def update(self):
        global lista_opc
        global palavra_sorteada
        global letras_palavra
        global venceu
        global lista_verifica

         # Velocidade do disparo 
        self.rect.y -= 10

        # Verifica colisão com as opções de letras 
        for i in range(26):
            
            if self.rect.colliderect(lista_opc[i].retangulo) and not lista_opc[i].colidiu:
                self.kill()
                lista_opc[i].cor = (0,0,0)

                lista_opc[i].colidiu = True
                # Verifica se a letra do disparo está na palavra sorteada 
                if lista_opc[i].letra in palavra_sorteada:
                    for letra in range (len(palavra_sorteada)):
                        if palavra_sorteada[letra] == lista_opc[i].letra:
                            letras_palavra[letra].letra = palavra_sorteada[letra]
                            lista_verifica[letra] = palavra_sorteada[letra]
                            print(lista_verifica)
                            # Verifica se o jogador venceu 
                            if "_" not in lista_verifica:
                                venceu = True
        # Remove o disparo quando sai da tela 
        if self.rect.y < 0:  
            self.kill()


# Classe para a palavra sorteada
class letra():
    def __init__(self,letra,fonteUsada,x,y,larguraFonte,alturaFonte):
        self.letra = letra
        self.fonteUsada = fonteUsada
        self.x = x
        self.y = y
        self.larguraFonte = larguraFonte
        self.alturaFonte = alturaFonte
        self.cor = (0,0,0)

    # Desenhas as letras da palavra sorteada para o jogador ver as letras que tera que acertar !

    def desenha_letras_alfabeto(self):
        retangulo = pygame.draw.rect(window,(85, 232, 84),(self.x,620,self.larguraFonte,self.alturaFonte), border_radius=10)

        letra_Tela = self.fonteUsada.render(self.letra, True, self.cor)

        xletra = retangulo.centerx - letra_Tela.get_width() // 2
        yletra = retangulo.centery - letra_Tela.get_height() // 2

        # Desenha a letra na posição correta
        window.blit(letra_Tela, (xletra, yletra))


#Funcao para escrever textos na tela 
def escrevertexto(texto,fonte,corTexto,posicaoX,posicaoY):
    textoEscrito = fonte.render(texto,True,corTexto)
    window.blit(textoEscrito,(posicaoX,posicaoY))

#Funcao para sortear palavras da lista de palavras
def sorteador():
    with open(caminhoRelativo("palavras.txt"), encoding="utf-8 ") as arquivo: # Lê o arquivo na forma de "utf-8"
        palavrasMisteriosa = arquivo.readlines() # Lê cada linha do arquivo e guarda elas em uma lista
        palavrasMisteriosa = list(map(str.strip, palavrasMisteriosa)) # Remove possiveis espaços em brancono inicio e no final da lista
        palavra_sorteada = random.choice(palavrasMisteriosa).upper() # padroniza a palavra sorteada para que todas as letras sejam minusculas
    return palavra_sorteada
  

def paraJogar():
    global jogar, venceu
    jogar = True
    
def paraJogar2():
    global jogar, venceu, infos
    jogar = True
    infos = False

def jogarFalse():
    global jogo
    jogo = False

#Caminho relativo para os arquivos.
def caminhoRelativo(nome:str):
    caminho_arq = os.path.dirname(os.path.realpath(__file__))
    caminho2 = os.path.join(caminho_arq, "assets/", nome)
    return caminho2

#Função para reiniciar o jogo caso o jogador escolha!
def retorna_comeco():
    global lista_ret
    global backup
    global lista_opc
    global palavra_sorteada
    global letras_palavra
    global lista_verifica
    global jogar
    global jogo
    global largura
    global contador
    global contando
    global venceu
    global x_conteiners
    global x_letra_atual


    lista_ret = []
    lista_opc = []
    letras_palavra = []
    lista_verifica = []
    

    jogar = True
    jogo = True
    contador = True
    contando = True
    venceu = False


    x_conteiners = 50
    x_letra_atual = int(580 - largura / 2)
    largura = (largura_fonte_palavrasorteada + 10) * len(palavra_sorteada)
    palavra_sorteada = sorteador()
    backup = x_letra_atual

        # Seta alfabeto na tela e a respectiva distantia entre as letras e tambem altura
    for i in range(26):
        lista_ret.append(pygame.Rect(x_conteiners,75,largura_fonte_alfabeto,alturaFonteAlfabeto))
        x_conteiners += 65

    #configs alfabeto
    for i in range(26):
        lista_opc.append(alfabeto(listaAlfabeto[i],fonte_alfabeto,lista_ret[i],5,largura_fonte_alfabeto,alturaFonteAlfabeto))


    for i in range(len(palavra_sorteada)):
        letras_palavra.append(letra(palavra_sorteada[i],fonte_palavrasorteada,x_letra_atual,550,largura_fonte_palavrasorteada,altura_fonte_palavraSorteada))

        x_letra_atual += (largura_fonte_palavrasorteada + 30)


def informacoes():
    global infos
    infos = True

def desenha_container_titulo():
    pygame.draw.rect(window,(21,0,80),(190,30,900,100),border_radius=90)

def desenha_container_titulo2():
    pygame.draw.rect(window,(21,0,80),(350,30,600,100),border_radius=90)

def desenha_container_info():
    pygame.draw.rect(window,(21,0,80),(39,222,1200,250),border_radius=80)


if __name__ == "__main__":
    pygame.init()
    pygame.font.init()
    relogio = pygame.time.Clock()

    largura = 1280
    altura = 720

    window = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption("WordZapper")

    #fonte texto
    fonte_texto = pygame.font.SysFont("arial", 30)

    botaojogar = botoes("JOGAR", 535, 200, 200, 100, paraJogar)

    botaoQUIT = botoes("QUIT", 585,520,100,100,jogarFalse)

    botaoQUIT2 = botoes("QUIT", 660,550,200,100,jogarFalse)

    botaojogar2 = botoes("JOGAR", 400, 550, 200, 100, paraJogar2)

    botaojogarDNV = botoes("JOGAR NOVAMENTE", 530, 275, 300, 100, retorna_comeco)

    botaoinfo = botoes("Informações", 490, 360, 300, 100, informacoes)

    #configs background
    tamanho_bg= (55,55)
    bg = pygame.image.load(caminhoRelativo('fundoINFO.png'))
    bg = pygame.transform.scale(bg, (largura,altura))

    bgInicio = pygame.image.load(caminhoRelativo('fundo2.jpg'))
    bgInicio = pygame.transform.scale(bgInicio, (largura,altura))

    fundoINFOS = pygame.image.load(caminhoRelativo('fundoINFO.png'))
    fundoINFOS = pygame.transform.scale(bgInicio, (largura,altura))

    fonte_alfabeto = pygame.font.Font(caminhoRelativo("fonte.ttf"),50)
    fonte_palavrasorteada = pygame.font.Font(caminhoRelativo("fonte.ttf"),50)

    fonteGeral = pygame.font.Font(caminhoRelativo("fonte2.ttf"),40)
    fonteGeral2 = pygame.font.Font(caminhoRelativo("fonte2.ttf"),30)
    fontePEQUENA = pygame.font.Font(caminhoRelativo("fonte.ttf"),15)

    # Tg exemplo de fonte que e utilizado
    largura_fonte_palavrasorteada = fonte_palavrasorteada.size("Ym")[0]
    altura_fonte_palavraSorteada = fonte_palavrasorteada.size("Ym")[1]

    largura_fonte_alfabeto = fonte_alfabeto.size("Ym")[0]
    alturaFonteAlfabeto = fonte_alfabeto.size("Ym")[1]

    listaAlfabeto = list(string.ascii_uppercase)

    lista_ret = []

    x_conteiners = 50

    letras_palavra = []

    grupoTiros = pygame.sprite.Group()

    palavra_sorteada = sorteador()

    caminho = os.getcwd()

    # Seta alfabeto na tela e a respectiva distantia entre as letras e tambem altura
    for i in range(26):
        lista_ret.append(pygame.Rect(x_conteiners,75,largura_fonte_alfabeto,alturaFonteAlfabeto))
        x_conteiners += 65

    lista_opc = []
    
    #configs alfabeto
    for i in range(26):
        lista_opc.append(alfabeto(listaAlfabeto[i],fonte_alfabeto,lista_ret[i],5,largura_fonte_alfabeto,alturaFonteAlfabeto))

    largura = (largura_fonte_palavrasorteada + 10) * len(palavra_sorteada)

    # Retangulo da palavra sorteada 
    x_letra_atual = int(580 - largura / 2)
    
    backup = x_letra_atual

    letras_palavra = []
  
    lista_verifica = []

    for i in range(len(palavra_sorteada)):
        letras_palavra.append(letra(palavra_sorteada[i],fonte_palavrasorteada,x_letra_atual,550,largura_fonte_palavrasorteada,altura_fonte_palavraSorteada))

        x_letra_atual += (largura_fonte_palavrasorteada + 30)


    player = principal(370,400,5)

    jogar = False
    jogo = True
    contador = True
    contando = True
    venceu = False
    infos = False

    contadorzinho = 0 

    while jogo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if jogar:
            if venceu:
                window.fill((0,0,0))

                window.blit(fundoINFOS, (0,0))

                desenha_container_titulo()
                escrevertexto("VOCÊ VENCEU !!",fonteGeral,(255,255,255),360,65)

                botaojogarDNV.desenha_botoes()
                botaojogarDNV.clicou()
                botaoQUIT.desenha_botoes()
                botaoQUIT.clicou()

            else:
                if contador:
                    if contando:
                        contadorzinho = pygame.time.get_ticks()
                        contando = False
                    # Tempo para ver a palavra
                    tempo = pygame.time.get_ticks()

                    diferenca = tempo - contadorzinho

                    if diferenca > 3000:
                        for i in range(len(palavra_sorteada)):

                            if palavra_sorteada != "-":
                                letras_palavra[i].letra = "_"
                                lista_verifica.append("_")
                            else:
                                letras_palavra[i].letra = "-"
                                lista_verifica.append("-")

                        contador = False

                window.blit(bg,(0,0))

                for i in range(26):
                    lista_opc[i].desenha_alfabeto_movendo()

                
                for i in range(len(palavra_sorteada)):
                    letras_palavra[i].desenha_letras_alfabeto()

                player.movimentacao()
                player.deftiro()

                grupoTiros.draw(window)

                grupoTiros.update()

        elif infos:

            window.fill((0,0,0))

            window.blit(fundoINFOS, (0,0))

            desenha_container_titulo()
            desenha_container_info()

            escrevertexto("INFORMAÇÕES ABAIXO:",fonteGeral,(255,255,255),240,65)
            escrevertexto("PARA JOGAR UTILIZE AS SETAS DO TECLADO",fonteGeral2,(255,255,255),85,280)
            escrevertexto("PARA DISPARAR UTILIZE A TECLA ESPAÇO!",fonteGeral2,(255,255,255),85,370)


            botaojogar2.desenha_botoes()
            botaojogar2.clicou()

            botaoQUIT2.desenha_botoes()
            botaoQUIT2.clicou()

        else:
            window.blit(bgInicio, (0,0))

            desenha_container_titulo2()
            
            escrevertexto("WORDZAPPER",fonteGeral,(255,255,255),450,60)
            escrevertexto("VERSÃO: SHOPEE",fontePEQUENA,(255,255,255),580,105)

            botaojogar.desenha_botoes()
            botaojogar.clicou()

            botaoinfo.desenha_botoes()
            botaoinfo.clicou()

            botaoQUIT.desenha_botoes()
            botaoQUIT.clicou()

        pygame.display.update()
        relogio.tick(60)