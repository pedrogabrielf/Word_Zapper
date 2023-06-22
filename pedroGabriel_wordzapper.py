import pygame
import sys
import string
import random
import os
from pathlib import Path

# Classe principal do jogo 
class principal:
    def __init__(self,posicao_x,posicao_y,vel):
        espaconave = pygame.image.load(caminho_arquivo('naveEspacial.png'))
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


class disparo(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        disparo = pygame.image.load(caminho_arquivo('Flame5.png'))
        self.image = pygame.transform.scale(disparo,(20,15))
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]

    def update(self):
        global listaOpcoes
        global palavraSorteada
        global letrasPalavra
        global venceu
        global listaVerificacao

        #Vel disparo
        self.rect.y -= 10

        # Configs colisao
        for i in range(26):
            
            if self.rect.colliderect(listaOpcoes[i].retangulo) and not listaOpcoes[i].colidiu:
                self.kill()
                listaOpcoes[i].cor = (0,0,0)

                listaOpcoes[i].colidiu = True

                if listaOpcoes[i].letra in palavraSorteada:
                    for letra in range (len(palavraSorteada)):
                        if palavraSorteada[letra] == listaOpcoes[i].letra:
                            letrasPalavra[letra].letra = palavraSorteada[letra]
                            listaVerificacao[letra] = palavraSorteada[letra]
                            print(listaVerificacao)
                            if "_" not in listaVerificacao:
                                venceu = True

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

        x_letra = retangulo.centerx - letra_Tela.get_width() // 2
        y_letra = retangulo.centery - letra_Tela.get_height() // 2

        # Desenha a letra na posição correta
        window.blit(letra_Tela, (x_letra, y_letra))


#Funcao para escrever textos na tela 
def escrever_texto(texto,fonte,corTexto,posicaoX,posicaoY):
    textoEscrito = fonte.render(texto,True,corTexto)
    window.blit(textoEscrito,(posicaoX,posicaoY))

#Funcao para sortear palavras da lista de palavras
def sorteia_palavra():
    with open(caminho_arquivo("palavras.txt"), encoding="utf-8 ") as arquivo: # Lê o arquivo na forma de "utf-8"
        palavras = arquivo.readlines() # Lê cada linha do arquivo e guarda elas em uma lista
        palavras = list(map(str.strip, palavras)) # Remove possiveis espaços em brancono inicio e no final da lista
        palavraSorteada = random.choice(palavras).upper() # padroniza a palavra sorteada para que todas as letras sejam minusculas
    return palavraSorteada


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

def caminho_arquivo(nome:str):
    caminho = os.path.dirname(os.path.realpath(__file__))
    caminhoAbsoluto = os.path.join(caminho, "assets/", nome)
    return caminhoAbsoluto

def retorna_comeco():
    global listaRetangulos
    global listaOpcoes
    global letrasPalavra
    global listaVerificacao
    global jogar
    global jogo
    global contador
    global contando
    global venceu
    global xRetangulosConteiners
    global xRetanguloLetraAtual
    global palavraSorteada
    global largura
    global backup

    listaRetangulos = []
    listaOpcoes = []
    letrasPalavra = []
    listaVerificacao = []
    

    jogar = True
    jogo = True
    contador = True
    contando = True
    venceu = False

    xRetangulosConteiners = 50
    xRetanguloLetraAtual = int(580 - largura / 2)
    largura = (larguraFontePalavraSorteada + 10) * len(palavraSorteada)
    palavraSorteada = sorteia_palavra()
    backup = xRetanguloLetraAtual

        # Seta alfabeto na tela e a respectiva distantia entre as letras e tambem altura
    for i in range(26):
        listaRetangulos.append(pygame.Rect(xRetangulosConteiners,75,larguraFonteAlfabeto,alturaFonteAlfabeto))
        xRetangulosConteiners += 65

    #configs alfabeto
    for i in range(26):
        listaOpcoes.append(alfabeto(listaAlfabeto[i],fonteAlfabeto,listaRetangulos[i],5,larguraFonteAlfabeto,alturaFonteAlfabeto))


    for i in range(len(palavraSorteada)):
        letrasPalavra.append(letra(palavraSorteada[i],fonteLetrasPalavraSorteada,xRetanguloLetraAtual,550,larguraFontePalavraSorteada,alturaFontePalavraSorteada))

        xRetanguloLetraAtual += (larguraFontePalavraSorteada + 30)


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
    bg = pygame.image.load(caminho_arquivo('fundoINFO.png'))
    bg = pygame.transform.scale(bg, (largura,altura))

    bgInicio = pygame.image.load(caminho_arquivo('fundo2.jpg'))
    bgInicio = pygame.transform.scale(bgInicio, (largura,altura))

    fundoINFOS = pygame.image.load(caminho_arquivo('fundoINFO.png'))
    fundoINFOS = pygame.transform.scale(bgInicio, (largura,altura))

    fonteAlfabeto = pygame.font.Font(caminho_arquivo("fonte.ttf"),50)
    fonteLetrasPalavraSorteada = pygame.font.Font(caminho_arquivo("fonte.ttf"),50)

    fonteGeral = pygame.font.Font(caminho_arquivo("fonte2.ttf"),40)
    fonteGeral2 = pygame.font.Font(caminho_arquivo("fonte2.ttf"),30)
    fontePEQUENA = pygame.font.Font(caminho_arquivo("fonte.ttf"),15)

    # Tg exemplo de fonte que e utilizado
    larguraFontePalavraSorteada = fonteLetrasPalavraSorteada.size("Ym")[0]
    alturaFontePalavraSorteada = fonteLetrasPalavraSorteada.size("Ym")[1]

    larguraFonteAlfabeto = fonteAlfabeto.size("Ym")[0]
    alturaFonteAlfabeto = fonteAlfabeto.size("Ym")[1]

    listaAlfabeto = list(string.ascii_uppercase)

    listaRetangulos = []

    xRetangulosConteiners = 50

    letrasPalavra = []

    grupoTiros = pygame.sprite.Group()

    palavraSorteada = sorteia_palavra()

    caminho = os.getcwd()

    # Seta alfabeto na tela e a respectiva distantia entre as letras e tambem altura
    for i in range(26):
        listaRetangulos.append(pygame.Rect(xRetangulosConteiners,75,larguraFonteAlfabeto,alturaFonteAlfabeto))
        xRetangulosConteiners += 65

    listaOpcoes = []
    
    #configs alfabeto
    for i in range(26):
        listaOpcoes.append(alfabeto(listaAlfabeto[i],fonteAlfabeto,listaRetangulos[i],5,larguraFonteAlfabeto,alturaFonteAlfabeto))

    largura = (larguraFontePalavraSorteada + 10) * len(palavraSorteada)

    # Retangulo da palavra sorteada 
    xRetanguloLetraAtual = int(580 - largura / 2)
    
    backup = xRetanguloLetraAtual

    letrasPalavra = []
  
    listaVerificacao = []

    for i in range(len(palavraSorteada)):
        letrasPalavra.append(letra(palavraSorteada[i],fonteLetrasPalavraSorteada,xRetanguloLetraAtual,550,larguraFontePalavraSorteada,alturaFontePalavraSorteada))

        xRetanguloLetraAtual += (larguraFontePalavraSorteada + 30)


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
                escrever_texto("VOCÊ VENCEU !!",fonteGeral,(255,255,255),360,65)

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
                        for i in range(len(palavraSorteada)):

                            if palavraSorteada != "-":
                                letrasPalavra[i].letra = "_"
                                listaVerificacao.append("_")
                            else:
                                letrasPalavra[i].letra = "-"
                                listaVerificacao.append("-")

                        contador = False

                window.blit(bg,(0,0))

                for i in range(26):
                    listaOpcoes[i].desenha_alfabeto_movendo()

                
                for i in range(len(palavraSorteada)):
                    letrasPalavra[i].desenha_letras_alfabeto()

                player.movimentacao()
                player.deftiro()

                grupoTiros.draw(window)

                grupoTiros.update()

        elif infos:

            window.fill((0,0,0))

            window.blit(fundoINFOS, (0,0))

            desenha_container_titulo()
            desenha_container_info()

            escrever_texto("INFORMAÇÕES ABAIXO:",fonteGeral,(255,255,255),240,65)
            escrever_texto("PARA JOGAR UTILIZE AS SETAS DO TECLADO",fonteGeral2,(255,255,255),85,280)
            escrever_texto("PARA DISPARAR UTILIZE A TECLA ESPAÇO!",fonteGeral2,(255,255,255),85,370)


            botaojogar2.desenha_botoes()
            botaojogar2.clicou()

            botaoQUIT2.desenha_botoes()
            botaoQUIT2.clicou()

        else:
            window.blit(bgInicio, (0,0))

            desenha_container_titulo2()
            
            escrever_texto("WORDZAPPER",fonteGeral,(255,255,255),450,60)
            escrever_texto("VERSÃO: SHOPEE",fontePEQUENA,(255,255,255),580,105)

            botaojogar.desenha_botoes()
            botaojogar.clicou()

            botaoinfo.desenha_botoes()
            botaoinfo.clicou()

            botaoQUIT.desenha_botoes()
            botaoQUIT.clicou()

        pygame.display.update()
        relogio.tick(60)